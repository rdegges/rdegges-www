---
title: "Serving Static Content With Django"
date: "2010-07-04"
tags: ["programming", "python", "django"]
slug: "serving-static-content-with-django"
description: "A quick article on serving static content with Django."
---


![Static Sketch][]


**NOTE**: I wrote this article a while back, and it's content is dated. Django
now automatically serves static content by default, so if you're having issues
getting static files working you should consult the [official documentation][].

A question that is frequently asked by new Django programmers is: "How can I
serve static content (CSS, images, Javascript) with the Django's development
server?".  This article is my attempt to answer that question by demonstrating
the best practices way to do so.


## Why Doesn't Django Serve Static Content Automatically?

Well, Django (and python in general) is built around the idea that it is better
to be explicit than implicit.  This concept means that you may need to write
more code in order to do something, but that by doing it that way, you preserve
code clarity and reduce complexity.

This means that Django doesn't force us to put all of static content into a
single, specific folder or tree, we can set it up however we like.  If we want
to serve all static content from a directory called `dontlookhere`, we can
(although I wouldn't recommend it).  It also gives us flexibility as to *where*
our static content resides: we can place it on a remote server, another user
account on our server, or in a directory completely outside of our project.

This flexibility is what Django provides for us at the cost of not being able
to automatically detect / serve our static content-which is why you are reading
this article :)


## Where Should I Put My Static Content?

In general, the convention I like to use is to put all static content in my
project directory underneath the `static` folder.  This means that all of my
new Django projects look something like:

```console
crapola/
|-- __init__.py
|-- manage.py
|-- settings.py
|-- static
|   |-- css
|   |   \-- style.css
|   |-- img
|   |   \-- banner.png
|   \-- js
|       \-- menu.js
\-- urls.py
```

Which allows me to have a good looking URL schema for my projects.  This isn't
a law (you can place it wherever you like), but this convention is followed by
a good amount of developers, and seems like a logical location for static
content.

For the rest of this article, I'll assume that your project is going to serve
all static content from the `static` directory shown in the output above.


## Configure Your Settings

The first thing we need to do is configure our `settings.py` file, to let
Django know where our static content is located.  To do that, open up your
favorite editor and add the following code:

```python
import os

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(SITE_ROOT, 'static')
MEDIA_URL = '/static/'
```

If you're unsure of where exactly to place that code, here's a complete example
of a brand new `settings.py` file for the fake project `crapola`:

```python
# Django settings for crapola project.

import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'u%-*1-3qgv$6#0fz&wgu@p)knta@0hnvzs8x%mbm-1j@_s4qx@'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'crapola.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
)
```

The code we added basically:

-   Creates a new variable, `SITE_ROOT`, which contains the absolute pathname
    of our project directory, then uses that variable to generate the absolute
    pathname of our static content directory.
-   Changes `MEDIA_URL` to reflect the URL location of our static content in
    our actual frontend code (HTML / CSS / JS / etc).  This will be useful
    later when you're writing CSS mockup (it will save you the trouble of
    hardcoding the location of your static content).


## Configure Your URLs

Now that we've got our settings configured, we can move onto the last step,
configuring our `urls.py` file.  In this section, we'll instruct the Django
development server to serve our static content while we are in development mode
only (e.g. when `DEBUG=True` in our `settings.py` file).  This will allow us
the maximum amount of flexibility as we'll be able to automatically serve the
static files during development, but once we go into production let our web
server handle the serving of these files (apache, nginx, lighttpd, etc.).

So, open up your `urls.py` file and add the following to the very bottom:

```python
from crapola.settings import DEBUG
if DEBUG:
    urlpatterns += patterns('', (
        r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': 'static'}
    ))
```

This will import the `DEBUG` variable from our `settings.py` file, and check
its value to see if `DEBUG=True`.  If `DEBUG` is true, then we'll have the
Django development server start serving static content-and if not, then we
won't do anything.

As mentioned above, this will give us maximum flexibility later on.  Once we're
ready to deploy our website in production, we simply set `DEBUG=False` and
*bam*, we'll let our web server handle all the static content serving (it is
much faster that way).


## Conclusion

As you can see, to serve static content is really not very difficult at all.
It's just a matter of configuring a few settings options, and then adding a URL
pattern if needed.


  [Static Sketch]: /static/images/2010/static-sketch.png "Static Sketch"
  [official documentation]: https://docs.djangoproject.com/en/dev/ "Django Documentation"
