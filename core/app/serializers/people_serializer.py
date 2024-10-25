from rest_framework import serializers
from core.models.system import Aluno, Orientador


class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = '__all__'


class OrientadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orientador
        fields = '__all__'
