from django.shortcuts import render
from .models import Evento

def home(request):
    return render(request, 'usuarios/home.html')

def cadastro_evento(request):
    return render(request, 'eventos/cadastro_evento.html')

def eventos(request):
    # salvar os dados da tela para o banco de dados
    novo_evento = Evento()
    novo_evento.valor = request.POST.get('valor')
    novo_evento.vagas_disponiveis = request.POST.get('vagas_disponiveis')
    novo_evento.data = request.POST.get('data')
    novo_evento.save
    # exibir todos os eventos já cadastrados
    eventos = {
        'eventos': Evento.objects.all()
    }
    # retornar os dados para a página de listagem de usuários
    return render(request, 'eventos/eventos.html', eventos)
        