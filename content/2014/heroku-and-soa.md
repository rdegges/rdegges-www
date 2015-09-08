---
title: "Heroku and SOA"
date: "2014-06-04"
tags: ["programming", "devops"]
slug: "heroku-and-soa"
description: "Heroku's platform was designed with services in mind.  If you're building a service oriented web app, you might find this interesting."
---


![Large Warrior Sketch][]


In the past, I've written a bit about [service oriented architecture][], what's
great about it, what's bad about it, and how I've used it extensively in past
ventures with incredible success.

Today I'd like to dive deeper on this, but cover a parallel topic: why
[Heroku][] is quite possibly the best platform for hosting service oriented
web apps.

If you're not already familiar with [Heroku][], it's an incredibly great
platform as a service company that hosts all your web apps in the simplest,
most best practices way possible.

If you haven't tried it, you might want to go ahead and read their
[quickstart][], or possibly one of my [previous articles][] on the subject to
familiarize yourself with basic Heroku concepts.

**NOTE**: I'm not in any way affiliated with Heroku.  I have some friends who
work there, and I've written a [book][] on the subject, but these thoughts are
completely my own.


## Hosting Web Apps is Expensive

![Sad Girl Sketch][]

Firstly, let's talk about some basics: hosting web apps is incredibly expensive
if you're working on anything with more than a few users.

How so?

Well, modern web apps require a great many infrastructure components to run
successfully.  For almost every app I can think of, some (or all) of the
following components will be necessary:

- Web servers to run your app code.
- Message queue servers to handle messaging inside your app.
- Worker servers to run your worker code, which process asynchronous events.
- Database servers (*in many cases, of different technologies*), to store your
  app's data.
- Cache servers, to cache information which is too slow to repeatedly pull out
  of your database servers.
- File servers, to store files that are frequently accessed (*images, static
  assets, user uploaded media, etc.*).
- Continuous integration servers to test and deploy your code onto these
  servers.
- Configuration management servers to handle synchronization of these other
  infrastructure components across a network.

And these are just the basics!  With all the apps I've built and worked on, I'd
be hard pressed to find one project that *doesn't* utilize the above resources
in one way or another.

If you consider the cost of running all the tools and services above to power
your app, you're looking at a hefty hosting bill (*not to mention
hundreds or thousands of hours of your own time*).


## SOA Can Be More Expensive

![Thief Face Sketch][]

While it is semi-intuitive that running web apps is expensive, not too many
people consider the following: if you're building a service oriented app, you
might very well be doubling or tripling the cost of running your service!

*But why?*

When you build service oriented web apps, you're essentially doing a few things:

- Spending time upfront to architect a distributed app.
- Spending time developing many small API services, which are each responsible
  for a single purpose.
- Deploying each service in an isolated environment.
- Provisioning whatever infrastructure tools your services require (*databases,
  caches, etc.*).

And -- since services are typically deployed independently of one another, you
tend to need more servers running your code than you would if you had a single,
monolithic app (*even if you have a small service, it'll most likely be running
on it's own server*).

Ouch!


## Sidenote: Heroku's Pricing

![Plant Sketch][]

Before continuing, I'd like to quickly discuss Heroku's [pricing][].

On Heroku, you can create any number of "Apps".  Apps on Heroku are essentially
services (single purpose web apps).

Each Heroku App you create gets a single free "Dyno" free each month (*think of a
Dyno as a web server*).

After your free Dyno, you begin paying by the second for Dynos you provision.
So if you run two Dynos for a solid month, you'd only be paying full price for a
single Dyno (roughly $34.50).

Heroku also allows you to provision additional infrastructure services through
their [Addon marketplace][].  The way this works is simple: Heroku has a number
of third party vendors which provide instantly provisioned infrastructure
services and per-second billing.

Let's say you want to add a small [Postgres][] database to your Heroku App.  You
could provision the [heroku-postgresql][] Addon, pick what size you want, and
pay for only the amount of seconds that Addon is active.  Each Addon has its own
pricing, but it's very easy to determine how much each Addon costs.


## Why Heroku's Pricing is Awesome for SOA

![Angry Tiger Sketch][]

Ok, now we're back on topic!  Hopefully you can already see where this is going.

Since Heroku allows you to provision many Apps, and each App gets a free Dyno,
**Heroku is actively encouraging you to build service oriented apps**, whether
you like it *or not*!

Let's say you're building a web app composed of 10 different web services.  If
you deployed each of these 10 services on Heroku, you'd be getting 10 free web
servers (*Dynos*)!  That's a pretty insane free tier.

If you total it up, you'd be saving roughly $345 per month (*the cost of running
10 paid Dynos*).

That's a lot of money saved!

Furthermore -- since each Dyno is capable of handling quite a bit of concurrent
traffic, depending on what each service does, you might be able to get ~1,000
requests per second out of each service you deploy...  **For $0.**

Is there any other provider out there with such an attractive offering for
service oriented web apps?  If there is, I haven't found them.

**NOTE**: When I was building [OpenCNAM][], I was able to get nearly 1,500
requests per second out of each Dyno using a [Python][] / [Flask][] stack.
Needless to say, Heroku has served me very well.


## Heroku and Vendor Lock In

![Jail Sketch][]

One of the other great reasons to use Heroku for service oriented apps is the
lack of vendor lock in.

Heroku's platform is as open as it can be:

- The way your Dynos work is clearly documented.
- You can easily build and tweak the way Heroku deploys and runs your App (check
  out the [buildpack docs][] for more info).  The best part about this is that
  Heroku can run apps written in almost any language imaginable!
- All App configuration is done via environment variables (*which is the best
  way to configure applications regardless*).
