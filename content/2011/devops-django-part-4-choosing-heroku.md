---
title: "DevOps Django - Part 4 - Choosing Heroku"
date: "2011-12-30"
tags: ["programming", "devops", "python", "django"]
slug: "devops-django-part-4-choosing-heroku"
description: "The last part of my DevOps Django series.  In this installment, I discuss why Heroku is a kickass solution to many of Django's deployment problems, and how you can benefit from using it."
---


![Troll Sketch][]


This is the fourth article in a series I'm writing titled *DevOps Django*.  If
you're new, you may want to read the [first part][] of the series before this
one.  In this article I'll be continuing where I left off in the
[previous article][]: explaining why I chose to move my company's
teleconferencing service from [Rackspace][] to [Heroku][].

Making the decision to move my company's infrastructure from Rackspace to
Heroku was no easy task.  As I'm sure you all know--moving infrastructure
components is an enormous risk, even in the best of circumstances.  However,
despite the immense risk involved, a change was needed.


## Time

As I mentioned earlier in this series, I work for a tech startup.  With a small
team of people, you don't have much time to mess around.  Our greatest expense
as a company is engineering time.  Our company's revenue is directly correlated
to our productivity.  The more bugs we fix, features we deliver, and users we
make happy--the more money we make.

Even though we were using the best devops tools available (puppet, nagios,
etc.), we were spending almost all of our engineering time building and
maintaining our infrastructure.  For me, this meant a typical day ended up
looking something like the following:

-   **85%** of my time spent writing or updating puppet modules to fix (or add)
    required functionality to our infrastructure.
-   **10%** of my time spent planning tasks, adding bugs to the tracker,
    updating the TODO list.
-   **5%** of my time doing actual development.

Regardless of the fact that I enjoy writing puppet modules and building a
large, scalable infrastructure--it is disheartening to spend an entire month
working extremely hard, building awesome back end tools, only to have nothing
to show your users for your hard work.  While I'm *extremely* happy and
grateful to have learned so much about deploying robust services, a change was
necessary.

When I sat down and calculated what a typical workday would look like for me if
we moved to Heroku, I immediately knew we needed to make the switch, regardless
of the risk.  Based on my time estimates, a typical day for me (after moving
all our infrastructure to Heroku) would look something like:

-   **10%** of time planning tasks, working on TODO items, etc.
-   **90%** of time hacking on our company projects.

**That is a drastic change.**

Going from **5%** to **90%** of available hacking time per day?  *I'll take
it!*

There's nothing I love more than writing code (excluding my wife and dog).
Building infrastructure tools is fun and all, but in comparison to building new
libraries and features?  No comparison.

With the ridiculous amount of time Heroku would save each day, my company would
be able to ship insane amounts of code.  When I discussed this with
[my boss][], the decision seemed clear: use Heroku.


## Price

After calculating the manpower time Heroku would save, the next thing I wanted
to calculate was the price.  Exactly how much will it cost us to move to
Heroku?

**NOTE**: I received a lot of price related questions when I published the
[last installment][previous article] of this series.  A lot of people emailed
me saying that they'd love to use Heroku, but after looking at their prices,
decided to stick with AWS or Rackspace.  Hopefully this information clears up
any misconceptions.

To start, I'd like to take a moment to explain Heroku's overall pricing scheme.
Understanding how Heroku bills will probably answer a lot of questions.

Heroku's core service is a [dyno][].  A dyno is essentially a long running
program that:

-   Uses up to 512M of RAM (and can burst up to 1.5G if you don't mind swap).
-   Shares CPU with other dynos on the system.
-   Can scale horizontally as much as necessary.

For each application you have on Heroku, you get 1 free dyno per month.  If you
just want to run a small website, you can do it completely free of charge.  For
each additional dyno you run, Heroku charges 35$ per month (5 cents per hour,
at the time of writing).

Based on Heroku's simple pricing rules, you can easily gauge how much running
your application will cost.  What's nice about Heroku's billing is that, like
AWS (which Heroku is built on top of), you pay only for your usage (per hour).
This allows you to instantly scale up (and down) your dynos based on traffic.
If you get a lot of hits every Friday night, you can spin up a few extra dynos
to handle the load, then remove them Saturday morning, only spending a few
dollars in the process.

In regards to Heroku's database pricing, here's what you need to know: every
application you create can use a free shared [PostgreSQL database][].  The
free database you get allows you store **as much data as you want**.  The
catch?  The free database only provides 5M of RAM for your data.  That means
queries will be slow; however--for a majority of sites, a shared database will
suffice.  What's great about the shared database is that, like their paid
counterparts, Heroku manages it for you.  That means no data loss, full access
to your backups, etc.

Heroku's dedicated databases are much more robust than their free counterparts.
In terms of pricing, their cost goes up based on the amount of allowed
connections, RAM, and CPU units.  Currently, the cheapest dedicated database
plan costs 200$ per month, allows 16 concurrent connections, has 1.7G of RAM,
and 1 CPU unit.

What's nice about the dedicated database plans (and what justifies their price,
in my opinion), is that:

