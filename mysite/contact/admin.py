from django.contrib import admin

from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "last_name", "add_contact", "add_contact_to")
    list_display_links = ("name", )
    
    
 