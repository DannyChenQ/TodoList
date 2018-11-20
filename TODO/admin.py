from django.contrib import admin
from models import list


# Register your models here.


class ToDoAdmin(admin.ModelAdmin):
	list_display = ["content", "add_time"]
	list_filter = ["complete_time"]
	ordering = ["-add_time"]


admin.site.register(list, ToDoAdmin)
