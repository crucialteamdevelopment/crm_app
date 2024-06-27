from django.contrib import admin
from .models import Property, PropertyType, PropertyUnit, PropertyImage, Bookmark, Violation


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['property_type', 'holding_company', 'state', 'city', 'street_address', 'zip_code', 'number_of_floors']
    search_fields = ['property_type', 'holding_company', 'state', 'city', 'address', 'zip_code', 'number_of_floors']


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(PropertyUnit)
class PropertyUnitAdmin(admin.ModelAdmin):
    pass


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    pass


@admin.register(Violation)
class ViolationAdmin(admin.ModelAdmin):
    pass

