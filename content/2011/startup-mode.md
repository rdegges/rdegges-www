---
title: "Startup Mode"
date: "2011-01-06"
tags: ["programming", "telephony", "startups"]
slug: "startup-mode"
description: "STARTUP MODE!  Let's do this shit."
---


![Monster Sketch][]


Yesterday I got some exciting news.  Very exciting.  My company is going to be
doing some massive, explosive expansion over the next 90 days.  How expansive?
Well, we're going to attempt to scale our services 10x across the board.  That
means 10x user count, 10x bug fixing, 10x feature additions, and 1/10th the
time.

We're going to do a sprint.  The most epic sprint I've ever done.  All or
nothing, win or go home.  I'm going into startup mode.


## The Story

I work for a telecommunications company.  We do a wide variety of stuff, one of
our largest services being free to use conference lines.  This project is
especially interesting to me, because it uses many different technologies, and
offers a lot of room for improvement and exciting research.

Our conference lines are pretty popular in the US (and Canada, surprisingly).
So popular, that we run into limits on the services we can offer due to lack of
capacity (we can only get so many phone lines, you know).

In order to continue growing, we signed a contract with an enormous telco to
give us almost unlimited capacity, but at a cost: we must increase our service
usage substantially in the first two months.  So--that's exactly what we're
going to do.


## The Challenge

This challenge is interesting from a technical standpoint.  In order to support
10x as many users, we need to update our infrastructure, and in order to keep
services running smoothly, we need to fix lots of bugs, and add new features
and monitoring tools to our lineup.

Over this next (crazy) month, I'm going to be providing some pretty regular
updates to my blog (you're reading it now), which contain the challenges we're
facing technically, and how we resolve them.  Telephony is pretty interesting
stuff, when you get down to it.


## The Technology

Our tech stack is pretty widely varied right now.  There are a LOT of things
that still need to get implemented and fixed, but here's the tools and tech we
use to operate:

-   [MySQL][]: for all of our current database stuff.
-   [PostgreSQL][]: migrating all our database stuff to it.
-   [Python][]: our programming language of choice.
-   [Django][]: our web framework.  We use it extensively for our public sites,
    internal API calls, and eventually public API calls as well.
-   [RabbitMQ][]: a message passing library used for time-intensive queued
    tasks.
-   [Celery][]: A Python / Django wrapper for using `rabbitmyq` easily.  We use
    this to handle stuff like report generation, accounting, etc.
-   [Puppet][]: a program for automatically configuring (and keeping
    configured) large groups of servers.  It installs all of our software,
    controls configuration files, and generally protects our servers from
    issues.
-   [Monit][]: a centralized monitoring solution that tries to self-heal many
    server problems, as well as report issues to us when necessary.
-   [sentry][]: an awesome Django plugin that provides a Django log viewer.  It
    helps us manage our errors and generate helpful TODO items.
-   [Github][]: for everything.  Fuck everything about my life before Github.
    Seriously.
-   [memcached][]: for caching everything.  Caching is becoming a much more
    important part of our stack.  It was initially totally neglected, but we're
    now revisiting it and making much better use of it.
-   [munin][]: for monitoring our network.  It provides a ton of sexy graphs
    and pictures that help us detect problems and plan for expansion.
-   [Asterisk][]: the core of our conference system is the Asterisk PBX.  We
    use it's dialplan, AGI, and AMI libraries to help us build kick ass
    software.  Over the next month we'll need to do a massive updating of our
    Asterisk code.
-   [OpenSIPS][]: our SIP router.  We're going to use this to load balance, and
    do accounting for all of our call transactions.  We've still got a bit of
    work to do to get this working nicely the way we want it to.
-   [FreeRadius][]: a tricky beast.  Radius is one of those protocols that I
    don't like, and don't really see the point of.  However, we have to use it
    to do proper call accounting, so I'll have to set it up and manage it
    again.  Damn.  It basically acts as a middleman between OpenSIPS and SQL.
-   [JSON][]: our favorite encoding schema :)
-   [Vim][]: need I say more?  Ok, maybe I should.  Vim + pyflakes + rope =
    win.  That is all.
-   [Jenkins][]: our CI server.  We use it to both automatically test all code,
    as well as automatically deploy it.
-   [git-flow][]: our git development model.  We use it extensively for all
    projects.
-   [fabric][]: a python library for automating deployments.  We use fabric to
    script our deployment processes.
-   [gunicorn][]: our WSGI server of choice.  It makes it insanely easy to
    throw up production web servers for our Django projects.
-   [nginx][]: serves all of our static content, and load balances all of our
    web requests.  Love it.

I'm probably forgetting some stuff here (there is a lot that we use on a
day-to-day basis), but that is at least a good portion of it.  At least half of
our tech stack needs significant improvements over the next 90 days, so that's
where all the action will be.


### Updates

As I mentioned before, I'll be updating my blog much more regularly over the
next 90 days, in order to share our insights, and help clarify my own thoughts
:)  And as usual, if you have any recommendations of your own, please
[share them][]!


  [Monster Sketch]: /static/images/2011/monster-sketch.png "Monster Sketch"
  [MySQL]: http://www.mysql.com/ "MySQL"
  [PostgreSQL]: http://www.postgresql.org/ "PostgreSQL"
  [Python]: http://python.org/ "Python"
  [Django]: https://www.djangoproject.com/ "Django"
  [RabbitMQ]: http://www.rabbitmq.com/ "RabbitMQ"
  [Celery]: http://celeryproject.org/ "Celery"
  [Puppet]: https://puppetlabs.com/ "Puppet"
  [Monit]: http://mmonit.com/monit/ "Monit"
  [sentry]: https://getsentry.com/welcome/ "Sentry"
  [Github]: https://github.com/ "Github"
  [memcached]: http://www.memcached.org/ "Memcached"
  [munin]: http://munin-monitoring.org/ "Munin"
  [Asterisk]: http://www.asterisk.org/ "Asterisk"
  [OpenSIPS]: http://www.opensips.org/ "OpenSIPS"
  [FreeRadius]: http://freeradius.org/ "FreeRadius"
  [JSON]: http://json.org/ "JSON"
  [Vim]: http://www.vim.org/ "Vim"
  [Jenkins]: http://jenkins-ci.org/ "Jenkins"
  [git-flow]: http://nvie.com/posts/a-successful-git-branching-model/ "Git Flow"
  [fabric]: http://docs.fabfile.org/en/latest/ "Fabric"
  [gunicorn]: http://gunicorn.org/ "Gunicorn"
  [nginx]: http://www.nginx.org/ "Nginx"
  [share them]: mailto:r@rdegges.com "Randall Degges' Email"
