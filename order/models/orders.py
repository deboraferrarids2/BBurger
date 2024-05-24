from django.db import models
import os
import re

from user_auth.models import BaseUser, Cpf
from .products import Product

class Order(models.Model):
    user = models.ForeignKey(BaseUser, verbose_name='usuario', null=True, blank=True,
                             on_delete=models.CASCADE)
    session_token = models.CharField(max_length=255, blank=True, null=True)
    cpf = models.ForeignKey(Cpf ,verbose_name="cpf", null=True, blank=True,
                             on_delete=models.CASCADE)
    status = models.CharField(max_length=20,verbose_name="status", choices=(("em aberto", "em aberto"), ("recebido", "recebido"), ('em preparacao','em preparacao'), ('pronto','pronto'), ('finalizado','finalizado'), ('cancelado','cancelado')), default='em aberto')
    created_at = models.DateTimeField(auto_now=True, verbose_name="criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="atualizado em", null=True, blank=True,)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return f"{self.id}"

 
    def save(self,*args,**kwargs):
        kwargs['using'] = 'default'
        return super().save(*args,**kwargs)


class OrderItems(models.Model):
    order = models.ForeignKey(Order, verbose_name='pedido',
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='produto',
                             on_delete=models.CASCADE)
    quantity = models.IntegerField()
    changes = models.TextField(max_length=300,verbose_name="alteracoes", null=True, blank=True,)


    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens do pedido'

    def __str__(self):
        return f"{self.order}-{self.product}"

 
    def save(self,*args,**kwargs):
        kwargs['using'] = 'default'
        return super().save(*args,**kwargs)