- Heroku requires no special setup or code to be inserted into your project
  (*except for a very minimal [Procfile][], which simply tells Heroku what
  command to run to launch your App*).

When I first migrated a large [Django][] service from Rackspace to Heroku, I was
surprised that in only a few minutes I was able to move the entire thing over!

To me, lock in is an incredibly important part of choosing a provider for
service oriented applications, primarily because many services grow in scope and
requirements as time goes on.

For instance, I was working on a small service a while ago that transcoded
video.  When I first launched the service, I ran it on Heroku.  After realizing
that I needed much larger CPUs than what was available, however, I ended up
moving that transcoding service onto a physical machine in a data center.

If I was relying heavily on vendor specific functionality, my move could have
been a nightmare.  Since Heroku has zero vendor lock in, it was painless for me
to move off when I needed to.


## Heroku's Open Source Tooling

![Scythe Sketch][]

Another interesting thing about Heroku is their open source tooling.  Heroku has
hundreds of public repos on their [Github account][], several of which are
incredibly useful when building service oriented apps.

My favorite Heroku tool for SOA developers is [Foreman][].  Foreman is what
Heroku uses internally to run your web apps, but is also an incredibly powerful
development tool.

One of the biggest problems that I've experienced when building service oriented
apps is local development and testing.  It's not exactly an easy task to run
integration tests when you need to have 10 different services all running and
configured in order to make something happen!

This is where Foreman really shines.  Foreman allows you to create a simple
`Procfile` in the root of your each project, which lets you instantly boot up as
many different services as you'd like.

For instance, if I wanted to run several services, I could define a `Procfile`
which looks something like this:

```
myapp: python app.py
service1: python /path/to/some/service.py
service2: python /path/to/some/service.py
service3: python /path/to/some/service.py
service4: python /path/to/some/service.py
service4: python /path/to/some/service.py
```

Then, to run all of these services concurrently, I could simply do:

```console
$ foreman start
```

This would boot up each service concurrently, and assign each service a
sequential port number from 5000 upwards (*you can also manually assign port
numbers, if you prefer*).

Foreman makes it easy to test and develop against complex service oriented
architectures by simplifying the starting and stopping of services.

For more information on Foreman, you should check out this [article][], written
by [David Dollar][] (*an awesome programmer, and the creator of Foreman*).


## Final Thoughts

![Brain Sketch][]

As a huge proponent of service oriented architecture, I find the topic of
deploying and scaling service oriented apps incredibly interesting.

Over the past several years, I've worked on numerous SOA projects hosted in
various places, but I've never had an experience as good as the Heroku
experience.

Heroku's allowed me to single-handedly build an API service that handles
billions of requests, with 0 maintenance work, and almost no downtime, for very
little money.

To say I'm a happy customer would be an understatement.

My hope is that my writing here convinces you to take a look at [Heroku][] the
next time you build a service oriented web app, so that you can feel the same
joy I do.

As always, if you have any questions, please hit me up by [email][] or
[twitter][].

-Randall


  [Large Warrior Sketch]: /static/images/2014/large-warrior-sketch.jpg "Large Warrior Sketch"
  [service oriented architecture]: http://en.wikipedia.org/wiki/Service-oriented_architecture "Service Oriented Architecture"
  [Heroku]: https://www.heroku.com/ "Heroku"
  [quickstart]: https://devcenter.heroku.com/articles/quickstart "Getting Started with Heroku"
  [previous articles]: {filename}/articles/2012/heroku-isnt-for-idiots.md "Heroku Isn't for Idiots"
  [book]: http://www.theherokuhackersguide.com/ "The Heroku Hacker's Guide"
  [Sad Girl Sketch]: /static/images/2014/sad-girl-sketch.jpg "Sad Girl Sketch"
  [Thief Face Sketch]: /static/images/2014/thief-face-sketch.png "Thief Face Sketch"
  [pricing]: https://www.heroku.com/pricing "Heroku Pricing"
  [Plant Sketch]: /static/images/2014/plant-sketch.png "Plant Sketch"
  [addon marketplace]: https://addons.heroku.com/ "Heroku Addons"
  [Postgres]: http://www.postgresql.org/ "PostgreSQL"
  [heroku-postgresql]: https://addons.heroku.com/heroku-postgresql "Heroku Postgres"
  [OpenCNAM]: https://www.opencnam.com/ "OpenCNAM"
  [Python]: https://www.python.org/ "Python"
  [Flask]: http://flask.pocoo.org/ "Flask"
  [Angry Tiger Sketch]: /static/images/2014/angry-tiger-sketch.jpg "Angry Tiger Sketch"
  [buildpack docs]: https://devcenter.heroku.com/articles/buildpacks "Heroku Buildpacks"
  [Procfile]: https://devcenter.heroku.com/articles/procfile "Heroku Procfile"
  [Jail Sketch]: /static/images/2014/jail-sketch.jpg "Jail Sketch"
  [Django]: https://www.djangoproject.com/ "Django"
  [Github account]: https://github.com/heroku "Heroku on Github"
  [Scythe Sketch]: /static/images/2014/scythe-sketch.jpg "Scythe Sketch"
  [Foreman]: https://github.com/ddollar/foreman "Foreman"
  [article]: http://blog.daviddollar.org/2011/05/06/introducing-foreman.html "Introducing Foreman"
  [David Dollar]: http://blog.daviddollar.org/ "David Dollar"
  [email]: mailto:r@rdegges.com "Randall Degges' Email"
  [twitter]: https://twitter.com/rdegges "Randall Degges on Twitter"
  [Brain Sketch]: /static/images/2014/brain-sketch.jpg "Brain Sketch"
