from django.db import models

# Create your models here.
from customer.models import User

class Notes(models.Model):
    note_id = models.CharField('id',  max_length=150, unique=True, blank=False, null=True)
    text = models.TextField('Текст')
    header = models.CharField('Заголовок', max_length=150)
    time = models.DateTimeField()
    class Meta:
        ordering = ['-time']
    

class UserNote(models.Model):
    note_id = models.ForeignKey('Notes', on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)