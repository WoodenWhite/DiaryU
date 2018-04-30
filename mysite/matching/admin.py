from django.contrib import admin
from .models import User, Diary, Pairing, Word, Message, Image

# Register your models here.
admin.site.register(User)
admin.site.register(Diary)
admin.site.register(Pairing)
admin.site.register(Word)
admin.site.register(Message)
admin.site.register(Image)
