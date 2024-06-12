# signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Procesos

@receiver(pre_save, sender=Procesos)
def populate_fields(sender, instance, **kwargs):
    if instance.asignado:
        instance.presupuesto = instance.asignado.cobro
        instance.trabajo_realizado = instance.asignado.trabajo_a_realizar
