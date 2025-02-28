from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
import traceback
from django.core.exceptions import ValidationError
from datetime import datetime, date
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import atividade, categoria_atividade, Evento, Usuario, InscricaoEvento
from .serializers import atividadeSerializer, categoriaAtividadeSerializer, eventoSerializer
from .services import CategoriaAtividadeService, AtividadeService, EventoService, InscricaoService

def home(request):
    return render(request, 'usuarios/home.html')

def cadastro_evento(request):
    return render(request, 'eventos/cadastro_evento.html')

def cadastro_atividades(request):
    return render(request, 'atividades/cadastro_atividades.html')

def categoria_atividades(request):
    return render(request, 'atividades/categoria_atividades.html')
##########################

def init_aplicacao():
    return redirect('login')

def logout(request):
    request.session.flush()
    messages.success(request, 'Você saiu da sua conta.')
    return redirect('login')

def listar_eventos(request):
    if not request.session.get('usuario_id'):
        return redirect('login')

    usuario_id = request.session.get('usuario_id')
    
    data_selecionada = request.GET.get('data', None)
    eventos = Evento.objects.all()

    if data_selecionada:
        data_selecionada = datetime.strptime(data_selecionada, '%Y-%m-%d').date()
        eventos = eventos.filter(data=data_selecionada)

    return render(request, 'eventos/listar_eventos.html', {'eventos': eventos, 'data_selecionada': data_selecionada, 'usuario_id': usuario_id})

def criar_usuario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        data_nascimento = request.POST.get('data_nascimento')
        telefone = request.POST.get('telefone')
        cidade = request.POST.get('cidade')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        tipo_usuario = request.POST.get('tipo_usuario')

        # Cria uma instância do modelo para validar os campos
        usuario = Usuario(
            nome=nome,
            cpf=cpf,
            data_nascimento=data_nascimento,
            telefone=telefone,
            cidade=cidade,
            email=email,
            senha=senha,
            tipo_usuario=tipo_usuario
        )

        try:
            usuario.full_clean() 
            usuario.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('login')
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                for error in errors:
                    messages.error(request, f'Erro no campo {field}: {error}')
            return redirect('criar_usuario')

    return render(request, 'usuarios/criar_conta.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            usuario = Usuario.objects.get(email=email, senha=senha)
            request.session['usuario_id'] = usuario.id_usuario
            request.session['tipo_usuario'] = usuario.tipo_usuario
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('home')
        except Usuario.DoesNotExist:
            messages.error(request, 'Email ou senha incorretos.')
            return redirect('login')

    return render(request, 'usuarios/login.html')

def perfil(request):
    if not request.session.get('usuario_id'):  # Verifica se o usuário está logado
        return redirect('login')

    try:
        # Busca o usuário pelo campo id_usuario
        usuario = Usuario.objects.get(id_usuario=request.session['usuario_id'])
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuário não encontrado.')
        return redirect('login')

    # Obtém os eventos nos quais o usuário está inscrito
    eventos_inscritos = usuario.eventos_inscritos.all()

    if request.method == 'POST':
        # Atualiza os dados do usuário
        usuario.nome = request.POST.get('nome')
        usuario.cidade = request.POST.get('cidade')
        usuario.telefone = request.POST.get('telefone')
        usuario.save()
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('perfil')

    # Passa o objeto 'usuario' e a lista de 'eventos_inscritos' para o template
    return render(request, 'usuarios/perfil.html', {'usuario': usuario, 'eventos_inscritos': eventos_inscritos})

def alterar_senha(request):
    if not request.session.get('usuario_id'):
        return redirect('login')

    usuario = Usuario.objects.get(id_usuario=request.session['usuario_id'])

    if request.method == 'POST':
        senha_atual = request.POST.get('senha_atual')
        nova_senha = request.POST.get('nova_senha')

        if usuario.senha == senha_atual:
            usuario.senha = nova_senha
            usuario.save()
            messages.success(request, 'Senha alterada com sucesso!')
        else:
            messages.error(request, 'Senha atual incorreta.')

        return redirect('perfil')

    return redirect('perfil')

@csrf_protect
def excluir_conta(request):
    if not request.session.get('usuario_id'):
        return redirect('login')

    if request.method == 'POST':
        try:
            usuario = Usuario.objects.get(id_usuario=request.session['usuario_id'])
            usuario.delete()
            request.session.flush()  # Limpa a sessão
            messages.success(request, 'Conta excluída com sucesso!')
            return redirect('login')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')
            return redirect('perfil')

    return redirect('perfil')

@csrf_exempt
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([AllowAny])
def categoriaManager(request):
    
    if request.method == 'GET':
        return (CategoriaAtividadeService.get_categoria(request))
    
    if request.method == 'POST':
        return(CategoriaAtividadeService.create_categoria(request))
    
    if request.method == 'PUT':
        return(CategoriaAtividadeService.update_categoria(request))
    
    if request.method == 'DELETE':
        return(CategoriaAtividadeService.delete_categoria(request))
        
@csrf_exempt
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([AllowAny])
def atividadeManager(request):
    
    if request.method == 'GET':
        return(AtividadeService.get_atividade(request))
    
    if request.method == 'POST':
        return(AtividadeService.create_atividade(request))
    
    if request.method == 'PUT':
        return(AtividadeService.update_atividade(request))
    
    if request.method == 'DELETE':
        return(AtividadeService.delete_atividade(request))
        


#Funções de acesso ao BD
# data = class.object.get(campo='parametro') = SELECT .. WHERE pk = parametro                  ##OBJETO
# data = class.object.filter(age='25') = filtrar SELECT, SELECT FROM class WHERE age = 25   ##QUERYSET
# data = class.object.exclude(age='25') = SELECT FROM class WHERE AGE != 25                 ##QUERYSET
# data.save() = Insere no banco de dados
# data.delete() = DELETE

@csrf_exempt
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([AllowAny])
def eventoManager(request):
    
    # GET
    if request.method == 'GET':
        return(EventoService.get_evento(request))

    # POST
    if request.method == 'POST':
        return(EventoService.create_evento(request))
    
    # PUT
    if request.method == 'PUT':
        return(EventoService.update_evento(request))
        
    # DELETE
    if request.method == 'DELETE':
        return(EventoService.delete_evento(request))

@api_view(['POST', 'DELETE'])
def inscricaoManager(request):
    if request.method == 'DELETE' or request.data.get('_method') == 'DELETE':
        return(InscricaoService.delete_inscricao(request))
    
    if request.method == 'POST':
        return(InscricaoService.create_inscricao(request))