---
title: "Service Oriented Problems"
date: "2012-10-01"
tags: ["programming"]
slug: "service-oriented-problems"
description: "A look at some of the problems you'll encounter when writing service oriented applications."
---


![Grim Reaper Smoking Sketch][]


In my [last post][], I discussed some of the benefits of writing service
oriented web applications.  In this post, I'd like to discuss some of the
problems commonly encountered when writing service oriented web applications.

For the rest of this article, I'm going to assume you have some basic web
application programming experience.


## Problem 1 - MVP

One of the largest complaints you'll hear about writing service oriented web
applications is that it takes longer to build a working MVP (minimum viable
product).  What this means is that if you're writing your web application from
scratch, and have to launch an initial version as quickly as possible, SOA
(service oriented architecture) probably isn't for you.

The reason this is true is that while service oriented web applications are far
simpler to maintain in the long run (among lots of other benefits), it requires
more upfront development time to get things working.  Let's look at *why*.

Let's say you're building a blogging engine (something like [tumblr][]).  If
you were start building your product as services, you'd start by writing:

-   A `tumblr-accounts` service which provides an API to create, edit, and
    remove user accounts as well as authenticate users.
-   A `tumblr-api` service which provides an API to create, edit, and publish
    a user's blog posts.
-   A `tumblr-www` service which provides a user facing website, and makes use
    of your `tumblr-accounts` and `tumblr-api` services to build its
    functionality.

**NOTE**: For something as large and ambitious as tumblr, you'd likely want to
have more than the three services listed above.  If you are getting started
with SOA, however, always writing an `accounts`, `api`, and `www` service is a
good starting point.

Through the process of writing your `accounts`, `api`, and `www` services
you'll also be faced with another obstacle: defining a clean and clear API
that you'll be using to work with your data.  When you begin writing services,
you can't half-ass anything--you have to make a working API for your `accounts`
project, and a working API for your `api` project--otherwise, nothing else will
work.

Compare this with writing a single monolithic project.  When writing a single
large application you can typically make time saving trade-offs as you're
writing your MVP.  For instance, instead of maintaining separate databases for
your user accounts and your blog posts, you can throw them all on a single
database.  This means you can also use your framework's ORM (object relational
mapper) to create, edit, and delete users and blog posts without having to
worry about writing any sort of APIs.

Over time, as your application grows in features and complexity, having
separate independent services that interact with each other via APIs is going
to be a lot simpler to maintain--but in the short term, it is typically much
quicker to hack together a single monolithic project as opposed to a nicely
modularized service oriented architecture.


## Problem 2 - Authentication Implementation

If you've never written service oriented web applications before, the first
time you give it a try you'll likely bump into a frustrating problem: handling
user authentication properly for your website.

In my experience writing service oriented web applications, this is without a
doubt the single largest implementation issue people bump into.  Let's
*analyze* the problem (and also discuss the solution).

Going back to our tumblr example from the previous section--we have `www`,
`api`, and `accounts` services.  The authentication implementation problem
you'll bump into happens when you start writing your `www` service.

Most web frameworks are built around the idea of creating monolithic web
applications.  Many web frameworks ship with an ORM, whose deep integration
makes handling certain types of problems very simple.  For instance, using many
web frameworks (I'll use [Django][] as an example), you can easily log a user
into their account, allowing them to access certain web pages.

The way this works is that each time a user makes an HTTP request to your site,
Django will perform a database query to ensure the user account exists and is
properly identified.  This ensures that a user is legitimate, and allows you
(the developer) to skip a lot of implementation details dealing with
authentication.

When you move to a service oriented architecture, however, you no longer have
an ORM available to your `www` service.  Instead of performing a database query
every time a user makes an HTTP request to your site, you need to make an HTTP
request to your internal `accounts` service, authenticating the user properly.

Since most web developers never have to worry about this sort of implementation
themselves, this can be a tricky thing to implement.

Solving this problem is typically different for each web framework.  If you're
using Django, for instance, the solution is to subclass the default
authentication back end that ships with Django and override the necessary
methods to perform HTTP requests to your `accounts` service instead of
performing ORM queries.  If you're using [Flask][] (another python web
framework), the solution is to use the wonderful third party application:
[flask-login][].

Regardless of your tool set, this is almost always a problem people bump into.


## Problem 3 - Cost

Another issue people frequently bring up when discussing SOA is cost.
Depending on your application requirements, cost can quickly become a
prohibiting factor.

To truly get the benefits of a service oriented web application, you need each
service to be ran and managed independently of one another.  This means that
you'd run each of your services on separate groups of servers, each with their
own dedicated resources (databases, caching servers, whatever).

If you have a very small application, and don't plan on getting a lot of usage
out of it--writing it in a service oriented fashion may be more work and more
expensive than it's worth.

One way around the cost issue, however, is to deploy your services to a
platform like [Heroku][].  Heroku's platform allows you to deploy your services
live with a generous free tier (a single free web server, free small databases,
caching servers, etc.).  This can be a good option if you'd like to build a
service oriented web application without breaking the bank, as you can easily
scale up when your usage gets higher, and begin paying for higher levels of
service as your application grows.


## Problem 4 - Documentation

Quite possibly the largest SOA issue you'll face if you decide to write service
oriented web applications is that there is very little practical documentation
around.

Many popular web frameworks, tool sets, books and classes only teach the
monolithic model of web application development.  This means that there are
very few guides, and very few helpful resources out there to help you when you
get stuck.

Unfortunately, since writing service oriented web applications is a lot more
difficult to explain (and has varying requirements depending on your specific
use case), many books, guides, and tutorials don't teach it as it adds
unnecessarily complex material and mental models, which may scare off new
developers.

In the future, as SOA continues to become more popular, I'd be surprised if
there weren't more resources available.  I'm guessing that in the next few
years there will be a large amount of books, tutorials, and guides written
covering these topics in more depth.


## Wrap Up

If you've read all the way down to here, you probably have a good understanding
of the challenges you'll face writing service oriented web applications.

Writing services means you need to have more development discipline, maintain a
stricter set of APIs for your services, and generally invest more time upfront
when writing your application.

In my experience, writing service oriented web applications can be an extremely
effective way to build great products.  Not only do you gain tremendous
benefits initially (a stricter set of APIs, redundancy at a service level,
simpler isolated code bases), but as time goes on these benefits become more
and more prevalent (it is easier to maintain your application, you can scale
your application quicker and more precisely, complexity drops substantially).

Regardless of how you write your applications, go hack something!  >:)


  [Grim Reaper Smoking Sketch]: /static/images/2012/grim-reaper-smoking-sketch.png "Grim Reaper Smoking Sketch"
  [last post]: {filename}/articles/2012/service-oriented-side-effects.md "Service Oriented Side Effects"
  [tumblr]: https://www.tumblr.com/ "Tumblr"
  [Django]: https://www.djangoproject.com/ "Django"
  [Flask]: http://flask.pocoo.org/ "Flask"
  [flask-login]: http://packages.python.org/Flask-Login/ "Flask-Login"
  [Heroku]: http://www.heroku.com/ "Heroku"
