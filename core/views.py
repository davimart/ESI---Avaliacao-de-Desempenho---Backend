from django.shortcuts import render
from rest_framework import generics
from .models import Disciplina
from .serializers import DisciplinaSerializer

from rest_framework import viewsets
from .models import Aluno, Orientador, Comissao, Disciplina, Relatorio, Avaliacao, Chamado
from .serializers import AlunoSerializer, OrientadorSerializer, ComissaoSerializer, DisciplinaSerializer, RelatorioSerializer, AvaliacaoSerializer, ChamadoSerializer

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

class OrientadorViewSet(viewsets.ModelViewSet):
    queryset = Orientador.objects.all()
    serializer_class = OrientadorSerializer

class ComissaoViewSet(viewsets.ModelViewSet):
    queryset = Comissao.objects.all()
    serializer_class = ComissaoSerializer

class DisciplinaViewSet(viewsets.ModelViewSet):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer

class RelatorioViewSet(viewsets.ModelViewSet):
    queryset = Relatorio.objects.all()
    serializer_class = RelatorioSerializer

class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer

class ChamadoViewSet(viewsets.ModelViewSet):
    queryset = Chamado.objects.all()
    serializer_class = ChamadoSerializer
