from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

# Inicializa as extensões aqui para evitar conflitos de importação
bcrypt = Bcrypt()
csrf = CSRFProtect()