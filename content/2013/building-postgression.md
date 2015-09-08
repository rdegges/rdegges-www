---
title: "Building postgression (an API Development Story)"
date: "2013-01-29"
tags: ["programming"]
slug: "building-postgression-an-api-development-story"
description: "How I built postgression, the free PostgreSQL database service."
---


![Dragon Sketch][]


[Last week][] my friend [Alven][] and I launched a new service for developers
using PostgreSQL: [postgression][].  postgression is a simple web service that
allows you (a programmer) to instantly provision a free PostgreSQL database
that automatically disappears after 30 minutes.

Why would you use this?  Primarily for testing code: running unit tests,
integration tests, etc.  It's handy because using postgression means you don't
need to configure (or even run) PostgreSQL server locally just so you can run
some tests.

Since launch, postgression has gotten some decent usage.  To date there have
been:

-   1,167 total databases created.
-   229 unique users.

While these aren't huge numbers, we're seeing consistent usage, which means
some developers (whoever you are, thanks!) are using the service to run their
unit tests daily.

I'm not going to talk about why we created postgression in this article (if
you're interested, you can read my [last article][]), but instead, I'd like to
talk about how we built postgression.

Since this was a fun project to build (it's been something I've wanted to make
for a while now), I figured I'd share how we did it, as some of you may
appreciate the technical aspects.  From here on out things are going to get
technical :)


## Tools

To build postgression Alven and I used [Flask][], a popular Python web
framework.  We ended up using the following Python libraries:

-   [Flask-Cache][]
-   [Flask-Script][]
-   [Flask-SQLAlchemy][]
-   [gevent][]
-   [gunicorn][]
-   [psycopg2][]
-   [python-dateutil][]
-   [redis][]
-   [requests][]

To host our project website, we used [GitHub pages][] (it's just a simple
static site).

To host our actual API service, as well as power the entire PostgreSQL database
back end functionality, we used [Heroku][] (the most awesome hosting platform
ever built).

To keep track of our usage statistics and metrics, we used [ducksboard][], a
really awesome company that gives you a dashboard you can customize to your
liking (it displays stuff like Google Analytics, custom metrics, etc.).  Also:
ducksboard was nice enough to give us a free account, as postgression is a free
service.  If you're interested in a sexy dashboard for your company (or
personal projects), you should check them out!


## The Backbone of It All: Heroku

As you can probably imagine (after seeing the tools listed above), Heroku is
really the core of postgression, and is what makes the service possible (and
affordable!).

Heroku is a web application hosting platform, that allows you to easily deploy
your applications (Python, Ruby, Java, Javascript, etc.).  We're using Heroku
several ways to make postgression work.

-   We're using Heroku to run our postgression API
    ([http://api.postgression.com][]).  Heroku runs our Flask application that
    powers the entire thing.  When users make an HTTP request to postgression's
    API, it hits Heroku's servers and stuff happens.
-   We're using [Heroku PostgreSQL][] (the largest hosted PostgreSQL service in
    the world, by the way) to instantly provision PostgreSQL databases for our
    users.
-   We're using [Heroku's API][] to automatically provision and deprovision the
    PostgreSQL databases on Heroku.
-   We're using the [Heroku Scheduler][] to run periodic tasks (like cron).
    Right now this includes: updating our metrics on our ducksboard dashboard,
    deprovisioning databases older than 30 minutes, etc.
-   We're using [Redis To Go][] as our Redis host.  We use Redis for preventing
    abuse of the system by throttling requests based on public IP address.
    Each public IP is allowed to provision no more than 100 databases per hour.

After we wrote the initial code for postgression, deploying the entire thing to
Heroku (including setting up cron, Redis, and PostgreSQL) took only a few
minutes.  Big kudos to the Heroku team for rocking so hard.

And since I know many of you will ask, here's how much it is currently costing
us to run postgression, along with a price breakdown:

-   1 domain name through [DNSimple][] (the best registrar ever) **$14** /
    year.
