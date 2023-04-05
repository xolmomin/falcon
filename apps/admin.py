from django.contrib import admin
from django.contrib.admin import StackedInline
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource
from mptt.admin import DraggableMPTTAdmin

from apps.models import Product, Tag, ProductImage, User, Category, ProductProxy


class ProductImagesInline(StackedInline):
    min_num = 1
    extra = 0
    model = ProductImage


class ProductMixin(admin.ModelAdmin):
    list_display = (
        'title', 'short_description', 'price', 'is_premium', 'shopping_cost', 'specification',
        'discount', 'quantity')

    fields = (
        'title', 'short_description', 'category', 'price', 'is_premium', 'description', 'shopping_cost',
        'specification', 'tags',
        'author',
        'discount', 'quantity', 'image')
    search_fields = ['title']


@admin.register(ProductProxy)
class ProductProxyAdmin(ProductMixin):

    def get_queryset(self, request):
        query = super().get_queryset(request)
        return query.filter(is_premium=True)


@admin.register(Product)
class ProductAdmin(ProductMixin):
    inlines = (ProductImagesInline,)
    readonly_fields = ['image']

    def get_queryset(self, request):
        query = super().get_queryset(request)
        return query.filter(is_premium=False)

    def image(self, obj):
        if obj.images.first():
            img = obj.images.first().image
            return mark_safe(f'<img src="{img.url}" width="{200}" height={200} />')
        return None


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


'''
Special products (is_premium=True)
Products (is_premium=False)
'''


class ProductInline(admin.StackedInline):
    model = Product
    min_num = 1
    extra = 1
    max_num = 5


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    inlines = [ProductInline]


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
