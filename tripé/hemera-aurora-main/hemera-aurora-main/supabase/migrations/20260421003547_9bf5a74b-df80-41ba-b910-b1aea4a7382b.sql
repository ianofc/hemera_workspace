
-- ============ TYPES ============
create type public.app_role as enum ('professor', 'aluno', 'admin');
create type public.education_level as enum ('creche', 'fundamental_1', 'fundamental_2', 'medio', 'superior');

-- ============ PROFILES ============
create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  full_name text not null default '',
  display_name text,
  avatar_url text,
  education_level public.education_level,
  school_tenant_id uuid,
  school_name text,
  bio text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

alter table public.profiles enable row level security;

create policy "profiles_select_own" on public.profiles
  for select to authenticated using (auth.uid() = id);
create policy "profiles_update_own" on public.profiles
  for update to authenticated using (auth.uid() = id) with check (auth.uid() = id);
create policy "profiles_insert_own" on public.profiles
  for insert to authenticated with check (auth.uid() = id);

-- ============ USER ROLES (separate table — security) ============
create table public.user_roles (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  role public.app_role not null,
  created_at timestamptz not null default now(),
  unique (user_id, role)
);

alter table public.user_roles enable row level security;

create policy "roles_select_own" on public.user_roles
  for select to authenticated using (auth.uid() = user_id);

-- ============ has_role function (SECURITY DEFINER, no RLS recursion) ============
create or replace function public.has_role(_user_id uuid, _role public.app_role)
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1 from public.user_roles
    where user_id = _user_id and role = _role
  )
$$;

-- ============ updated_at trigger ============
create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create trigger profiles_set_updated_at
  before update on public.profiles
  for each row execute function public.set_updated_at();

-- ============ Auto-create profile + role on signup ============
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
declare
  _role public.app_role;
  _level public.education_level;
begin
  _role := coalesce(
    (new.raw_user_meta_data->>'role')::public.app_role,
    'aluno'
  );
  _level := nullif(new.raw_user_meta_data->>'education_level', '')::public.education_level;

  insert into public.profiles (id, full_name, display_name, education_level, school_name)
  values (
    new.id,
    coalesce(new.raw_user_meta_data->>'full_name', ''),
    coalesce(new.raw_user_meta_data->>'display_name', new.raw_user_meta_data->>'full_name', ''),
    _level,
    new.raw_user_meta_data->>'school_name'
  );

  insert into public.user_roles (user_id, role)
  values (new.id, _role)
  on conflict do nothing;

  return new;
end;
$$;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();
