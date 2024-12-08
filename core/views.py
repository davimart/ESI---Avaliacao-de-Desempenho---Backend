from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
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


@api_view(['POST'])
def api_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    print(email)
    print(password)

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

@api_view(['GET'])
def get_relatorio_by_matricula(request, matricula):
    mock_data = {
        "nomeParecerista": "John Doe",
        "papelParecerista": "Professor",
        "nomeAluno": "Alice Smith",
        "parecerDesempenho": "",
        "avaliacaoDesempenho": ""
    }
    return JsonResponse(mock_data)


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


@api_view(['POST'])
def post_relatorio(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Mocked relatorio data received:", data)
            return JsonResponse({"status": "success", "message": "Relatório enviado com sucesso"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)



"""
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

@api_view(['POST'])
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            tipo = form.cleaned_data['tipo']

            # Create a Django User
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )

            # Create the Usuario
            usuario = Usuario.objects.create(
                nome_completo=email.split('@')[0],
                email=email,
                tipo=tipo
            )

            # Link to the specific type
            if tipo == Usuario.ALUNO:
                Aluno.objects.create(usuario=usuario, id_matricula=f"MAT-{usuario.id}")
            elif tipo == Usuario.ORIENTADOR:
                Orientador.objects.create(usuario=usuario)
            elif tipo == Usuario.COMISSAO:
                Comissao.objects.create(usuario=usuario)

            # Automatically log the user in and redirect
            login(request, user)
            return redirect('home')  # Replace 'home' with your desired redirect URL

    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})
"""