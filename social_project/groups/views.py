from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import Group, GroupMember
from django.contrib import messages
# Create your views here.


class CreateGroupView(generic.CreateView, LoginRequiredMixin):
    fields = ('name', 'description')
    model = Group
    template_name = 'groups/groups_form.html'


class SingleGroupView(generic.DetailView):
    model = Group
    template_name = 'groups/groups_detail.html'


class ListGroupView(generic.ListView):
    model = Group
    template_name = 'groups/groups_list.html'


class JoinGroupView(generic.RedirectView, LoginRequiredMixin):

    # redirects to the group detail page once joined
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    # to check if the member is already in the group
    def get(self, request, *args, **kwargs):

        # getting the slug object ie the pk to try and check if the member is already in
        group = get_object_or_404(Group, slug=self.kwargs.get("slug"))

        # we create the user inside the group
        try:
            GroupMember.objects.create(user=self.request.user, group=group)

        # raises integrity error, ie if a duplicate key was inserted
        except IntegrityError:
            messages.warning(
                self.request, ("Warning, already a member of {}".format(group.name)))

        # else a welcome msg
        else:
            messages.success(
                self.request, "You are now a member of the {} group.".format(group.name))

        return super().get(request, *args, **kwargs)


class LeaveGroupView(LoginRequiredMixin, generic.RedirectView):

    # redirects to the group detail page once joined
    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single", kwargs={"slug": self.kwargs.get("slug")})

    # check if member is in the group
    def get(self, request, *args, **kwargs):
        try:
            membership = GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()
        # if membership is not in the group
        except GroupMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )
        # if so
        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this group."
            )
        return super().get(request, *args, **kwargs)
