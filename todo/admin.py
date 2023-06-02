from django.contrib import admin

from todo.models import Tag, Todo,User

# Register your models here.
class TodoAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Todo)
admin.site.register(Tag)
admin.site.register(User)