-   You get direct [psql][] access.
-   They run PostgreSQL 9.2 (instead of 8.3).
-   **You can instantly create read slaves, and duplicate masters (for staging,
    testing, etc.).**
-   You are billed by the hour (just like dynos).
-   They are fully managed (you'll never lose data, or have to worry about
    downtime).

If you take into account what you get for those database prices, you'll see
that you're getting an insanely good deal.  My favorite feature is Heroku's
concept of forking and following.

Let's say you have a single paid database (with the name
`HEROKU_POSTGRESQL_GREEN`), and you want to create a read slave.  Heroku allows
you to *follow* your existing database (`HEROKU_POSTGRESQL_GREEN`), and in
doing so, automatically provisions your new database as a read slave.  For
instance, to provision a new read slave in the scenario I just described, I
could simply run:

```console
$ heroku addons:add heroku-postgresql:ronin --follow HEROKU_POSTGRESQL_GREEN
```

And I'd have a new read slave up and running in a short period of time.

Similarly to Heroku's `follow` feature is `fork`.  Forking a database gives you
a new database with a snapshot of your existing database's data.  It won't stay
up-to-date with changes (aka: become a read slave).  This is useful for
creating staging environments with real production data in them, testing schema
changes, etc.

Given the amount of work it takes to create new read slaves and databases by
hand (or using tools like puppet and chef), Heroku's method is infinitely
simpler, and more graceful.  Furthermore, in my experience, the process is very
fast.  When I've provisioned read slaves for my applications, they only take as
long to finish building as the amount of data needed to copy over to them.

**OK, let's talk about add-ons.**

Heroku's add-ons are...  Well...  Perfect.  All the add-ons I use in
production: [memcached][], [NewRelic][] (this particular add-on is so amazing
that I'm dedicating an entire section of this series to it), [Redis][], and
[RabbitMQ][] are all excellent.

The add-ons are all very fairly priced (in my opinion), and have free tiers
that allow you to use them at no cost with small amounts of data.  Just as with
Heroku's free tier, a majority of the add-ons' free tiers are sufficient to use
for small websites without paying a dime.  This lets you bootstrap your
projects from the start, and pay for them as they grow.

As with Heroku's dynos, all the add-ons I've used provision instantly.  In
addition to fast provisioning--all add-ons can also be resized; you can
downgrade or upgrade them at any time using the Heroku command line tool.  This
makes scaling your infrastructure components a one liner.


## Hidden Cost

One thing that played an important role in our decision was the hidden cost of
running our infrastructure ourselves.

When you're simply looking at basic price comparisons between services (in our
case, Rackspace vs. Heroku), it's easy to miscalculate cost.  In our case, we
looked at the cost of Rackspace instances vs. the cost of Heroku dynos.

Since Heroku dynos give you 512M of RAM to work with, I based my initial price
comparison on this factor.  A single Heroku dyno costs 35$ per month, and a
512M Rackspace server costs 21.90$ per month.  According to this simplistic
analysis--Heroku looks approximately 1.5x's as expensive.

The hidden costs show themselves in three primary areas:

-   Infrastructure management cost.
-   Scaling cost.
-   Bandwidth.


### Infrastructure Management Cost

Quite possibly the largest hidden cost for us was infrastructure management.

The most obvious manifestation of infrastructure management cost in our company
was engineering time.  As I stated above, it was not uncommon for me to spend
85% of my time (per day!) writing infrastructure related code.  That's an
enormous investment.

The second hidden infrastructure cost is related to building reliable services.
Since my company primarily builds teleconferencing systems, high availability
is a requirement.  It is simply unacceptable for us to have even small periods
of downtime, since we're dealing with real-time conversations.

What this meant in our case was that we needed to have multiple copies of
everything.  One web server?  No good.  One MySQL master server?  No good.  One
load balancer?  No good.  One RabbitMQ server?  No good.  I'm sure you can see
where this is going.

Having multiple backup servers ready to handle outages adds considerable
expense to any infrastructure.  For us, it meant we paid nearly twice as much
as necessary to host our servers so that we could reliably recover from
failures.

In addition to the extra server cost per month, there is also a high overhead
for time required to not only build working backup and fail over programs for
each piece of our infrastructure, but also to build (and test) the recovery
software itself, to ensure that when we do fail over, it actually works.


### Scaling Cost

While not nearly as devious infrastructure management cost--scaling cost is
also infrequently mentioned.

