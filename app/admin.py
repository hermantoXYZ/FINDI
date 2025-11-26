from django.contrib import admin
from django.db import models
from .models import UserAdmin, UserAnggota, Article, Category, Page, Topic, Saham
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .admin_resources import UserAnggotaResource
from import_export import fields

class SahamResource(resources.ModelResource):
    symbol = fields.Field(attribute="symbol", column_name="symbol")
    long_name = fields.Field(attribute="long_name", column_name="long_name")
    papan_pencatatan = fields.Field(attribute="papan_pencatatan", column_name="papan_pencatatan")
    sektor = fields.Field(attribute="sektor", column_name="sektor")

    class Meta:
        model = Saham
        import_id_fields = ["symbol"]  
        fields = ("symbol", "long_name", "papan_pencatatan", "sektor")

@admin.register(Saham)
class SahamAdmin(ImportExportModelAdmin):
    resource_class = SahamResource
    
    list_display = ("symbol", "sektor", "last_updated")
    search_fields = ("symbol", "long_name", "sektor", "papan_pencatatan")

class TopicResource(resources.ModelResource):
    class Meta:
        model = Topic
        fields = ('name', 'slug')
        import_id_fields = ('name',) 


@admin.register(Topic)
class TopicAdmin(ImportExportModelAdmin):
    resource_class = TopicResource
    list_display = ('name', 'slug')
    search_fields = ('name',)


class UserAnggotaImport(ImportExportModelAdmin):
    resource_class = UserAnggotaResource  # Import User DOSEN

admin.site.register(UserAnggota)
admin.site.register(UserAdmin)
admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Page)
