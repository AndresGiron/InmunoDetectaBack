from django.db import models
from django.contrib.auth.models import AbstractUser, Group

# Create your models here.
class Paciente(models.Model):
    cedula = models.CharField(primary_key=True,max_length=30)
    nombre = models.CharField(max_length=35)
    apellido = models.CharField(max_length=35)
    fechaNacimiento = models.DateField(auto_now_add=False)
    sexo = models.CharField(max_length= 10)
    correo = models.CharField(max_length=60, unique= True)

class Medico(models.Model):
    cedula = models.CharField(primary_key=True,max_length=30)
    nombre = models.CharField(max_length=35)
    apellido = models.CharField(max_length=35)
    correo = models.CharField(max_length=60, unique= True)

class Diagnostico(models.Model):
    diagnostico_id = models.AutoField(primary_key=True)
    diagnostico_fecha = models.DateField(auto_now_add=True)
    cedula_paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    cedula_medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    diagnostico_completo = models.JSONField()
    #Variable para la aprobacion de los diagnosticos
    diagnostico_aprobacion = models.BooleanField(null=True, default=None)
    
class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    estado = models.BooleanField(default=True)
    rol = models.CharField(max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 




# {
# "email":"andresfelipe042001@gmail.com",
# "username":"andresfelipe042001@gmail.com",
# "rol":"paciente",
# "password":"1234"
# }

# {
# "email":"dummy@gmail.com",
# "username":"dummy@gmail.com",
# "rol":"paciente",
# "password":"12345678910"
# }

