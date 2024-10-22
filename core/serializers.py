from rest_framework import serializers
from .models import Disciplina

from rest_framework import serializers
from .models import Aluno, Orientador, Comissao, Disciplina, Relatorio, Avaliacao, Chamado

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = '__all__'

class OrientadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orientador
        fields = '__all__'

class ComissaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comissao
        fields = '__all__'

class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = '__all__'

class RelatorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relatorio
        fields = '__all__'

class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = '__all__'

class ChamadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chamado
        fields = '__all__'

