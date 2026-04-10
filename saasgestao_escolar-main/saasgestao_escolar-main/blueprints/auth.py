# blueprints/auth.py

from datetime import date
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user, login_required 

# CORREÇÃO: Importa o objeto 'bcrypt' global diretamente para contornar o KeyError no extensions
try:
    from app import bcrypt # Isso deve ser possível após o registro dos Blueprints em app.py
except ImportError:
    # Fallback para evitar falha completa se o import direto não for possível
    bcrypt = None 
    print("AVISO: bcrypt não importado diretamente. Acesso via extensions['bcrypt'] será tentado.")


# Imports de Módulos Locais
from models import db, User, Horario, BlocoAula
from forms import RegisterForm, LoginForm

# Criação do Blueprint para Autenticação
auth_bp = Blueprint('auth', __name__, url_prefix='/')

# --- ROTAS DE AUTENTICAÇÃO ---

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        # CORREÇÃO 1: Deve apontar para o endpoint do Blueprint 'core'
        return redirect(url_for('core.index')) 
    
    form = RegisterForm()
    if form.validate_on_submit():
        
        # Acesso ao Bcrypt: usa a instância importada diretamente
        bcrypt_instance = bcrypt if bcrypt else current_app.extensions['bcrypt']
        hashed_password = bcrypt_instance.generate_password_hash(form.password.data).decode('utf-8')
        
        # O restante do código de registro é movido para dentro do if
        user = User(username=form.username.data, password_hash=hashed_password)
        db.session.add(user)
        # db.session.commit() # Commit será feito após criar o horário
        
        novo_horario = Horario(nome=f"Horário de {user.username}", autor=user)
        db.session.add(novo_horario)
        horarios_texto_padrao = ["13:10", "14:00", "14:50", "16:00", "16:50"]
        for dia in range(5): 
            for pos in range(1, 6):
                bloco = BlocoAula(
                    horario=novo_horario, 
                    dia_semana=dia, 
                    posicao_aula=pos,
                    texto_horario=horarios_texto_padrao[pos-1]
                )
                db.session.add(bloco)
        db.session.commit()
        
        flash('Sua conta foi criada! Você já pode fazer o login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # CORREÇÃO 3: Deve apontar para o endpoint do Blueprint 'core'
        return redirect(url_for('core.index')) 
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        # CORREÇÃO: Acesso ao Bcrypt (que deve estar registrada após o init_app em app.py)
        # Usa a instância importada diretamente
        bcrypt_instance = bcrypt if bcrypt else current_app.extensions['bcrypt']
        
        if user and bcrypt_instance.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login realizado com sucesso!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('core.index'))
        else:
            flash('Login falhou. Verifique o usuário e a senha.', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('auth.login'))