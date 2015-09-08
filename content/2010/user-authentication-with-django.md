---
title: "User Authentication With Django"
date: "2010-02-17"
tags: ["programming", "python", "django"]
slug: "user-authentication-with-django"
description: "A quick guide to successfully using Django's authentication module."
---


![Lock Sketch][]


This article will teach you how to authenticate users with [Django][] in a
simple, quick, and secure manner.  You'll also learn how to require
authentication on certain pages of your website, and how to gracefully handle
login and logout functionality.

The target audience is people who have had minimal experience with Django, and
are aware of how Django works in a basic manner.


## What are We Building?

To demonstrate how user authentication works, we'll be building an extremely
minimalistic website and user portal.  We'll create a home page that directs
users to the web portal (which is for authenticated users only).  We'll create
a login page, a logout page, and a basic web portal home page.

The goal of this article is not to teach you web design, or how to make
websites, but merely to show you how simple user authentication can be with
Django.


## What's Needed?

Django 1.0 or later.


## Create a New Project

Before we get started, create a new Django project.  For the rest of this
article, we'll be building a website for the fictitious company 'Django
Consultants'.

```console
rdegges@cora:~/code$ django-admin.py startproject django_consultants
rdegges@cora:~/code$ ls django_consultants/
__init__.py  manage.py  settings.py  urls.py
rdegges@cora:~/code$ cd django_consultants/
rdegges@cora:~/code/django_consultants$
rdegges@cora:~/code/django_consultants$ python manage.py syncdbCreating table auth_permission
Creating table auth_group
Creating table auth_user
Creating table auth_message
Creating table django_content_type
Creating table django_session
Creating table django_site

You just installed Django's auth system, which means you don't have any superusers defined.
Would you like to create one now? (yes/no): yes
Username (Leave blank to use 'rdegges'):
E-mail address: r@rdegges.com
Password:
Password (again):
Superuser created successfully.
Installing index for auth.Permission model
Installing index for auth.Message model
rdegges@cora:~/code/django_consultants$
```

Be sure to create a user account when you run the `python manage.py syncdb`
command, as you'll need that later to test your login.


## Determine URLs

There are many ways to design a website, but I prefer to build the URL schema
first, then build the site to match the URL schema.  So let's decide on what
URLs we will need now.  If you are going to build a real website and not just
this simple example, feel free to add whatever else you need.

-   `/` Show the company logo and direct users to a login portal.
-   `/login/` Allow users to login.

This should be sufficient for what we are doing.


## Configure Django Settings

Below is my `settings.py` for the project.  Make changes where necessary.

```python
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Randall Degges', 'r@rdegges.com'),
)
MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'django_consultants.db'
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(SITE_ROOT, 'static')
MEDIA_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/media/'

# URL of the login page.
LOGIN_URL = '/login/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'somerandomnumbers'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'django_consultants.urls'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'portal',
)
```

Take note of the `LOGIN_URL` setting.  This needs to be changed to whatever URL
your login view will be at. For us, this should be `/login/`, as that is the
URL we decided will supply users with a login page.

Everything else is pretty standard, nothing special going on.


## Write Our `urls.py`

Now let's write our main `urls.py` file which will control what content is
served based on our URL schema.

```python
from django_consultants.views import *
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', main_page),

    # Login / logout.
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', logout_page),

    # Web portal.
    (r'^portal/', include('portal.urls')),

    # Serve static content.
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'static'}),
)
```

There are two things to notice here.  First off, the login view
`(r'^login/$', 'django.contrib.auth.views.login')` is defined as using
`django.contrib.auth.views.login`, which is a pre-defined view for logging in
users.  We won't need to make any changes to this, as it does all of the Django
magic to securely authenticate users.

Next, you'll notice that the view for our web portal will be part of a separate
application `(r'^portal/', include('portal.urls'))`.  You don't have to do it
this way, but breaking your website up into independent applications is useful
for keeping logic separated.  For example, a login and logout are useful to
have as part of your main site (e.g. not in an application) because you may
have multiple parts of your website that perform different actions but that all
require authentication for users to access.  In our case, one of these
applications will be a user portal, so we'll be making it into a separate
application.


## Writing the Views

Now that we've defined the URLs for our site, let's go ahead and write the
views that our main site will use.  Here's the `views.py`:

```python
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

def main_page(request):
    return render_to_response('index.html')

def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')
```

Since the login page already has a view defined (thanks to
`django.contrib.auth`), we only need to define our main page (which will tell
users to go to the portal) and a logout page that allows users to logout
anywhere on the website.

