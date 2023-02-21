from django.contrib import admin

from .models import Basket, Category, Ingredient, Product

admin.site.site_header = "Админ панель WheelPizza"
admin.site.index_title = 'Админ панель'

admin.site.register(Ingredient)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}


class BasketAdmin(admin.TabularInline):
    model = Basket
    extra = 0
    fields = ['product', 'quantity']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    list_display = ['name', 'category', 'price', 'image', 'slug']
    list_editable = ['category', 'price', 'image', 'slug']
    ordering = ['category']
    filter_horizontal = ['consist']
