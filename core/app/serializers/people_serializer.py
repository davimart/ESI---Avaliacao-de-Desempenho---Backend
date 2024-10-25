from rest_framework import serializers
from core.models.people import Usuario, Aluno, Orientador


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'


class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = '__all__'


class OrientadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orientador
        fields = '__all__'
