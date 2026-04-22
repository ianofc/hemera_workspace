import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { AuroraBackground } from "@/components/HemeraChrome";
import { HemeraSun } from "@/components/HemeraSun";
import { Mail, Lock, GraduationCap, BookOpen, User, Sparkles, Loader2 } from "lucide-react";
import { toast } from "sonner";
import { supabase } from "@/integrations/supabase/client";
import { useAuth, EducationLevel } from "@/hooks/useAuth";

const DEMO_USERS = {
  professor: { email: "prof@hemera.dev", password: "Hemera2026!", full_name: "Iansantos Demo", education_level: "medio" as EducationLevel, school_name: "Escola Aurora" },
  aluno: { email: "aluno@hemera.dev", password: "Hemera2026!", full_name: "Eloisa Demo", education_level: "medio" as EducationLevel, school_name: "Escola Aurora" },
};

const Login = () => {
  const navigate = useNavigate();
  const { user, role, loading: authLoading } = useAuth();
  const [mode, setMode] = useState<"login" | "signup">("login");
  const [role_, setRole_] = useState<"professor" | "aluno">("professor");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [level, setLevel] = useState<EducationLevel>("medio");
  const [school, setSchool] = useState("");
  const [submitting, setSubmitting] = useState(false);

  // Already logged in? Redirect.
  useEffect(() => {
    if (!authLoading && user && role) {
      navigate(role === "professor" ? "/professor" : "/aluno", { replace: true });
    }
  }, [user, role, authLoading, navigate]);

  const handleLogin = async (emailArg: string, passwordArg: string) => {
    const { error } = await supabase.auth.signInWithPassword({
      email: emailArg,
      password: passwordArg,
    });
    if (error) throw error;
  };

  const handleSignup = async (
    emailArg: string,
    passwordArg: string,
    meta: { full_name: string; role: "professor" | "aluno"; education_level: EducationLevel; school_name: string }
  ) => {
    const redirectUrl = `${window.location.origin}/`;
    const { error } = await supabase.auth.signUp({
      email: emailArg,
      password: passwordArg,
      options: {
        emailRedirectTo: redirectUrl,
        data: meta,
      },
    });
    if (error) throw error;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      if (mode === "signup") {
        await handleSignup(email, password, {
          full_name: fullName || email.split("@")[0],
          role: role_,
          education_level: level,
          school_name: school,
        });
        toast.success("Conta criada — entrando…");
        // auto-confirm is on, so signInWithPassword will work next event tick.
        await handleLogin(email, password);
      } else {
        await handleLogin(email, password);
        toast.success("Bem-vindo ao Hemera");
      }
    } catch (err: any) {
      const msg = err?.message ?? "Falha ao autenticar";
      if (msg.toLowerCase().includes("invalid login")) {
        toast.error("Email ou senha incorretos");
      } else if (msg.toLowerCase().includes("already registered")) {
        toast.error("Este email já está cadastrado — use 'Entrar'");
      } else {
        toast.error(msg);
      }
    } finally {
      setSubmitting(false);
    }
  };

  const enterAsDemo = async (kind: "professor" | "aluno") => {
    setSubmitting(true);
    const demo = DEMO_USERS[kind];
    try {
      // Try login first
      const { error: loginErr } = await supabase.auth.signInWithPassword({
        email: demo.email,
        password: demo.password,
      });
      if (loginErr) {
        // Account doesn't exist yet → create it
        const { error: signErr } = await supabase.auth.signUp({
          email: demo.email,
          password: demo.password,
          options: {
            emailRedirectTo: `${window.location.origin}/`,
            data: {
              full_name: demo.full_name,
              role: kind,
              education_level: demo.education_level,
              school_name: demo.school_name,
            },
          },
        });
        if (signErr) throw signErr;
        // signUp auto-creates session when email confirmation is off
        const { error: retryErr } = await supabase.auth.signInWithPassword({
          email: demo.email,
          password: demo.password,
        });
        if (retryErr) throw retryErr;
      }
      toast.success(`Entrando como ${kind} demo…`);
    } catch (err: any) {
      toast.error(err?.message ?? "Falha no demo");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen grid place-items-center px-4 py-8 relative">
      <AuroraBackground />
      <div className="w-full max-w-md animate-scale-in">
        <Link to="/" className="flex flex-col items-center gap-3 mb-6">
          <HemeraSun size={64} />
          <div className="text-center">
            <div className="font-display text-3xl text-primary">Hemera</div>
            <div className="text-[10px] uppercase tracking-[0.25em] text-muted-foreground">OS Educacional</div>
          </div>
        </Link>

        <div className="glass-strong rounded-3xl p-8">
          <h1 className="font-display text-3xl text-center mb-2">
            {mode === "login" ? "A aurora te aguarda" : "Cadastre-se no Hemera"}
          </h1>
          <p className="text-center text-sm text-muted-foreground mb-6">
            {mode === "login" ? "Acesse seu ambiente Hemera" : "Crie seu acesso em segundos"}
          </p>

          {/* Demo buttons */}
          <div className="grid grid-cols-2 gap-2 mb-5">
            <Button type="button" variant="outline" size="sm" disabled={submitting}
              onClick={() => enterAsDemo("professor")}
              className="gap-1.5 border-primary/30 hover:bg-primary/10">
              <Sparkles className="h-3.5 w-3.5 text-sun" /> Demo professor
            </Button>
            <Button type="button" variant="outline" size="sm" disabled={submitting}
              onClick={() => enterAsDemo("aluno")}
              className="gap-1.5 border-primary/30 hover:bg-primary/10">
              <Sparkles className="h-3.5 w-3.5 text-sun" /> Demo aluno
            </Button>
          </div>

          <div className="relative my-4">
            <div className="absolute inset-0 flex items-center"><span className="w-full border-t border-border" /></div>
            <div className="relative flex justify-center text-[10px] uppercase tracking-wider">
              <span className="bg-card px-2 text-muted-foreground">ou com email</span>
            </div>
          </div>

          {/* Role switch (only on signup) */}
          {mode === "signup" && (
            <div className="grid grid-cols-2 gap-2 p-1 bg-muted/60 rounded-xl mb-4">
              <button type="button" onClick={() => setRole_("professor")}
                className={`flex items-center justify-center gap-2 py-2 rounded-lg text-sm transition-all ${role_ === "professor" ? "bg-card shadow text-primary font-medium" : "text-muted-foreground"}`}>
                <GraduationCap className="h-4 w-4" /> Professor
              </button>
              <button type="button" onClick={() => setRole_("aluno")}
                className={`flex items-center justify-center gap-2 py-2 rounded-lg text-sm transition-all ${role_ === "aluno" ? "bg-card shadow text-primary font-medium" : "text-muted-foreground"}`}>
                <BookOpen className="h-4 w-4" /> Aluno
              </button>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-3">
            {mode === "signup" && (
              <>
                <div className="space-y-1.5">
                  <Label htmlFor="name">Nome completo</Label>
                  <div className="relative">
                    <User className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                    <Input id="name" value={fullName} onChange={(e) => setFullName(e.target.value)}
                      placeholder="Seu nome" className="pl-9 bg-background/60" required />
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-2">
                  <div className="space-y-1.5">
                    <Label htmlFor="level">Nível</Label>
                    <select id="level" value={level} onChange={(e) => setLevel(e.target.value as EducationLevel)}
                      className="w-full h-10 px-3 rounded-md border border-input bg-background/60 text-sm">
                      <option value="creche">Creche</option>
                      <option value="fundamental_1">Fund. I</option>
                      <option value="fundamental_2">Fund. II</option>
                      <option value="medio">Médio</option>
                      <option value="superior">Superior</option>
                    </select>
                  </div>
                  <div className="space-y-1.5">
                    <Label htmlFor="school">Escola</Label>
                    <Input id="school" value={school} onChange={(e) => setSchool(e.target.value)}
                      placeholder="(opcional)" className="bg-background/60" />
                  </div>
                </div>
              </>
            )}
            <div className="space-y-1.5">
              <Label htmlFor="email">Email</Label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)}
                  placeholder="voce@email.com" className="pl-9 bg-background/60" required />
              </div>
            </div>
            <div className="space-y-1.5">
              <Label htmlFor="pwd">Senha</Label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input id="pwd" type="password" value={password} onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••" minLength={6} className="pl-9 bg-background/60" required />
              </div>
            </div>
            <Button type="submit" disabled={submitting}
              className="w-full bg-primary hover:bg-primary/90 shadow-[var(--shadow-elegant)]" size="lg">
              {submitting && <Loader2 className="h-4 w-4 mr-2 animate-spin" />}
              {mode === "login" ? "Entrar" : `Cadastrar como ${role_ === "professor" ? "Professor" : "Aluno"}`}
            </Button>
          </form>

          <p className="text-center text-xs text-muted-foreground mt-6">
            {mode === "login" ? (
              <>Primeiro acesso?{" "}
                <button onClick={() => setMode("signup")} className="text-primary hover:underline">Cadastre-se</button>
              </>
            ) : (
              <>Já tem conta?{" "}
                <button onClick={() => setMode("login")} className="text-primary hover:underline">Entrar</button>
              </>
            )}
          </p>
        </div>

        <p className="text-center text-[11px] text-muted-foreground mt-6">
          © 2026 Hemera OS · Heimdall protege seus dados
        </p>
      </div>
    </div>
  );
};

export default Login;
