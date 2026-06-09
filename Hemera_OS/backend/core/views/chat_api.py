import json
import uuid
import requests
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max, Q, Count
from core.models import CustomUser, Room, Message, ChatFolder

def get_current_user_from_request(request):
    user_id = request.headers.get('X-User-Id')
    if not user_id:
        user_id = request.GET.get('user_id')
    
    if user_id:
        if user_id == 'mock-professor-id':
            user = CustomUser.objects.filter(username='iansantos').first() or CustomUser.objects.filter(role='ADMIN').first() or CustomUser.objects.first()
            return user
        elif user_id == 'mock-aluno-id':
            user = CustomUser.objects.filter(username='lucas_silva').first() or CustomUser.objects.filter(role__icontains='ALUNO').first() or CustomUser.objects.first()
            return user
        elif user_id == 'mock-admin-id':
            user = CustomUser.objects.filter(username='iansantos').first() or CustomUser.objects.filter(role='ADMIN').first() or CustomUser.objects.first()
            return user
        else:
            try:
                return CustomUser.objects.get(id=user_id)
            except (CustomUser.DoesNotExist, ValueError):
                user = CustomUser.objects.filter(username=user_id).first()
                if user:
                    return user
    
    if request.user.is_authenticated:
        return request.user
        
    return CustomUser.objects.filter(username='iansantos').first() or CustomUser.objects.first()

def get_or_create_zios_bot():
    zios, created = CustomUser.objects.get_or_create(
        username='zios_bridge_bot',
        defaults={
            'first_name': '🤖 ZIOS Bridge',
            'last_name': '(PentaIA)',
            'role': 'bot',
            'email': 'zios@niocortex.test',
            'bio': 'Núcleo Cognitivo e assistente de IA oficial do Hemera OS. Pergunte-me qualquer dúvida sobre a BNCC ou matérias.',
        }
    )
    return zios

def _participant_payload(user: CustomUser):
    name = user.get_full_name() or user.username
    return {
        'id': str(user.id),
        'username': user.username,
        'name': name,
        'handle': f"@{user.username}",
        'initials': (name[:2] if len(name) >= 2 else user.username[:2]).upper(),
        'avatar': user.avatar.url if user.avatar else None,
        'role': user.role,
        'bio': user.bio or 'Sem descrição.',
        'phone': user.telefone or '',
    }

def _message_payload(message: Message, current_user=None):
    return {
        'id': message.id,
        'room_id': message.room_id,
        'sender': _participant_payload(message.sender),
        'content': message.content or '',
        'created_at': message.created_at.isoformat(),
        'is_read': message.is_read,
        'is_me': message.sender == current_user if current_user else False
    }

def chat_rooms_api(request):
    user = get_current_user_from_request(request)
    if not user:
        return JsonResponse({'error': 'Não autenticado'}, status=401)
        
    # Certificar que a sala do Zios Bridge existe para este usuário
    zios = get_or_create_zios_bot()
    if user != zios:
        zios_room = Room.objects.filter(type='dm', participants=user).filter(participants=zios).first()
        if not zios_room:
            zios_room = Room.objects.create(type='dm', name='🤖 ZIOS Bridge (PentaIA)')
            zios_room.participants.add(user, zios)
            Message.objects.create(
                room=zios_room,
                sender=zios,
                content="Olá! Eu sou o ZIOS-Bridge, o assistente inteligente cognitivo integrado ao Thorth. Consigo explicar dúvidas sobre os microsserviços do Hemera OS (como Hermes, Polis, Olimpo e HemeraLM), e também resolver exercícios acadêmicos da BNCC baseando-se nas suas fontes curriculares. Como posso ajudar você hoje?"
            )

    # Certificar que a sala do Grupão da Turma existe
    if user.turma:
        group_name = f"💬 Grupão do {user.turma.nome}"
        group_room = Room.objects.filter(type='group', name=group_name).first()
        if not group_room:
            group_room = Room.objects.create(
                type='group',
                name=group_name,
                description=f"Grupo de discussão oficial dos discentes e docentes da turma {user.turma.nome}."
            )
            # Adiciona membros da turma + professores de teste
            class_members = list(CustomUser.objects.filter(turma=user.turma))
            teachers = list(CustomUser.objects.filter(role__icontains='PROFESSOR'))
            group_room.participants.add(*class_members)
            group_room.participants.add(*teachers)
            
            Message.objects.create(
                room=group_room,
                sender=zios,
                content=f"Bem-vindos ao grupo oficial da turma {user.turma.nome}! Este canal é seguro e monitorado pelo Heimdall."
            )

    rooms_qs = (
        user.chat_rooms
        .prefetch_related('participants')
        .annotate(last_msg_time=Max('messages__created_at'))
        .order_by('-last_msg_time', '-updated_at')
    )

    payload = []
    for room in rooms_qs:
        participants = [_participant_payload(p) for p in room.participants.all()]
        other_participants = [p for p in participants if p['id'] != str(user.id)]
        
        last_message = room.messages.select_related('sender').order_by('-created_at').first()

        if room.type == 'dm' and other_participants:
            title = other_participants[0]['name']
            subtitle = other_participants[0]['handle']
            avatar = other_participants[0]['avatar']
            bio = other_participants[0]['bio']
            phone = other_participants[0]['phone']
            username = other_participants[0]['username']
            p_type = 'bot' if other_participants[0]['role'] == 'bot' else 'private'
        else:
            title = room.name or 'Grupo'
            subtitle = f"{room.participants.count()} membros"
            avatar = room.icon.url if room.icon else None
            bio = room.description or ''
            phone = ''
            username = f"@{room.name.lower().replace(' ', '_')}" if room.name else ''
            p_type = room.type  # 'group' or 'channel'

        payload.append({
            'id': room.id,
            'type': p_type,
            'title': title,
            'subtitle': subtitle,
            'avatar': avatar,
            'bio': bio,
            'phone': phone,
            'username': username,
            'last_message': _message_payload(last_message, user) if last_message else None,
            'unread_count': room.messages.exclude(sender=user).filter(is_read=False).count(),
        })

    return JsonResponse({'rooms': payload})

