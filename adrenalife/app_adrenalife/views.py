from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

from .services import CategoriaAtividadeService, AtividadeService, EventoService, InscricaoService, UserServices

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
    return(UserServices.logout(request))

def listar_eventos(request):
    return(UserServices.listagem_eventos(request))

def criar_usuario(request):
    return(UserServices.create_usuario(request))

def login(request):
    return(UserServices.login(request))

def perfil(request):
    return(UserServices.perfil(request))

def alterar_senha(request):
    return(UserServices.alter_senha(request))

@csrf_protect
def excluir_conta(request):
    return(UserServices.delete_usuario(request))

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