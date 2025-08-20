from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.http import JsonResponse
import json
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password, make_password
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
from django.db import IntegrityError, transaction
from django.db.models import Prefetch
# from rest_framework.permissions import IsAuthenticated
from django.db.models.functions import Random

@method_decorator(csrf_exempt, name='dispatch')
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer  # Usar el serializer personalizado

    def post(self, request, *args, **kwargs):
        try:
            # Llamada al método post de TokenObtainPairView para obtener los tokens
            response = super().post(request, *args, **kwargs)

            # Si la respuesta es exitosa (status 200), se procesan los tokens
            if response.status_code == 200:
                tokens = response.data  # Diccionario con "access" y "refresh"
                
                # Aquí personalizamos la respuesta, devolviendo los tokens en el formato deseado
                respuesta = {
                    "status": "000",
                    "type": "success",
                    "detail": "Petición válida",
                    "results": tokens  # Devolvemos los tokens de acceso y refresco
                }
                
                return Response(respuesta, status=status.HTTP_200_OK)

            return response  # Si hay otro error, devolvemos la respuesta original

        except AuthenticationFailed:  # Capturamos el error de autenticación
            return Response(
                {
                    "status": "001",
                    "type": "error",
                    "detail": "Credenciales inválidas.",
                    "results": {}
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data.copy()

        # Rol por defecto 1 si no envían
        data.setdefault('rol_int_id', 1)

        # Normaliza email antes de cualquier cosa
        email = (data.get('usu_txt_email') or '').strip().lower()
        data['usu_txt_email'] = email

        # Fail-fast: si ya existe, 409
        if Usuario.objects.filter(usu_txt_email__iexact=email).exists():
            return Response({
                "status": "001",
                "type": "warning",
                "detail": "El correo ya está registrado.",
                "results": {"usu_txt_email": ["El correo ya está registrado."]}
            }, status=status.HTTP_409_CONFLICT)

        serializer = RegisterSerializer(data=data)

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = serializer.save()
            except IntegrityError:
                # Respaldo por condición de carrera
                return Response({
                    "status": "001",
                    "type": "warning",
                    "detail": "El correo ya está registrado.",
                    "results": {"usu_txt_email": ["El correo ya está registrado."]}
                }, status=status.HTTP_409_CONFLICT)

            return Response({
                "status": "000",
                "type": "success",
                "detail": f"Usuario {user.usu_txt_nombre} {user.usu_txt_apellidos} registrado correctamente",
                "results": {}
            }, status=status.HTTP_201_CREATED)

        # Si el error viene por email duplicado vía UniqueValidator, devuelve 409
        if 'usu_txt_email' in serializer.errors:
            return Response({
                "status": "001",
                "type": "warning",
                "detail": "El correo ya está registrado.",
                "results": serializer.errors
            }, status=status.HTTP_409_CONFLICT)

        # Otros errores de validación
        return Response({
            "status": "003",
            "type": "error",
            "detail": "Error en la validación",
            "results": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['usu_txt_email']
            password = serializer.validated_data['usu_txt_password']
            print(email)
            try:
                user = Usuario.objects.get(usu_txt_email=email)
                if check_password(password, user.usu_txt_password):
                    # Generar el token JWT para el usuario autenticado
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    refresh_token = str(refresh)

                    return Response({
                        "status": "000",
                        "type": "success",
                        "detail": "Inicio de sesión exitoso",
                        "results": {
                            "user": UsuarioSerializer(user).data,
                            "access_token": access_token,
                            "refresh_token": refresh_token
                        }
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "status": "001",
                        "type": "error",
                        "detail": "Contraseña incorrecta",
                        "results": {}
                    }, status=status.HTTP_401_UNAUTHORIZED)
            except Usuario.DoesNotExist:
                return Response({
                    "status": "002",
                    "type": "error",
                    "detail": "Usuario no encontrado",
                    "results": {}
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({
                "status": "003",
                "type": "error",
                "detail": "Error en la validación",
                "results": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
@csrf_exempt
def crear_rol(request):
    if request.method == 'POST':
        try:
            # Obtener los datos del cuerpo de la solicitud
            data = json.loads(request.body)
            nombre = data.get('rol_txt_nombre')
            descripcion = data.get('rol_txt_descripcion')

            # Validar que los campos no estén vacíos
            if not nombre or not descripcion:
                return JsonResponse({'error': 'Nombre y descripción son requeridos.'}, status=400)

            # Crear el nuevo rol
            nuevo_rol = Rol.objects.create(
                rol_txt_nombre=nombre,
                rol_txt_descripcion=descripcion
            )
            return JsonResponse({
                'mensaje': 'Rol creado con éxito',
                'rol': {
                    'id': nuevo_rol.rol_int_id,
                    'nombre': nuevo_rol.rol_txt_nombre,
                    'descripcion': nuevo_rol.rol_txt_descripcion
                }
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato de datos inválido.'}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)

# Cursos
class CursoListCreateView(generics.ListCreateAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class CursoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

# Niveles
class NivelListCreateView(generics.ListCreateAPIView):
    queryset = Nivel.objects.all()
    serializer_class = NivelSerializer

class NivelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Nivel.objects.all()
    serializer_class = NivelSerializer

# Usuarios
class UsuarioListCreateView(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class UsuarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

# Examenes
class ExamenListCreateView(generics.ListCreateAPIView):
    queryset = Examen.objects.all()
    serializer_class = ExamenSerializer

class ExamenDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Examen.objects.all()
    serializer_class = ExamenSerializer

# Lecciones
class LeccionListCreateView(generics.ListCreateAPIView):
    queryset = Leccion.objects.all()
    serializer_class = LeccionSerializer

class LeccionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Leccion.objects.all()
    serializer_class = LeccionSerializer

# Preguntas
class PreguntaListCreateView(generics.ListCreateAPIView):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializer

class PreguntaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializer

# Respuestas
class RespuestaListCreateView(generics.ListCreateAPIView):
    queryset = Respuesta.objects.all()
    serializer_class = RespuestaSerializer

class RespuestaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Respuesta.objects.all()
    serializer_class = RespuestaSerializer

# Intentos
class IntentoExamenListCreateView(generics.ListCreateAPIView):
    queryset = IntentoExamen.objects.all()


class PreguntasPorCursoPostView(APIView):
    """
    POST /api/cursos/preguntas/
    Body JSON:
      {
        "curso_id": <int>,     // requerido
        "limit": 5,            // opcional (default 5, máx 50)
        "random": true         // opcional (default true)
      }

    Respuesta:
      {
        "status": "000"|"003"|"004",
        "type": "success"|"error",
        "detail": "...",
        "results": [ { pregunta+respuestas }, ... ]
      }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        curso_id = request.data.get('curso_id')
        if not curso_id:
            return Response({
                "status": "003",
                "type": "error",
                "detail": "Falta el campo obligatorio 'curso_id'.",
                "results": {}
            }, status=status.HTTP_400_BAD_REQUEST)

        # Verifica que exista el curso
        if not Curso.objects.filter(cur_int_id=curso_id).exists():
            return Response({
                "status": "004",
                "type": "error",
                "detail": "Curso no encontrado.",
                "results": {}
            }, status=status.HTTP_404_NOT_FOUND)

        # Lee y sanea parámetros opcionales
        try:
            limit = int(request.data.get('limit', 5))
        except (TypeError, ValueError):
            limit = 5
        limit = max(1, min(limit, 50))  # 1..50

        random_flag = str(request.data.get('random', True)).lower() in ('1', 'true', 't', 'yes', 'y')

        base_qs = Pregunta.objects.filter(cur_int_id_id=curso_id)
        respuestas_qs = Respuesta.objects.order_by('res_int_id')

        if random_flag:
            preguntas_qs = (
                base_qs
                .order_by(Random())  # aleatorio en DB
                .prefetch_related(Prefetch('respuesta_set', queryset=respuestas_qs))
            )[:limit]
        else:
            preguntas_qs = (
                base_qs
                .order_by('pre_int_id')
                .prefetch_related(Prefetch('respuesta_set', queryset=respuestas_qs))
            )[:limit]

        data = PreguntaConRespuestasSerializer(preguntas_qs, many=True).data

        return Response({
            "status": "000",
            "type": "success",
            "detail": "Preguntas obtenidas correctamente.",
            "results": data
        }, status=status.HTTP_200_OK)
