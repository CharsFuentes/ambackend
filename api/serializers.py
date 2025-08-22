from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Aquí simplemente llamamos al método validate() del serializer base
        return super().validate(attrs)  # Esto maneja la validación del usuario y el password


class RegisterSerializer(serializers.ModelSerializer):
    # Unicidad de email con mensaje claro
    usu_txt_email = serializers.EmailField()
    # FK por PK
    rol_int_id = serializers.PrimaryKeyRelatedField(queryset=Rol.objects.all())
    # password solo entrada
    usu_txt_password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Usuario
        fields = [
            'usu_txt_nombre',
            'usu_txt_apellidos',
            'usu_txt_email',
            'usu_txt_password',
            'usu_txt_colegio',
            'usu_txt_grado',
            'rol_int_id',
        ]

    # Normaliza email siempre (lowercase/trim)
    def validate_usu_txt_email(self, value: str) -> str:
        return value.strip().lower()

    def create(self, validated_data):
        raw_password = validated_data.pop('usu_txt_password')
        validated_data['usu_txt_password'] = make_password(raw_password)
        # rol_int_id ya es instancia de Rol
        user = Usuario.objects.create(**validated_data)
        return user
    
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['usu_int_id', 'rol_int_id', 'usu_txt_nombre', 'usu_txt_apellidos', 
                  'usu_txt_email', 'usu_txt_colegio', 'usu_txt_grado', 'usu_dat_fecha_registro']

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

class NivelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nivel
        fields = '__all__'

class ExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examen
        fields = '__all__'

class LeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leccion
        fields = '__all__'

class PreguntaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregunta
        fields = '__all__'

# class RespuestaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Respuesta
#         fields = '__all__'

class IntentoExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntentoExamen
        fields = '__all__'

class RespuestaUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespuestaUsuario
        fields = '__all__'

# Login simple (solo email y password)
class LoginSerializer(serializers.Serializer):
    usu_txt_email = serializers.EmailField()
    usu_txt_password = serializers.CharField()



class RespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuesta
        fields = ['res_int_id', 'res_txt_texto', 'res_bol_es_correcta']

class PreguntaConRespuestasSerializer(serializers.ModelSerializer):
    # Sin related_name => reverso por defecto 'respuesta_set'
    respuestas = RespuestaSerializer(source='respuesta_set', many=True, read_only=True)

    class Meta:
        model = Pregunta
        fields = ['pre_int_id', 'pre_txt_texto', 'respuestas']