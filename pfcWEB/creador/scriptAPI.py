#! /usr/bin/env python3 

import shlex, subprocess
from elasticsearch import Elasticsearch
import elasticsearch_dsl

es = Elasticsearch()
requ = elasticsearch_dsl.Search(using=es, index='usuariosapp')
resp = requ.execute()

i=0
for x in resp:
    if i==0:
        usuario1=x.usuario
        token1=x.token
    if i==1:
        usuario2=x.usuario
        token2=x.token
    i=i+1

raw_input("Presione enter para continuar")
     
print("Usuario 1: "+usuario1+".")
print("Usuario 2: "+usuario2+".")

raw_input("Presione enter para continuar y comprobar que los usuarios son correctos.")
 
cmd = "curl https://api.github.com/user?access_token="+token1+""
cmd = shlex.split(cmd)
p1 = subprocess.Popen(cmd)
p1.wait()
 
cmd = "curl https://api.github.com/user?access_token="+token2+""
cmd = shlex.split(cmd)
p1 = subprocess.Popen(cmd)
p1.wait()

raw_input("Presione enter para continuar y ver el contenido del indice de Elasticsearch.")

cmd = "curl -XGET http://34.212.39.231/tareas/listaAPI/"
cmd = shlex.split(cmd)
p1 = subprocess.Popen(cmd)
p1.wait()

raw_input("Presione enter para continuar y anadir una tarea al sistema para cada usuario.")
  
cmd = "curl -X POST -b 'login="+usuario1+"' -F 'usuario=usuarioprueba' -F 'repositorio=repositorioprueba' http://34.212.39.231/tareas/add/"
cmd = shlex.split(cmd)
p1 = subprocess.Popen(cmd)
p1.wait()
  
cmd = "curl -X POST -b 'login="+usuario2+"' -F 'usuario=usuarioprueba2' -F 'repositorio=repositorioprueba2' http://34.212.39.231/tareas/add/"
cmd = shlex.split(cmd)
p1 = subprocess.Popen(cmd)
p1.wait()
 
raw_input("Presione enter para continuar")
# 
raw_input("Presione enter para continuar y ver el contenido del indice de Elasticsearch una vez anadidas las tareas.")

cmd = "curl -XGET http://34.212.39.231/tareas/listaAPI/"
cmd = shlex.split(cmd)
p1 = subprocess.Popen(cmd)
p1.wait()
# 
raw_input("Presione enter para continuar y ver las tareas pendientes de ejecucion del usuario 1.")
  
cmd = "curl -XGET -b 'login="+usuario1+"' http://34.212.39.231/tareas/listapendientesAPI/"
cmd = shlex.split(cmd)
p1 = subprocess.Popen(cmd)
p1.wait()

user=raw_input("Introduza un propietario del listado de tareas pendientes para ver sus estadisticas: ")
repo=raw_input("Introduza un repositorio del listado de tareas pendientes para ver sus estadisticas: ")
cmd = "curl -XPOST -b 'login="+usuario1+"' -F 'usuario="+user+"' -F 'repositorio="+repo+"' http://34.212.39.231/tareas/estadisticasPendAPI/"
cmd = shlex.split(cmd)
p1 = subprocess.Popen(cmd)
p1.wait()
  
raw_input("Presione enter para continuar y ver las tareas pendientes de ejecucion del usuario 2.")
  
cmd = "curl -XGET -b 'login="+usuario2+"' http://34.212.39.231/tareas/listapendientesAPI/"
cmd = shlex.split(cmd)
p1 = subprocess.Popen(cmd)
p1.wait()

user=raw_input("Introduza un propietario del listado de tareas pendientes para ver sus estadisticas: ")
repo=raw_input("Introduza un repositorio del listado de tareas pendientes para ver sus estadisticas: ")
cmd = "curl -XPOST -b 'login="+usuario2+"' -F 'usuario="+user+"' -F 'repositorio="+repo+"' http://34.212.39.231/tareas/estadisticasPendAPI/"
cmd = shlex.split(cmd)
p1 = subprocess.Popen(cmd)
p1.wait()
 
raw_input("Presione enter para continuar y ver las tareas ejecutadas del usuario 1.")
 
cmd = "curl -XGET -b 'login="+usuario1+"' http://34.212.39.231/tareas/listaejecutadosAPI/"
cmd = shlex.split(cmd)
p1 = subprocess.Popen(cmd)
p1.wait()
 
user=raw_input("Introduza un propietario del listado de tareas ejecutadas para ver sus estadisticas: ")
repo=raw_input("Introduza un repositorio del listado de tareas ejecutadas para ver sus estadisticas: ")
cmd = "curl -XPOST -b 'login="+usuario1+"' -F 'usuario="+user+"' -F 'repositorio="+repo+"' http://34.212.39.231/tareas/estadisticasExecAPI/"
cmd = shlex.split(cmd)
p1 = subprocess.Popen(cmd)
p1.wait()
 
raw_input("Presione enter para continuar y ver las tareas ejecutadas del usuario 2.")
 
cmd = "curl -XGET -b 'login="+usuario2+"' http://34.212.39.231/tareas/listaejecutadosAPI/"
cmd = shlex.split(cmd)
p1 = subprocess.Popen(cmd)
p1.wait()

user=raw_input("Introduza un propietario del listado de tareas ejecutadas para ver sus estadisticas: ")
repo=raw_input("Introduza un repositorio del listado de tareas ejecutadas para ver sus estadisticas: ")
cmd = "curl -XPOST -b 'login="+usuario2+"' -F 'usuario="+user+"' -F 'repositorio="+repo+"' http://34.212.39.231/tareas/estadisticasExecAPI/"
cmd = shlex.split(cmd)
p1 = subprocess.Popen(cmd)
p1.wait()

# raw_input("Presione enter para continuar")
# 
# cmd = "curl GET http://34.212.39.231/tareas/listaAPI/"
# cmd = shlex.split(cmd)
# p1 = subprocess.Popen(cmd)
# p1.wait()

user=raw_input("Introduzca un propietario de GitHub para ver sus repositorios: ")

cmd = "curl -X POST -F 'usuario="+user+"' http://34.212.39.231/tareas/listausuarioAPI/"
cmd = shlex.split(cmd)
p1 = subprocess.Popen(cmd)
p1.wait()
