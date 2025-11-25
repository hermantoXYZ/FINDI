from django.contrib import admin
from django.db import models
from .models import UserAdmin, UserAnggota, Article, Category, Page, Topic, Saham
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .admin_resources import UserAnggotaResource


class SahamResource(resources.ModelResource):
    class Meta:
        model = Saham
        fields = (
            "id",
            "symbol",
            "nama_perusahaan",
            "tanggal_listing",
            "current_share",
            "papan_pencatatan",
            "sektor",
        )
        export_order = fields
        
@admin.register(Saham)
class SahamAdmin(ImportExportModelAdmin):
    resource_class = SahamResource

    list_display = (
        "symbol",
        "nama_perusahaan",
        "sektor",
        "papan_pencatatan",
        "current_share",
        "tanggal_listing",
    )

    search_fields = ("symbol", "nama_perusahaan", "sektor")
    list_filter = ("papan_pencatatan", "sektor")
    ordering = ("symbol",)

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
