from django.core.exceptions import PermissionDenied
from core.models import CustomUser
from .models import Funcionario, Departamento, Cargo

class HRService:
    @staticmethod
    def _get_tenant(user: CustomUser):
        if not user.tenant_id:
            raise PermissionDenied("Usuário sem Tenant ID.")
        return user.tenant_id

    @classmethod
    def create_employee(cls, user: CustomUser, data: dict) -> Funcionario:
        tenant_id = cls._get_tenant(user)
        return Funcionario.objects.create(tenant_id=tenant_id, **data)

    @classmethod
    def create_department(cls, user: CustomUser, data: dict) -> Departamento:
        tenant_id = cls._get_tenant(user)
        return Departamento.objects.create(tenant_id=tenant_id, **data)

    @classmethod
    def create_position(cls, user: CustomUser, data: dict) -> Cargo:
        tenant_id = cls._get_tenant(user)
        return Cargo.objects.create(tenant_id=tenant_id, **data)
    
    @classmethod
    def list_employees(cls, user: CustomUser):
        tenant_id = cls._get_tenant(user)
        return Funcionario.objects.filter(tenant_id=tenant_id).select_related('cargo', 'departamento')