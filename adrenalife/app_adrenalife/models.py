from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date
import re

def validar_nome(value):
    if any(char.isdigit() for char in value):
        raise ValidationError(_('O nome não pode conter números.'))

def validar_cpf(value):
    cpf = re.sub(r'\D', '', value) 
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        raise ValidationError(_('CPF inválido.'))

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10 % 11) % 10
    if digito1 != int(cpf[9]):
        raise ValidationError(_('CPF inválido.'))

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10 % 11) % 10
    if digito2 != int(cpf[10]):
        raise ValidationError(_('CPF inválido.'))

def validar_email(value):
    if '@' not in value:
        raise ValidationError(_('O email deve conter um @.'))

def validar_data_nascimento(value):
    hoje = date.today()
    idade = hoje.year - value.year - ((hoje.month, hoje.day) < (value.month, value.day))
    if idade < 18:
        raise ValidationError(_('O usuário deve ter pelo menos 18 anos.'))

def validar_telefone(value):
    if value.isdigit() and (value in ['123456789', '987654321', value[0] * len(value)]):
        raise ValidationError(_('Número de telefone inválido.'))

def validar_cidade(value):
    if any(char.isdigit() for char in value):
        raise ValidationError(_('O nome da cidade não pode conter números.'))

class categoria_atividade(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.TextField(max_length=255, default='')
    def __str__(self):
        return f'Nome: {self.nome}'


class atividade(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=255, default='')
    descricao = models.TextField(max_length=255, default='')
    
    categoria = models.ForeignKey(categoria_atividade, on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return f'Nome: {self.nome} | Descrição: {self.descricao} | Categoria: {self.categoria.nome}'


class Evento(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=255, default='')
    atividade = models.ForeignKey(atividade, on_delete=models.CASCADE, null=False)
    valor = models.FloatField()
    vagas_disponiveis = models.IntegerField()
    data = models.DateField()
    
    def __str__(self):
        return f'Nome: {self.nome} | Atividade: {self.atividade.nome} | Valor: {self.valor} | Vagas Disponíveis: {self.vagas_disponiveis} | Data: {self.data}'


class Usuario(models.Model):
    TIPO_USUARIO_CHOICES = [
        ('cliente', 'Cliente'),
        ('funcionario', 'Funcionário'),
    ]

    id_usuario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, validators=[validar_nome])
    cpf = models.CharField(max_length=14, unique=True, validators=[validar_cpf])
    data_nascimento = models.DateField(validators=[validar_data_nascimento])
    telefone = models.CharField(max_length=11, validators=[validar_telefone])
    cidade = models.CharField(max_length=255, validators=[validar_cidade])
    email = models.EmailField(max_length=254, validators=[validar_email])
    senha = models.CharField(max_length=8)
    tipo_usuario = models.CharField(max_length=11, choices=TIPO_USUARIO_CHOICES, default='cliente')
    
    eventos_inscritos = models.ManyToManyField("Evento", through="InscricaoEvento")

    def __str__(self):
        return f'{self.nome} ({self.tipo_usuario})'
    
class InscricaoEvento(models.Model):
    usuario = models.ForeignKey("Usuario", on_delete=models.CASCADE)
    evento = models.ForeignKey("Evento", on_delete=models.CASCADE)
    data_inscricao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'evento')

    def __str__(self):
        return f'{self.usuario.nome} inscrito em {self.evento.nome}'