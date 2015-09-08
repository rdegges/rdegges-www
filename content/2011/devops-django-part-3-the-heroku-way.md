---
title: "DevOps Django - Part 3 - The Heroku Way"
date: "2011-12-18"
tags: ["programming", "devops", "python", "django"]
slug: "devops-django-part-3-the-heroku-way"
description: "The third part of my DevOps Django series.  In this article, I discuss Heroku as a best practices solution for deploying Django projects."
---


This article is part of a series I'm writing called *DevOps Django*, which
explains how to best deploy modern Django sites.  If you're new, you should
probably read the [first article][] of the series before this one.

![Deploying Django Meme][]


## My Search for Solutions

In the [previous installment][] of this series, I discussed (in depth) the
problems with deploying Django as a devops guy.  After struggling with
deployment for ~2 years, and finding very little relief in modern devops tools
(puppet, monit, nagios, etc.), I started looking for new solutions.

Several months ago I was reading [Hacker News][] and noticed that [Heroku][]
had recently added Python support to their platform-as-a-service stack.  If
you're not familiar with Heroku, they're a very popular polyglot hosting
platform.  They've been around since 2007 providing Ruby hosting, but over the
past year they've added support for multiple languages, and seem to be kicking
ass and growing like mad.

I've continuously heard their name mentioned by other programmers, but this was
the first I'd heard of them having any Python support, so I bookmarked their
[Django tutorial][] and told myself I'd give it a spin sometime.

Coincidentally, a few weeks later I was asked to give an impromptu lightning
talk during a [pyladies][] hack-a-thon, so I decided to give Heroku a spin,
and do my lightning talk on that.  In a weird twist of fate, the few hours I
spent learning Heroku turned out to be some of the best invested hours of my
life.

During the hack-a-thon I built and deployed a simple Django site (with celery
support) in just under an hour.  If I were to build the same site and attempt
to deploy it on EC2, I'd have easily spent a week getting things deployed using
puppet, monit, nagios, etc.

After the hack-a-thon ended, I decided to play around with Heroku a bit more,
and see what the platform really had to offer other than what I used during my
short sprint.


## A Second Look

Later that week, I had a few hours to kill, so I revisited Heroku's website,
and read through all their [help resources][] and tutorials.  I also took an
in-depth look at their [add-ons][], trying to decide what their services could
be used for: personal projects, business ideas, work projects?

The first thing I was blown away to discover is that Heroku has an enormous
amount of add-ons.  They literally have add-ons for almost any piece of
infrastructure you could ever want: [PostgreSQL][], [Redis][], [cron][],
[memcached][], [RabbitMQ][], [Solr][], etc.  Upon seeing this, I started to
get excited.

Second, I took the opportunity to play around with their extremely easy to
install and use [CLI tool][], and was blown away again.  Heroku's CLI tool
gives you complete control over your Heroku applications.  You're able to
create new Heroku applications out of Git repositories, instantly provision
add-ons for your application (PostgreSQL, Redis, etc.), view streaming log
files, instantly scale up (and down) your nodes, etc.  Furthermore, you're able
to run shell commands locally using their CLI tool.  Need to access the Django
shell?  No problem, you can simply execute `heroku run python manage.py shell`
from your terminal.

*By this point, I was really itching to use Heroku for something serious.*

While I was able to build and deploy a simple Django site on Heroku in under an
hour during the hack-a-thon, I knew that I needed to port a much larger, more
complex site over to Heroku to really see if it could meet my professional
needs.

So, I checked out a fresh copy of the teleconferencing service that I develop
at work, and got to it.


## How I Ported My Work Application to Heroku

If you'd like to see details about what technologies the teleconferencing
service uses, check out the [previous part][previous installment] of this
series.  As the teleconferencing service is large, complex, and infrastructure
heavy--I figured that if I could port it to Heroku then I'd be able to use
Heroku for almost anything.

The first thing I did was create a new Heroku application using their CLI tool:
`heroku create`, then deploy my application to Heroku using Git:
`git push heroku master`.

Secondly, I installed a few add-ons so I could use my required infrastructure
components (RabbitMQ, memcached, PostgreSQL, and cron):

