from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from core.app.views import system_view, people_view
from core.app.views.people_view import AlunoViewSet, OrientadorViewSet
from core.app.views.system_view import ComissaoViewSet, DisciplinaViewSet, RelatorioViewSet, AvaliacaoViewSet, \
    ChamadoViewSet

router = DefaultRouter()
router.register(r'alunos', AlunoViewSet)
router.register(r'orientadores', OrientadorViewSet)
router.register(r'comissoes', ComissaoViewSet)
router.register(r'disciplinas', DisciplinaViewSet)
router.register(r'relatorios', RelatorioViewSet)
router.register(r'avaliacoes', AvaliacaoViewSet)
router.register(r'chamados', ChamadoViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Avaliação de Desempenho",
        default_version='v1',
        description="Projeto ESI",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=([permissions.AllowAny]),
)


urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('get-disciplinas/<str:aluno_id>/', system_view.get_disciplinas, name='get_disciplinas'),
    path('get-user-info/<int:user_id>/', people_view.get_user_info, name='get_user_info'),
    path('set-user-info/<int:user_id>/', people_view.set_user_info, name='set_user_info'),
    path('set-relatorio/', system_view.set_relatorio, name='set_relatorio'),
    path('get-relatorio/<int:relatorio_id>', system_view.get_relatorio, name='get_relatorio'),
]
