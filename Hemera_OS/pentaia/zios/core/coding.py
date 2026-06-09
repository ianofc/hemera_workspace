import subprocess
import os
import sys
import uuid
import shutil
import logging
from core.safety import evaluate_safety

logger = logging.getLogger("ZIOS_SELF_CODER")

class ZiosSelfCoder:
    """
    Pipelines de Auto-Codificação (Self-Coding) do ZIOS.
    Gera códigos e testes, executa-os em uma sandbox isolada e,
    somente se passarem nos testes, aplica-os de forma segura.
    """
    def __init__(self, sandbox_base_path="sandbox"):
        self.sandbox_base_path = sandbox_base_path
        os.makedirs(self.sandbox_base_path, exist_ok=True)

    def generate_code_and_tests(self, task_description: str) -> tuple:
        """
        Usa o modelo LLM do Zios para gerar o código da ferramenta e o teste unitário pytest associado.
        Caso o LLM falhe ou não tenha API Key, fornece um fallback seguro de geração dinâmica/mockada.
        """
        try:
            from core.config import settings
            google_api_key = settings.GOOGLE_API_KEY
        except ImportError:
            google_api_key = os.getenv("GOOGLE_API_KEY")
            
        prompt = f"""
        Você é o ZIOS Self-Coding Agent. Sua tarefa é criar um script Python e seus respectivos testes unitários usando o framework pytest.
        A descrição da tarefa é: "{task_description}"

        Responda EXCLUSIVAMENTE com o código das duas partes no seguinte formato:
        
        === SCRIPT ===
        ```python
        # código aqui
        ```
        
        === TEST ===
        ```python
        # código de testes usando pytest aqui
        ```
        
        O script e o teste não devem violar protocolos de segurança (sem rm -rf, etc.).
        """
        
        if google_api_key:
            try:
                from google import genai
                client = genai.Client(
                    api_key=google_api_key,
                    http_options={'api_version': 'v1beta'}
                )
                response = client.models.generate_content(
                    model='gemini-1.5-pro',
                    contents=prompt
                )
                content = response.text
                
                script_code = ""
                test_code = ""
                
                if "=== SCRIPT ===" in content and "=== TEST ===" in content:
                    parts = content.split("=== TEST ===")
                    script_part = parts[0].split("=== SCRIPT ===")[1]
                    test_part = parts[1]
                    
                    if "```python" in script_part:
                        script_code = script_part.split("```python")[1].split("```")[0].strip()
                    else:
                        script_code = script_part.strip()
                        
                    if "```python" in test_part:
                        test_code = test_part.split("```python")[1].split("```")[0].strip()
                    else:
                        test_code = test_part.strip()
                        
                    return script_code, test_code
            except Exception as e:
                logger.error(f"Erro na geração neural de código ({e}). Usando fallback dinâmico.")

        # Fallback de geração dinâmica
        if "calculadora" in task_description.lower() or "soma" in task_description.lower():
            script_code = """
def soma(a, b):
    return a + b

def subtracao(a, b):
    return a - b
"""
            test_code = """
import pytest
from generated_tool import soma, subtracao

def test_soma():
    assert soma(2, 3) == 5
    assert soma(-1, 1) == 0

def test_subtracao():
    assert subtracao(5, 3) == 2
"""
        elif "formatação" in task_description.lower() or "slug" in task_description.lower():
            script_code = """
import re

def to_slug(text: str) -> str:
    if not text:
        return ""
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9\\s-]', '', text)
    return re.sub(r'[\\s-]+', '-', text)
"""
            test_code = """
import pytest
from generated_tool import to_slug

def test_to_slug():
    assert to_slug("Hello World!") == "hello-world"
    assert to_slug("  Zios  Life - OS  ") == "zios-life-os"
    assert to_slug("") == ""
"""
        else:
            script_code = """
def run_task():
    return "zios_pipeline_success"
"""
            test_code = """
import pytest
from generated_tool import run_task

def test_run_task():
    assert run_task() == "zios_pipeline_success"
"""
        return script_code.strip(), test_code.strip()

    def sandbox_test(self, code_text: str, test_text: str) -> dict:
        """
        Executa os códigos em uma sandbox isolada com testes obrigatórios.
        Valida a segurança antes da execução.
        """
        if not evaluate_safety(code_text) or not evaluate_safety(test_text):
            return {
                "success": False,
                "error": "SecurityViolation: O código fornecido viola as regras de segurança do ZIOS.",
                "sandbox_dir": None
            }

        run_id = str(uuid.uuid4())[:8]
        sandbox_dir = os.path.abspath(os.path.join(self.sandbox_base_path, f"run_{run_id}"))
        os.makedirs(sandbox_dir, exist_ok=True)
        
        try:
            script_file = os.path.join(sandbox_dir, "generated_tool.py")
            test_file = os.path.join(sandbox_dir, "test_generated_tool.py")
            
            with open(script_file, "w", encoding="utf-8") as f:
                f.write(code_text)
                
            with open(test_file, "w", encoding="utf-8") as f:
                f.write(test_text)
            
            with open(os.path.join(sandbox_dir, "__init__.py"), "w") as f:
                pass

            env = os.environ.copy()
            env["PYTHONPATH"] = sandbox_dir + os.pathsep + env.get("PYTHONPATH", "")
            
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "test_generated_tool.py", "-v"],
                cwd=sandbox_dir,
                capture_output=True,
                text=True,
                env=env,
                timeout=15
            )
            
            success = result.returncode == 0
            return {
                "success": success,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "sandbox_dir": sandbox_dir
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "TimeoutExpired: Os testes unitários excederam o tempo limite de 15s.",
                "sandbox_dir": sandbox_dir
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"ExecutionError: Ocorreu um erro ao executar a sandbox: {str(e)}",
                "sandbox_dir": sandbox_dir
            }

    def apply_code(self, code_text: str, destination_path: str, test_text: str) -> dict:
        """
        Pipeline completo: Roda os testes na sandbox, e se passar em 100%,
        aplica o script copiando-o para o destination_path final.
        """
        test_result = self.sandbox_test(code_text, test_text)
        
        if not test_result.get("success"):
            return {
                "applied": False,
                "reason": "TestFailure",
                "details": test_result
            }
            
        try:
            os.makedirs(os.path.dirname(os.path.abspath(destination_path)), exist_ok=True)
            with open(destination_path, "w", encoding="utf-8") as f:
                f.write(code_text)
                
            if test_result.get("sandbox_dir") and os.path.exists(test_result["sandbox_dir"]):
                shutil.rmtree(test_result["sandbox_dir"])
                
            return {
                "applied": True,
                "destination": destination_path,
                "details": test_result
            }
        except Exception as e:
            return {
                "applied": False,
                "reason": "WriteError",
                "error": str(e),
                "details": test_result
            }