from django.db import models
from django.forms import ModelForm
from .search import tareasIndex, usuariosAppIndex
from django.utils import timezone
import time
from datetime import datetime
    
class usuariosapp(models.Model):
    usuario=models.CharField(max_length=100)
    token=models.CharField(max_length=100)
    
    def indexing(self):
        obj = usuariosAppIndex(
           meta={'type': "doc_type", 'id': self.usuario},
           usuario=self.usuario,
           token=self.token,
        )
        obj.save(index='usuariosapp')
        return obj.to_dict(include_meta=True)

def horainicio():
        ahora = datetime.now()
        inicio = ahora.replace(hour=0, minute=0, second=0, microsecond=1, year=1970, month=1, day=1)
        print(inicio)
        return inicio   
  
class tareas(models.Model):
    usuario=models.CharField(max_length=100)
    repositorio=models.CharField(max_length=100)
    fechaRegistro=models.DateTimeField(default=datetime.now)
    inicioEjecucion=models.DateTimeField(default=horainicio)
    finEjecucion=models.DateTimeField(default=horainicio)
    estado=models.BooleanField(default=False)
    creador=models.CharField(max_length=100, default="None")
    
    def indexing(self):
        obj = tareasIndex(
           meta={'type': "doc_type", 'id': self.usuario+"-"+self.repositorio},
           usuario=self.usuario,
           repositorio=self.repositorio,
           fechaRegistro=self.fechaRegistro,
           inicioEjecucion=self.inicioEjecucion,
           finEjecucion=self.finEjecucion,
           estado=self.estado,
           creador=self.creador,
        )
        print(self.fechaRegistro)
        obj.save(index='tareas')
        return obj.to_dict(include_meta=True)
    
class tareasForm(ModelForm):
    class Meta:
        model = tareas
        fields = ('usuario', 'repositorio')
    
# class BlogPost(models.Model):
#    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogpost')
#    posted_date = models.DateField(default=timezone.now)
#    title = models.CharField(max_length=200)
#    text = models.TextField(max_length=1000)