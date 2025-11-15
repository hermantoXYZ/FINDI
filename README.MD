Deploy Django ke Vercel
=========================


---

## Requirements

Pastikan project django berhasil dijalankan secara lokal sebelum deploy.

* Python 3.10+
* pip
* Git
* Akun Vercel

---

## 2. Struktur Project (Direkomendasikan)

```
project/
│── manage.py
│── requirements.txt
│── vercel.json
│── core/               ← folder utama Django/nama project
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── staticfiles/       ← hasil collectstatic
```

---

## 3. Install Dependensi

Tambahkan package berikut:

```bash
pip install django gunicorn whitenoise
```

Setelah install packge itu, Export list tsb ke requirements, caranya berikut ini;

```bash
pip freeze > requirements.txt
```

---

## 4. Update `settings.py`

### Tambahkan Allowed Hosts:

```python
ALLOWED_HOSTS = ['*']
```

### Konfigurasi static file:

```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

```

tambahkan 
```python
INSTALLED_APPS = [
    'whitenoise.runserver_nostatic', #ini harus di atas django.contrib.staticfiles
]
```

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    ...
]
```

---

## 5. Buat `vercel.json`

File ini memberi tahu Vercel bagaimana menjalankan Django.
- Perhatikan core adalah nama folder project Django.

```json
{
    "builds": [{
      "src": "core/wsgi.py",
      "use": "@vercel/python",
      "config": { "maxLambdaSize": "15mb", "runtime": "python3.11.3" }
    }],
    "routes": [
      {
        "src": "/(.*)",
        "dest": "core/wsgi.py"
      }
    ]
}
```

---

## 6. Edit file `wsgi.py` (sudah ada di Django)

Pastikan isi standar seperti, dengn menambahkan app = application

```python
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()

app = application
```

---

## 📦 7. Collect static sebelum deploy

```bash
python manage.py collectstatic
```


## Selesai!

[WEBSITE DJANGO DEPLOY VERCEL](https://findi-indol.vercel.app/)
---