-   `heroku addons:add cloudamqp`
-   `heroku addons:add memcache`
-   `heroku addons:add heroku-postgresql:dev`
-   `heroku addons:add scheduler`

**NOTE**: By leaving off the size of the add-ons at the end, you install the
cheapest (smallest) plan for each service.  By adding these add-ons just as
I've shown above, it adds **0$** per month to your bill.

Next, I modified my production settings file (`project/settings/prod.py`, in my
case), to work with Heroku's hosted RabbitMQ, memcached, and PostgreSQL
services.  In the end, my settings file looked something like this:

```python
"""Production settings and globals."""


from os import environ
from sys import exc_info
from urlparse import urlparse, uses_netloc

from S3 import CallingFormat

from common import *


########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/1.3/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# See: https://docs.djangoproject.com/en/1.3/ref/settings/#email-host
EMAIL_HOST = environ.get('EMAIL_HOST', 'smtp.gmail.com')

# See: https://docs.djangoproject.com/en/1.3/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD', '')

# See: https://docs.djangoproject.com/en/1.3/ref/settings/#email-host-user
EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', 'your_email@example.com')

# See: https://docs.djangoproject.com/en/1.3/ref/settings/#email-port
EMAIL_PORT = environ.get('EMAIL_PORT', 587)

# See: https://docs.djangoproject.com/en/1.3/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

# See: https://docs.djangoproject.com/en/1.3/ref/settings/#email-use-tls
EMAIL_USE_TLS = True

# See: https://docs.djangoproject.com/en/1.3/ref/settings/#server-email
SERVER_EMAIL = EMAIL_HOST_USER
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
# See: http://devcenter.heroku.com/articles/django#postgres_database_config
uses_netloc.append('postgres')
uses_netloc.append('mysql')

try:
    if environ.has_key('DATABASE_URL'):
        url = urlparse(environ['DATABASE_URL'])
        DATABASES['default'] = {
            'NAME': url.path[1:],
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port,
        }
        if url.scheme == 'postgres':
            DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
        if url.scheme == 'mysql':
            DATABASES['default']['ENGINE'] = 'django.db.backends.mysql'
except:
    print "Unexpected error:", exc_info()

#DATABASE_ROUTERS = ('settings.routers.MasterSlaveRouter',)
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/1.3/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'LOCATION': 'localhost:11211',
        'TIMEOUT': 500,
        'BINARY': True,
        'OPTIONS': {
            'tcp_nodelay': True,
            'ketama': True,
        }
    }
}
########## END CACHE CONFIGURATION


########## CELERY CONFIGURATION
# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-transport
BROKER_TRANSPORT = 'amqplib'

# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-url
BROKER_URL = environ.get('CLOUDAMQP_URL', '')

# See: http://docs.celeryproject.org/en/latest/configuration.html#celery-result-backend
CELERY_RESULT_BACKEND = 'amqp'

# See: http://docs.celeryproject.org/en/latest/configuration.html#celery-task-result-expires
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 5
########## END CELERY CONFIGURATION


########## STORAGE CONFIGURATION
# See: http://django-storages.readthedocs.org/en/latest/index.html
INSTALLED_APPS += (
    'storages',
)

# See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN

AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = environ.get('AWS_STORAGE_BUCKET_NAME', '')

STATIC_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME
########## END STORAGE CONFIGURATION


########## WEBSERVER CONFIGURATION
# See: http://gunicorn.org/
INSTALLED_APPS += (
    'gunicorn',
)
########## END WEBSERVER CONFIGURATION


########## SECRET KEY CONFIGURATION
SECRET_KEY = environ.get('SECRET_KEY', '')
########## END SECRET KEY CONFIGURATION
```

As a quick note, every time you push code to Heroku, they automatically read
your top-level `requirements.txt` file, and install any packages you've
defined.  This makes handling site dependencies completely transparent to you
(the developer).  In order to get my site working on Heroku, the only change I
had to make to my requirements file was adding `django-pylibmc-sasl*`, as the
Heroku memcached add-on requires SASL authentication, which the commonly used
`python-memcached` library doesn't provide.

