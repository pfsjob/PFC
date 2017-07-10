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

input("Presione enter para continuar")
     
print("Usuario 1: "+usuario1+" Token 1: "+token1)
print("Usuario 2: "+usuario2+" Token 2: "+token2)

# input("Presione enter para continuar")
# 
# cmd = "curl https://api.github.com/user?access_token="+token1+""
# cmd = shlex.split(cmd)
# p1 = subprocess.Popen(cmd)
# p1.wait()
# 
# cmd = "curl https://api.github.com/user?access_token="+token2+""
# cmd = shlex.split(cmd)
# p1 = subprocess.Popen(cmd)
# p1.wait()

# input("Presione enter para continuar")
# 
# cmd = "curl -X POST -b 'login="+usuario1+"' -F 'usuario=usuarioprueba' -F 'repositorio=repositorioprueba' http://127.0.0.1:8000/tareas/add/"
# cmd = shlex.split(cmd)
# p1 = subprocess.Popen(cmd)
# p1.wait()
# 
# input("Presione enter para continuar")
# 
# cmd = "curl -X POST -b 'login="+usuario2+"' -F 'usuario=usuarioprueba2' -F 'repositorio=repositorioprueba2' http://127.0.0.1:8000/tareas/add/"
# cmd = shlex.split(cmd)
# p1 = subprocess.Popen(cmd)
# p1.wait()
# 
# input("Presione enter para continuar")
# 
# cmd = "curl -XGET http://localhost:9200/tareas/_search?pretty"
# cmd = shlex.split(cmd)
# p1 = subprocess.Popen(cmd)
# p1.wait()
# 
# input("Presione enter para continuar")
# 
# cmd = "curl -XGET -b 'login="+usuario1+"' http://127.0.0.1:8000/tareas/listapendientes/"
# cmd = shlex.split(cmd)
# p1 = subprocess.Popen(cmd)
# p1.wait()
# 
# input("Presione enter para continuar")
# 
# cmd = "curl -XGET -b 'login="+usuario2+"' http://127.0.0.1:8000/tareas/listapendientes/"
# cmd = shlex.split(cmd)
# p1 = subprocess.Popen(cmd)
# p1.wait()

# input("Presione enter para continuar")
# 
# cmd = "curl GET -b 'login="+usuario1+"' http://127.0.0.1:8000/tareas/listaejecutados/"
# cmd = shlex.split(cmd)
# p1 = subprocess.Popen(cmd)
# p1.wait()
# 
# input("Presione enter para continuar")
# 
# cmd = "curl GET -b 'login="+usuario2+"' http://127.0.0.1:8000/tareas/listaejecutados/"
# cmd = shlex.split(cmd)
# p1 = subprocess.Popen(cmd)
# p1.wait()

input("Presione enter para continuar")

cmd = "curl GET http://127.0.0.1:8000/tareas/lista/"
cmd = shlex.split(cmd)
p1 = subprocess.Popen(cmd)
p1.wait()

input("Presione enter para continuar")

cmd = "curl -X POST -F 'usuario="+usuario1+"' http://127.0.0.1:8000/tareas/listausuario/"
cmd = shlex.split(cmd)
p1 = subprocess.Popen(cmd)
p1.wait()
