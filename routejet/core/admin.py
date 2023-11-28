from django.contrib import admin

# Register your models here.

from .models import RouteJetUser

@admin.register(RouteJetUser)

class RouteJetUserAdmin(admin.ModelAdmin):
  list_display= ('username', 'email', 'country', 'city', 'address', 'is_active', 'is_staff', 'is_superuser')

