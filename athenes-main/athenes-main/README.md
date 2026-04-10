# 🏛️ ATHENES - Ambiente Virtual de Aprendizagem

Sistema completo de AVA (Ambiente Virtual de Aprendizagem) com design Glassmorphism/Alpine, inteligência artificial Zeus, e integração com APIs de bibliotecas.

## ✨ Funcionalidades

- **👨‍🎓 Área do Aluno**: Dashboard, cursos, materiais, biblioteca
- **👨‍🏫 Área do Professor**: Upload de aulas, gerenciamento de cursos, analytics
- **🤖 Zeus AI**: Assistente de aprendizagem integrado
- **📚 Biblioteca Digital**: Integração com Google Books, Open Library
- **🎬 Player de Vídeo**: Streaming com materiais anexos
- **📱 Design Responsivo**: Glassmorphism, Aurora gradients, animações

## 🚀 Instalação Rápida

### Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

Acesse: http://localhost:5173

### Backend (Django)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

API: http://localhost:8000

### FastAPI

```bash
cd backend
uvicorn fastapi_app.main:app --reload --port 8001
```

API: http://localhost:8001

## 🐳 Docker (Opcional)

```bash
docker-compose up --build
```

## 📁 Estrutura do Projeto

```
athenes/
├── frontend/          # React + TypeScript + Tailwind
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── store/
│   │   └── styles/
│   └── package.json
├── backend/           # Django + FastAPI
│   ├── django_core/
│   ├── apps/
│   ├── fastapi_app/
│   └── requirements.txt
└── docker-compose.yml
```

## 🔑 Tecnologias

**Frontend:**
- React 18 + TypeScript
- Vite
- Tailwind CSS
- Framer Motion
- Zustand (state management)
- React Query
- Lucide Icons

**Backend:**
- Django 4.2
- Django REST Framework
- FastAPI
- PostgreSQL
- Redis
- Celery
- OpenAI API

## 🎨 Design System

- **Estilo**: Glassmorphism, Alpine Clean, Light Theme
- **Cores**: Alpine Blue, Zeus Indigo, Aurora gradients
- **Fontes**: Inter (body), Space Grotesk (headings)
- **Animações**: Float, fade-in, smooth transitions

## 📝 Licença

MIT License - Universidade/Instituição
