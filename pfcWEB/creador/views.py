from django.shortcuts import render, render_to_response, redirect

from django.http import HttpResponse, HttpResponseRedirect
from creador.models import tareasForm
from django.core.urlresolvers import reverse
from django.views.generic import ListView
from .models import tareas, usuariosapp
from .search import tareasIndex, usuariosAppIndex
from elasticsearch import Elasticsearch, TransportError
from elasticsearch_dsl import query, Q
import elasticsearch_dsl
import time
import requests
import json
import sys
from datetime import datetime

class TareaList(ListView):
    model = tareas

def index(request):
    return render_to_response('index.html')

def indexregistrado(request):
    
    if request.GET.get('code')==None:
        respuesta = render(request, 'indexregistrado.html')
        respuesta.set_cookie('login',request.COOKIES['login'])
        return respuesta

    else:
        client_id='bd2ade5d39bb1b529fb7'
        client_secret='35b46ffbac1f02ea2ca84f44d2450fd00ffd6f40'
        codigo = request.GET.get('code')
        url = 'https://github.com/login/oauth/access_token'
        header = {'content-type':'application/json', 'Accept': 'application/json'}
        payload = {}
        payload['client_id']=client_id
        payload['client_secret']=client_secret
        payload['code']=codigo
    
        res = requests.post(
            url,
            data = json.dumps(payload),
            headers=header
            )
        
        salidaaux=json.loads(res.content)
        salida=json.dumps(salidaaux,indent=2)
        
        header2 = {'content-type':'application/json', 'Accept': 'application/json','Authorization': 'token '+salidaaux['access_token']+''}
        url2='https://api.github.com/user'
        payload2={}
        payload2['access_token']=salidaaux['access_token']
        res2 = requests.get(
            url2,
            headers=header2)
        
        salidaaux2=json.loads(res2.content)
        salida2=json.dumps(salidaaux2, indent=2)
        
        ##############################
        access_token=salidaaux['access_token']
        login=salidaaux2['login']
        ##############################
        
        ##############################
        nuevoUsuario = usuariosapp(
            usuario=login,
            token=access_token,
        )
        es = Elasticsearch()
        req = elasticsearch_dsl.Search(using=es, index='usuariosapp')
        resp = req.scan()
        try:
            for x in resp:
                if x['usuario']==login:
                    entrada = usuariosAppIndex.get(id=x.meta.id, using=es, index='usuariosapp')
                    entrada.update(using=es, token=access_token)
                else:
                    nuevoUsuario.indexing()
        except TransportError:
            nuevoUsuario.indexing()

        respuesta = render(request, 'indexregistrado.html')
        respuesta.set_cookie('login',login)

        return respuesta

def pantalla_lista_usuario(request):
    return render(request, 'user_form.html')

def lista_tareas_usuario(request):
    usuario=request.POST.get('usuario')
    url='https://api.github.com/users/'+usuario+'/repos'
    res = requests.get(
        url,
        )

    salidaaux=json.loads(res.content)

    lista=[]
    for x in salidaaux:
        nodo={}
        nodo['propietario']=x['owner']['login']
        nodo['nombre']=x['name']
        nodo['nombre_completo']=x['full_name']
        nodo['direccion_html']=x['html_url']
        lista.append(nodo)

    sal=json.dumps(lista,indent=2)

    return render(request, 'listaRepo.html', {'object_list': lista})

def lista_tareas_usuarioAPI(request):
    usuario=request.POST.get('usuario')
    url='https://api.github.com/users/'+usuario+'/repos'
    res = requests.get(
        url,
        )

    salidaaux=json.loads(res.content)

    lista=[]
    for x in salidaaux:
        nodo={}
        nodo['propietario']=x['owner']['login']
        nodo['nombre']=x['name']
        nodo['nombre_completo']=x['full_name']
        nodo['direccion_html']=x['html_url']
        lista.append(nodo)

    sal=json.dumps(lista,indent=2)
    
    return HttpResponse(sal, content_type='application/json')

