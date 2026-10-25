---
aliases:
  - /django-and-ssl/
title: "Django and SSL"
date: "2012-05-31"
tags: ["programming", "python", "django"]
slug: "django-and-ssl"
description: "I couldn't find a simple way to force HTTPS in Django, so I wrote django-sslify: add one middleware line and every HTTP request redirects to SSL."
---


![Hooded Figure Sketch][]


**NOTE**: I wrote this article a while back, and its content is dated. Django now has HTTPS redirects built in, so you don't need django-sslify: just set [`SECURE_SSL_REDIRECT = True`](https://docs.djangoproject.com/en/stable/ref/settings/#secure-ssl-redirect) in your settings.

I'm a huge proponent of [encrypting everything][].  Why make it easy for the
government (or other nasty organizations) to snoop on your personal data?  As
such, over the past several months I've been slowly migrating all my Django
sites to SSL.  Along the way, I realized how horrifically underserved the SSL
library market actually is for Django.

A quick search for 'Django + SSL' on google returned nothing useful.  I
couldn't find any libraries or tools that made 'forcing HTTPs' a one liner.
The only useful thing I was able to dig up after a bit of hunting was this
[StackOverflow][] post that contains some custom middleware code that forces
HTTPs redirection.

After a bit of unit testing (and some [PyPI][] action), I published
[django-sslify][]--a simple Django app that forces all SSL across your Django
site.

Setting up `django-sslify` is a piece of cake.  Essentially--all you have to do
is install `django-sslify` (duh!) and then modify your Django `settings.py`
file like so:

```python
# ...

MIDDLEWARE_CLASSES = (
    'sslify.middleware.SSLifyMiddleware',
    # ...
)

# ...
```

Once you've done that, all HTTP requests to your site will be permanently
redirected to their HTTPs equivalents, forcing SSL encryption.

**NOTE**: If you're using [Heroku][] to host your applications (like I am), be
sure to use their new [SSL endpoint][] add-on.  The new SSL endpoint add-on
makes using SSL as easy as possible.


[Hooded Figure Sketch]: hooded-figure-sketch.png "Hooded Figure Sketch"
  [encrypting everything]: https://blog.codinghorror.com/should-all-web-traffic-be-encrypted/ "Encrypt Everything"
  [StackOverflow]: http://stackoverflow.com/questions/8436666/how-to-make-python-on-heroku-https-only "Django + SSL"
  [PyPI]: http://pypi.python.org/pypi "PyPI"
  [django-sslify]: https://github.com/rdegges/django-sslify "django-sslify"
  [Heroku]: http://www.heroku.com/ "Heroku"
  [SSL endpoint]: https://devcenter.heroku.com/articles/ssl-endpoint "SSL Endpoint"