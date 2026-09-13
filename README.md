# django-jazzmin-addons

## What is this

A Django app that ships template overrides for [django-jazzmin](https://github.com/farridav/django-jazzmin), so admin pages from third-party packages look like the rest of your Jazzmin admin instead of the stock Django admin.

Requires Python 3.10+ and Django 5.2+. This is an alpha release.

## How to install it

```bash
pip install django-jazzmin-addons
```

Add it to `INSTALLED_APPS` **before** `jazzmin`, which itself must come before `django.contrib.admin`:

```python
INSTALLED_APPS = [
    "jazzmin_addons",
    "jazzmin",
    "django.contrib.admin",
    # ...
]
```

Nothing else to configure. Templates are picked up by app order.

## Features

### django-constance

Restyles the [django-constance](https://github.com/jazzband/django-constance) admin page with Jazzmin's layout: one card per fieldset, Bootstrap switches for booleans, Jazzmin breadcrumbs, and a sticky Save button. Collapsible fieldsets and "Reset to default" links keep working.

Install with the extra and add `constance` to `INSTALLED_APPS`:

```bash
pip install "django-jazzmin-addons[django-constance]"
```

```python
INSTALLED_APPS = [
    "jazzmin_addons",
    "jazzmin",
    "django.contrib.admin",
    # ...
    "constance",
]
```

Configure `CONSTANCE_CONFIG` as usual. `CONSTANCE_CONFIG_FIELDSETS` is optional; each fieldset becomes its own card.