def estadisticasExec(request):
    lista=[]
    if request.POST.get('usuario')==None:
        lista=request.COOKIES['lista']
    else:
        q = Q('bool', must=[Q("match", usuario=request.POST.get('usuario')), Q("match", repositorio=request.POST.get('repositorio'))])
        es = Elasticsearch()
        req = elasticsearch_dsl.Search(using=es, index='tareas').query(q)
        resp = req.execute()
        for x in resp:
            nodo={}
            nodo['propietario']=x.usuario
            nodo['repositorio']=x.repositorio
            aux=datetime.strptime(x.fechaRegistro, '%Y-%m-%dT%H:%M:%S.%f')
            aux=aux.strftime('Creado a las %Hh %Mmin %Sseg del %d-%m-%Y')
            nodo['fechaRegistro']=aux
            aux=datetime.strptime(x.inicioEjecucion, '%Y-%m-%dT%H:%M:%S.%f')
            aux=aux.strftime('Iniciado a las %Hh %Mmin %Sseg del %d-%m-%Y')
            nodo['inicioEjecucion']=aux
            aux=datetime.strptime(x.finEjecucion, '%Y-%m-%dT%H:%M:%S.%f')
            aux=aux.strftime('Finalizado a las %Hh %Mmin %Sseg del %d-%m-%Y')
            nodo['finEjecucion']=aux
            nodo['tEjecucion'] = str(datetime.strptime(x.finEjecucion, '%Y-%m-%dT%H:%M:%S.%f') - datetime.strptime(x.inicioEjecucion, '%Y-%m-%dT%H:%M:%S.%f'))
            nodo['tProceso'] = str(datetime.strptime(x.finEjecucion, '%Y-%m-%dT%H:%M:%S.%f') - datetime.strptime(x.fechaRegistro, '%Y-%m-%dT%H:%M:%S.%f'))
            nodo['tRespuesta'] = str(datetime.now() - datetime.strptime(x.fechaRegistro, '%Y-%m-%dT%H:%M:%S.%f'))
            lista.append(nodo)

    respuesta=render(request, 'statsExec.html', {'object_list': lista})    
    respuesta.set_cookie('lista',lista)
    return respuesta

def estadisticasExecAPI(request):
    lista=[]
    if request.POST.get('usuario')==None:
        lista=request.COOKIES['lista']
    else:
        q = Q('bool', must=[Q("match", usuario=request.POST.get('usuario')), Q("match", repositorio=request.POST.get('repositorio'))])
        es = Elasticsearch()
        req = elasticsearch_dsl.Search(using=es, index='tareas').query(q)
        resp = req.execute()
        for x in resp:
            nodo={}
            nodo['propietario']=x.usuario
            nodo['repositorio']=x.repositorio
            aux=datetime.strptime(x.fechaRegistro, '%Y-%m-%dT%H:%M:%S.%f')
            aux=aux.strftime('Creado a las %Hh %Mmin %Sseg del %d-%m-%Y')
            nodo['fechaRegistro']=aux
            aux=datetime.strptime(x.inicioEjecucion, '%Y-%m-%dT%H:%M:%S.%f')
            aux=aux.strftime('Iniciado a las %Hh %Mmin %Sseg del %d-%m-%Y')
            nodo['inicioEjecucion']=aux
            aux=datetime.strptime(x.finEjecucion, '%Y-%m-%dT%H:%M:%S.%f')
            aux=aux.strftime('Finalizado a las %Hh %Mmin %Sseg del %d-%m-%Y')
            nodo['finEjecucion']=aux
            nodo['tEjecucion'] = str(datetime.strptime(x.finEjecucion, '%Y-%m-%dT%H:%M:%S.%f') - datetime.strptime(x.inicioEjecucion, '%Y-%m-%dT%H:%M:%S.%f'))
            nodo['tProceso'] = str(datetime.strptime(x.finEjecucion, '%Y-%m-%dT%H:%M:%S.%f') - datetime.strptime(x.fechaRegistro, '%Y-%m-%dT%H:%M:%S.%f'))
            nodo['tRespuesta'] = str(datetime.now() - datetime.strptime(x.fechaRegistro, '%Y-%m-%dT%H:%M:%S.%f'))
            lista.append(nodo)

    salida=json.dumps(lista, indent=2)
    
    return HttpResponse(salida, content_type='application/json')
    

