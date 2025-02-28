from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError

from datetime import datetime, date

from rest_framework.response import Response
from rest_framework import status

from .models import atividade, categoria_atividade, InscricaoEvento, Usuario, Evento
from .serializers import atividadeSerializer, categoriaAtividadeSerializer, eventoSerializer

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
    
class UserServices:
    @staticmethod
    def logout(request):
        request.session.flush()
        messages.success(request, 'Você saiu da sua conta.')
        return redirect('login')
    
    @staticmethod
    def listagem_eventos(request):
        if not request.session.get('usuario_id'):
            return redirect('login')

        usuario_id = request.session.get('usuario_id')
        
        data_selecionada = request.GET.get('data', None)
        eventos = Evento.objects.all()

        if data_selecionada:
            data_selecionada = datetime.strptime(data_selecionada, '%Y-%m-%d').date()
            eventos = eventos.filter(data=data_selecionada)

        return render(request, 'eventos/listar_eventos.html', {'eventos': eventos, 'data_selecionada': data_selecionada, 'usuario_id': usuario_id})
    
    @staticmethod
    def create_usuario(request):
        if request.method == 'POST':
            nome = request.POST.get('nome')
            cpf = request.POST.get('cpf')
            data_nascimento = request.POST.get('data_nascimento')
            telefone = request.POST.get('telefone')
            cidade = request.POST.get('cidade')
            email = request.POST.get('email')
            senha = request.POST.get('senha')
            tipo_usuario = request.POST.get('tipo_usuario')

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
                erros = {field: errors[0] for field, errors in e.message_dict.items()}  # Pega apenas o primeiro erro de cada campo
                return render(request, 'usuarios/criar_conta.html', {'erros': erros, 'dados': request.POST})  # Passa os erros e os dados preenchidos

        return render(request, 'usuarios/criar_conta.html')
    
    @staticmethod
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
    
    @staticmethod
    def perfil(request):
        if not request.session.get('usuario_id'):
            return redirect('login')

        try:
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

        # Passa o objeto 'usuario' para o template
        return render(request, 'usuarios/perfil.html', {'usuario': usuario, 'eventos_inscritos': eventos_inscritos})
    
    @staticmethod
    def alter_senha(request):
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
    
    @staticmethod
    def delete_usuario(request):
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