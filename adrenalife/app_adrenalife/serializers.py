from rest_framework import serializers

from .models import categoria_atividade
from .models import atividade
from .models import Evento
from .models import InscricaoEvento
from .models import Usuario

class categoriaAtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = categoria_atividade
        fields = ['id', 'nome']
        read_only_fields = ['id']
        
class atividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = atividade
        fields = ['id', 'nome', 'descricao', 'categoria']
        
class eventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = ['id', 'nome', 'atividade', 'valor', 'vagas_disponiveis', 'data']
        
class InscricaoEventoSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())
    evento = serializers.PrimaryKeyRelatedField(queryset=Evento.objects.all())

    class Meta:
        model = InscricaoEvento
        fields = '__all__'