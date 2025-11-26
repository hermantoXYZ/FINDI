import os
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
# User.add_to_class("__str__", lambda self: f"{self.username} - {self.first_name}")

# MODEL USER ANGGOTA DAN ADMIN

def rename_photo_anggota(instance, filename):
    ext = filename.split('.')[-1]
    nip_username = instance.id_anggota.username
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    new_filename = f"{nip_username}_{timestamp}.{ext}"
    return os.path.join('img_profile/dsn/', new_filename)

class UserAnggota(models.Model):
    id_anggota = models.OneToOneField(User, on_delete=models.CASCADE, to_field="username", primary_key=True)
    telp = models.CharField(max_length=15, verbose_name="Nomor Telepon")
    gender = models.CharField(max_length=15,choices=[('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan')],)
    alamat = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to=rename_photo_anggota, null=True, blank=True) # Tambahkan null=True, blank=True agar tidak wajib

    class Meta:
        verbose_name_plural = "User Anggota" # Penamaan yang lebih baik di admin

    def __str__(self):
        nama_lengkap = f"{self.id_anggota.first_name} {self.id_anggota.last_name}".strip()
        if not nama_lengkap:
            nama_lengkap = self.id_anggota.username
        return f"{nama_lengkap} ({self.id_anggota.username})"

def rename_photo_admin(instance, filename):
    ext = filename.split('.')[-1]
    admin_username = instance.username.username
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    new_filename = f"{admin_username}_{timestamp}.{ext}"
    return os.path.join('img_profile/admin/', new_filename)


class UserAdmin(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, to_field="username", primary_key=True, verbose_name="Username Admin")
    telp = models.CharField(max_length=15, verbose_name="Nomor Telepon")
    gender = models.CharField(max_length=15, choices=[('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan')],)
    photo = models.ImageField(upload_to=rename_photo_admin, null=True, blank=True) 


    def __str__(self):
        nama_lengkap = f"{self.username.first_name} {self.username.last_name}".strip()
        if not nama_lengkap:
            nama_lengkap = self.username.username
        return f"{nama_lengkap} ({self.username.username})"

# MODEL CATEGORY DAN ARTICLE UNTUK BLOG/NEWS

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
def rename_logo_saham(instance, filename):
    ext = filename.split('.')[-1]
    symbol = instance.symbol
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    new_filename = f"{symbol}_{timestamp}.{ext}"
    return os.path.join('saham/logos/', new_filename)

class Saham(models.Model):
    symbol = models.CharField(max_length=20)
    short_name = models.CharField(max_length=255, null=True, blank=True)
    long_name = models.CharField(max_length=255, null=True, blank=True)
    currency = models.CharField(max_length=10, null=True, blank=True)

    # Profil
    sektor = models.CharField(max_length=100, null=True, blank=True)
    papan_pencatatan = models.CharField(max_length=100, null=True, blank=True)
    logo = models.ImageField(upload_to=rename_logo_saham, null=True, blank=True)
    firt_trade_date = models.BigIntegerField(null=True, blank=True)

    # Harga pasar
    price = models.FloatField(null=True, blank=True)
    change = models.FloatField(null=True, blank=True)
    change_pct = models.FloatField(null=True, blank=True)
    volume = models.BigIntegerField(null=True, blank=True)
    open_price = models.FloatField(null=True, blank=True)
    time = models.DateTimeField(null=True, blank=True)

    # Valuasi
    market_cap = models.BigIntegerField(null=True, blank=True)
    pe = models.FloatField(null=True, blank=True)
    forward_pe = models.FloatField(null=True, blank=True)
    pbv = models.FloatField(null=True, blank=True)

    # Dividend
    div_yield = models.FloatField(null=True, blank=True)
    div_rate = models.FloatField(null=True, blank=True)

    # EPS data
    eps_ttm = models.FloatField(null=True, blank=True)
    eps_forward = models.FloatField(null=True, blank=True)
    eps_year = models.FloatField(null=True, blank=True)
    price_eps_year = models.FloatField(null=True, blank=True)

    # Saham beredar
    shares_outstanding = models.BigIntegerField(null=True, blank=True)

    # Harga harian
    prev_close = models.FloatField(null=True, blank=True)
    day_high = models.FloatField(null=True, blank=True)
    day_low = models.FloatField(null=True, blank=True)

    # Volume rata-rata
    avg_vol_3m = models.BigIntegerField(null=True, blank=True)
    avg_vol_10d = models.BigIntegerField(null=True, blank=True)

    # 52-week range
    week52_high = models.FloatField(null=True, blank=True)
    week52_low = models.FloatField(null=True, blank=True)
    week52_high_change = models.FloatField(null=True, blank=True)
    week52_high_change_pct = models.FloatField(null=True, blank=True)
    week52_low_change = models.FloatField(null=True, blank=True)
    week52_low_change_pct = models.FloatField(null=True, blank=True)

    # Additional
    book_value = models.FloatField(null=True, blank=True)
    confidence = models.CharField(max_length=50, null=True, blank=True)

    # Auto update timestamp
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.symbol} - {self.short_name}"


class Topic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Topics"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

def rename_featured_image(instance, filename):
    ext = filename.split('.')[-1]
    title_slug = slugify(instance.title)
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    new_filename = f"{title_slug}_{timestamp}.{ext}"
    return os.path.join('articles/featured_images/', new_filename)


class Article(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    unique_id = models.CharField(max_length=7, unique=True, editable=False, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles')
    topic = models.ManyToManyField(Topic, blank=True, related_name='articles')
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    featured_image = models.ImageField(upload_to=rename_featured_image, blank=False, null=False)
    caption_image = models.CharField(max_length=255, blank=True, null=True, verbose_name='Keterangan Gambar')
    is_headline = models.BooleanField(default=False, verbose_name='Tampilkan di Headline')
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.unique_id:
            self.unique_id = uuid.uuid4().hex[:7]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Page(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='pages')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
