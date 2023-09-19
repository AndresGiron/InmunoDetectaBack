from rest_framework import serializers
from .models import Usuario,Paciente,Medico,Diagnostico


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class RegistroUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = '__all__'

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'

class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = '__all__'

class DiagnosticoSerializer(serializers.ModelSerializer):
    nombre_medico = serializers.CharField(source='cedula_medico.nombre', read_only=True)
    apellido_medico = serializers.CharField(source='cedula_medico.apellido', read_only=True)
    
    class Meta:
        model = Diagnostico
        fields = '__all__'

class DiagnosticoSerializerGeneralReport(serializers.ModelSerializer):
    class Meta:
        model = Diagnostico
        fields = '__all__'
