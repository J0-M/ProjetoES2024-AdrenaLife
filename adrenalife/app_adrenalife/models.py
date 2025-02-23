from django.db import models

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField(null=True)
    telefone = models.CharField(max_length=9)
    cidade = models.TextField(max_length=255)
    meio = models.TextField(max_length=255)
    email = models.EmailField(max_length=254)
    senha = models.CharField(max_length=8, null=True)
    
class atividade(models.Model):
    #relacionamento com categoria
    id = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=255, default='')
    descricao = models.TextField(max_length=255, default='')
    def __str__(self):
        return f'Nome: {self.nome} | Descrição: {self.descricao}'

class Evento(models.Model):
    #relacionamento com atividade 
    id = models.IntegerField(primary_key=True)
    valor = models.IntegerField()
    vagas_disponiveis = models.IntegerField()
    data = models.DateTimeField()

class categoria_atividade(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.TextField(max_length=255, default='')
    def __str__(self):
        return f'Nome: {self.nome}'

