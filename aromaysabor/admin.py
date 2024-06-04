from django.contrib import admin
from .models import CPC, NEIGHBORHOOD_COMMUNE

@admin.register(CPC)
class CPCAdmin(admin.ModelAdmin):
    list_display = ('name', 'neighborhood', 'commune', 'category', 'local_type', 'address')
    search_fields = ('name', 'neighborhood', 'category', 'local_type')
    list_filter = ('neighborhood', 'category', 'local_type', 'commune')

    exclude = ('commune',)

    def save_model(self, request, obj, form, change):
        # Automatically set the commune based on the neighborhood
        obj.commune = int(NEIGHBORHOOD_COMMUNE.get(obj.neighborhood, '0'))
        super().save_model(request, obj, form, change)