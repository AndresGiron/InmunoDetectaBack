"""
URL configuration for Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from InmunoDetecta.views import (
    LoginView,
    RegistroUsuarioView,
    CreatePacienteView,
    ConsultarPacienteView,
    CreateMedicoView,
    ConsultarMedicoView,
    ConsultarTodosPacientesView,
    ConsultarTodosMedicosView,
    CreateDiagnosticoView,
    ConsultarTodosDiagnosticosView,
    ConsultarDiagnosticosPorCedulaPacienteView,
    ConsultarDiagnosticosPorCedulaMedicoView,
    ConsultarUserMedicosView,
    CambiarEstadoUsuarioView,
    ConsultarPacienteCorreoView,
    HacerPrediccionesView,
    ConsultarMedicoPorEmailView,
    PacienteUpdateView,
    MedicoUpdateView,
    MedicosConUsuariosView,
    DiagnosticoUpdateView
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegistroUsuarioView.as_view(), name='register'),
    path('get-user-medicos/', MedicosConUsuariosView.as_view(), name='consultar-medicos'),
    path('cambiar-estado-usuario/<int:user_id>/', CambiarEstadoUsuarioView.as_view(), name='cambiar-estado-usuario'),
    path('create-paciente/', CreatePacienteView.as_view(), name='crear-paciente'),
    path('get-paciente/<str:cedula>/', ConsultarPacienteView.as_view(), name='consultar-paciente'),
    path('get-paciente-byemail/<str:correo>/', ConsultarPacienteCorreoView.as_view(), name='consultar-paciente-correo'),
    path('get-all-pacientes/', ConsultarTodosPacientesView.as_view(), name='consultar-todos-pacientes'),
    path('create-medico/', CreateMedicoView.as_view(), name='crear-medico'),
    path('get-medico/<str:cedula>/', ConsultarMedicoView.as_view(), name='consultar-medico'),
    path('get-all-medicos/', ConsultarTodosMedicosView.as_view(), name='consultar-todos-medicos'),
    path('create-diagnostico/', CreateDiagnosticoView.as_view(), name='crear-diagnostico'),
    path('get-all-diagnosticos/', ConsultarTodosDiagnosticosView.as_view(), name='consultar-todos-diagnosticos'),
    path('get-diagnosticos-bypaciente/<str:cedula_paciente>/', ConsultarDiagnosticosPorCedulaPacienteView.as_view(), name='consultar-diagnosticos-paciente'),
    path('get-diagnosticos-bymedico/<str:cedula_medico>/', ConsultarDiagnosticosPorCedulaMedicoView.as_view(), name='consultar-diagnosticos-medico'),
    path('hacer-predicciones/', HacerPrediccionesView.as_view(), name='hacer-predicciones'),
    path('get-medico-byemail/<str:correo>/', ConsultarMedicoPorEmailView.as_view(), name='consultar-medico-por-email'),
    path('paciente/<str:correo>/update/', PacienteUpdateView.as_view(), name='update_paciente'),
    path('medico/<str:correo>/update/', MedicoUpdateView.as_view(), name='update_medico'),
    path('diagnostico-update/<str:diagnostico_id>/', DiagnosticoUpdateView.as_view(), name='diagnostico-update'),
]
