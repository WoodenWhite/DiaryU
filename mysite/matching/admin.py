from django.contrib import admin
from .models import User, Diary, Pairing, Word

# Register your models here.
admin.site.register(User)
admin.site.register(Diary)
admin.site.register(Pairing)
admin.site.register(Word)
