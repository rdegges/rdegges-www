---
title: "Building a Heroku Addon"
date: "2015-04-06"
tags: ["programming", "devops"]
slug: "building-a-heroku-addon"
description: "I'm buiding a Heroku addon, and you'll do it with me!  In this series we'll build a Heroku addon together!"
---


![Retro Robot Sketch][]


I hope it's no surprise to any of you that I'm a big fan of [Heroku][].  If
you're not already familiar with the service, it's probably the most popular,
well designed, oldest, and best all around platform-as-a-service company.

Heroku hosts all sorts of applications (*large and small*), and does so in a
best practices way.

If you want to learn more about Heroku, you might enjoy reading an old post I
wrote on it: [Heroku Isn't for Idiots][], or possibly even check out my book:
[The Heroku Hacker's Guide][].

But...  Enough messing around.  Let's get into this.

In this series we're going to build a full, live, Heroku addon together.  I'll
walk you through each step of the process, I'll show you all the code, and I'll
explain things every step of the way.

If you've ever wanted to build a Heroku addon (*or learn more about how they
work*), this series is for you.

Now, throughout this series I'll be writing my code in Node.js, but the
principles apply regardless of what language you're using.  My goal is to make
this a fun, informative, and practical series that everyone can benefit from.


## A Quick Review of Addons

One of my favorite parts of Heroku is...  Addons!

The core Heroku platform is very simple:

- You put your code into a Git repository.
- You tell Heroku what commands to run to start your project code (*usually your
  web server*).
- You tell Heroku what environment variables to set to store secret information
  (*API keys, etc.*).
- You push your Git repository to Heroku, and they deploy your app and run it on
  as many servers (*dynos*) as you want!

*SIMPLE*, right?

Well, what happens if your project needs access to additional resources to run?
Databases?  Cache servers?  Queueing servers?  Etc?

*ADDONS*!

This is what addons are for: providing additional infrastructure / services for
your application to use.

You can view a list of all available addons here: [addons.heroku.com][]
(*go ahead and look, there are quite a few great ones!*).

Addons are awesome because they allow Heroku developers to:

- Instantly provision infrastructure / additional services.
- Scale these services up and down instantly.
- Pay for services with their Heroku account (*this means addon usage is
  pro-rated to the second*) -- if you spin up a paid addon service for 10
  seconds, you'll pay for exactly 10 seconds worth of usage.

Addons are, in my opinion, the most optimal and efficient way of using and
integrating with infrastructure components.

And the best part?  Anyone can make an addon.

Heroku provides an API for addon providers -- you implement their API spec, and
you can get listed in the addon marketplace.

Which brings us to the next section:


## Let's Build an Addon

Over the past several years, I've actually built and worked on several Heroku
addons.  Some are in the addon marketplace right now!

Building addons is quite simple.  And fun!  So I figured why not build one out
in the open?

Through this series I'll be walking you through the process of building my new
Heroku addon: [Vanity][] (*don't bother checking out the domain, there's nothing
there yet!*).

The idea for this addon is simple: I want to create an addon which counts all my
Heroku request traffic: and that's basically it.  I love vanity metrics, and
there's nothing quite as satisfying (*to me at least*) as seeing how many
requests my application has serviced over a given time period.

Furthermore, I'd like to expose a simple API for developers, so they can
pragmatically access this information as well.


## The Plan

The main plan is to build this addon in a few phases:

- Planning.  The first thing to do (*and what I'll cover in the next article*)
  is to lay out everything that needs to be built.  We'll make some mockups,
  we'll write down exactly what we're going to make, and we'll cover some
  overall planning stuff (*how much will it cost?*), etc.

- Research.  In the second article, I'll get into the research aspect.  In this
  part I'll cover all the documentation / links you need to build an addon, and
  discuss how this thing will work in great detail.

- Implementing the Addon API.  In this article, we'll actually start building
  the addon itself.  The first part to building an addon is being able to
  integrate with Heroku's Addon API -- so that's what we'll do.  By the end of
  this article we'll be able to create, upgrade, and remove Addon instances.

- Implementing the Counting.  In this article, we'll write our core addon logic,
  which stores request counts for each Addon user.

- Implementing a Dashboard.  In this article, we'll actually build a Heroku
  dashboard page for our addon, and learn how to make it accessible via Heroku
  SSO.  This dashboard will let users view their request counts, and get their
  vanity metrics in a nice format.

- Implementing a CLI Plugin.  In this article we'll build a Heroku CLI plugin,
  so developers can access their request count information via the command line!

- Launching.  In this article I'll talk about launching the addon, and how the
  process works.

- Growing.  In this article I'll talk about growing the addon, and scaling it to
  support demand.

- Review.  Finally, I'll cover how the entire process went from start to finish.
  We'll look at *everything*: how the addon is performing, how many users it
  has, how much revenue it's generated (*if any*), etc.

Overall, it should be quite fun.

So...  Stay tuned!  More to come =)

**UPDATE**: The next part of this series is now available!  You can
[find it here][].


  [Retro Robot Sketch]: /static/images/2015/retro-robot-sketch.jpg "Retro Robot Sketch"
  [Heroku]: https://www.heroku.com/ "Heroku"
  [Heroku Isn't for Idiots]: http://www.rdegges.com/heroku-isnt-for-idiots/ "Heroku Isn't for Idiots"
  [The Heroku Hacker's Guide]: http://www.theherokuhackersguide.com/ "The Heroku Hacker's Guide"
  [addons.heroku.com]: https://addons.heroku.com/ "Heroku Addon Marketplace"
  [Vanity]: http://www.vanityaddon.com "Heroku Vanity Addon"
  [find it here]: {filename}/articles/2015/building-a-heroku-addon-planning.md "Building a Heroku Addon - Planning"
