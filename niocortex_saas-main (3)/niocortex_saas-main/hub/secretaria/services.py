from django.template import Template, Context
from django.core.exceptions import ValidationError
from core.models import CustomUser
from lumenios.pedagogico.models import Aluno
from .models import ModeloDocumento, DocumentoEmitido
import datetime

class SecretariatService:
    
    @staticmethod
    def _get_tenant(user):
        return user.tenant_id

    @classmethod
    def create_template(cls, user: CustomUser, data: dict):
        tenant_id = cls._get_tenant(user)
        return ModeloDocumento.objects.create(tenant_id=tenant_id, **data)

    @classmethod
    def emitir_documento(cls, user: CustomUser, aluno_id: str, modelo_id: str) -> DocumentoEmitido:
        """
        Gera o documento final substituindo as variáveis e grava o histórico.
        """
        tenant_id = cls._get_tenant(user)
        
        try:
            aluno = Aluno.objects.get(id=aluno_id, tenant_id=tenant_id)
            modelo = ModeloDocumento.objects.get(id=modelo_id, tenant_id=tenant_id)
        except (Aluno.DoesNotExist, ModeloDocumento.DoesNotExist):
            raise ValidationError("Aluno ou Modelo não encontrado.")

        # 1. Preparar o Contexto
        context_data = {
            'aluno': aluno,
            'escola': aluno.escola if hasattr(aluno, 'escola') else "NioCortex School",
            'data_hoje': datetime.date.today().strftime("%d/%m/%Y")
        }

        # 2. Renderizar o Conteúdo
        django_template = Template(modelo.conteudo)
        context = Context(context_data)
        conteudo_renderizado = django_template.render(context)

        # 3. Gravar o Registo
        documento = DocumentoEmitido.objects.create(
            tenant_id=tenant_id,
            aluno=aluno,
            modelo=modelo,
            conteudo_final=conteudo_renderizado,
            emitido_por=user
        )
        
        return documento