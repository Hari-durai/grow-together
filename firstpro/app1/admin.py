from django.contrib import admin

# Register your models here.
from .models import room,topic,Message

admin.site.register(room)
admin.site.register(topic)
admin.site.register(Message)
