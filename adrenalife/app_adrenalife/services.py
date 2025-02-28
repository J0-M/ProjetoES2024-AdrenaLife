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

from .models import atividade, categoria_atividade, InscricaoEvento, Usuario
from .serializers import atividadeSerializer, categoriaAtividadeSerializer, eventoSerializer

from .models import Evento

class CategoriaAtividadeService:
    @staticmethod
    def create_categoria(request):
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
    
    @staticmethod
    def get_categoria(request):
        
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
        
    @staticmethod
    def update_categoria(request):
        data = request.data
        name = request.GET.get('nome', None)
        
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
    
    @staticmethod
    def delete_categoria(request):
        name = request.GET.get('nome', None)
        
        if not name:
            return Response({"Nome não informado"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            categoria = categoria_atividade.objects.get(nome=name)
            
            categoria.delete()
            return Response(status=status.HTTP_200_OK)
        
        except:
            return Response({"Categoria não encontrada"}, status=status.HTTP_404_NOT_FOUND)
        




class AtividadeService:
    @staticmethod
    def create_atividade(request):
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
    
    @staticmethod
    def get_atividade(request):
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
    
    @staticmethod
    def update_atividade(request):
        data = request.data
        identificador = request.GET.get('id', None)
        
        if not identificador:
            return Response({"Id não informado"}, status=status.HTTP_400_BAD_REQUEST)
        
        nameTest = data.get("nome", None)
        atividadeTest = atividade.objects.filter(nome=nameTest)
        
        if nameTest and atividade.objects.filter(nome=nameTest).exclude(id=identificador).exists():
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
    
    @staticmethod
    def delete_atividade(request):
        identificador = request.GET.get('id', None)
        
        if not id:
            return Response({"Id não informado"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            att = atividade.objects.get(id=identificador)
            
            att.delete()
            return Response(status=status.HTTP_200_OK)
        
        except:
            return Response({"Atividade não encontrada"}, status=status.HTTP_404_NOT_FOUND)
        




class EventoService:
    @staticmethod
    def create_evento(request):
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
    
    @staticmethod
    def get_evento(request):
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
    
    @staticmethod
    def update_evento(request):
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
    
    @staticmethod
    def delete_evento(request):
        identificador = request.GET.get('id', None)
        
        if not id:
            return Response({"Id não informado"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            evt = Evento.objects.get(id=identificador)
            
            evt.delete()
            return Response(status=status.HTTP_200_OK)
        
        except:
            return Response({"Evento não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
class InscricaoService:
    @staticmethod
    def create_inscricao(request):
        usuario_id = request.data.get('usuario_id')
        evento_id = request.data.get('evento_id')

        if not usuario_id or not evento_id:
            return Response({"error": "Usuário e Evento são necessários."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = Usuario.objects.get(id_usuario=usuario_id)
            evento = Evento.objects.get(id=evento_id)
        except Usuario.DoesNotExist:
            return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Evento.DoesNotExist:
            return Response({"error": "Evento não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        if usuario.eventos_inscritos.filter(id=evento.id).exists():
            return Response({"message": "Usuário já inscrito neste evento."}, status=status.HTTP_200_OK)

        try:
            inscricao = InscricaoEvento.objects.create(usuario=usuario, evento=evento)
            
            evento.vagas_disponiveis -= 1
            evento.save()
            
            return Response({"message": f"Usuário {usuario.nome} inscrito no evento {evento.nome} com sucesso!"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @staticmethod
    def delete_inscricao(request):
        usuario_id = request.data.get('usuario_id')
        evento_id = request.data.get('evento_id')

        if not usuario_id or not evento_id:
            return Response({"error": "Usuário e Evento são necessários."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = Usuario.objects.get(id_usuario=usuario_id)
            evento = Evento.objects.get(id=evento_id)
        except Usuario.DoesNotExist:
            return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Evento.DoesNotExist:
            return Response({"error": "Evento não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        inscricao = InscricaoEvento.objects.filter(usuario=usuario, evento=evento).first()

        if not inscricao:
            return Response({"error": "Usuário não está inscrito neste evento."}, status=status.HTTP_400_BAD_REQUEST)

        inscricao.delete()

        evento.vagas_disponiveis += 1
        evento.save()

        return Response({"message": f"Inscrição de {usuario.nome} no evento {evento.nome} cancelada com sucesso! Vagas restantes: {evento.vagas_disponiveis}"}, status=status.HTTP_200_OK)