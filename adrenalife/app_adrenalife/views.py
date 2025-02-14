from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json

from rest_framework.decorators import api_view
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


##########################


@api_view(['GET'])
def getCategoriasAtividades(request):
    if request.method == 'GET':
        categorias = categoria_atividade.objects.all()
        
        serializer = categoriaAtividadeSerializer(categorias, many=True)
        return Response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)
    



#Funções de acesso ao BD
# data = class.object.get(pk='parametro') = SELECT .. WHERE pk = parametro                  ##OBJETO
# data = class.object.filter(age='25') = filtrar SELECT, SELECT FROM class WHERE age = 25   ##QUERYSET
# data = class.object.exclude(age='25') = SELECT FROM class WHERE AGE != 25                 ##QUERYSET
# data.save() = Insere no banco de dados
# data.delete() = DELETE