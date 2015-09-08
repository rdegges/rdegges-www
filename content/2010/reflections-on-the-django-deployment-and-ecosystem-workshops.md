---
title: "Reflections on the Django Deployment and Ecosystem Workshops"
date: "2010-12-12"
tags: ["programming", "python", "django"]
slug: "reflections-on-the-django-deployment-and-ecosystem-workshops"
description: "My review of the Django Deployment and Ecosystem workshop.  It was great!"
---


![Dump Truck Sketch][]


Earlier this week, I attended the two day [Revolution Systems][] Django
workshop in Santa Monica, CA.  Day one was the "Django Deployment Workshop",
and day two was the "Django Ecosystem" workshop, both of which were led by
[Jacob Kaplan-Moss][], one of the creators of the Django web framework.

I'm a huge fan of python and Django.  I use them for fun and for work, and
couldn't be happier.  One of the reasons I wanted to attend the RevSys
workshops was to meet Jacob, and also to see how he handles very large
scalability issues (which I'm currently solving at my work).

If you're interested in attending one of these workshops, please keep reading.


## Django Deployment Workshop

This workshop covered all areas of deployment for Django apps.  Some of the
topics covered included:

-   Cloud providers.  In the class Jacob discussed some of the dominant cloud
    server providers that are out there (namely Rackspace and Amazon), and
    compared the benefits and drawbacks of each.
-   Bootstrapping servers with [Chef][] (or [Puppet][]).  If you need to manage
    lots of servers, you will be hard pressed to find a better tool for the job
    than Chef or Puppet.  Both allow you to build simple configuration files
    which keep all of your servers synced.  For example, you can specify which
    packages should be installed on all web servers, which files must be
    present, how to install custom code and software, etc.  With a single
    configuration update, you can make changes to hundreds (or more) servers,
    removing the need for manual systems administration in most cases.
-   Using `pip` to build and distribute your Django sites.  `pip` manages
    project dependencies in a simple way, and can even fetch and build code
    straight from version control systems (git, svn, etc.), which makes it a
    great tool for large companies who may not have the freedom to store code
    on the PyPI mirrors.
-   Sandboxing your python and Django code using `virtualenv`.  `virtualenv`
    lets you build local python environments that your applications can run in,
    ensuring that regardless of OS updates and other worrisome issues, your
    code will still run as it should.
-   Using [fabric][] to build simple deployment scripts, which allow you to
    push the latest version of your code into production, staging, or
    development with a single command.
-   Storing media content across multiple web servers using Django's file store
    backends.
-   Monitoring your networks with [munin][].
-   Monitoring your server processes with [upstart][].
-   Monitoring your logs with [sentry][].
-   Using [celery][] to distribute asynchronous, resource intensive tasks to
    improve site performance.
-   Load balancing web requests to a variable amount of web servers.
-   Using [PostgreSQL][] to efficiently handle lots of database queries.
-   And a lot of other cool stuff.

Overall I was really impressed with this workshop.  The class size was small,
which was awesome.  We got to spend a ton of time with Jacob, and really cover
interesting areas of scaling and deployment which every company should be
using.

Jacob was very thorough, and it was enlightening listen to him talk about the
various technologies and methods that he uses to help scale extremely large
systems.

Regardless of whether you're developing Django apps for fun or work, if you
have a chance to attend the Django Deployment Workshop, do so.  You won't
regret it.


## Django Ecosystem Workshop

The Django Ecosystem Workshop discussed various open source Django apps, why
you should know about them, and how to use them.  I won't go into the details
here (because there were far too many apps covered to remember), but the
workshop provided solutions to pretty much all common site problems in a simple
reusable manner.

This workshop was particularly neat because I hadn't played around with a lot
of the apps discussed, and now have a massive TODO list which includes
implementing a good portion of these apps into my production systems at work.

As with the Django Deployment Workshop, Jacob was very thorough, and helped
with any (and all) questions that everyone had.


## My Thoughts

Both workshops were excellent, and well worth the money.  Jacob did an amazing
job covering some very complex topics, and was careful to answer everyone's
questions and make sure that everyone was on the same page.

Luckily, the class size was small both days, which gave everyone a chance to
get to know each other, and I met some really cool people.  Jacob in particular
is a really awesome guy, and it was a great experience to hang out with him and
get to pick his brain on various topics.

I highly recommend you sign up for the classes when they're available next.  As
long as you're a competent Django developer, you should have no problem
following along with the topics discussed, and you will surely learn a lot as
you go.

A lot of the scalability issues discussed in the workshops are ones I'm
currently solving at my workplace, and so I plan to do some very detailed write
ups on my methods and tools over the coming weeks.


  [Dump Truck Sketch]: /static/images/2010/dump-truck-sketch.png "Dump Truck Sketch"
  [Revolution Systems]: http://www.revsys.com/ "Revolution Systems"
  [Jacob Kaplan-Moss]: http://jacobian.org/ "Jacob Kaplan-Moss"
  [Chef]: http://wiki.opscode.com/display/chef/Home "Chef"
  [Puppet]: https://puppetlabs.com/ "Puppet"
  [fabric]: http://docs.fabfile.org/en/latest/ "fabric"
  [munin]: http://munin-monitoring.org/ "munin"
  [upstart]: http://upstart.ubuntu.com/ "upstart"
  [sentry]: https://getsentry.com/welcome/ "sentry"
  [celery]: http://www.celeryproject.org/ "celery"
  [PostgreSQL]: http://www.postgresql.org/ "PostgreSQL"
