
from django import template
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
# https://docs.djangoproject.com/en/3.1/ref/utils/
# A Slug is a short label for something, containing only letters, underscores or hyphens.
# Slugs are generally used in URL, For example in a typical blog entry URL:
# https://www.kodnito.com/posts/slugify-urls-in-django
# instead of being posts/1

import misaka as m
# https://misaka.61924.nl/
# idk what it does upto now

# we are getting the user which is already used.
from django.contrib.auth import get_user_model
User = get_user_model()

# idk what it does anyways
register = template.Library()


class Group(models.Model):
    name = models.CharField(verbose_name='Clan Name',
                            max_length=220, unique=True,)  # verbose_name is the label for fields
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(
        verbose_name='All About The Clan', blank=True, default='', max_length=250,)
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User, through='GroupMember')
    # A ManyToMany field is used when a model needs to reference multiple instances of another model. Use cases include:
    # https://medium.com/swlh/django-forms-for-many-to-many-fields-d977dec4b024

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = m.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('groups:single', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['name']


class GroupMember(models.Model):
    group = models.ForeignKey(
        Group, related_name="membershit", on_delete=models.CASCADE)
    # the above line means the groupmember is related to group via the foreignkey which we call as membershit
    user = models.ForeignKey(
        User, related_name="user_group", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group', 'user')
        # dk what is this
