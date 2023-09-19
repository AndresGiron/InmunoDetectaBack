from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import (
    UsuarioSerializer,
    RegistroUsuarioSerializer,
    PacienteSerializer,
    MedicoSerializer,
    DiagnosticoSerializer,
    DiagnosticoSerializerGeneralReport)
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import make_password
from .models import Paciente, Medico, Diagnostico, Usuario
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework import generics
from .IA.reumaIA import hacerPrediccion

#Vistas de usuario
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        print(email,password)
        user = authenticate(email=email, password=password)
        print(user)


        if user:
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                print(token)
                serializer = UsuarioSerializer(user)
                return Response({'token': token.key, 'user': serializer.data})
            else:
                return Response({'error': 'Este usuario se encuentra inactivo'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
        
class RegistroUsuarioView(APIView):
    def post(self, request):

        data = request.data.copy()
        password = data.get('password')
        data['password'] = make_password(password)
        print(data['password'])

        serializer = RegistroUsuarioSerializer(data=data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'Usuario registrado exitosamente'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConsultarUserMedicosView(ListAPIView):
    queryset = Usuario.objects.filter(rol='medico')
    serializer_class = UsuarioSerializer

class CambiarEstadoUsuarioView(APIView):
    def put(self, request, user_id):
        try:
            usuario = Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        # Cambiar el valor del atributo estado
        usuario.estado = not usuario.estado  # Invertir el valor

        usuario.save()  # Guardar los cambios en la base de datos

        return Response({'estado_actualizado': usuario.estado}, status=status.HTTP_200_OK)

#Vistas para paciente
class CreatePacienteView(APIView):
    def post(self, request):
        serializer = PacienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ConsultarPacienteView(RetrieveAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    lookup_field = 'cedula'

class ConsultarPacienteCorreoView(RetrieveAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    lookup_field = 'correo'

class ConsultarTodosPacientesView(ListAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

class PacienteUpdateView(generics.UpdateAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    lookup_field = 'correo'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

#Vistas para medico
class CreateMedicoView(APIView):
    def post(self, request):
        serializer = MedicoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ConsultarMedicoView(RetrieveAPIView):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    lookup_field = 'cedula'

class ConsultarTodosMedicosView(ListAPIView):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer

class ConsultarMedicoPorEmailView(RetrieveAPIView):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    lookup_field = 'correo'

class MedicoUpdateView(generics.UpdateAPIView):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    lookup_field = 'correo'  # Utilizamos el campo 'correo' como identificador

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
class MedicosConUsuariosView(APIView):
    def get(self, request):
        # Obtener usuarios con rol "medico"
        medicos_usuarios = Usuario.objects.filter(rol='medico')

        # Obtener información de médicos cuyo correo coincide con el email del usuario
        medicos_info = []
        for usuario in medicos_usuarios:
            try:
                medico = Medico.objects.get(correo=usuario.email)
                medico_serializer = MedicoSerializer(medico)
                medicos_info.append(medico_serializer.data)
            except Medico.DoesNotExist:
                pass

        # Serializar usuarios con información de médicos
        usuarios_serializer = UsuarioSerializer(medicos_usuarios, many=True)
        
        # Agregar la información de médicos al resultado
        for index, usuario_data in enumerate(usuarios_serializer.data):
            usuario_data['medico_info'] = medicos_info[index]

        return Response(usuarios_serializer.data, status=status.HTTP_200_OK)

#Vistas para diagnostico
class CreateDiagnosticoView(APIView):
    def post(self, request):
        serializer = DiagnosticoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConsultarTodosDiagnosticosView(APIView):
    def get(self, request, format=None):
        diagnosticos = Diagnostico.objects.all()
        diagnosticos_data = []

        for diagnostico in diagnosticos:
            # Obtener los nombres y apellidos del paciente y el médico
            paciente = diagnostico.cedula_paciente
            medico = diagnostico.cedula_medico

            paciente_nombre_apellido = f"{paciente.nombre} {paciente.apellido}"
            medico_nombre_apellido = f"{medico.nombre} {medico.apellido}"

            # Serializar el diagnóstico y agregar los nombres y apellidos
            serializer = DiagnosticoSerializerGeneralReport(diagnostico)
            diagnostico_data = serializer.data
            diagnostico_data['paciente_nombre_apellido'] = paciente_nombre_apellido
            diagnostico_data['medico_nombre_apellido'] = medico_nombre_apellido

            diagnosticos_data.append(diagnostico_data)

        return Response(diagnosticos_data, status=status.HTTP_200_OK)

class ConsultarDiagnosticosPorCedulaPacienteView(ListAPIView):
    serializer_class = DiagnosticoSerializer

    def get_queryset(self):
        cedula_paciente = self.kwargs['cedula_paciente']
        return Diagnostico.objects.filter(cedula_paciente__cedula=cedula_paciente).select_related('cedula_medico')
    

class ConsultarDiagnosticosPorCedulaMedicoView(ListAPIView):
    serializer_class = DiagnosticoSerializer

    def get_queryset(self):
        cedula_medico = self.kwargs['cedula_medico']
        return Diagnostico.objects.filter(cedula_medico__cedula=cedula_medico)
    
#Vista de la IA

class HacerPrediccionesView(APIView):

    def post(self, request, format=None):
        data = request.data  # Datos enviados en la solicitud POST
        result = hacerPrediccion(data)  # Llama a tu función para hacer predicciones
        return Response(result, status=status.HTTP_200_OK)