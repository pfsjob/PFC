from django.conf.urls import url, include
from social_django.urls import urlpatterns as social_django_urls
from . import views

urlpatterns = [
    url(r'^index/', views.index, name='tindex'),
    url(r'^estadisticasExec/$', views.estadisticasExec, name='tstatsExec'),
    url(r'^estadisticasExecAPI/$', views.estadisticasExecAPI, name='tstatsExecAPI'),
    url(r'^estadisticasPend/$', views.estadisticasPend, name='tstatsPend'),
    url(r'^estadisticasPendAPI/$', views.estadisticasPendAPI, name='tstatsPendAPI'),
    url(r'^lista/$', views.lista_tareas, name='tlist'),
    url(r'^listaAPI/$', views.lista_tareasAPI, name='tlistAPI'),
    url(r'^listaejecutados/$', views.lista_tareas_ejecutadas, name='tlistexec'),
    url(r'^listaejecutadosAPI/$', views.lista_tareas_ejecutadasAPI, name='tlistexecAPI'),
    url(r'^listapendientes/$', views.lista_tareas_pendientes, name='tlistpend'),
    url(r'^listapendientesAPI/$', views.lista_tareas_pendientesAPI, name='tlistpendAPI'),
    url(r'^listausuario/', views.lista_tareas_usuario, name='tlistu'),
    url(r'^listausuarioAPI/', views.lista_tareas_usuarioAPI, name='tlistuAPI'),
    url(r'^pantallalistausuario/', views.pantalla_lista_usuario, name='tlistuser'),
    url(r'^add/$', views.add_tarea, name='tadd'),
]
