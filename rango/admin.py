from django.contrib import admin
from rango.models import Category, Page

#Customisation below
class PageAdmin(admin.ModelAdmin):
    fields =["category", "title", "url", "views"]
    list_display = ("title","category", "url")

# Register your models here.

admin.site.register(Category)
admin.site.register(Page, PageAdmin)

