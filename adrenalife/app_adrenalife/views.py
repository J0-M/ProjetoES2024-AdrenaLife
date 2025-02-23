from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json

from django.views.decorators.csrf import csrf_exempt

from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .models import categoria_atividade
from .serializers import categoriaAtividadeSerializer


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

        if categoriaName:
            try:
                categoria = categoria_atividade.objects.get(nome=categoriaName)
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

#Funções de acesso ao BD
# data = class.object.get(campo='parametro') = SELECT .. WHERE pk = parametro                  ##OBJETO
# data = class.object.filter(age='25') = filtrar SELECT, SELECT FROM class WHERE age = 25   ##QUERYSET
# data = class.object.exclude(age='25') = SELECT FROM class WHERE AGE != 25                 ##QUERYSET
# data.save() = Insere no banco de dados
# data.delete() = DELETE