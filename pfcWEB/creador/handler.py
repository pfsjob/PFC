#! /usr/bin/env python3 

import shlex, subprocess, os.path
from elasticsearch import Elasticsearch
import elasticsearch_dsl
from elasticsearch_dsl import DocType, String, Boolean, Q
from datetime import datetime
import time

class tareasIndex(DocType):
        usuario = String()
        repositorio = String()
        estado = Boolean()

while 1:   
    print("Comienzo la ejecucion")
    if os.path.exists("/tmp/git-dashboard.json"):
        print("Existe")
    else:
        print("No existe")
        cmdTmp="curl -o /tmp/git-dashboard.json https://raw.githubusercontent.com/jgbarah/GrimoireLab-training/master/grimoireelk/dashboards/git-dashboard.json"
        cmdTmp=shlex.split(cmdTmp)
        subprocess.call(cmdTmp)
    
    if os.path.exists("/tmp/github-dashboard.json"):
        print("Existe")
    else:
        print("No existe")
        cmdTmp="curl -o /tmp/github-dashboard.json https://raw.githubusercontent.com/jgbarah/GrimoireLab-training/master/grimoireelk/dashboards/github-dashboard.json"
        cmdTmp=shlex.split(cmdTmp)
        subprocess.call(cmdTmp)
    
    es = Elasticsearch()
    q = Q("match", estado='false')
    requ = elasticsearch_dsl.Search(using=es, index='tareas').query(q)
    resp = requ.execute()
    
    
    for commit in resp:
  
        qitem = Q("match", usuario=commit.creador)
        reqitem = elasticsearch_dsl.Search(using=es, index='usuariosapp').query(qitem)
        respitem = reqitem.execute()
        for x in respitem:
            req = tareasIndex.get(id=commit.usuario+"-"+commit.repositorio, using=es, index='tareas')
            req.update(using=es, inicioEjecucion=datetime.now())
            repo_url = 'https://github.com/'+commit.usuario+'/'+commit.repositorio+'.git'
            cmd = "p2o.py --enrich --index git_raw --index-enrich git \-e http://localhost:9200 --no_inc --debug \git "+repo_url+""
            cmd = shlex.split(cmd)
            p1 = subprocess.Popen(cmd)
      
            cmd3 = "kidash.py --elastic_url-enrich http://locahost:9200 \--import /tmp/git-dashboard.json"
            cmd3 = shlex.split(cmd3)
            p2 = subprocess.Popen(cmd3)
            p1.wait()
            p2.wait()
            
            cmd = "p2o.py --enrich --index github_raw --index-enrich github \-e http://localhost:9200 --no_inc --debug \github "+commit.usuario+" "+commit.repositorio+" \-t "+x.token+""
            cmd = shlex.split(cmd)
            p1 = subprocess.Popen(cmd)
       
            cmd3 = "kidash.py --elastic_url-enrich http://locahost:9200 \--import /tmp/github-dashboard.json"
            cmd3 = shlex.split(cmd3)
            p2 = subprocess.Popen(cmd3)
            p1.wait()
            p2.wait()
    
            req.update(using=es, estado=True, finEjecucion=datetime.now())
            
    time.sleep(30)
