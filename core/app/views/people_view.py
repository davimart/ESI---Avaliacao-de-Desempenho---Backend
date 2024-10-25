from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from core.app.serializers.people_serializer import AlunoSerializer, OrientadorSerializer
import json

from core.models.people import Aluno, Orientador, Usuario


class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer


class OrientadorViewSet(viewsets.ModelViewSet):
    queryset = Orientador.objects.all()
    serializer_class = OrientadorSerializer


@api_view(['GET'])
def get_user_info(user_id):
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
