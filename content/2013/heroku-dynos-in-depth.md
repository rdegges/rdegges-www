---
title: "Heroku Dynos (in Depth)"
date: "2013-02-10"
tags: ["programming"]
slug: "heroku-dynos-in-depth"
description: "A technical look at Heroku's dynos, and how they work."
---


![T-Rex Sketch][]


**NOTE**: This article is all about [Heroku][].  If you've never heard of them,
you may want to skip this one >:)

So, I'd like to talk about dynos with you (not *dinosaurs*, although, I do love
talking about dinosaurs).  Ok, maybe I'll talk about dinosaurs a little bit,
but mainly about Heroku dynos: containers that run user-defined processes on
Heroku's cloud platform.

Dynos are really the 'core' of Heroku's platform.  Dynos are what run your web
processes, your one-off tasks, etc.  If you're building a Rails website, for
instance, a dyno would run your web process as well as any background tasks
you've defined with rake: cleaning up user sessions, doing stuff every hour,
whatever.  Dynos also run worker processes (stuff like [resque][], etc.).  I'm
sure you get the idea.

So if dynos are just process containers (essentially), why are they cool?
Well, other than the fact that their name reminds me of little dinosaurs (see
picture below), there are a lot of reasons.

![Triceratops Sketch][]

-   Dynos (like the rest of Heroku's platform) run on top of
    [Amazon Web Services][], one of the largest cloud providers in the world.
-   Dynos come with unlimited bandwidth (this can end up costing you a fortune
    with other providers).
-   Dynos run in their own isolated execution environment.  This means no
    shared files, users, etc.  Every time a dyno is created it is identical to
    the rest.
-   Dynos have 512MB of RAM reserved for them, enough to do *almost* anything
    you need to do.  (Looking to render videos and stuff?  Best to do that
    separately.)
-   Dynos can be instantly provisioned or removed, allowing you to easily
    'scale up' your application's infrastructure.
-   Dynos are billed by the second, meaning you can easily handle 'burst'
    traffic and not pay a fortune to do so.
-   You get **750** hours of dyno time free each month, per Heroku application
    (a 30 day month is about 720 hours, for reference).  **PER APPLICATION!**
    This means that if you've got 10 apps running on Heroku, you get 7,500 dyno
    hours free, each month!
-   If a dyno crashes for some reason (maybe the underlying Amazon server
    broke), it will be automatically moved to another server transparently,
    ensuring your application stays running (no maintenance needed!).
-   Web dynos (any dynos powering your website: Rails, Django, Node, whatever)
    have load balancing taken care of out of the box (Heroku's routing mesh
    automatically load balances incoming HTTP requests to however many web dynos
    you have active).

Not bad, right?  In terms of cost alone, Heroku can cut your hosting bill
significantly in the form of free bandwidth and free dyno hours.

The real kicker, however, (at least in my opinion) is the automatic load
balancing Heroku provides.  Heroku's routing mesh is incredibly awesome:

-   It randomly distributes incoming HTTP requests to your application across
    all available dynos.  This means that if you have a single active dyno all
    requests will hit it.  If you have 10 dynos, each of those 10 will get hit
    by incoming requests.  This means you can easily scale your application
    without worrying about the routing logic.
-   It provides you with both HTTP **and** HTTPS load balancing.  Each Heroku
    application automatically supports both HTTP and HTTPS out of the box,
    meaning you can use SSL easily with the domain name your application is
    assigned: `appname.herokuapp.com`.
-   The routing mesh gives your application 30 seconds to respond to incoming
    requests.  If it takes longer the request is killed with a 503.  This is
    GOOD because it forces you to write decent code that takes user experience
    into account.  NOTE: If a request takes longer than 30 seconds to complete,
    while the Heroku routing mesh will return a 503, your application server
    will still continue to process the request--this way, valuable user
    information isn't lost.

And, in case you missed it above, since dynos are automatically maintained by
Heroku's Dyno Manifold, you never have to worry about bad things happening.
Even if your application crashes, an Amazon server crashes, an IT guy trips
over a wire and shuts down 100 of your dynos--you don't need to worry because
Heroku will automatically spin up all your dynos (instantly) on other Amazon
cloud servers.

The Heroku Dyno Manifold's restorative powers, paired with the Heroku Routing
Mesh means you get the best of everything: no maintenance web hosting,
automatic load balancing, and happy users.

As a side note--if you're at all interested in this stuff, you may enjoy my
book: [The Heroku Hacker's Guide][].  I'm currently working on the second
edition, which I promise you'll love >:)


  [T-Rex Sketch]: /static/images/2013/t-rex-sketch.png "T-Rex Sketch"
  [Heroku]: http://www.heroku.com/ "Heroku"
  [resque]: https://github.com/defunkt/resque "resque"
  [Triceratops Sketch]: /static/images/2013/triceratops-sketch.png "Triceratops Sketch"
  [Amazon Web Services]: http://aws.amazon.com/ "Amazon Web Services"
  [The Heroku Hacker's Guide]: http://www.theherokuhackersguide.com/ "The Heroku Hacker's Guide"
