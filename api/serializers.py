from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Aquí simplemente llamamos al método validate() del serializer base
        return super().validate(attrs)  # Esto maneja la validación del usuario y el password


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['usu_txt_nombre', 'usu_txt_apellidos', 'usu_txt_email', 'usu_txt_password', 'usu_txt_colegio', 'usu_txt_grado', 'rol_int_id']

    def validate_usu_txt_email(self, value):
        if Usuario.objects.filter(usu_txt_email=value).exists():
            raise serializers.ValidationError("El correo ya está registrado.")
        return value
    
    def create(self, validated_data):
        return Usuario.objects.create(**validated_data)
    
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

class RespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuesta
        fields = '__all__'

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