Just for clarity, here's my `requirements.txt` file:

```console
Django==1.3.1
docutils==0.8.1
psycopg2==2.4.2
Fabric==1.3.2
South==0.7.3
gunicorn==0.13.4
newrelic==1.0.5.156
django-celery==2.4.2
django-kombu==0.9.4
django-storages==1.1.3
boto==2.1.1
pylibmc==1.2.2
django-pylibmc-sasl==0.2.4
django-sorting==0.1
django-guardian==1.0.3
django-pagination==1.0.7
pyst2==0.4
django-annoying==0.7.6
django-tastypie==0.9.11
django-coverage==1.2.1
django-nose==0.1.3
nosexcover==1.0.7
django-debug-toolbar==0.8.5
Sphinx==1.1.2
django-cache-machine==0.6
```

As you can see in the settings file, Django is simply using environment
variables to interact with the various infrastructure components we added
earlier.  All of Heroku's add-ons work by exporting one (or more) environment
variables that your application can use.  This makes using Heroku add-ons
extremely convenient.  You can reuse most of your Django settings across all
your projects, since you're storing the important stuff in environment
variables.  No coupling required.

Additionally, the Heroku CLI tool also allows you to set, edit, and remove your
own environment variables.  I used this functionality to set my application's
`SECRET_KEY`, along with other arbitrary stuff (like my [Amazon S3][]
credentials, etc.).  To add these environment variables to my Heroku
application, I simply ran:

```console
$ heroku config:add SECRET_KEY=xxx
$ heroku config:add AWS_ACCESS_KEY_ID=xxx
...
```

The next thing I did was define a top-level file, `Procfile`, which Heroku uses
to specify the different types of *dynos* you'll be running.  Essentially, a
Procfile just lists a series of executable commands that do stuff.  Here's the
Procfile I wrote:

```console
web: python project/manage.py run_gunicorn -b "0.0.0.0:$PORT" -w 3 --log-level info --settings=settings.prod
scheduler: python project/manage.py celeryd -B -E --settings=settings.prod
worker: python project/manage.py celeryd -E --settings=settings.prod
```

Each line contains a reference name, followed by the command you want to run.
In my case, I've got three separate *dyno* types: a Gunicorn instance (this is
my actual Django web application), a celerybeat instance (for scheduling
periodic tasks), and a celery worker instance (for processing asynchronous
tasks).

The way Heroku runs and manages your application is via these *dyno* types.
For instance, let's say I want to have Heroku run three `web` instances (this
is the equivalent of running three separate web servers), I could run:
`heroku scale web=3` from the CLI, and Heroku would instantly ensure that three
of my `web` *dynos* are running--automatically load balancing incoming HTTP
requests across the three.

**NOTE**: You can run `heroku ps` to see what processes (and how many of each) are running.

After defining my `Procfile`, I just ran:

```console
$ heroku scale web=1 scheduler=1 worker=1
```

And Heroku instantly spun up my entire cloud infrastructure.

**INSANE!**

**NOTE**: If you are running celerybeat, be sure to only run it a single time,
and no more.  If you have multiple celerybeat instances running, you'll have
duplicate tasks in your queue.  That's why I specifically created two separate
celery *dyno* types, `scheduler` and `worker`, so that I could safely scale my
worker processes using: `heroku scale worker=x`, while keeping only a single
scheduler.


## A Quick Recap

It took me a total of ~2 hours to:

-   Make a large website and API completely Heroku compatible.
-   Fully provision a PostgreSQL server.
-   Fully provision a memcached server.
-   Fully provision a RabbitMQ server.

And don't forget--this is the amount of time it took me while still learning
about Heroku, and reading through the documentation.  I think it is fair to say
that if there were more tutorials, articles, and information available, this
process could be shortened substantially.

I'll repeat this again: that is *INSANE*.

Compared to the time, effort, and maintenance required to setup my
teleconferencing application normally using a standard devops tool set, this
was a piece of cake.  I didn't have to provision a puppet server, manage a
puppet repository, or anything.

Heroku makes deployment so easy, you don't even need a [fabfile][].


## The Heroku Way

