from django.urls import path
from . import views

urlpatterns = [
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('crear-rol/', views.crear_rol, name='crear_rol'),

    path('cursos/', views.CursoListCreateView.as_view(), name='lista-cursos'),
    path('curso/<int:pk>/', views.CursoDetailView.as_view(), name='detalle-curso'),

    path('niveles/', views.NivelListCreateView.as_view(), name='lista-niveles'),
    path('nivel/<int:pk>/', views.NivelDetailView.as_view(), name='detalle-nivel'),

    path('usuarios/', views.UsuarioListCreateView.as_view(), name='lista-usuarios'),
    path('usuario/<int:pk>/', views.UsuarioDetailView.as_view(), name='detalle-usuario'),

    path('examenes/', views.ExamenListCreateView.as_view(), name='lista-examenes'),
    path('examen/<int:pk>/', views.ExamenDetailView.as_view(), name='detalle-examen'),

    path('lecciones/', views.LeccionListCreateView.as_view(), name='lista-lecciones'),
    path('leccion/<int:pk>/', views.LeccionDetailView.as_view(), name='detalle-leccion'),

    path('preguntas/', views.PreguntaListCreateView.as_view(), name='lista-preguntas'),
    path('pregunta/<int:pk>/', views.PreguntaDetailView.as_view(), name='detalle-pregunta'),

    path('respuestas/', views.RespuestaListCreateView.as_view(), name='lista-respuestas'),
    path('respuesta/<int:pk>/', views.RespuestaDetailView.as_view(), name='detalle-respuesta'),

    path('intentos/', views.IntentoExamenListCreateView.as_view(), name='lista-intentos'),
    
    path('cursos/preguntas/', views.PreguntasPorCursoPostView.as_view(), name='lista-de-cursos'),
]
