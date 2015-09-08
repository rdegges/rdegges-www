---
title: "The Perfect Django Settings File"
date: "2011-04-29"
tags: ["programming", "python", "django"]
slug: "the-perfect-django-settings-file"
description: "There's only one way to make a perfect Django settings file -- my way >:)"
---


![Turtle Sketch][]


I know this isn't the best way to start an article, but *I lied*.  This article
won't show you how to make the perfect Django settings file.  Instead, it will
show you how to build the perfect Django settings *module*.

When I'm first starting a new Django project, I like to make sure that my
settings file(s) are crafted in an organized, ideal manner.  My settings
file(s) should allow me to:

-   Maintain as many specific deployment environment settings as I choose in a
    clear and separate manner.  For example: *production*, *staging*,
    *development*, etc.
-   Maintain common project settings that are used by all specific deployment
    environments.  For example: maybe *production*, *staging*, and
    *development* all share a common `ADMINS` setting.  I don't want to
    duplicate this code in all of my enviornment specific settings files.
-   Easily test and deploy code to each specific environment.


## Old Habits Die Hard

I'd like to quickly discuss why I think most people design their settings
file(s) wrong.

The approach to settings that I see many people take is simplistic--they'll
define all of their values in their `settings.py` file, and then at the bottom
of the file write something like this:

```python
try:
    from settings_local import *
except ImportError:
    pass
```

What sucks about this approach is that you now need to maintain a file--in this
case, `settings_local.py`, for each of your environments, and it isn't going to
be easy to version control.  Why?  Because you have two choices in this
scenario of fail:

1.  Don't version control the `settings_local.py` files on your various
    servers.  This sucks because now you've got stuff like database credentials
    that will lay around, and gradually break future deployments when you
    forget to update them.  It also sucks because you've got to constantly
    worry about that file.  It isn't part of your source repository, so you
    have to back it up manually, and take special care of it.
2.  Version control the `settings_local.py` files for each environment you
    have, and then manually change the `settings.py` file (or `__init__.py`
    file) in your project folder on each server.  Now you've got the same
    problem as before--you've got to manually manage some source files, and
    constantly worry about breaking shit.

*There is a better way!*


## Write a Settings Module

Instead of maintaining multiple flat settings files, build a settings module.
Go ahead and `rm` your `settings.py` file, and in its place, create a new
directory, called `settings`, and put in a blank `__init__.py` file to start.

The goal here will be to do meet all the criteria that I defined in the
beginning of this article.  In order to meet all those requirements, we need
to:

Define a `common.py` file inside of our settings module.  This file will
contain all of our 'shared' settings between all environments.  For example:

```python
"""Common settings and globals."""


import sys
from os.path import abspath, basename, dirname, join, normpath

from helpers import gen_secret_key


########## PATH CONFIGURATION
# Absolute filesystem path to this Django project directory.
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Site name.
SITE_NAME = basename(DJANGO_ROOT)

# Absolute filesystem path to the top-level project folder.
SITE_ROOT = dirname(DJANGO_ROOT)

# Absolute filesystem path to the secret file which holds this project's
# SECRET_KEY. Will be auto-generated the first time this file is interpreted.
SECRET_FILE = normpath(join(SITE_ROOT, 'deploy', 'SECRET'))

# Add all necessary filesystem paths to our system path so that we can use
# python import statements.
sys.path.append(SITE_ROOT)
sys.path.append(normpath(join(DJANGO_ROOT, 'apps')))
sys.path.append(normpath(join(DJANGO_ROOT, 'libs')))
########## END PATH CONFIGURATION


########## DEBUG CONFIGURATION
# Disable debugging by default.
DEBUG = False
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## MANAGER CONFIGURATION
# Admin and managers for this project. These people receive private site
# alerts.
ADMINS = (
    ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS
########## END MANAGER CONFIGURATION


########## GENERAL CONFIGURATION
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name although not all
# choices may be available on all operating systems. On Unix systems, a value
# of None will cause Django to use the same timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html.
LANGUAGE_CODE = 'en-us'

# The ID, as an integer, of the current site in the django_site database table.
# This is used so that application data can hook into specific site(s) and a
# single database can manage content for multiple sites.
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True
########## END GENERAL CONFIGURATION


########## MEDIA CONFIGURATION
# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = normpath(join(DJANGO_ROOT, 'media'))

# URL that handles the media served from MEDIA_ROOT.
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION


########## STATIC FILE CONFIGURATION
# Absolute path to the directory static files should be collected to. Don't put
# anything in this directory yourself; store your static files in apps' static/
# subdirectories and in STATICFILES_DIRS.
STATIC_ROOT = normpath(join(DJANGO_ROOT, 'static'))

# URL prefix for static files.
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files.
STATICFILES_DIRS = (
    normpath(join(DJANGO_ROOT, 'assets')),
)

# List of finder classes that know how to find static files in various
# locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
########## END STATIC FILE CONFIGURATION


########## TEMPLATE CONFIGURATION
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

# Directories to search when loading templates.
TEMPLATE_DIRS = (
    normpath(join(DJANGO_ROOT, 'templates')),
)
########## END TEMPLATE CONFIGURATION


########## MIDDLEWARE CONFIGURATION
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
########## END MIDDLEWARE CONFIGURATION


########## APP CONFIGURATION
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Admin panel and documentation.
    'django.contrib.admin',
    'django.contrib.admindocs',

    # South migration tool.
    'south',

    # Celery task queue.
    'djcelery',

    # django-sentry log viewer.
    'indexer',
    'paging',
    'sentry',
    'sentry.client',
)
########## END APP CONFIGURATION


########## CELERY CONFIGURATION
import djcelery
djcelery.setup_loader()
########## END CELERY CONFIGURATION


########## URL CONFIGURATION
ROOT_URLCONF = '%s.urls' % SITE_NAME
########## END URL CONFIGURATION


########## KEY CONFIGURATION
# Try to load the SECRET_KEY from our SECRET_FILE. If that fails, then generate
# a random SECRET_KEY and save it into our SECRET_FILE for future loading. If
# everything fails, then just raise an exception.
try:
    SECRET_KEY = open(SECRET_FILE).read().strip()
except IOError:
    try:
        with open(SECRET_FILE, 'w') as f:
            f.write(gen_secret_key(50))
    except IOError:
        raise Exception('Cannot open file `%s` for writing.' % SECRET_FILE)
########## END KEY CONFIGURATION
```

