
from groups.models import Group
from django.db import models
from django.urls import reverse
from django.conf import settings
import misaka as m
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts',
                             on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    message = models.TextField(
        verbose_name='Serve here !')
    message_html = models.TextField(editable=False)
    groups = models.ForeignKey(
        Group, verbose_name='Clan', related_name='posts', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = m.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:single', kwargs={'username': self.user.username,
                                               'pk': self.pk})

    class Meta:
        ordering = ['-created_on']
        unique_together = ['user', 'message']


# groups model is kinda same check it for details