-   1 web dyno to power the postgression API: **$0** / month.
-   1 Heroku basic database for powering our postgression PostgreSQL database
    (this is what we use to track our databases states): **$9** / month.
-   1 Redis To Go database: **$0** / month.
-   Heroku Scheduler usage (you pay by the minute for extra computing resources
    if you go beyond the free tier): **$0** / month.
-   PostgreSQL backups on AWS powered by Heroku's [pgbackups][] addon: **$0** /
    month.

Total cost for running this service (per month)?  **~11$**


## Flask and APIs

As I mentioned earlier, we wrote the code for postgression in python and Flask.
Why did we choose these technologies?  A few reasons:

-   I'm extremely familiar with python and Flask.
-   Alven had almost no experience with python, so it would be a fun learning
    experience for him.
-   Flask makes writing small web services extremely simple (there's very little
    you have to know to build a functioning service).

For instance, here's the 'core' of our Flask app.  Note how simple this is,
compared to the typically heavy amount of base framework code you'll find other
places.

![postgression Core][]

Our view code is equally straightforward, and our models aren't too bad either
:)

Here's how the API logic works:

1.  A user makes a request to the API (`api.postgression.com`).
2.  We get the user's public IP, and increment their usage count in Redis using
    Flask-Cache.  If the user has gone above the 100 allowed requests per hour
    throttle, we return a HTTP 403 FORBIDDEN code.
