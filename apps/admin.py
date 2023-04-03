import csv
from io import StringIO

from django.contrib import admin
from django.contrib.admin import StackedInline
from django.contrib.auth.admin import UserAdmin
from django.forms import forms
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import path
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource
from mptt.admin import DraggableMPTTAdmin

from apps.models import Product, Tag, ProductImage, User, Category


class ProductImagesInline(StackedInline):
    min_num = 1
    extra = 0
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductImagesInline,)
    list_display = (
        'title', 'short_description', 'price', 'is_premium', 'shopping_cost', 'specification',
        'discount', 'quantity')

    fields = (
        'title', 'short_description', 'price', 'is_premium', 'description', 'shopping_cost', 'specification', 'tags',
        'author',
        'discount', 'quantity')


# class ExportCsvMixin:
#     def export_as_csv(self, request, queryset):
#         meta = self.model._meta
#         field_names = (field.name for field in meta.fields)
#
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
#         writer = csv.writer(response)
#         writer.writerow(field_names)
#         for obj in queryset:
#             row = writer.writerow(getattr(obj, field) for field in field_names)
#
#         return response
#
#     export_as_csv.short_description = 'Export Selected'

class TagResource(ModelResource):
    class Meta:
        model = Tag
        export_order = ('name', 'id')


class TagNameResource(ModelResource):
    class Meta:
        model = Tag
        fields = ('name',)
        name = "Export/Import only tag names"


@admin.register(Tag)
class TagAdmin(ImportExportModelAdmin):
    resource_classes = [TagResource, TagNameResource]
    list_display = ('name',)
    fields = ('name',)
    # actions = ('export_as_csv',)


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('status', 'email')


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    pass


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_tag')

    def image_tag(self, obj):
        return format_html(f'''<a href="{obj.image.url}" target="_blank"><img src="{obj.image.url}"
         alt="image" width="100 height="100" style="object-fit : cover;"/></a>''')

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted.objects:
            obj.delete()
        for instance in instances:
            instance.user = request.user
            instance.save()
        formset.save.m2m()
