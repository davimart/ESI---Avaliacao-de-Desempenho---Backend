from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlunoViewSet, OrientadorViewSet, ComissaoViewSet, DisciplinaViewSet, RelatorioViewSet, AvaliacaoViewSet, ChamadoViewSet

router = DefaultRouter()
router.register(r'alunos', AlunoViewSet)
router.register(r'orientadores', OrientadorViewSet)
router.register(r'comissoes', ComissaoViewSet)
router.register(r'disciplinas', DisciplinaViewSet)
router.register(r'relatorios', RelatorioViewSet)
router.register(r'avaliacoes', AvaliacaoViewSet)
router.register(r'chamados', ChamadoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

