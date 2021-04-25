from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404  # for raising errors
from django.views import generic
from braces.views import SelectRelatedMixin
from django.urls import reverse_lazy
from groups.models import Group
# need to pip install django-braces
# Mixins to add easy functionality to Django class-based views, forms, and models.
# Create your views here.

from . import models
from . import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class PostListView(SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related = ('user', 'groups')

    queryset = models.Post.objects.all()

    def get_context_data(self, **kwargs):

        context = super(PostListView, self).get_context_data(**kwargs)
        context['user_groups'] = Group.objects.filter(
            members__in=[self.request.user])
        context['all_groups'] = Group.objects.all()

        return context
    # so it shows posts related to either the user or the group or both
# https://stackoverflow.com/questions/31237042/whats-the-difference-between-select-related-and-prefetch-related-in-django-orm
# we use select_related to select foreign keys


class UserPostListView(generic.ListView):
    model = models.User
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):

        # checking if the user from User model (accounts app) is the same user in the Post model (post app).
        # and fetching the posts of the user and assigning them to a new variable called post_user

        # https://www.udemy.com/course/python-and-django-full-stack-web-developer-bootcamp/learn/lecture/7133890#questions/2559398
        try:
            self.post_user = User.objects.prefetch_related('posts').get(
                username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context


class PostDetailView(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ('user', 'groups')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))


class CreatePostView(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    fields = ('message', 'groups')
    model = models.Post

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeletePostView(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ("user", "groups")
    success_url = reverse_lazy("posts:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Vanished !")
        return super().delete(*args, **kwargs)

# https://docs.djangoproject.com/en/3.2/ref/models/querysets/
