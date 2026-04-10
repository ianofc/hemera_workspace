import subprocess
import os

class ZiosSelfCoder:
    """Capacidade do Zios de gerar ferramentas para seus novos projetos."""
    def __init__(self, sandbox_path="sandbox/runtime"):
        self.sandbox_path = sandbox_path
        os.makedirs(self.sandbox_path, exist_ok=True)

    def run_tool(self, code: str):
        file_path = os.path.join(self.sandbox_path, "generated_tool.py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
        return subprocess.run(["python", file_path], capture_output=True, text=True)