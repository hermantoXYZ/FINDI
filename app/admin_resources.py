from import_export import resources, fields
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .models import UserAnggota


class UserAnggotaResource(resources.ModelResource):
    password = fields.Field(column_name='password', attribute='password')

    class Meta:
        model = User
        import_id_fields = ('username',)
        fields = (
            'username', 'email', 'first_name', 'last_name', 
            'is_active', 'password',
            'telp', 'gender', 'tempat_lahir', 'tgl_lahir', 
            'nidn', 'alamat', 'bidang_keahlian', 'photo'
        )

    def before_import_row(self, row, **kwargs):
        # Hash password sebelum disimpan
        if 'password' in row and row['password']:
            row['password'] = make_password(row['password'])

    def after_import_row(self, row, row_result, **kwargs):
        if row_result.import_type in ('new', 'update'):
            try:
                user = User.objects.get(username=row['username'])
            except ObjectDoesNotExist:
                raise ValidationError(f"User dengan username '{row['username']}' tidak ditemukan.")

            # Pastikan UserAnggota terhubung ke user yang sesuai
            anggota, created = UserAnggota.objects.get_or_create(id_anggota=user)

            anggota.telp = row.get('telp', '')
            anggota.gender = row.get('gender', '')
            anggota.tempat_lahir = row.get('tempat_lahir', '')
            anggota.tgl_lahir = row.get('tgl_lahir', None)
            anggota.nidn = row.get('nidn', '')
            anggota.alamat = row.get('alamat', '')
            anggota.bidang_keahlian = row.get('bidang_keahlian', '')

            # Kolom foto opsional — bisa dilewati jika tidak ada
            photo_value = row.get('photo')
            if photo_value:
                anggota.photo = photo_value

            anggota.save()