def chat_messages_api(request, room_id):
    user = get_current_user_from_request(request)
    if not user:
        return JsonResponse({'error': 'Não autenticado'}, status=401)
        
    room = get_object_or_404(user.chat_rooms, id=room_id)
    messages = room.messages.select_related('sender').order_by('created_at')[:200]
    
    # Marcar lidas
    room.messages.exclude(sender=user).filter(is_read=False).update(is_read=True)

    return JsonResponse({
        'room_id': room.id,
        'messages': [_message_payload(m, user) for m in messages],
    })

@csrf_exempt
def create_message_api(request, room_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Apenas POST permitido'}, status=405)
        
    user = get_current_user_from_request(request)
    if not user:
        return JsonResponse({'error': 'Não autenticado'}, status=401)
        
    room = get_object_or_404(user.chat_rooms, id=room_id)
    
    try:
        body = json.loads(request.body)
        content = body.get('content', '').strip()
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
        
    if not content:
        return JsonResponse({'error': 'Mensagem vazia'}, status=400)
        
    message = Message.objects.create(
        room=room,
        sender=user,
        content=content
    )
    
    # Zios Reply Automation
    zios = get_or_create_zios_bot()
    is_zios_dm = room.type == 'dm' and room.participants.filter(id=zios.id).exists()
    
    if is_zios_dm and user != zios:
        payload = {
            "message": content,
            "role": "zios",
            "user_name": user.get_full_name() or user.username,
            "context": {
                "user_role": user.role,
                "school": user.school.nome if user.school else "Hemera OS"
            }
        }
        
        reply_content = None
        for url in ["http://pentaia:8001/v1/chat/interact", "http://localhost:8001/v1/chat/interact"]:
            try:
                response = requests.post(url, json=payload, timeout=10)
                if response.status_code == 200:
                    reply_content = response.json().get('reply')
                    break
            except Exception as e:
                pass
                
        if not reply_content:
            query = content.lower()
            if "hermes" in query:
                reply_content = "O módulo Hemera Hermes é o nosso ERP de gestão administrativa e repasses financeiros. Ele opera com imutabilidade rígida de dados via Event Sourcing sobre transações ACID. Isso impede qualquer fraude de exclusão direta de boletos ou mensalidades."
            elif "polis" in query:
                reply_content = "A Polis é o portal de colaboração social da turma! Ela unifica o mural de avisos fixados da diretoria (como gincanas e conselhos), o feed de posts dos estudantes com curtidas e comentários, o cofre de arquivos da aula e agora o Ambiente EAD Moodle."
            elif "olimpo" in query:
                reply_content = "O Olimpo é o portal administrativo centralizado da reitoria, controlando métricas de evasão escolar, gamificação e controle de prêmios acadêmicos."
            elif "moodle" in query or "ead" in query:
                reply_content = "O Ambiente Moodle agora está integrado diretamente dentro da aba da Polis! Lá você confere os materiais de aula estruturados por tópicos semanais, assiste a videoaulas, responde questionários interativos de fixação e envia tarefas curriculares."
            elif "olá" in query or "ola" in query or "oi" in query:
                reply_content = f"Olá {payload['user_name']}! Como posso ajudar você no ecossistema de inteligência Hemera OS hoje? Digite sua dúvida sobre os módulos (Hermes, Polis, Olimpo, HemeraLM) ou matérias pedagógicas."
            else:
                reply_content = f"Recebi sua mensagem. Analisando a documentação sob a PentaIA, entendi que sua dúvida está associada a '{content}'. Deseja que eu analise seus arquivos no HemeraLM para um grounding mais detalhado com base na BNCC?"
                
        bot_message = Message.objects.create(
            room=room,
            sender=zios,
            content=reply_content
        )
        
        return JsonResponse({
            'message': _message_payload(message, user),
            'reply': _message_payload(bot_message, user)
        })
        
    return JsonResponse({'message': _message_payload(message, user)})

@csrf_exempt
def start_dm_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Apenas POST permitido'}, status=405)
        
    user = get_current_user_from_request(request)
    if not user:
        return JsonResponse({'error': 'Não autenticado'}, status=401)
        
    try:
        body = json.loads(request.body)
        username = body.get('username', '').strip()
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
        
    if not username:
        return JsonResponse({'error': 'username é obrigatório.'}, status=400)
        
    target_user = get_object_or_454(CustomUser, username=username)
    if target_user == user:
        return JsonResponse({'error': 'Não é possível criar chat com você mesmo.'}, status=400)
        
    dm_room = (
        user.chat_rooms
        .filter(type='dm', participants=target_user)
        .annotate(participant_count=Count('participants'))
        .filter(participant_count=2)
        .first()
    )
    
    if not dm_room:
        dm_room = Room.objects.create(type='dm')
        dm_room.participants.add(user, target_user)
        
    return JsonResponse({'room_id': dm_room.id})

def search_users_api(request):
    user = get_current_user_from_request(request)
    if not user:
        return JsonResponse({'error': 'Não autenticado'}, status=401)
        
    query = request.GET.get('q', '').strip()
    
    zios = get_or_create_zios_bot()
    users_qs = CustomUser.objects.exclude(id=user.id).exclude(id=zios.id)
    
    if query:
        users_qs = users_qs.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )
        
    users_qs = users_qs[:50]
    payload = [_participant_payload(u) for u in users_qs]
    
    return JsonResponse({'users': payload})
