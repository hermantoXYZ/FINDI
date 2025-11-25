from django import forms
from django.utils import timezone
from .models import Page, Article, UserAnggota, UserAdmin, Topic
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
tgl_now = timezone.now()


class formProfile(forms.ModelForm):
    class Meta:
        model = UserAdmin
        fields = [    
            'telp',
            'gender',
            'photo',
        ]
        widgets = {
            'gender': forms.Select(
                choices=[
                    ('Laki-laki', 'Laki-laki'),
                    ('Perempuan', 'Perempuan'),
                ],
                attrs={'class': 'form-control'}
            ),
            'telp': forms.NumberInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

        
class formUserEdit(forms.ModelForm):
    class Meta:
        model = UserAdmin
        fields = [
            'telp',
            'gender',
            'photo',
        ]
        widgets = {
            'gender': forms.Select(
                choices=[
                    ('Laki-laki', 'Laki-laki'),
                    ('Perempuan', 'Perempuan'),
                ],
                attrs={'class': 'form-control'}
            ),
            'telp': forms.NumberInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }



class formPageEdit(forms.ModelForm):
    content = forms.CharField(widget=SummernoteWidget())
    class Meta:
        model = Page
        fields = ['title', 'slug', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Slug'}),
        }


class formPageCreate(forms.ModelForm):
    content = forms.CharField(widget=SummernoteWidget())
    class Meta:
        model = Page
        fields = ['title', 'slug', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title (Bahasa Indonesia)'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Slug'}),
        }

class formArticleCreate(forms.ModelForm):
    content = forms.CharField(widget=SummernoteWidget())
    class Meta:
        model = Article
        fields = ['title', 'created_at', 'slug', 'category', 'topic', 'content', 'featured_image', 'caption_image', 'status', 'is_headline']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan Judul Artikel'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Slug/URL Artikel (Boleh dikosongkan)'}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Kategori Artikel'}),
            'topic': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Pilih Topik Artikel'}),
            'created_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'caption_image': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan Keterangan Gambar (Opsional)'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'is_headline': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class formArticleEdit(forms.ModelForm):
    content = forms.CharField(widget=SummernoteWidget())
    class Meta:
        model = Article
        fields = ['title', 'slug', 'category', 'topic', 'content', 'featured_image', 'caption_image', 'status','created_at', 'is_headline']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan Judul Artikel'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Slug/URL Artikel (Boleh dikosongkan)'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'topic': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'created_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'caption_image': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan Keterangan Gambar (Opsional)'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'is_headline': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }



class formTopicCreate(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukan Judul Topik'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Slug'}),
        }
