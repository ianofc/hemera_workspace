import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, 'lumenios', 'templates', 'pedagogico', 'turmas', 'form_turmas.html')

def update_template():
    print(f"🎨 Aplicando estilo Glass Aurora em: {TEMPLATE_PATH}")
    
    html = """{% extends "professor/base_professor.html" %}
{% load static %}

{% block title %}Gerenciar Turma | Cortex{% endblock %}

{% block content %}

<div class="fixed inset-0 overflow-hidden pointer-events-none -z-10">
    <div class="absolute top-0 left-1/4 w-96 h-96 bg-[#6200EA] rounded-full mix-blend-multiply filter blur-[128px] opacity-20 animate-blob"></div>
    <div class="absolute top-0 right-1/4 w-96 h-96 bg-cyan-400 rounded-full mix-blend-multiply filter blur-[128px] opacity-20 animate-blob animation-delay-2000"></div>
    <div class="absolute -bottom-32 left-1/3 w-96 h-96 bg-pink-400 rounded-full mix-blend-multiply filter blur-[128px] opacity-20 animate-blob animation-delay-4000"></div>
</div>

<div class="relative z-10 max-w-2xl pt-10 pb-20 mx-auto">

    <div class="mb-10 text-center animate-fade-in-down">
        <span class="inline-flex items-center gap-2 px-3 py-1 text-[10px] font-bold tracking-widest text-[#6200EA] uppercase bg-white/40 border border-white/50 rounded-full backdrop-blur-md mb-4 shadow-sm">
            {% if form.instance.pk %}
                <i class="fas fa-edit"></i> Edição
            {% else %}
                <i class="fas fa-plus"></i> Cadastro
            {% endif %}
        </span>
        <h1 class="mb-2 text-4xl font-black tracking-tight text-slate-800 dark:text-white">
            Gerenciar <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#6200EA] to-purple-500">Turma</span>
        </h1>
        <p class="font-medium text-slate-500">
            Configure os detalhes da turma para o ano letivo.
        </p>
    </div>

    <div class="bg-white/70 dark:bg-slate-900/70 backdrop-blur-2xl rounded-[2.5rem] shadow-2xl border border-white/40 dark:border-white/5 p-8 md:p-12 relative overflow-hidden animate-fade-in-up">
        
        <div class="absolute top-0 right-0 w-40 h-40 bg-gradient-to-bl from-[#6200EA]/10 to-transparent rounded-bl-full pointer-events-none"></div>

        <form method="POST" class="relative z-10 space-y-8">
            {% csrf_token %}
            
            {% if form.non_field_errors %}
                <div class="flex items-start gap-3 p-4 border border-red-100 bg-red-50 rounded-2xl">
                    <i class="fas fa-exclamation-circle text-red-500 mt-0.5"></i>
                    <div class="text-xs font-bold text-red-600">
                        {{ form.non_field_errors }}
                    </div>
                </div>
            {% endif %}

            <div class="group">
                <label for="{{ form.nome.id_for_label }}" class="block text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-2 group-hover:text-[#6200EA] transition-colors pl-2">
                    Nome da Turma <span class="text-red-500">*</span>
                </label>
                <div class="relative">
                    <input type="text" name="nome" id="{{ form.nome.id_for_label }}" 
                           value="{{ form.nome.value|default:'' }}"
                           class="w-full px-6 py-4 rounded-2xl bg-white/50 border border-indigo-100 focus:border-[#6200EA] focus:ring-4 focus:ring-[#6200EA]/10 outline-none font-bold text-slate-700 placeholder-slate-400 transition-all"
                           placeholder="Ex: 9º Ano A - Matutino" required>
                    <div class="absolute inset-y-0 right-0 flex items-center px-6 pointer-events-none text-slate-400">
                        <i class="fas fa-layer-group"></i>
                    </div>
                </div>
                {% if form.nome.errors %}
                    <p class="flex items-center gap-1 pl-2 mt-2 text-xs font-bold text-red-500">
                        <i class="fas fa-exclamation-circle"></i> {{ form.nome.errors.0 }}
                    </p>
                {% endif %}
            </div>

            <div class="group">
                <label for="{{ form.ano_letivo.id_for_label }}" class="block text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-2 group-hover:text-[#6200EA] transition-colors pl-2">
                    Ano Letivo <span class="text-red-500">*</span>
                </label>
                <div class="relative">
                    <input type="number" name="ano_letivo" id="{{ form.ano_letivo.id_for_label }}" 
                           value="{{ form.ano_letivo.value|default:'2025' }}"
                           class="w-full px-6 py-4 rounded-2xl bg-white/50 border border-indigo-100 focus:border-[#6200EA] focus:ring-4 focus:ring-[#6200EA]/10 outline-none font-bold text-slate-700 placeholder-slate-400 transition-all">
                    <div class="absolute inset-y-0 right-0 flex items-center px-6 pointer-events-none text-slate-400">
                        <i class="fas fa-calendar-alt"></i>
                    </div>
                </div>
                {% if form.ano_letivo.errors %}
                    <p class="flex items-center gap-1 pl-2 mt-2 text-xs font-bold text-red-500">
                        <i class="fas fa-exclamation-circle"></i> {{ form.ano_letivo.errors.0 }}
                    </p>
                {% endif %}
            </div>

            <div class="flex flex-col-reverse gap-4 pt-6 border-t md:flex-row border-indigo-50 dark:border-indigo-900/20">
                <a href="{% url 'pedagogico:listar_turmas' %}" 
                   class="w-full py-4 text-xs font-bold tracking-wider text-center uppercase transition-colors shadow-sm md:w-1/3 bg-slate-100 hover:bg-slate-200 text-slate-600 rounded-2xl">
                    Cancelar
                </a>
                
                <button type="submit" 
                        class="w-full md:w-2/3 py-4 bg-gradient-to-r from-[#6200EA] to-purple-600 hover:from-[#5000BF] hover:to-purple-700 text-white rounded-2xl shadow-xl shadow-purple-500/30 font-bold uppercase tracking-wider text-xs transition-all transform hover:-translate-y-1 hover:shadow-2xl flex items-center justify-center gap-3">
                    <i class="fas fa-save"></i> 
                    {% if form.instance.pk %}Salvar Alterações{% else %}Criar Turma{% endif %}
                </button>
            </div>

        </form>
    </div>
</div>

<style>
    .animate-blob { animation: blob 7s infinite; }
    .animation-delay-2000 { animation-delay: 2s; }
    .animation-delay-4000 { animation-delay: 4s; }
    @keyframes blob {
        0% { transform: translate(0px, 0px) scale(1); }
        33% { transform: translate(30px, -50px) scale(1.1); }
        66% { transform: translate(-20px, 20px) scale(0.9); }
        100% { transform: translate(0px, 0px) scale(1); }
    }
</style>

{% endblock %}
"""
    with open(TEMPLATE_PATH, 'w', encoding='utf-8') as f:
        f.write(html)
    print("✅ Template form_turmas.html atualizado com estilo Glass Aurora!")

if __name__ == "__main__":
    update_template()