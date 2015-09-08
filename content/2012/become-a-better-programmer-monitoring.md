---
title: "Become a Better Programmer - Monitoring"
date: "2012-08-26"
tags: ["programming"]
slug: "become-a-better-programmer-monitoring"
description: "One way to become a better programmer is to increase your usage of application monitoring software.  You'd be surprised how much you'll learn!  My suggestion: use New Relic."
---


![Grim Reaper Gesturing][]


Becoming a better programmer is hard work.  Luckily, there's one foolproof way
to improve your programming skills while simultaneously getting real world
feedback: monitoring.  There are tons of other ways to improve your programming
skills, but I'm only going to touch on one aspect (monitoring) in this post.

*Before I continue, I just wanted to let you know I have absolutely no
affiliation with [New Relic][] (I'm going to be talking about them a lot).*


## Prerequisites

There is really only one prerequisite to using monitoring to improving your
programming skills: you need to write / maintain web software that people
actually use.

Since almost everyone that reads my blog is a web programmer, I figure it's
pretty safe to assume you meet this prerequisites already.

In the off chance you don't write web software, I'll be covering other
strategies in future posts.


## How it Works

Learning is really *really* hard without feedback.

Even if you write software all day every day, while you'll certainly become a
better typist and human compiler--you'll completely miss out on the important
lessons that really affect your programming ability:

-   How to write performant code.
-   How to properly refactor code.
-   How to not break backwards compatibility.
-   How to scale your software to support lots of users optimally.
-   And about a million other lessons: caching, compatibility, handling failure
    properly, etc.

The only way to learn and enhance these skills is to actively (and
pragmatically) evaluate your code as users are using it.  This is the *absolute
best* way to better your programming skills, as you immediately get real world
feedback about your code.


## A Scenario

Let's say you're writing some blog software, and you'd like to know how your
code can be improved.

The first thing you do is write unit tests for your software.  You think "this
will help me flush out the bugs".  So you spend some time writing tests, flush
out a few edge cases, and think your code is absolutely flawless.

Later that night you get an email from a user saying your blogging software is
slow, and errors our constantly.  You feel a bit of a rush: "what could have
gone wrong?"

So now you're looking at your code, trying to figure out what failed.  You spin
up a local instance of the site, do a lot of testing, but don't see any issues.
Bummer.

*This happens way too often.*

The best way to become a better programmer is to monitor your application
(using monitoring software) and use this information as a feedback tool.


## New Relic - Monitoring for Hackers

There are tons of application monitoring solutions out there, but my personal
favorite is [New Relic][New Relic].  Using New Relic to monitor your
applications will undoubtedly make you feel like this dude:

![Oh Stop It You][]

Just to enumerate some of the ways in which New Relic rocks:

-   You can get it running without modifying your application code at all.
-   It gives you a beautiful web interface (see screenshots below) that allows
    you to easily track all of your application metrics:
    -   Application response time.
    -   Errors (404s, 500s, etc.).
    -   Downtime.
    -   Slow transactions.
    -   Throughput.
    -   Requests per minute.
    -   Locations of your users.
    -   Memory usage.
    -   CPU usage.
    -   And a *ton* of other metrics. 

-   They have a free tier (which varies depending on how you run your code, but
    is awesome).
-   They let you create custom dashboards to track special metrics you define.
-   And they're real time.  Yeah.

Here are the obligatory screenshots:

![New Relic Map Screenshot][]

![New Relic Pages Screenshot][]

![New Relic Tasks Screenshot][]

![New Relic Overview Screenshot][]

![New Relic Web Screenshot][]

![New Relic Task Breakdown Screenshot][]

As you can see, the New Relic panel lets you see a ton of data and metrics about
your application, making it really easy to identify issues, slow functions, code
that needs to be refactored, slow infrastructure components, etc.


## Code, Push, Analyze, Repeat

Learning is all about repeating the cycle.

-   You start by writing code (the first release of your blog software, let's
    say).
-   You push your code live, and get users to use it.
-   You look at your New Relic panel, hunting for issues.
-   Can't find any issues? Pick a metric to improve: average application
    response time, page load time, database query count, whatever.  Since you
    have the stats in front of you, challenge yourself--find ways to make things
    faster, simpler, and more elegant.
-   Make some code changes, and the process starts again.

Through this continuous process of tracking your code (and subsequently,
yourself), you'll force yourself to learn new things, practice your skills, and
get scientific feedback along the way.


## Push Yourself

Without real world analysis, you'll only be able to push your skills so far.
If you really want to further your programming skills, you should be actively
monitoring and analyzing your applications--looking for ways to improve them.

Don't be easy on yourself.

Of course--monitoring isn't the only way to better yourself as a programmer--
but it is a great way.  If you're serious about practicing your craft, you
should check out [New Relic][New Relic].

In future posts I'm hoping to write about other methods to becoming a better
programmer.


  [Grim Reaper Gesturing]: /static/images/2012/grim-reaper-gesturing.png "Grim Reaper Gesturing"
  [New Relic]: http://newrelic.com/ "NewRelic - Shit just got real for programmers."
  [Oh Stop It You]: /static/images/2012/oh-stop-it-you.png "Oh Stop It You"
  [New Relic Map Screenshot]: /static/images/2012/newrelic-map-screenshot.png "New Relic Map Screenshot"
  [New Relic Pages Screenshot]: /static/images/2012/newrelic-pages-screenshot.png "New Relic Pages Screenshot"
  [New Relic Tasks Screenshot]: /static/images/2012/newrelic-tasks-screenshot.png "New Relic Tasks Screenshot"
  [New Relic Overview Screenshot]: /static/images/2012/newrelic-overview-screenshot.png "New Relic Overview Screenshot"
  [New Relic Web Screenshot]: /static/images/2012/newrelic-web-screenshot.png "New Relic Web Screenshot"
  [New Relic Task Breakdown Screenshot]: /static/images/2012/newrelic-task-breakdown-screenshot.png "New Relic Task Breakdown Screenshot"
