from rest_framework import serializers

from .models import categoria_atividade
from .models import atividade

class categoriaAtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = categoria_atividade
        fields = ['id', 'nome']
        read_only_fields = ['id']
        
class atividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = atividade
        fields = ['id', 'nome', 'descricao', 'categoria']