from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Boolean, String, Date
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
import elasticsearch_dsl
import shlex, subprocess

connections.create_connection()
    
class usuariosAppIndex(DocType):
    usuario = String()
    token = String()

class tareasIndex(DocType):
    usuario = String()
    repositorio = String()
    fechaRegistro = Date()
    inicioEjecucion = String()
    finEjecucion = Date()
    estado = Boolean()
    creador = String()
    
# def bulk_indexing():
#     print("DENTRO")
#     tareasIndex.init(index='tareas')
#     es = Elasticsearch()
#     bulk(client=es, actions=(b.indexing() for b in models.tareas.objects.all().iterator()))
    
def contador():
    es = Elasticsearch()
    print(elasticsearch_dsl.Search(using=es, index='tareas').count())
    
def makeDash():
    es = Elasticsearch()
    request = elasticsearch_dsl.Search(using=es, index='tareas')#, doc_type='summary')
    request = request.source(['usuario', 'repositorio', 'estado'])
    response = request.scan()
    for commit in response:
        print(commit.usuario, commit.repositorio, commit.estado)
        subprocess.call("pwd")
        cmd = "python3 makeDashboard.py -u "+commit.usuario+" -r "+commit.repositorio+""
        cmd = shlex.split(cmd)
        subprocess.call(cmd)
        
def cambiaDato():
    es = Elasticsearch()
    request = tareasIndex.get(id="grimoirelab-perceval", using=es, index='tareas')
    request.delete()

    
    
# def indexing(self):
#    obj = tareasIndex(
#       meta={'id': self.id},
#       usuario=self.usuario,
#       repositorio=self.repositorio,
#    )
#    obj.save()
#    return obj.to_dict(include_meta=True)