---
title: "Building a Heroku Addon - Planning"
date: "2015-04-22"
tags: ["programming", "devops"]
slug: "building-a-heroku-addon-planning"
description: "In this part of the series, we'll lay out our Heroku addon plans, take a look at mockups, and cover high-level functionalities."
---


![Robot with Chaingun Arm Sketch][]


**NOTE**: You're currently reading part 2 of a series I'm writing called
*"Building a Heroku Addon"*.  If you haven't read the
[previous installment][], you'll want to go do that before continuing.

Welcome back!  Glad to see you again.  In this article I'll be sharing my Heroku
addon plans with you.  I'll discuss exactly what I'll be building, what it'll
look like, and how it'll work.

If there's one thing I've come to learn through all of my years hacking on
side projects, it's this: *always have a goal*.


## The Overall Goal

I love looking at overall application metrics.  There's something inherently
appealing to my own sense of vanity about seeing how many users / requests /
etc. my application has served.

These numbers aren't at all business metrics -- they're vanity metrics.

Through speaking with other developer friends, I've come to realize that it's
not *just me* -- lots of other programmers feel the same way!  It's a *rush*
when you see how much usage *your code* is getting -- it's motivating,
inspiring, and more than anything: *fun*!

The purpose of the Vanity addon I'll be creating through this series is to
**provide clear vanity metrics that Heroku developers will enjoy looking at**.

The metrics that Vanity provides should be encouraging, inspirational, and fun.
Developers should *want* to check their Vanity dashboard as they hack on their
projects, and should view it as a source of enjoyment: not dread.


## List of Things to Build

In regards to what needs to be built -- there are several components to
consider.

Firstly, I'll need to build an API service (*api.vanityaddon.com*), which runs on
a Heroku dyno itself, and implements the [Heroku Addon Provider][] API
specification.  This will allow Heroku developers to run commands like:

```console
$ heroku addons:add vanity
$ heroku addons:upgrade vanity <planname>
$ heroku addons:remove vanity
```

I'll need to store Heroku addon users in a database of some sort, and keep track
of their ID and plan information.

Next up, I need to build a marketing site to advertise the addon (*primarily so
developers searching for this thing on Google can find it*).  For this, I'll
build a 100% static site that lives at *www.vanityaddon.com*.  I'll need to
throw something that looks clean and simple together -- as well as generate some
assets (*a logo, a banner, etc.*).

Next, I need to write a Heroku SSO compatible dashboard page.  This is the page
that developers will see if they run the following command:

```console
$ heroku addons:open vanity
```

It should open the user's browser, and immediately show them the Vanity
dashboard having already logged the user in with their Heroku SSO credentials.
This is the primary interface developers will be looking at day-to-day, so it
should be pretty, clean, and intuitive.

Lastly, I need to write a Heroku CLI plugin.  This step is optional (*not
required*), but will give the addon a bit of *zest*.  The CLI plugin should
allow developers to run a simple command like the following:

```console
$ heroku vanity
```

To output their Vanity metrics to the console.

I know that *I* spend most of my time on the terminal, so this is something I'd
want / use.  I love web interfaces too -- but I'm old school -- there's nothing
quite as satisfying as a command line utility >:)


## Functionality Concerns

The high level architecture of the Vanity addon will be fairly simple.

All Vanity needs to do (*when provisioned*) is create a [syslog drain][] to
capture *all* of an application's Heroku logs.  These logs can then be parsed
later to generate various metrics.

Since all of the Vanity metrics are going to be fairly simple (*at least, at
first*), there should be no need for developers to learn any new technologies to
use this addon -- they should simply be able to provision it from the Heroku
marketplace and instantly start enjoying the service.

In regards to what metrics Vanity will need to display -- I think that the most
important things to cover initially will be:

- How many total requests have been served over a given timeframe.
- How many total successful requests have been served over a given timeframe.
- How many total failed requests have been served over a given timeframe.

In the future, as I think about this more, I'm sure there will be other metrics
to consider -- but for now, I think these will suffice.  If you have any good
ideas of what metrics you'd like to see included -- [email me][]!


## Design Mockup

I'm not a great designer (*I'm more of a backend guy*), but I can most
definitely hack together a clean front-end using tools like [Bootstrap][] and
[Bootswatch][].

Here's what I'm thinking the dashboard layout will look like:

![Vanity Dashboard Mockup][]

I think this is suitable for a first release, and as I continue working on this
series I'll fine tune the details.  Again -- if you have any ideas, let me know
via [email][email me].  I love getting input from fellow developers!


## Pricing Thoughts

Running the Vanity addon won't be terribly expensive, but could most definitely
become expensive over time as the addon will be storing *every single log from
every single Heroku dyno using Vanity*.  I can see this adding up to quite a bit
of storage space in a short period of time.

The main cost will likely be storage space on Amazon S3.

Secondary costs will include some sort of database server for processing
metrics.  I've got a bunch of choices for this -- so I'll skip on the guess work
for now and save that for the next article in the series where I discuss
research.

There will also be fees for running syslog servers which ingest all incoming
logs.  I'm not sure how well syslog *"scales"*, or what type of EC2 requirements
it has for my estimated workload, so I won't estimate costs here.

Next up is email fees.  I'll likely be using [mailgun][] to send email as I love
their service, so depending on how many addon users I have, I might end up
spending a few dollars per month on transactional email fees (*not much*).

For addon plans, I'd like to definitely offer a free plan, which would most
likely restrict metrics to the current day only (*this way I can purge old logs
to decrease my storage fees*), and provide several other addon plans that
provide for various levels of metric storage / analysis.


## Next Time

Welp, that's about it for this installment.  Hope you had a good time!

In the next article, I'll be discussing all of my research.  I'll research and
summarize the technical details of what I'll need to do to build this thing,
figure out cost approximations based on tools / usage, and also provide lots of
useful links for anyone else (*like you!*) who wants to build their own Heroku
addon.

So...  Stay tuned!  More to come soon!


  [Robot with Chaingun Arm Sketch]: /static/images/2015/robot-with-chaingun-arm-sketch.jpg "Robot with Chaingun Arm Sketch"
  [previous installment]: {filename}/articles/2015/building-a-heroku-addon.md "Building a Heroku Addon"
  [syslog drain]: https://devcenter.heroku.com/articles/log-drains "Heroku Log Drains"
  [Heroku Addon Provider]: https://devcenter.heroku.com/articles/bootstrapping-add-on-provider "Bootstrapping an Addon Provider"
  [Bootstrap]: http://getbootstrap.com/ "Twitter Bootstrap"
  [Bootswatch]: https://bootswatch.com/ "Bootswatch - Themes for Bootstrap"
  [email me]: mailto:r@rdegges.com "Randall Degges' Email"
  [Vanity Dashboard Mockup]: /static/images/2015/vanity-dashboard-mockup.png "Vanity Dashboard Mockup"
  [mailgun]: http://www.mailgun.com/ "mailgun"
