from django.contrib import admin
from .models import Group, GroupMember
# Register your models here.

# in admin page
# ability to edit models on the same page as parent model
# parent model is Group, we can edit Group Member inside group
# we use admin.TabularInline
# to make it simple,
# Inline models are used on the admin pages to show two models on the same page

# the goal is that we could edit users inside each group in admin page,
# like pc group has 10 users we can edit user there

# we use TabularInline for GroupMember model


class GroupMemberInLine(admin.TabularInline):
    model = GroupMember


# in model.admin we give the inlines
class GroupAdmin(admin.ModelAdmin):
    inlines = [GroupMemberInLine]


# we register the the inline in groupadmin and the parent model
admin.site.register(Group, GroupAdmin)
