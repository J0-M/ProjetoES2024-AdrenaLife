from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
import traceback
from datetime import datetime, date

from django.views.decorators.csrf import csrf_exempt

from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .models import atividade, categoria_atividade
from .serializers import atividadeSerializer, categoriaAtividadeSerializer, eventoSerializer

from .models import Evento

def home(request):
    return render(request, 'usuarios/home.html')

def cadastro_evento(request):
    return render(request, 'eventos/cadastro_evento.html')

def cadastro_atividades(request):
    return render(request, 'atividades/cadastro_atividades.html')

def categoria_atividades(request):
    return render(request, 'atividades/categoria_atividades.html')
##########################

@csrf_exempt
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([AllowAny])
def categoriaManager(request):
    
    # GET um objeto
    
    if request.method == 'GET':
        categoriaName = request.GET.get('nome', None)
        categoriaId = request.GET.get('id', None)

        if categoriaName:
            try:
                categoria = categoria_atividade.objects.get(nome=categoriaName)
                serializer = categoriaAtividadeSerializer(categoria)
                return Response(serializer.data)
            except categoria_atividade.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif categoriaId:
            try:
                categoria = categoria_atividade.objects.get(id=categoriaId)
                serializer = categoriaAtividadeSerializer(categoria)
                return Response(serializer.data)
            except categoria_atividade.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:    
            categorias = categoria_atividade.objects.all()
            serializer = categoriaAtividadeSerializer(categorias, many=True)
            return Response(serializer.data)

    #POST
    
    if request.method == 'POST':
        
        newCategoria = request.data
        name = newCategoria.get("nome", None)
        
        categoriaTest = categoria_atividade.objects.filter(nome=name)
        
        if categoriaTest.exists():
            return Response({"Nome já cadastrado"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = categoriaAtividadeSerializer(data=newCategoria)
        
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PUT':
        
        data = request.data
        name = request.GET.get('nome', None) # api/categoia/?nome=xxxxx, xxxxx será o objeto a ser alterado
        
        if not name:
            return Response({"Nome não informado"}, status=status.HTTP_400_BAD_REQUEST)
        
        nameTest = data.get("nome", None)
        categoriaTest = categoria_atividade.objects.filter(nome=nameTest)
        
        if categoriaTest.exists():
            return Response({"Nome já cadastrado"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            updatedcategoria = categoria_atividade.objects.get(nome=name)
        
        except:
            return Response({"Categoria não encontrada"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = categoriaAtividadeSerializer(updatedcategoria, data=data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        name = request.GET.get('nome', None)  # name = ?nome=xxxxx
        
        if not name:
            return Response({"Nome não informado"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            categoria = categoria_atividade.objects.get(nome=name)
            
            categoria.delete()
            return Response(status=status.HTTP_200_OK)
        
        except:
            return Response({"Categoria não encontrada"}, status=status.HTTP_404_NOT_FOUND)
        
@csrf_exempt
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([AllowAny])
def atividadeManager(request):
    
    if request.method == 'GET':
        atividadeId = request.GET.get('id', None)

        if atividadeId:
            try:
                att = atividade.objects.get(id=atividadeId)
                serializer = atividadeSerializer(att)
                return Response(serializer.data)
            except atividade.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            atividades = atividade.objects.all()
            serializer = atividadeSerializer(atividades, many=True)
            return Response(serializer.data)
    
    if request.method == 'POST':
        
        newAtividade = request.data
        name = newAtividade.get("nome", None)
        description = newAtividade.get("descricao", None)
        category = newAtividade.get("categoria", None)
        
        if not name or not description or not category:
            return Response({"Preencha todos os campos"}, status=status.HTTP_400_BAD_REQUEST)
        
        categoriaTest = categoria_atividade.objects.filter(id = category)
        
        if not categoriaTest.exists():
            return Response({"Categoria inválida"}, status=status.HTTP_400_BAD_REQUEST)
        
        atividadeTest = atividade.objects.filter(nome=name)
        
        if atividadeTest.exists():
            return Response({"Nome já cadastrado"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = atividadeSerializer(data=newAtividade)
        
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
    
    if request.method == 'PUT':
        data = request.data
        identificador = request.GET.get('id', None)
        
        if not identificador:
            return Response({"Id não informado"}, status=status.HTTP_400_BAD_REQUEST)
        
        nameTest = data.get("nome", None)
        atividadeTest = atividade.objects.filter(nome=nameTest)
        
        if atividadeTest.exists():
            return Response({"Nome já cadastrado"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            updatedAtividade = atividade.objects.get(id=identificador)
        
        except:
            return Response({"Atividade não encontrada"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = atividadeSerializer(updatedAtividade, data=data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    if request.method == 'DELETE':
        identificador = request.GET.get('id', None)
        
        if not id:
            return Response({"Id não informado"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            att = atividade.objects.get(id=identificador)
            
            att.delete()
            return Response(status=status.HTTP_200_OK)
        
        except:
            return Response({"Atividade não encontrada"}, status=status.HTTP_404_NOT_FOUND)
    
    return None
        


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
    
    # GET um objeto
    
    if request.method == 'GET':
        eventoId = request.GET.get('id', None)

        if eventoId:
            try:
                evt = Evento.objects.get(id=eventoId)
                serializer = eventoSerializer(evt)
                return Response(serializer.data)
            except Evento.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            eventos = Evento.objects.all()
            serializer = eventoSerializer(eventos, many=True)
            return Response(serializer.data)

    # POST
    
    if request.method == 'POST':
        
        newEvento = request.data
        name = newEvento.get("nome", None)
        activity = newEvento.get("atividade", None)
        value = newEvento.get("valor", None)
        slots = newEvento.get("vagas_disponiveis", None)
        dateEvento = newEvento.get("data", None)
        
        if not name or not activity or not value or not slots or not dateEvento:
            return Response({"Preencha todos os campos"}, status=status.HTTP_400_BAD_REQUEST)
        
        dateEvento_obj = datetime.strptime(dateEvento, "%Y-%m-%d").date()
        if dateEvento_obj < date.today():
            return Response({"Data Inválida, Esta data já passou"}, status=status.HTTP_400_BAD_REQUEST)
        
        atividadeTest = atividade.objects.filter(id = activity)
        
        if not atividadeTest.exists():
            return Response({"Atividade inválida"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = eventoSerializer(data=newEvento)
        
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        
        # Mostrar qual o erro caso algo dê errado
        if not serializer.is_valid():
            return Response({"erro": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # PUT
    if request.method == 'PUT':
        data = request.data # alterações enviadas pelo json(pelo body)
        identificador = request.GET.get('id', None)
        dateEvento = data.get("data", None)
        
        if not identificador:
            return Response({"Id não informado"}, status=status.HTTP_400_BAD_REQUEST)
        
        dateEvento_obj = datetime.strptime(dateEvento, "%Y-%m-%d").date()
        if dateEvento_obj < date.today():
            return Response({"Data Inválida, Esta data já passou"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            updatedEvento = Evento.objects.get(id=identificador)
        
        except:
            return Response({"Evento não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = eventoSerializer(updatedEvento, data=data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    # DELETE
    if request.method == 'DELETE':
        identificador = request.GET.get('id', None)
        
        if not id:
            return Response({"Id não informado"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            evt = Evento.objects.get(id=identificador)
            
            evt.delete()
            return Response(status=status.HTTP_200_OK)
        
        except:
            return Response({"Evento não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
    return None
