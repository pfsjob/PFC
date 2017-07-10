from .models import tareas
from django.db.models.signals import post_save
from django.dispatch import receiver
from elasticsearch import Elasticsearch
import elasticsearch_dsl
from . import search
import time

@receiver(post_save, sender=tareas)
def index_post(sender, instance, **kwargs):
    instance.indexing()
    time.sleep(2)
    #search.cambiaDato()
    #search.makeDash()
#     es = Elasticsearch()
#     request = elasticsearch_dsl.Search(using=es, index='tareas')#, doc_type='summary')
#     request = request.source(['usuario', 'repositorio', 'estado'])
#     response = request.scan()
#     for commit in response:
#         cmd = "python3 makeDashboard.py -u "+commit.usuario+" -r "+commit.repositorio+" -add"
#         cmd = shlex.split(cmd)
#         subprocess.call(cmd)