3.  We check (using Heroku's API) to see if we have any Heroku apps currently
    provisioned that are not using 100% of their allotted database slots (each
    Heroku app allows you to provision a maximum of 30 PostgreSQL databases).
4.  If there is a Heroku app available, we use Heroku's Addon API
    ([https://api-docs.heroku.com/addons][]) to provision a new Heroku
    PostgreSQL database.
5.  If there is no Heroku app available, we create a new Heroku app using the
    Heroku App API ([https://api-docs.heroku.com/apps][]), then provision a new
    Heroku PostgreSQL database inside the newly created app.
6.  We then check the user's request to see if they want their database
    credentials back as a PostgreSQL connection string, or as a JSON dictionary,
    and return the credentials appropriately.

In the background, we have a cron job running every 10 minutes which
de-provisions any Heroku PostgreSQL databases that were created 30 minutes ago
(or more) using Heroku's API.

Simple, right?  When it all comes together, we get the following behavior
(screenshot below).

![postgression API][]


## Database Layout

As I mentioned above, postgression uses PostgreSQL itself to keep track of all
the Heroku resources it consumes.  This makes it easy for us to keep track of
things like:

-   Usage statistics.
-   How many active Heroku databases we have.
-   Which databases need to be de-provisioned (any database more than 30
    minutes old).
-   How many Heroku applications we currently have (and if they're running at
    capacity or not).

Stuff like that.

To make all that work, we used Flask-SQLAlchemy to define two simple database
models:

-   HerokuApp, which keeps track of all our Heroku applications.
-   HerokuDB, which keeps track of all our Heroku databases, who created them,
    which Herou app they belong to, when they were created, etc.

Here's how they ended up looking:

![postgression Models][]


## Management Commands and Monitoring

In order to automatically send statistics to our shiny new ducksboard dashboard
(pictured below), we used Flask-Script to write some simple management commands
that are ran automatically by the Heroku Scheduler every 10 minutes.

![postgression Ducksboard][]

Writing the cron tasks using Flask-Script is really simple, and makes running
automated tasks a breeze.  Below are a couple of the tasks (screenshot), which
we can run with the `python manage.py blah` command.

![postgression Script][]

Pretty easy, right?


## Building our Website with GitHub Pages

The last thing we did was throw together a simple website using GitHub Pages.
While Alven and I can both throw together a simple website, we figured we'd
roll with the simplest option available.

Essentially what we did was put all our documentation (in Markdown format) into
our project's `README.md`.  Then, using the 'Automatic Page Generator'
(available under your GitHub repository settings), we imported our `README`
file, picked a theme, and published the site.

After it was published, I made some small tweaks, but nothing too big.

The end result?  We got the public website going
([http://www.postgression.com/][postgression]) in about 10 minutes.


## Takeaways

Building postgression has been really fun.  While it's not a complex project by
any means, it's been on my TODO list for a while, and throwing it online has
been an interesting experience.

Both Alven and I are constantly amazed by:

-   How cheap it is to build a fully functional web service on Heroku.
-   How simple it is to deploy code to Heroku, and make updates.
-   How easy it is to build a REST API using Flask.
-   How fast you can throw together a decent looking web page on GitHub.

I'd also like to give one last shout out to all the Heroku guys (and gals).
They've built an amazing service, and allowed me to build an entire
Database-Testing-as-a-Service API on top of their platform for almost no cost.

If you're interested in postgression at all, be sure to give it a go and check
out our website: [http://www.postgression.com/][postgression]

If you'd like to know more about postgression, feel free to leave a comment or
shoot me an email ([r@rdegges.com][]).


  [Dragon Sketch]: /static/images/2013/dragon-sketch.png "Dragon Sketch"
  [Last week]: {filename}/articles/2013/postgression-a-postgresql-database-for-every-test-case.md "Postgression - a PostgreSQL Database for Every Test Case"
  [Alven]: https://twitter.com/zaidos "Alven on Twitter"
  [postgression]: http://www.postgression.com/ "postgression"
  [last article]: http://rdegges.com/postgression-a-postgresql-database-for-every "postgression"
  [Flask]: http://flask.pocoo.org/ "Flask"
  [Flask-Cache]: http://packages.python.org/Flask-Cache/ "Flask-Cache"
  [Flask-Script]: http://flask-script.readthedocs.org/en/latest/ "Flask-Script"
  [Flask-SQLAlchemy]: http://packages.python.org/Flask-SQLAlchemy/ "Flask-SQLAlchemy"
  [gevent]: http://www.gevent.org/ "gevent"
  [gunicorn]: http://gunicorn.org/ "gunicorn"
  [psycopg2]: http://initd.org/psycopg/ "psycopg2"
  [python-dateutil]: http://labix.org/python-dateutil "python-dateutil"
  [redis]: http://redis.io/ "Redis"
  [requests]: http://docs.python-requests.org/en/latest/ "requests"
  [GitHub pages]: http://pages.github.com/ "GitHub Pages"
  [Heroku]: http://www.heroku.com/ "Heroku"
  [ducksboard]: http://ducksboard.com/ "Ducksboard"
  [http://api.postgression.com]: http://api.postgression.com "postgression API"
  [Heroku PostgreSQL]: https://postgres.heroku.com/ "Heroku PostgreSQL"
  [Heroku's API]: https://api-docs.heroku.com/ "Heroku API Docs"
  [Heroku Scheduler]: https://addons.heroku.com/scheduler "Heroku Scheduler Add-on"
  [Redis To Go]: https://addons.heroku.com/redistogo "Redistogo Add-on"
  [DNSimple]: https://dnsimple.com/r/d9a8f0b92dfb78 "DNSimple"
  [pgbackups]: https://devcenter.heroku.com/articles/pgbackups "PGbackups Add-on"
  [postgression Core]: /static/images/2013/postgression-core.png "postgression Core"
  [https://api-docs.heroku.com/addons]: https://api-docs.heroku.com/addons "Heroku Add-on API"
  [https://api-docs.heroku.com/apps]: https://api-docs.heroku.com/apps "Heroku Apps API"
  [postgression API]: /static/images/2013/postgression-api.png "postgression API"
  [postgression Models]: /static/images/2013/postgression-models.png "postgression Models"
  [postgression Ducksboard]: /static/images/2013/postgression-ducksboard.png "postgression Ducksboard"
  [postgression Script]: /static/images/2013/postgression-script.png "postgression Script"
  [r@rdegges.com]: mailto:r@rdegges.com "Randall Degges' Email"