Define as many environment-specific settings files as you need.  Just make sure
to import from `common` at the top of your file.  For example--here's a
`dev.py` file:

```python
"""Development settings and globals."""


from common import *
from os.path import join, normpath


########## DEBUG CONFIGURATION
DEBUG = True
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## EMAIL CONFIGURATION
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': normpath(join(SITE_ROOT, 'db', 'default.db')),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
########## END CACHE CONFIGURATION


########## DJANGO-DEBUG-TOOLBAR CONFIGURATION
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS += (
    'debug_toolbar',
)

# IPs allowed to see django-debug-toolbar output.
INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_CONFIG = {
    # If set to True (default), the debug toolbar will show an intermediate
    # page upon redirect so you can view any debug information prior to
    # redirecting. This page will provide a link to the redirect destination
    # you can follow when ready. If set to False, redirects will proceed as
    # normal.
    'INTERCEPT_REDIRECTS': False,

    # If not set or set to None, the debug_toolbar middleware will use its
    # built-in show_toolbar method for determining whether the toolbar should
    # show or not. The default checks are that DEBUG must be set to True and
    # the IP of the request must be in INTERNAL_IPS. You can provide your own
    # method for displaying the toolbar which contains your custom logic. This
    # method should return True or False.
    'SHOW_TOOLBAR_CALLBACK': None,

    # An array of custom signals that might be in your project, defined as the
    # python path to the signal.
    'EXTRA_SIGNALS': [],

    # If set to True (the default) then code in Django itself won't be shown in
    # SQL stacktraces.
    'HIDE_DJANGO_SQL': True,

    # If set to True (the default) then a template's context will be included
    # with it in the Template debug panel. Turning this off is useful when you
    # have large template contexts, or you have template contexts with lazy
    # datastructures that you don't want to be evaluated.
    'SHOW_TEMPLATE_CONTEXT': True,

    # If set, this will be the tag to which debug_toolbar will attach the debug
    # toolbar. Defaults to 'body'.
    'TAG': 'body',
}
########## END DJANGO-DEBUG-TOOLBAR CONFIGURATION


########## CELERY CONFIGURATION
INSTALLED_APPS += (
    'djkombu',
)

BROKER_BACKEND = 'djkombu.transport.DatabaseTransport'
########## END CELERY CONFIGURATION
```

When you're using any sort of management command, just specify the settings
module you want to use.  For example: instead of running
`python manage.py syncdb`, you would do
`python manage.py syncdb --settings=settings.dev`.  Same goes with `runserver`,
or any other command.

As you can see, the benefits of a settings module are numerous, and meet all of
our requirements.  We're able to have our cake (by version controlling all
environment specific settings) and eat it too (by choosing which one to use
simply via our application server).

I've been working on numerous Django projects for around 2 years now, and I've
not found any better ways to do it.

**UPDATE**: Since writing this article, I've created a really neat generic
Django project that you can use as a project *base*.  It's called
`django-skel`, and you can check it out on the official project
[GitHub Page][].  It contains (among other things) examples of a
production ready settings module.  Take a look!


  [Turtle Sketch]: /static/images/2011/turtle-sketch.png "Turtle Sketch"
  [GitHub Page]: https://github.com/rdegges/django-skel "django-skel on GitHub"