The `main_page` view is pretty simple, it just renders an `index.html` template
(don't worry, we'll write all of the templates later).

The `logout_page` view calls the logout function on the request object.  This
magically logs users out and kills their sessions.  After logging them out, we
then direct them back to the main page of the website.  You can always spice
this up (by adding a custom log out page or something), but for simplicity's
sake, we will just send them back home.


## Create the Portal Application

Now let's create our web portal application.  We'll call it portal and it will
be used to display the portal homepage and other portal functionality (if you
choose to add it):

```console
rdegges@cora:~/code/django_consultants$ django-admin.py startapp portal
rdegges@cora:~/code/django_consultants$ ls portal/
__init__.py  models.py  tests.py  views.py
rdegges@cora:~/code/django_consultants$ cd portal/
rdegges@cora:~/code/django_consultants/portal$
```


## Determine the Portal URLs

Again, let's quick write up a URL schema for our portal application.  If you
are designing an actual website, you'll want to add more functionality.  For
now, all we will do is create a single page (that will be accessed via
`/portal/`) which gives users some basic options.

-   `/` Main page.  Will display the login portal and give users a menu of options.


## Write the Portal `urls.py`

Now that we've come up with a schema for our portal application, let's
implement it and write the `urls.py`:

```python
from django.conf.urls.defaults import *
from portal.views import *

urlpatterns = patterns('',

    # Main web portal entrance.
    (r'^$', portal_main_page),

)
```

Nothing complicated here, moving on.


## Write the Portal Views

Now let's write our portal views:

```python
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

@login_required
def portal_main_page(request):
    """
    If users are authenticated, direct them to the main page. Otherwise, take
    them to the login page.
    """
    return render_to_response('portal/index.html')
```

This is where things get interesting.  Since we decided a while back that our
`/portal/` page was going to require users to be authenticated, we are going
to import the `login_required` function from `django.contrib.auth`.  This
decorator allows us to specify which views require users to be authenticated to
use!  All we need to do is place `@login_required` above each view definition
that we have which requires user authentication, and *bam*.  Everything
magically works!

If you were to visit `/portal/` without being logged in, the `login_required`
function would see that you are not authenticated, and would read the variable
value in your settings.py file called `LOGIN_URL` which currently contains
`/login/`, and would then direct you to the login page.  Pretty awesome right?
Full user authentication in only 1 line of code!


## Creating the Templates

Now that we've done all the hard work, let's go ahead and write our templates.

To start, let's create all of the necessary directories and files:

```console
rdegges@cora:~/code/django_consultants$ mkdir -p templates/{registration,portal}
rdegges@cora:~/code/django_consultants$ touch templates/base.html templates/index.html
rdegges@cora:~/code/django_consultants$ touch templates/portal/portal.html templates/portal/index.html templates/portal/menu.html templates/portal/footer.html templates/portal/header.html
rdegges@cora:~/code/django_consultants$ touch templates/registration/login.html
```

Next, let's define a generic template (`base.html`) for our main pages to use
as a generic template.  Since I like to do things fancy, we might as well make
it HTML 5 :)

```django
<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
    {% block head %}{% endblock %}
  </head>
  <body>
    {% block body %}{% endblock %}
  </body>
</html>
```

Now that we have a base template, let's create the main page of the website
(`index.html`) as our `main_page` view renders:

```django
{% extends "base.html" %}
{% comment %}
  Main page of django_consultant's website.
{% endcomment %}

{% block head %}
  <title>Django Consultants</title>
{% endblock %}

{% block body %}
  <header>
      <h1>Django Consultants</h1>
  </header>

  <section>
      <p>Welcome to Django Consultants. Please click <a href="/portal/">here</a> to log into our web portal.</p>
  </section>
{% endblock %}
```

At this point, we've got the basic templates done for the main page of our
website.  Mind you, they are very basic.  The next thing we need to do is
create a template for our user portal page.  So let's do that:

```django
{% extends "base.html" %}
{% comment %}
  This is the main template for all portal pages.
{% endcomment %}

{% block head %}
  <title>Django Consultants | {% block title %}{% endblock %}</title>
{% endblock %}

{% block body %}
  <header>
    <h1>Django Consultants | Web Portal</h1>
  </header>

  <section>
    <ul>
      <li><a href="/">home</a></li>
      <li><a href="/logout/">logout</a></li>
    </ul>
  </section>

  {% block content %}{% endblock %}

  <footer>
    <span>&copy; 2010, Django Consultants</span>
  </footer>
{% endblock %}
```

