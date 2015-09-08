---
title: "The Simplest Way to Compress HTML in Django"
date: "2012-03-04"
tags: ["programming", "python", "django"]
slug: "the-simplest-way-to-compress-html-in-django"
description: "This article shows you the simplest way to compress your HTML code with Django."
---


![Electron Sketch][]


**NOTE**: Since writing this post, it has been brought to my attention that as
of 2013, there is a new potential attack vector on sites using gzip.  Please
read this [Django security comment][] for more information after reading this
article.

I've been working on a lot of website optimization stuff recently for my Django
projects, and thought I'd share a cool utility I found for compressing your
entire site's HTML code.

If you're running any site that could benefit from reduced page load times (who
wouldn't want that?) you may want to consider giving this a go.  Essentially,
what we're going to do is take your normal Django template code:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
  </head>
</html>
```

And compress it so that when the page is rendered for users, it looks like
this:

```html
<!doctype html><html lang="en"><head><meta charset="utf-8"/></head></html>
```

Obviously this is a simple example, but when you have pages with lots of
content on them, compressing your pages can lead to a really big page load
performance boost, since you're sending significantly less data to the end
user.

The Django app you'll be using to do this is [django-htmlmin][].  To get
started, you really only need to do two things:

1.  `pip install django-htmlmin`
2.  Add `htmlmin.middleware.HtmlMinifyMiddleware` to your `MIDDLEWARE_CLASSES`
    setting.

By default, `django-htmlmin` will only compress HTML when your `DEBUG` setting
is set to `False` (e.g. when your site is running in production)--this way,
while you're developing and testing your code, you'll still have your HTML
uncompressed so you can look at it in its original form.

Here's a quick snippet from my `settings.py` which shows my
`MIDDLEWARE_CLASSES` (for reference):

```python
MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
```

**NOTE**: If you're concerned about compressing HTML, you should probably also
enable Django's `GZipMiddleware` (as you can see in my snippet above).  GZip
compression will greatly reduce the size of your page's data for transfer to
the end user, further decreasing page load time.

**IMPORTANT**: You should always have both `GZipMiddleware` and
`HtmlMinifyMiddleware` defined before all other middleware classes.  The
ordering of the `MIDDLEWARE_CLASSES` tuple matters in Django, and since both of
these middleware modify HTML after it's already been passed through the other
middleware classes, it is necessary to have them executed last by Django (which
means defining them first in `MIDDLEWARE_CLASSES`).


  [Electron Sketch]: /static/images/2012/electron-sketch.png "Electron Sketch"
  [Django security comment]: https://docs.djangoproject.com/en/1.8/ref/middleware/#module-django.middleware.gzip "Django GZip Middleware"
  [django-htmlmin]: https://github.com/cobrateam/django-htmlmin "django-htmlmin"
