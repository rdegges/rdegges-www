---
title: "DevOps Django - Part 1 - Goals"
date: "2011-12-05"
tags: ["programming", "devops", "python", "django"]
slug: "devops-django-part-1-goals"
description: "The first part of my series discussing Django deployment best practices and devops strategies."
---


![Airplane Sketch][]


A little over a month ago I [published an article][] describing the state of
[Django][] deployment.  If you don't want to read the back story, I'll
summarize it for you here: *deploying Django is hard*.

Surprisingly, my previous article drew quite a bit of attention from the Django
community.  I was fortunate enough to speak with some really brilliant people,
and hear stories from lots of developers who had both good and bad experiences
with deployment.  However, the overwhelming majority of developers I spoke with
all agreed: deploying Django is hard.

Now, a lot of the *deployment problem* (as I've come to refer to it) is not
directly Django's fault, but rather a side effect of working with so many
technologies, services, and libraries.  It is only natural that building
complex and performant software require sufficient deployment and
administration attention in order to work well.

After writing [Deploying Django][], I decided to embark on a personal quest to
find, implement, and write about the best possible deployment strategies
currently around.  Since then, I've been extremely fortunate in that I've found
what I consider to be the best possible deployment strategy for modern Django
projects.

The goal of this article series is to tell my own tale of deploying Django:
what my problems were, what solutions I've found, and what problems still
exist--in hopes that my experiences will help guide other Djangonauts looking
for a *better way*.


## Deployment Goals

To kick start this article, I'd like to explain where I'm coming from: what I
do, what I value, and what my deployment goals are--as these are all crucial to
the story.  Everyone has different needs, and there's a good chance that your
needs (and subsequently, goals) may be vastly different from mine.

I'm the lead developer at a small telecommunications startup in the USA.  My
company builds various telephony services, all of which are free for personal
usage.  For more than a year, I was the sole technical employee, responsible
for:

-   Building our products.
-   Building our architecture.
-   Scaling our services.

**NOTE**: I'm still responsible for all of the above, but we've expanded a bit
so I'm no longer alone =)

As we're a small tech company, our primary concern is productivity.  Our
revenue is directly related to the amount of bugs we fix and features we add,
so it is in our best interest to free up as much engineering time as possible
so that we can focus on adding value to our users' lives.

What this means for my company is that we greatly value devops work.  Any
pieces of our infrastructure that we can automate and scale through code are
infinitely valuable to us, as they free up engineering time in the long run,
giving us more time to make an impact in our product.

In an perfect world, as a developer, I should be able to:

-   Run a single command to deploy my application into production.
-   Run a single command to automatically scale up (or scale down) my
    application.
-   Instantly add services to my infrastructure that my application needs
    ([memcached][], [Redis][], [PostgreSQL][], etc.).
-   Have full access to logs and metrics for all parts of my infrastructure, so
    that I can find problems and fix them based on facts, not assumptions.

Furthermore, *I want my application and all of its related infrastructure
components to just work, and require NO maintenance.*  For instance, if I
provision a Redis server, I want to know that it will always be up and
available, and that I will never need to make changes to it again (other than
scaling it up or down).

I think we can all agree that if the conditions above could be met with minimal
work, life as a developer would be grand.

In the next part of this series, I'll explain my company's product technology
in detail, highlighting the pain points of deployment.


**UPDATE**: I finished part 2 of the series, you can continue reading [here][].


  [Airplane Sketch]: /static/images/2011/airplane-sketch.png "Airplane Sketch"
  [published an article]: {filename}/articles/2011/deploying-django.md "Deploying Django"
  [Django]: https://www.djangoproject.com/ "Django"
  [Deploying Django]: {filename}/articles/2011/deploying-django.md "Deploying Django"
  [memcached]: http://memcached.org/ "memcached"
  [Redis]: http://redis.io/ "Redis"
  [postgresql]: http://www.postgresql.org/ "PostgreSQL"
  [here]: {filename}/articles/2011/devops-django-part-2-the-pain-of-deployment.md "DevOps Django - Part 2 - The Pain of Deployment"
