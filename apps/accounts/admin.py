from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone


from apps.accounts.forms import UserChangeForm, UserCreationForm
from apps.accounts.models import User

# Register your models here.



class UserAdmin(BaseUserAdmin):

    # The forms to add and change user instances
    readonly_fields = ('created_at', 'updated_at', 'last_updated_password',
                       'password')
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'full_name', 'last_name','admin', 'created_at',
                    'updated_at','days_since_last_login')
    list_filter = ("created_at",)
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
            'fields': (
                'first_name', 'middle_name', 'last_name',
                'username', 'email_verified', "uuid", 
            
            )
        }),
        ('Permissions', {
            'fields': (
                'admin', 'staff', 'active',
                'groups', 'user_permissions'
            )
        }),
        ('Activity', {
            'fields': (
                'created_at', 'updated_at', 'last_login',
                'last_updated_password',
            )
        })
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name',
                'password1',
                'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    def full_name(self, obj):
        """Return the full name of the user in title case"""
        return f"{obj.first_name} {obj.last_name}".title()

    def days_since_last_login(self, obj):
        return (timezone.now() - obj.created_at).days


admin.site.register(User, UserAdmin)