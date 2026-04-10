import os
import django
import uuid
import sys
sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niocortex.settings')
django.setup()
from core.models import CustomUser, School
from django.contrib.auth.models import Group

def run():
    print(">>> [SETUP] Inserindo dados...")
    escola, _ = School.objects.get_or_create(nome='Niocortex Central', defaults={'tipo': 'SaaS_Head'})
    if not escola.tenant_id:
        escola.tenant_id = uuid.uuid4()
        escola.save()
    
    users = [
        {'u': 'ana.diretora', 'r': 'DIRETOR', 'c': 2},
        {'u': 'bia.secretaria', 'r': 'SECRETARIA', 'c': 1},
        {'u': 'carlos.rh', 'r': 'RH', 'c': 1},
        {'u': 'dani.fin', 'r': 'FINANCEIRO', 'c': 1},
        {'u': 'edu.crm', 'r': 'CRM', 'c': 10},
    ]
    for d in users:
        grp, _ = Group.objects.get_or_create(name=d['r'])
        mat = f"101{d['c']}{uuid.uuid4().hex[:6]}"
        user, _ = CustomUser.objects.update_or_create(
            username=d['u'],
            defaults={'role': d['r'], 'matricula': mat, 'school': escola, 'tenant_id': escola.tenant_id, 'is_staff': True}
        )
        user.set_password('123456')
        user.groups.add(grp)
        user.save()
        print(f"    [OK] {user.username}")
if __name__ == '__main__': run()