In the teleconferencing business, it is normal to get large amounts of traffic
during certain hours of the day.  Since our business is fairly easy to predict,
dynamically resizing our infrastructure based on actual need can save a lot of
money.

Unfortunately, in order to dynamically resize your infrastructure, you need to
spend an enormous amount of time building tools that can do this.  In my case,
I spent many hours over a period of almost a year writing [fabric][] scripts
that could bootstrap new nodes (new web servers, RabbitMQ servers, etc.) using
the [apache-libcloud][] library.  While both fabric and apache-libcloud make
writing these sorts of scripts easier, it is still a large task to do it right.

Even after writing scripts that make dynamically creating and removing servers
simple--there is still a time factor involved in the actual process.  For
instance--booting a Rackspace server can take anywhere from 60 seconds to 5
minutes.  In addition to that, once the server has been booted, the scripts I
wrote would install the required base software along with puppet (to handle the
node configuration).  Once puppet is installed, it would take another large
block of time (up to 30 minutes for some applications) to fully finish
provisioning the server for usage.  That's a long time.

Having a 35+ minute delay when you need to scale your infrastructure?
Unacceptable.

One of Heroku's greatest strengths is their incredibly simple scaling
procedures.  You can instantly add and remove dynos with a single command.
Furthermore, their scaling seems to be instant.  There is no waiting to
provision new servers, install puppet, etc.--it just works.


### Bandwidth

Depending on what sort of applications you run, bandwidth pricing may be a
concern for you.  In my case, we don't use much bandwidth, so it was never a
considerable cost--but I thought I'd mention this anyhow.

The way Heroku handles bandwidth pricing is that each application you have is
allowed 2TB of bandwidth per month, included in your cost.  Any more than that,
and I'm assuming they'll charge you extra (although I could not find
information on this anywhere on their site).

In comparison to Heroku, Rackspace charges for bandwidth in a per-gigabyte
fashion.  According to the [Rackspace pricing calculator][] I used on their
site, 2TB of bandwidth on Rackspace can cost you an additional $368.64 per
month.  That's a lot in comparison to the 0$ you'd pay for the same amount of
bandwidth using Heroku.


## Summary

After analyzing the costs (both obvious and hidden) of both keeping our setup
the way it was, or switching to Heroku; we decided overwhelmingly to move to
Heroku.

In terms of usefulness, simplicity, elegance, and cost--there is absolutely no
comparison.  For my company, using Heroku was clearly the best choice to make.

Since switching to Heroku, my company has saved lots of money on server costs,
and even more money in engineering time.  Since the switch, we've completed
more features, bug fixes, and have overall accomplished more than at any other
point in the year.  The effect has been tremendous.

In the next part of this series, I'll be discussing how I actually moved my
company's infrastructure from Rackspace to Heroku.  I'll get into the technical
details, and explain the entire setup from start to finish.


**UPDATE**: I wrote a book on Heroku!  If you liked this post, you should check
it out.  It's called **The Heroku Hacker's Guide**, and you can buy it here:
[http://www.theherokuhackersguide.com/][]


  [Troll Sketch]: /static/images/2011/troll-sketch.png "Troll Sketch"
  [first part]: {filename}/articles/2011/devops-django-part-1-goals.md "DevOps Django - Part 1 - Goals"
  [previous article]: {filename}/articles/2011/devops-django-part-3-the-heroku-way.md "DevOps Django - Part 3 - The Heroku Way"
  [Rackspace]: http://www.rackspacecloud.com/3149.html "Rackspace"
  [Heroku]: http://www.heroku.com/ "Heroku"
  [my boss]: http://www.chrisbrunner.com/ "Chris Brunner"
  [dyno]: https://devcenter.heroku.com/articles/dynos "Heroku Dyno Documentation"
  [PostgreSQL database]: https://devcenter.heroku.com/articles/heroku-postgresql "Heroku PostgreSQL Docs"
  [psql]: http://www.postgresql.org/docs/9.2/static/app-psql.html "psql"
  [memcached]: https://addons.heroku.com/memcache "Heroku Memcached Addon"
  [NewRelic]: https://addons.heroku.com/newrelic "Heroku NewRelic Addon"
  [Redis]: https://addons.heroku.com/redistogo "Heroku Redis Addon"
  [RabbitMQ]: https://addons.heroku.com/cloudamqp "Heroku RabbitMQ Addon"
  [fabric]: http://docs.fabfile.org/en/latest/ "python fabric"
  [apache-libcloud]: http://libcloud.apache.org/ "apache libcloud"
  [Rackspace pricing calculator]: http://www.rackspace.com/cloud/servers/pricing/ "Rackspace Pricing Calculator"
  [http://www.theherokuhackersguide.com/]: http://www.theherokuhackersguide.com/ "The Heroku Hacker's Guide"
