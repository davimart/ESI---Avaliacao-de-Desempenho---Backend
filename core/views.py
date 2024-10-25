from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Aluno, Usuario, Orientador, Comissao, Disciplina, Relatorio, Avaliacao, Chamado
from .serializers import AlunoSerializer, OrientadorSerializer, ComissaoSerializer, DisciplinaSerializer, RelatorioSerializer, AvaliacaoSerializer, ChamadoSerializer
from datetime import date
import json

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

@api_view(['GET'])
def get_disciplinas(request, aluno_id):
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
def get_user_info(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    user_data = {
        'nome_completo': usuario.nome_completo,
        'email': usuario.email,
        'data_nascimento': usuario.data_nascimento,
        'rg': usuario.rg,
        'local_nascimento': usuario.local_nascimento,
        'nacionalidade': usuario.nacionalidade,
        'curso': usuario.curso,
        'link_lattes': usuario.link_lattes,
        'data_matricula': usuario.data_matricula,
        'data_aprovacao_exame_qualificacao': usuario.data_aprovacao_exame_qualificacao,
        'data_aprovacao_exame_proficiencia': usuario.data_aprovacao_exame_proficiencia,
        'data_limite_deposito_trabalho': usuario.data_limite_deposito_trabalho,
        'tipo': usuario.tipo,
    }
    return JsonResponse(user_data)

@api_view(['POST'])
def set_user_info(request, user_id):
    if request.method == 'POST':
        usuario = get_object_or_404(Usuario, id=user_id)
        data = json.loads(request.body)  # Parse JSON data

        fields_to_update = {
            'nome_completo': 'nome_completo',
            'email': 'email',
            'numero_usp': 'id_matricula',
            'orientador': 'orientador',
            'link_lattes': 'link_lattes',
            'last_lattes_update': 'last_lattes_update',
            'curso': 'curso',
            'mes_ano_ingresso': 'data_matricula',
            'data_matricula': 'data_matricula',
            'data_aprov_exame_qualificacao': 'data_aprovacao_exame_qualificacao',
            'data_aprov_exame_proeficiencia': 'data_aprovacao_exame_proficiencia',
            'data_trab_final': 'data_limite_deposito_trabalho'
        }

        for field, model_field in fields_to_update.items():
            if field in data:
                setattr(usuario, model_field, data[field])

        usuario.save()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@api_view(['GET'])
def get_relatorio(request, relatorio_id):
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