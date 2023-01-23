from django.contrib import admin
from .models import *
from django.forms import Textarea
from nested_admin import NestedModelAdmin, NestedTabularInline, NestedStackedInline
from django.forms import TextInput, Textarea



# @admin.register(Identifier)
class IdentifierAdmin(NestedStackedInline):
    model = Identifier
    list_display = ['uz', 'ru']
    extra=0
    formfield_overrides = {
		models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':40})},
	}

    # fields = (('uz', 'ru'), 'type')

@admin.register(Product)
class ProductAdmin(NestedModelAdmin):
    model = Product
    inlines = [IdentifierAdmin]
    extra=0
    # list_display = ['uz', 'ru', 'identifier', 'type']

    formfield_overrides = {
		models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':40})},
	}

    # fields = (('uz', 'ru'), 'type', 'identifier')


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    model = Type
    list_display = ['uz', 'ru']
    formfield_overrides = {
		models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':40})},
	}

    fields = (('uz', 'ru'), 'poll')


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    model = Record
    # list_display = ['uz', 'ru']
    formfield_overrides = {
		models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':40})},
	}

    # fields = '__all__'















# admin.site.register(Item, ItemAdmin)
# # admin.site.register(Response, ResponseAdmin)

# # Register your models here.
