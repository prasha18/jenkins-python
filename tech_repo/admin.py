from django.contrib import admin
from .models import District, State, Inventor, Tech_Director

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'state']
    search_fields = ['name']
    list_filter = ['state']

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(Inventor)
class InventorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'designation', 'dob', 'mobile', 'email']
    search_fields = ['name', 'designation', 'mobile', 'email']
    list_filter = ['designation', 'dob']
    readonly_fields = ['content_type', 'object_id', 'content_object']

    def get_content_object(self, obj):
        """Display the related content object in the admin list view."""
        return str(obj.content_object) if obj.content_object else 'None'
    get_content_object.short_description = 'Related Object'



@admin.register(Tech_Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'designation', 'dob', 'mobile', 'email']
    search_fields = ['name', 'designation', 'mobile', 'email']
    list_filter = ['designation', 'dob']
    readonly_fields = ['content_type', 'object_id', 'content_object']

    def get_content_object(self, obj):
        """Display the related content object in the admin list view."""
        return str(obj.content_object) if obj.content_object else 'None'
    get_content_object.short_description = 'Related Object'