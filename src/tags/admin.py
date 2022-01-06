from django.contrib import admin
from .models import TaggedItem

class TaggedItemAdmin(admin.ModelAdmin):
    
    readyonly_fields = ('content_object',)
    class Meta: 
        model = TaggedItem
        fields = ['tag','content_type','object_id','content_object',]
admin.site.register(TaggedItem,TaggedItemAdmin)
