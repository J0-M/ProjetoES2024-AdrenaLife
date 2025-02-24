from rest_framework import serializers

from .models import categoria_atividade
from .models import atividade

class categoriaAtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = categoria_atividade
        fields = ['nome']
        
class atividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = atividade
        fields = ['nome', 'descricao', 'categoria']