def estadisticasPend(request):
    lista=[]
    if request.POST.get('usuario')==None:
        lista=request.COOKIES['lista']
    else:
        q = Q('bool', must=[Q("match", usuario=request.POST.get('usuario')), Q("match", repositorio=request.POST.get('repositorio'))])
        es = Elasticsearch()
        req = elasticsearch_dsl.Search(using=es, index='tareas').query(q)
        resp = req.execute()
        for x in resp:
            nodo={}
            nodo['propietario']=x.usuario
            nodo['repositorio']=x.repositorio
            nodo['fechaRegistro']=x.fechaRegistro
            nodo['inicioEjecucion']=x.inicioEjecucion
            nodo['finEjecucion']=x.finEjecucion
            nodo['tRespuesta'] = str(datetime.now() - datetime.strptime(x.fechaRegistro, '%Y-%m-%dT%H:%M:%S.%f'))
            lista.append(nodo)

    respuesta=render(request, 'statsPend.html', {'object_list': lista})    
    respuesta.set_cookie('lista',lista)
    return respuesta

def estadisticasPendAPI(request):
    lista=[]
    if request.POST.get('usuario')==None:
        lista=request.COOKIES['lista']
    else:
        q = Q('bool', must=[Q("match", usuario=request.POST.get('usuario')), Q("match", repositorio=request.POST.get('repositorio'))])
        es = Elasticsearch()
        req = elasticsearch_dsl.Search(using=es, index='tareas').query(q)
        resp = req.execute()
        for x in resp:
            nodo={}
            nodo['propietario']=x.usuario
            nodo['repositorio']=x.repositorio
            nodo['fechaRegistro']=x.fechaRegistro
            nodo['inicioEjecucion']=x.inicioEjecucion
            nodo['finEjecucion']=x.finEjecucion
            nodo['tRespuesta'] = str(datetime.now() - datetime.strptime(x.fechaRegistro, '%Y-%m-%dT%H:%M:%S.%f'))
            lista.append(nodo)

    salida=json.dumps(lista,indent=2)
    return HttpResponse(salida, content_type='application/json')

def lista_tareas_ejecutadas(request):
    q = Q('bool', must=[Q("match", creador=request.COOKIES['login']), Q("match", estado='true')])
    es = Elasticsearch()
    req = elasticsearch_dsl.Search(using=es, index='tareas').query(q)
    resp = req.execute()
    salida = json.dumps(resp.to_dict(), indent=2)
    
    return render(request, 'listatareasExec.html', {'object_list': resp})
    
def lista_tareas_ejecutadasAPI(request):
    q = Q('bool', must=[Q("match", creador=request.COOKIES['login']), Q("match", estado='true')])
    es = Elasticsearch()
    req = elasticsearch_dsl.Search(using=es, index='tareas').query(q)
    resp = req.execute()
    salida = json.dumps(resp.to_dict(), indent=2)
     
    return HttpResponse(salida, content_type='application/json')
    
def lista_tareas_pendientes(request):
    q = Q('bool', must=[Q("match", creador=request.COOKIES['login']), Q("match", estado='false')])
    es = Elasticsearch()
    req = elasticsearch_dsl.Search(using=es, index='tareas').query(q)
    resp = req.execute()
    salida = json.dumps(resp.to_dict(), indent=2)
       
    return render(request, 'listatareasPend.html', {'object_list': resp})   
    
def lista_tareas_pendientesAPI(request):
    q = Q('bool', must=[Q("match", creador=request.COOKIES['login']), Q("match", estado='false')])
    es = Elasticsearch()
    req = elasticsearch_dsl.Search(using=es, index='tareas').query(q)
    resp = req.execute()
    salida = json.dumps(resp.to_dict(), indent=2)

    return HttpResponse(salida, content_type='application/json')
      

def lista_tareas(request):
    es = Elasticsearch()
    req = elasticsearch_dsl.Search(using=es, index='tareas')
    resp = req.execute()
    salida = json.dumps(resp.to_dict(), indent=2)

    return render(request, 'listatareas.html', {'object_list': resp})

def lista_tareasAPI(request):
    es = Elasticsearch()
    req = elasticsearch_dsl.Search(using=es, index='tareas')
    resp = req.execute()
    salida = json.dumps(resp.to_dict(), indent=2)

    return HttpResponse(salida, content_type='application/json')

def add_tarea(request):
    if request.method == 'POST':
        form = tareasForm(request.POST)
        if form.is_valid():
            new_tarea = form.save(commit=False)
            new_tarea.creador = request.COOKIES['login']
            new_tarea.save()
            return HttpResponseRedirect(reverse('pantallainicio'))
    else:
        form = tareasForm()
        
    respuesta = render(request, 'tarea_form.html', {'form': form})
    respuesta.set_cookie('login',request.COOKIES['login'])
    respuesta.set_cookie('atras','si',10)
    return respuesta
