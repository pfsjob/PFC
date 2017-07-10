#! /usr/bin/env python3 

import argparse, shlex, subprocess, os.path
from argparse import Action

parser = argparse.ArgumentParser(description = "Creador de dashboards mediante usuario y repositorio")
parser.add_argument("-u", "--usuario", help="Dueño del repositorio")
parser.add_argument("-r", "--repositorio", help="Nombre del repositorio")
parser.add_argument("-add", "--añadir", action="store_true", help="Añadir al dashboard actual")

args = parser.parse_args()

if args.añadir==False:
    borrar1="curl -XDELETE http://localhost:9200/git"
    borrar1=shlex.split(borrar1)
    subprocess.call(borrar1)
    borrar2="curl -XDELETE http://localhost:9200/git_raw"
    borrar2=shlex.split(borrar2)
    subprocess.call(borrar2)

repo_url = 'https://github.com/'+args.usuario+'/'+args.repositorio+'.git'
# repo_dir = '/tmp/'+sys.argv[2]+'.git'

cmd = "p2o.py --enrich --index git_raw --index-enrich git \-e http://localhost:9200 --no_inc --debug \git "+repo_url+""
cmd = shlex.split(cmd)
subprocess.call(cmd)

if os.path.exists("/tmp/git-dashboard.json"):
    print("Existe")
else:
    print("No existe")
    cmdTmp="curl -o /tmp/git-dashboard.json https://raw.githubusercontent.com/jgbarah/GrimoireLab-training/master/grimoireelk/dashboards/git-dashboard.json"
    cmdTmp=shlex.split(cmdTmp)
    subprocess.call(cmdTmp)

cmd3 = "kidash.py --elastic_url-enrich http://locahost:9200 \--import /tmp/git-dashboard.json"
cmd3 = shlex.split(cmd3)
subprocess.call(cmd3)

