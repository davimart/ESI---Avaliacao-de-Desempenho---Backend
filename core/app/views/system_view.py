from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models.people import Aluno
from core.models.system import Comissao, Disciplina, Relatorio, Avaliacao, Chamado
from core.app.serializers.system_serializer import ComissaoSerializer, DisciplinaSerializer, RelatorioSerializer, \
    AvaliacaoSerializer, ChamadoSerializer
from datetime import date


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


@api_view(['GET'])
def get_disciplinas(aluno_id):
    try:
        aluno = Aluno.objects.get(id_matricula=aluno_id)
        disciplinas = aluno.disciplinas.all()

        disciplinas_data = [
            {
                "nome": disciplina.nome,
                "professor": disciplina.professor,
                "numero_alunos": disciplina.numero_alunos,
                "periodo": disciplina.periodo,
                "semestre": disciplina.semestre,
                "sala": disciplina.sala,
            }
            for disciplina in disciplinas
        ]
        return JsonResponse({"disciplinas": disciplinas_data})
    except Aluno.DoesNotExist:
        return Response({"error": "Aluno nao encontrado"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_relatorio(relatorio_id):
    try:
        relatorio = Relatorio.objects.get(id=relatorio_id)
        serializer = RelatorioSerializer(relatorio)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Relatorio.DoesNotExist:
        return Response({"error": "Relatorio nao encontrado"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def set_relatorio(request):
    try:
        data = request.data

        aluno_id = data.get('aluno_id')
        aluno = Aluno.objects.get(id_matricula=aluno_id)

        relatorio = Relatorio.objects.create(
            aluno=aluno,
            data_entrega=data.get('data_entrega', date.today()),
            semestre=data.get('semestre'),
            descricao=data.get('descricao'),
            houve_reavaliacao=data.get('houve_reavaliacao', False),
            desempenho=None
        )

        return Response({
            'aluno_id': relatorio.aluno.id_matricula,
            'data_entrega': relatorio.data_entrega,
            'semestre': relatorio.semestre,
            'descricao': relatorio.descricao,
            'houve_reavaliacao': relatorio.houve_reavaliacao,
            'desempenho_id': relatorio.desempenho
        }, status=status.HTTP_201_CREATED)

    except Aluno.DoesNotExist:
        return Response({'error': 'Aluno nao encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
