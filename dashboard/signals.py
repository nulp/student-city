
from .models import Person, PersonHistory
from .serializers import PersonTableSerializer

from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Person, dispatch_uid="add_person_too_history")
def add_person_too_history(sender, instance, **kwargs):
    prev = PersonHistory.objects.filter(person_id=instance.id).order_by('-timestamp').first()
    cur_text = str(PersonTableSerializer(instance).data)
    if not prev or not prev.data == cur_text:
        PersonHistory.objects.create(person_id=instance.id, data=cur_text)
