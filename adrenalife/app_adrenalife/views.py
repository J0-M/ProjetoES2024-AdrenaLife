from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
import traceback
from datetime import datetime, date
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import atividade, categoria_atividade, Evento, Usuario
from .serializers import atividadeSerializer, categoriaAtividadeSerializer, eventoSerializer
from .services import CategoriaAtividadeService, AtividadeService, EventoService

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

def criar_usuario(request):
    if request.method == 'POST':
        # Coleta os dados do formulário
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        data_nascimento = request.POST.get('data_nascimento')
        telefone = request.POST.get('telefone')
        cidade = request.POST.get('cidade')
        meio = request.POST.get('meio')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # Verifica se o email já está cadastrado
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'Este email já está cadastrado.')
            return redirect('criar_usuario')

        # Verifica se o CPF já está cadastrado
        if Usuario.objects.filter(cpf=cpf).exists():
            messages.error(request, 'Este CPF já está cadastrado.')
            return redirect('criar_usuario')

        # Cria o usuário
        try:
            usuario = Usuario.objects.create(
                nome=nome,
                cpf=cpf,
                data_nascimento=data_nascimento,
                telefone=telefone,
                cidade=cidade,
                meio=meio,
                email=email,
                senha=senha 
            )
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('login') 
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar usuário: {str(e)}')
            return redirect('criar_usuario')

    return render(request, 'usuarios/criar_conta.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            usuario = Usuario.objects.get(email=email, senha=senha)
            request.session['usuario_id'] = usuario.id_usuario
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('home')
        except Usuario.DoesNotExist:
            messages.error(request, 'Email ou senha incorretos.')
            return redirect('login')

    return render(request, 'usuarios/login.html')

def perfil(request):
    if not request.session.get('usuario_id'): 
        return redirect('login')

    usuario = Usuario.objects.get(id_usuario=request.session['usuario_id'])

    if request.method == 'POST':
        novo_email = request.POST.get('email')
        novo_cpf = request.POST.get('cpf')

        if novo_email != usuario.email and Usuario.objects.filter(email=novo_email).exists():
            messages.error(request, 'Este email já está cadastrado.')
            return redirect('perfil')

        if novo_cpf != usuario.cpf and Usuario.objects.filter(cpf=novo_cpf).exists():
            messages.error(request, 'Este CPF já está cadastrado.')
            return redirect('perfil')

        usuario.nome = request.POST.get('nome')
        usuario.cpf = novo_cpf
        usuario.data_nascimento = request.POST.get('data_nascimento')
        usuario.telefone = request.POST.get('telefone')
        usuario.cidade = request.POST.get('cidade')
        usuario.meio = request.POST.get('meio')
        usuario.email = novo_email
        usuario.senha = request.POST.get('senha')
        usuario.save()
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('perfil')

    return render(request, 'usuarios/perfil.html', {'usuario': usuario})

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
