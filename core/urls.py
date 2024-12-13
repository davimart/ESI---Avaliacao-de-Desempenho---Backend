from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import AlunoViewSet, OrientadorViewSet, ComissaoViewSet, DisciplinaViewSet, RelatorioViewSet, AvaliacaoViewSet, ChamadoViewSet
from . import views

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
        title="Avaliacao Desempenho",
        default_version='v1',
        description="Projeto ESI",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('login/', views.api_login, name='login'),


    path('relatorio/', views.relatorios, name='relatorio_view'),
    path('formulario/', views.formularios, name='formulario_view'),

    path('orientador/alunos/', views.get_alunos_orientados),
    path('orientador/orientacoes/', views.get_orientacoes_for_orientador, name='get_orientacoes_for_orientador'),

    path('avaliacao/', views.post_avaliacao, name='post_avaliacao'),
    path('aluno/info', views.get_aluno_info),

    #remover
    path('user/<int:user_id>', views.get_user_info, name='get_user_info'),
]