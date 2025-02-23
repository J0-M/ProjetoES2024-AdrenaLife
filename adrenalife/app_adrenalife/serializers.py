from rest_framework import serializers

from .models import categoria_atividade

class categoriaAtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = categoria_atividade
        fields = ['nome']