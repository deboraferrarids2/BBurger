from django.db import models
from django.utils.translation import gettext_lazy as _
import os



def imageFileUpdload(filename, instance):
    name = str(filename)
    return name

class Product(models.Model):
    name = models.CharField(max_length=400, unique=False)
    category = models.CharField(max_length=40,verbose_name="categoria", choices=(("bebida", "bebida"), ("lanche", "lanche"), ('sobremesa','sobremesa'), ('acompanhamento','acompanhamento')))
    description = models.CharField(max_length=400, unique=False)
    size = models.CharField(max_length=10,verbose_name="tamanho", choices=(("pequeno", "pequeno"), ("medio", "medio"), ('grande','grande')), blank=True, null=True)
    image = models.FileField(_('imagem'), upload_to=imageFileUpdload, blank=True, null=True)
    amount = models.IntegerField(verbose_name="valor",help_text="em centavos",default=0)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return f"{self.id}-{self.name}"

 
    def save(self,*args,**kwargs):
        kwargs['using'] = 'default'
        return super().save(*args,**kwargs)