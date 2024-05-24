import re
from django.db import models
from django.utils.translation import gettext_lazy as _


class Cpf(models.Model):
    cpf = models.CharField(max_length=11, unique=True, primary_key=True)

    class Meta:
        verbose_name = 'CPF'
        verbose_name_plural = 'CPFs'

    def __str__(self):
        return self.cpf

 
    def save(self, *args, **kwargs):
        self.cpf = self.clean_cpf(self.cpf)
        if self.pk is None:
            if Cpf.objects.filter(cpf=self.cpf).exists():
                raise ValueError(_('CPF já existe'))
        return super().save(*args, **kwargs)

    
    @classmethod
    def get_or_create_cpf(cls, cpf):
        try:
            return cls.objects.get(cpf=cpf), False
        except cls.DoesNotExist:
            return cls.objects.create(cpf=cpf), True

        
    @staticmethod
    def clean_cpf(cpf):
        cpf = re.sub('[^0-9]', '', cpf)
        return cpf