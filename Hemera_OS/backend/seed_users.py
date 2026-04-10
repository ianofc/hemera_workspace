import os
import django
import sys
import unicodedata

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niocortex.settings')
django.setup()

from core.models import CustomUser
from lumenios.pedagogico.models import Aluno

def remove_accents(input_str):
    """Normalizes text to remove accents (e.g., 'João' -> 'Joao')."""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def generate_username(nome):
    """Generates a username: firstname_lastname (lowercase, no accents)."""
    clean_name = remove_accents(nome).lower()
    parts = clean_name.split()
    if len(parts) >= 2:
        return f"{parts[0]}_{parts[-1]}"
    return parts[0]

def seed_student_users():
    print("🌱 Starting Student User Seeding...")
    
    alunos = Aluno.objects.all()
    count_created = 0
    count_existing = 0

    for aluno in alunos:
        # Generate Username
        username = generate_username(aluno.nome)
        
        # Determine First and Last Name for User model
        parts = aluno.nome.strip().split()
        first_name = parts[0]
        last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
        
        # Generate Password: First Name + 123456
        # Example: Ian -> Ian123456
        password_plain = f"{first_name}123456"

        # Check if user exists to avoid duplicates
        if not CustomUser.objects.filter(username=username).exists():
            print(f"   Creating user for: {aluno.nome} -> User: {username} / Pass: {password_plain}")
            
            user = CustomUser.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=aluno.email if aluno.email else f"{username}@niocortex.test",
                role='ALUNO_FREE', # Defaulting to Free for testing
                tenant_id=aluno.tenant_id, # Keep tenant consistency
                tenant_type='INDIVIDUAL' 
            )
            user.set_password(password_plain)
            user.save()
            count_created += 1
        else:
            # Optional: Update existing user if needed, or just skip
            # print(f"   User {username} already exists. Skipping.")
            count_existing += 1

    print("-" * 30)
    print(f"✅ Seeding Complete.")
    print(f"   Created: {count_created}")
    print(f"   Existing: {count_existing}")
    print(f"   Total Students Processed: {len(alunos)}")

if __name__ == "__main__":
    seed_student_users()