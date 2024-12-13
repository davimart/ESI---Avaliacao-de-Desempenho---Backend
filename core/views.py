from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
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
def get_alunos_orientados(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)

        if request.user.tipo != 'Orientador':
            return JsonResponse({"error": "User is not an Orientador"}, status=403)

        orientador = Orientador.objects.get(usuario=request.user)

        alunos = Aluno.objects.filter(orientador=orientador)

        alunos_data = [
            {
                "id_matricula": aluno.id_matricula,
                "nome_completo": aluno.usuario.nome_completo,
                "email": aluno.usuario.email,
                "curso": aluno.usuario.curso,
                "data_matricula": aluno.usuario.data_matricula,
            }
            for aluno in alunos
        ]

        return Response({
            "numero_alunos_orientados": alunos.count(),
            "alunos": alunos_data
        }, status=200)

    except Orientador.DoesNotExist:
        return JsonResponse({"error": "Orientador not found"}, status=404)

@api_view(['GET'])
def get_orientacoes_for_orientador(request):
    user = request.user

    if user.tipo != 'Orientador':
        return JsonResponse({"error": "Access denied. Only Orientadores can access this."}, status=403)

    try:
        orientador = Orientador.objects.get(usuario=user)
        orientacoes = Aluno.objects.filter(orientador=orientador)
        data = [
            {
                "matricula": aluno.id_matricula,
                "nome_completo": aluno.usuario.nome_completo,
            }
            for aluno in orientacoes
        ]
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Orientador not found."}, status=404)

@api_view(['GET'])
def get_aluno_info(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)

        if request.user.tipo != 'Aluno':
            return JsonResponse({"error": "User is not an Aluno"}, status=403)

        aluno = Aluno.objects.get(usuario=request.user)

        aluno_info = {
                "id_matricula": aluno.id_matricula,
                "nome_completo": aluno.usuario.nome_completo,
                "email": aluno.usuario.email,
                "curso": aluno.usuario.curso,
                "data_matricula": aluno.usuario.data_matricula
        }

        return Response(aluno_info, status=200)

    except Aluno.DoesNotExist:
        return JsonResponse({"error": "Aluno not found"}, status=404)

@api_view(['POST'])
def api_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request, username=email, password=password)
    if user is not None:
        print('Authentication successful!')
    else:
        print('Authentication failed.')

    if user:
        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({
            'token': token.key,
            'user_id': user.id,
            'tipo': user.tipo,
            'nome_completo': user.nome_completo,
        })
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)

# remover
@csrf_exempt
def get_user_info(request, user_id):
    try:
        usuario = get_object_or_404(Usuario, id=user_id, tipo='Aluno')
        aluno = get_object_or_404(Aluno, usuario=usuario)

        user_data = {
            "nomeParecerista": usuario.nome_completo,
            "email": usuario.email,
            "curso": usuario.curso,
            "lattesLink": usuario.link_lattes,
            "lattesUpdate": usuario.data_matricula.strftime("%Y-%m-%d") if usuario.data_matricula else None,
            "mesAnoIngresso": usuario.data_matricula.strftime if usuario.data_matricula else None,
            "nomeAluno": usuario.nome_completo,
            "numeroUSP": aluno.id_matricula,
            "nomeOrientador": aluno.orientador.usuario.nome_completo,
            #"mesAnoIngresso": usuario.data_matricula,
            "avaliacaoAnterior": "N/A",
        }

        return JsonResponse(user_data)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@api_view(['POST'])