Through the process of learning, using, and eventually moving my company's
entire infrastructure over to Heroku, I learned quite a bit about Heroku's
ideals.

In my [initial article][] discussing the *deployment problem* in the Django
community, I said that I have a dream for the Django community; a dream that
all Django developers can build their websites with peace of mind, knowing a
production deployment is no more than 10 minutes away.

**Heroku is quickly making my dream a reality.**

The *Heroku Way*, as I refer to it now, consists of a few simple principles:

-   Build your Django sites using standard open source tools.
-   Use Git to manage your deployment revisions.
-   Instantly provision, resize, or remove any infrastructure components you
    need.
-   Keep your private data decoupled from your code base via environment
    variables.
-   Instantly scale your infrastructure up and down as you please.
-   Pay by usage.

After having tried numerous deployment methods myself, and after using Heroku,
I strongly believe that Heroku's approach to solving the *deployment problem*
is the right way.  As a developer, using Heroku is a big win:

-   You can deploy both small and large sites the same way (and scale them as
    large as you'd like with no added complexity).
-   It's cost effective (Heroku's prices aren't much more expensive than
    Amazon's, which Heroku is built on top of).  I'll go into more depth on
    this in my next article.
-   You aren't locked into anything: the same code base you use to develop your
    site locally can be used on Heroku in a matter of minutes.

Deploying code to Heroku *feels right*.  As a developer, you shouldn't have to
spend 90% of your time writing puppet rules and working with vendor APIs to
provision servers.  You shouldn't need two weeks to scale your site when you
get an influx of users.

Instead, you should be coding--which is precisely what Heroku is designed to
help you do.

In the next part of this series, I'll be detailing my decision to move from
Rackspace to Heroku.  Making an infrastructure move is a big decision.  In the
next article I'll discuss my reasoning with you.


**UPDATE**: I've finished the next part of the series!  You can read it
[here][].

**UPDATE**: I also published a book on Heroku!  If you'd like to check it out,
you can do so here: [http://www.theherokuhackersguide.com/][].


  [first article]: {filename}/articles/2011/devops-django-part-1-goals.md "DevOps Django - Part 1 - Goals"
  [Deploying Django Meme]: /static/images/2011/deploying-django-meme.png "Deploying Django Meme"
  [previous installment]: {filename}/articles/2011/devops-django-part-2-the-pain-of-deployment.md "DevOps Django - Part 2 - The Pain of Deployment"
  [Hacker News]: http://news.ycombinator.com/ "Hacker News"
  [Heroku]: http://www.heroku.com/ "Heroku"
  [Django tutorial]: https://devcenter.heroku.com/articles/django "Heroku Django Tutorial"
  [pyladies]: http://www.pyladies.com/ "Python Ladies"
  [help resources]: https://devcenter.heroku.com/ "Heroku DevCenter"
  [add-ons]: https://addons.heroku.com/ "Heroku Addons"
  [PostgreSQL]: https://addons.heroku.com/heroku-postgresql "Heroku PostgreSQL Addon"
  [Redis]: https://addons.heroku.com/redistogo "Heroku Redis Addon"
  [cron]: https://addons.heroku.com/scheduler "Heroku Scheduler Addon"
  [memcached]: https://addons.heroku.com/memcache "Heroku Memcached Addon"
  [RabbitMQ]: https://addons.heroku.com/cloudamqp "Heroku RabbitMQ Addon"
  [Solr]: https://addons.heroku.com/websolr "Heroku Solr Addon"
  [CLI tool]: https://toolbelt.heroku.com/ "Heroku CLI Tool"
  [Amazon S3]: http://aws.amazon.com/s3/ "Amazon S3"
  [fabfile]: http://docs.fabfile.org/en/latest/ "Python Fabric"
  [initial article]: {filename}/articles/2011/deploying-django.md "Deploying Django"
  [here]: {filename}/articles/2011/devops-django-part-4-choosing-heroku.md "DevOps Django - Part 4 - Choosing Heroku"
  [http://www.theherokuhackersguide.com/]: http://www.theherokuhackersguide.com/
  [r@rdegges.com]: mailto:r@rdegges.com "Randall Degges' Email"
