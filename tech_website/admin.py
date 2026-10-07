from django.contrib import admin
from .models import Technology,Sector, ContactSubmission
from django.contrib import admin
from .models import Technology, Sector, generate_custom_id

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('title', 'unique_id', 'sector', 'pdf')  
    search_fields = ('title', 'description')
    list_filter = ('sector',)

    def save_model(self, request, obj, form, change):
        if not obj.unique_id:  
            obj.unique_id = generate_custom_id()
        super().save_model(request, obj, form, change)


admin.site.register(Sector)
admin.site.register(ContactSubmission)