def post_avaliacao(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Mocked relatorio data received:", data)
            return JsonResponse({"status": "success", "message": "Relatório enviado com sucesso"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

@api_view(['GET', 'POST'])
def formularios(request):
    if request.method == "POST":
        return post_formulario(request)
    elif request.method == "GET":
        return get_formulario(request)

def post_formulario(request):
    user = request.user
    if user.tipo == 'Orientador' or user.tipo == 'Comissao':
        try:
            payload = json.loads(request.body)

            relatorio_id = payload.get('relatorioId')
            parecer_desempenho = payload.get('parecerDesempenho')
            avaliacao_desempenho = payload.get('avaliacaoDesempenho')

            if not all([relatorio_id, parecer_desempenho, avaliacao_desempenho]):
                return JsonResponse({"error": "Todos os campos são obrigatórios."}, status=400)

            try:
                relatorio = Relatorio.objects.get(id=relatorio_id)
            except Relatorio.DoesNotExist:
                return JsonResponse({"error": "Relatório não encontrado."}, status=404)

            avaliacao = Avaliacao.objects.create(
                avaliador=user,
                parecer=parecer_desempenho,
                conceito=avaliacao_desempenho,
                status='Fechado',
                data_avaliacao=timezone.now().date(),
            )

            relatorio.desempenho = avaliacao
            relatorio.save()

            return JsonResponse({"message": "Formulário de avaliação enviado com sucesso."}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Dados inválidos."}, status=400)

    return JsonResponse({"error": "Acesso negado. Apenas orientadores ou membros da comissão podem enviar avaliações."}, status=403)

def get_formulario(request):
    user = request.user
    if user.tipo == 'Aluno':
        relatorio_id = request.GET.get('relatorioId')
        try:
            relatorio = Relatorio.objects.get(id=relatorio_id, aluno__usuario=user)
            aluno = relatorio.aluno

            data = {
                "email": aluno.usuario.email,
                "nomeAluno": aluno.usuario.nome_completo,
                "nomeOrientador": aluno.orientador.usuario.nome_completo if aluno.orientador else "",
                "numeroUSP": aluno.id_matricula,
                "lattesLink": aluno.usuario.link_lattes,
                "lattesUpdate": aluno.usuario.data_matricula.strftime('%Y-%m-%d') if aluno.usuario.data_matricula else "",
                "curso": aluno.usuario.curso,
                "mesAnoIngresso": aluno.usuario.data_matricula.strftime('%m/%Y') if aluno.usuario.data_matricula else "",
                "avaliacaoAnterior": relatorio.desempenho.conceito if relatorio.desempenho else "nao-aplicavel",
            }
            return JsonResponse(data)
        except Relatorio.DoesNotExist:
            return JsonResponse({"error": "Relatório não encontrado."}, status=404)
        except Aluno.DoesNotExist:
            return JsonResponse({"error": "Aluno não encontrado."}, status=404)

    if user.tipo == 'Orientador':
        relatorio_id = request.GET.get('relatorioId')
        try:
            relatorio = Relatorio.objects.get(id=relatorio_id)
            aluno = relatorio.aluno
            parecerista = request.user
            data = {
                "nomeParecerista": parecerista.nome_completo,
                "papelParecerista": parecerista.tipo,
                "nomeAluno": aluno.usuario.nome_completo,
            }
            return JsonResponse(data)
        except Relatorio.DoesNotExist:
            return JsonResponse({"error": "Relatório não encontrado."}, status=404)

@api_view(['GET', 'POST'])
def relatorios(request):
    if request.method == "POST":
        return post_relatorio(request)
    elif request.method == "GET":
        return get_relatorio(request)

def post_relatorio(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Usuário não autenticado."}, status=401)

    user = request.user
    if user.tipo != 'Aluno':
        return JsonResponse({"error": "Apenas alunos podem submeter relatórios."}, status=403)

    try:
        data = json.loads(request.body)
        aluno = Aluno.objects.get(usuario=user)

        relatorio_id = data.get('relatorioId', None)
        print(f"RELATORIO ID: {relatorio_id}")

        if relatorio_id:
            try:
                relatorio = Relatorio.objects.get(id=relatorio_id, aluno=aluno)
                print(f"Updating existing Relatorio with ID: {relatorio_id}")
            except Relatorio.DoesNotExist:
                return JsonResponse({"error": "Relatório não encontrado ou não pertence ao aluno."}, status=404)
        else:
            return JsonResponse({"error": "ID do relatório não fornecido."}, status=400)

        relatorio.qualificacao = data.get('qualificacao', '')
        relatorio.prazoQualificacao = data.get('prazoQualificacao', '')
        relatorio.prazoDeposito = data.get('prazoDeposito', '')
        relatorio.producaoArtigos = data.get('producaoArtigos', '')
        relatorio.atividadesAcademicas = data.get('atividadesAcademicas', '')
        relatorio.resumoAtividades = data.get('resumoAtividades', '')
        relatorio.declaracaoAdicional = data.get('declaracaoAdicional', '')
        relatorio.apoioCoordenacao = data.get('apoioCoordenacao', '')
        relatorio.data_entrega = timezone.now().date()

        relatorio.semestre = data.get('semestre', relatorio.semestre)

        relatorio.save()
        print(f"Relatorio updated successfully with ID: {relatorio.id}")

        if not relatorio.desempenho:
            avaliacao = Avaliacao(
                avaliador=aluno.orientador.usuario,
                parecer="Aguardando avaliação",
                conceito="Insatisfatório",
                status="Aberto",
                data_avaliacao=timezone.now().date(),
            )
            avaliacao.save()
            print(f"Avaliacao created with ID: {avaliacao.id}")

            relatorio.desempenho = avaliacao
            relatorio.save()

        return JsonResponse({"message": "Relatório enviado com sucesso."}, status=201)

    except Aluno.DoesNotExist:
        return JsonResponse({"error": "Aluno não encontrado."}, status=404)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({"error": str(e)}, status=400)

def get_relatorio(request):
    user = request.user

    if user.tipo == 'Aluno':
        try:
            aluno = Aluno.objects.get(usuario=user)
            relatorios = Relatorio.objects.filter(aluno=aluno).select_related('desempenho')
            data = [
                {
                    "id": relatorio.id,
                    "semestre": relatorio.semestre,
                    "data_submissao": relatorio.data_entrega,
                    "avaliado": bool(relatorio.desempenho),
                    "avaliacao": {
                        "conceito": relatorio.desempenho.conceito if relatorio.desempenho else None
                    }
                }
                for relatorio in relatorios
            ]
            return JsonResponse(data, safe=False)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Aluno not found."}, status=404)

    elif user.tipo == 'Orientador':
        try:
            relatorios = Relatorio.objects.filter(aluno__orientador__usuario=user).select_related('aluno', 'desempenho')
            data = [
                {
                    "id": relatorio.id,
                    "semestre": relatorio.semestre,
                    "data_submissao": relatorio.data_entrega,
                    "matricula": relatorio.aluno.id_matricula,
                    "avaliado": bool(relatorio.desempenho),
                    "avaliacao": {
                        "conceito": relatorio.desempenho.conceito if relatorio.desempenho else None
                    }
                }
                for relatorio in relatorios
            ]
            return JsonResponse(data, safe=False)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Orientador not found."}, status=404)

    return JsonResponse({"error": "Invalid user type."}, status=400)