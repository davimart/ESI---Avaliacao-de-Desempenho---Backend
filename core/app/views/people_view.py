from rest_framework import viewsets

from core.models.system import Aluno, Orientador
from ..serializers.people_serializer import AlunoSerializer, OrientadorSerializer


class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer


class OrientadorViewSet(viewsets.ModelViewSet):
    queryset = Orientador.objects.all()
    serializer_class = OrientadorSerializer