This is a generic template which will be used for all portal pages.  As you can
see, there isn't much functionality except to return to the main page and
logout.  If you are developing an actual portal, you'll obviously want to add
lots more features!  Now we'll create the actual portal home page:

```django
{% extends "portal/portal.html" %}
{% comment %}
  Main page of the portal.
{% endcomment %}

{% block title %}
  Portal
{% endblock %}

{% block content %}
  <section>
    <h2>Welcome, {{ user.username }}</h2>
    <p>This is the main page of the web portal.</p>
  </section>
{% endblock %}
```

This page is special in that it uses the `{{ "user.username" }}` variable to
print the user name of the logged in user.  The Django authentication system
passes the user object to each template that requires authentication (using the
`login_required` decorator), that we can use to fetch information on the user.
In this case, we are going to display a simple welcome message.

The last thing we need to do is create a template for our login page (remember
that it uses the magical view that we didn't have to write?)  Here it is:

```django
{% extends "base.html" %}
{% comment %}
  Main page to authenticate users.
{% endcomment %}

{% block head %}
  <title>Django Consultants | Login</title>
{% endblock %}

{% block body %}
  <header>
    <h1>Django Consultants</h1>
    <h2>Login Page</h2>
  </header>

  <section>
    {% if form.errors %}
      <p>Your username and password didn't match, please try again.</p>
    {% endif %}

    <form method="post" action=".">
      {% csrf_token %}
      <p>
        <label for="id_username">Username:</label>
        {{ form.username }}
      </p>
      <p>
        <label for="id_password">Password:</label>
        {{ form.password }}
      </p>
      {% if next %}
        <input type="hidden" name="next" value="{{ next }}" />
      {% else %}
        <input type="hidden" name="next" value="/portal/" />
      {% endif %}
      <input type="submit" value="login" />
    </form>
  </section>
{% endblock %}
```

Now, as you can see, we create a form which performs a `POST` to itself.  This
lets the Django login view do its magic.  The interesting thing here are the
hidden fields and how they are processed:

```django
{% if next %}
  <input type="hidden" name="next" value="{{ next }}" />
{% else %}
  <input type="hidden" name="next" value="/portal/" />
{% endif %}
```

The hidden field next is special to the login view.  It determines where the
user is re-directed to after logging in.  Let's say, for example, that a user
visits our homepage, and clicks the link there that directs them to `/portal/`.
Since `/portal/` requires authentication, it will direct the user to the URL
`/login/?next=/portal/`.  This GET argument is sent automatically by the
`login_required` decorator to help inform the login page of where to direct the
user after they've logged in.

Our code above says "If the user requests a page, and they are not
authenticated-then direct them to the login page, and after they've logged in
send them back to the page they originally requested.  If the user simply
visited the `/login/` page directly, then by default send them to `/portal/`
once they've logged in."

This is the correct way to handle login and redirection in complex websites as
it gives users the maximum amount of flexibility.  Don't you just hate it when
you try to visit a website and get into an important protected section, only to
discover that after you've logged in you are redirected to the main page
instead of the page you were trying to get to?  You won't have that problem
using Django's authentication as long as you implement the login template as we
did above.


## Test It Out

We're done.  So give everything a test.  Go to your `django_consultants`
directory and run the command `python manage.py runserver` to start up the
development web server.  Then open a browser and visit
`http://localhost:8000/`.

You should be greeted by the main page, and provided with a link to log into
the web portal.  So click the portal link, and since you are not authenticated,
you will be directed to the login page.

Now log in using the `username` and `password` you generated when you ran
`python manage.py syncdb` and you'll see the portal home page!  Feel free to
play around with logout / login / etc.


## Where to Go From Here

For more information and advanced usage of Django authentication, check out the
[official documentation][].  The best way to learn is to play around with
things, test them out, and get a good feel for how everything works.


## Conclusion

Hopefully this article has helped you understand how Django authentication
works, and how easy it is to add secure authentication to your website without
going through too much trouble.  If you have any questions, suggestions, or
anything else, feel free to [shoot me an email][], and I'll try to get back as
quick as I can.


  [Lock Sketch]: /static/images/2010/lock-sketch.png "Lock Sketch"
  [Django]: http://www.djangoproject.com/ "Django"
  [official documentation]: http://docs.djangoproject.com/en/dev/topics/auth/ "Django Authentication Documentation"
  [shoot me an email]: mailto:r@rdegges.com "Randall Degges' Email"
