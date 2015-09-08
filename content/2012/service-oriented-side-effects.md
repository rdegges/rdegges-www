---
title: "Service Oriented Side Effects"
date: "2012-09-28"
tags: ["programming"]
slug: "service-oriented-side-effects"
description: "A quick look at some of the side effects you'll encounter when writing service oriented applications.  Many of them are positive."
---


![Robot Warrior Sketch][]


There are two primary ways to write web applications these days:

-   By building a single, monolithic web application (where all your code is in
    a single project and runs on a single domain).
-   By building lots of small independent web services, each one with their own
    codebase and URL endpoint.  (This methodology is known as
    [Service Oriented Architecture][].)

There are benefits and drawbacks to each approach.

What this article is about, however, are the side effects of writing your
applications as web services as opposed to monolithic web applications.  This
article assumes you have some basic knowledge of writing web applications.

To get started, lets discuss the basics: the monolithic pattern and the service
pattern.


## The Monolithic Pattern

If I had to guess, I'd say that close to 99% of all active web applications are
written as monolithic web apps.  Why?  I think that with so little practical
information around on building service oriented web applications, it is only
natural to build monolithic applications instead.

For starters, it's a lot easier (at least in the beginning) to put all your web
app code into a single project.  Over time, as your project grows and more and
more complexity is added, it's a lot easier to simply refactor the old stuff
than it is to rip your application apart into multiple independent services.

With so many monolithic applications out there, certain patterns have emerged
over the years that make building and scaling monolithic web applications
simpler--primarily, [message queues][].

When you're working on a large monolithic web application, and need to:

-   Speed up your response time,
-   Render things asynchronously, or
-   Perform time intensive operations on separate hardware...

The de-facto way to do so is by relying on the message queueing pattern.  What
this allows you to do is dump tasks into a message queue (something
like [RabbitMQ][], [Amazon SQS][], or [Redis][]), which will then be read
(consumed) by one or more worker servers which read the task, process it, and
dump the resulting values into some place that your web application can
retrieve it.

Using message queues allows you to fire-and-forget slow operations, letting
them happen naturally behind the scenes without delaying your web response
time.


## The Service Pattern

While service oriented architecture is certainly a hot topic in tech circles,
it has still not gained widespread adoption, primarily due to the fact that it
can be complex to implement, and has a steeper learning curve for new
developers.

Service oriented web applications differ from monolithic web applications in
several main ways:

-   They are composed of multiple, small, independent services (think: `www`,
    `api`, `accounts`, `portal`).
-   Each of these small services talks via HTTP to the other services.
-   Each of these small services has less code in it (since they do less
    things), making them generally easier to maintain over long periods of
    time.
-   Each of these small services has their own resources: web servers,
    databases, etc.

As you can probably see, building service oriented web applications essentially
gives you many small moving parts as opposed to a single large part.


## Effect 1: Maintainability

The first side effect you get by writing service oriented web applications is
simple: better maintainability for your web application.

By having multiple small code bases that are each responsible for a very small
amount of logic, you'll typically have an easier time maintaining your code in
the long term--since complexity is always kept to a minimum and the code is
easy to navigate.

Let's say you've written an `accounts` web service, which is solely responsible
for creating, updating, and removing user accounts.  This means that if you
need to update some account logic, you know exactly where it is.  There is no
searching through thousands of lines of view code, database wrappers, or
anything else--as this logic exists in only a single small place in your
application.

Compare this with maintaining monolithic applications with lots of complexity
in a single place, it becomes harder to make code changes without side effects,
more difficult for new developers to dive in (where do I get started?), and
tricky to refactor without breaking things.


## Effect 2: Scalability

One of my favorite effects of writing service oriented web applications is the
passive effect it has on scalability.

By having multiple small web services, each with their own resources
(databases, message queues, web servers), this gives you the ultimate
flexibility in scaling your web application.  Let's say your application
consists of the following services:

-   `myapp-api`, your public facing web API for developers.
-   `myapp-www`, your public facing website.
-   `myapp-accounts`, your internal API for managing user accounts.

Let's say that each time a developer makes a request to your `myapp-api`
project, you first have to authenticate the user against your `myapp-accounts`
project (real-world scenario).  Let's also say that each time users log into
their account on `myapp-www`, they ALSO must authenticate against your
`myapp-accounts` project.

Since both your `myapp-api` and `myapp-www` projects rely on `myapp-accounts`
for authentication data, it is likely that your `myapp-accounts` project will
be getting a lot more usage than either your `myapp-api` or `myapp-www`
projects.

Luckily, since you've built your web application as a composition of
independent services, you now have several options to scale your
`myapp-accounts` project:

-   You can add more web servers.
-   You can add a larger database.
-   You can scale your database queries out (through read slaves).
-   You can add or refactor your logic to make better use of message queues for
    time intensive tasks.

And you can do this all without affecting either of your other two services:
`myapp-api` or `myapp-www`!

Compare this with scaling monolithic web applications: if you need to increase
capacity for users authenticating against your database, you must scale your
entire application--you can't selectively choose which parts to scale, and
which parts to leave alone (note: this isn't *entirely* true, but I'm saying
it anyway).


## Effect 3: Simplicity

Another effect of writing service oriented web applications is that you
generally have a much simpler back end system.

As I mentioned at the start of this article, one of the primary ways to scale
monolithic web applications is by heavily relying on message queues to process
time intensive tasks.  When you begin writing services as opposed to monolithic
apps, you can actually rely much less on messages queues than you'd think,
eliminating technical complexity and architectural burden.

Let's say you have a monolithic application that fires off a time intensive
task (via a message queue) which subtracts money from a user's bank account.
The reason you fire this off as a task is because this function must perform a
lot of sanity checks before removing the user's money, and you want to ensure
this happens safely outside of your user's request-response cycle.

What if one of your internal services handled all banking transactions for
users?  Instead of:

-   Running a message queue,
-   Running a backup message queue (in case of failure), and
-   Running multiple worker servers...

You could simply fire off an HTTP POST request to your internal
`myapp-transactions` project and let it handle things in real time.  The reason
you could do this is because, knowing your transactions application requires
fast servers, you could:

-   Ensure your `myapp-transactions` service runs on very fast web servers,
-   Can quickly process and handle banking transactions,
-   Keep your code simple and independent of external dependencies.

Instead of relying on a message queue, you could: rip it out of your
architecture all together, have a small (easily maintainable) code base for
your transactions, expose a simple HTTP service that your other applications
can talk with, and scale your transactions service independent of all your
other services (this way, if you suddenly start doing a lot of transactions,
you only need to focus on scaling a single small code base).


## Wrap Up

In my experience, building service oriented web applications generally leads to
simpler, faster, and more scalable web applications.  Without realizing it, you
can:

-   Make maintaining and expanding your code base easier.
-   Lower the bar for new developers.
-   Make scaling your application a simple process.
-   Reduce architectural overhead and complexity.

Also: if you're at all interested in building service oriented web
applications, you may want to check out my book:
[The Heroku Hacker's Guide][], it teaches you how to use
[Heroku's platform][] to build fast, small, independent web services.


  [Robot Warrior Sketch]: /static/images/2012/robot-warrior-sketch.png "Robot Warrior Sketch"
  [Service Oriented Architecture]: http://en.wikipedia.org/wiki/Service-oriented_architecture "Service Oriented Architecture"
  [message queues]: http://en.wikipedia.org/wiki/Message_queue "Message Queues"
  [RabbitMQ]: http://www.rabbitmq.com/ "RabbitMQ"
  [Amazon SQS]: http://aws.amazon.com/sqs/ "Amazon SQS"
  [Redis]: http://redis.io/ "Redis"
  [The Heroku Hacker's Guide]: http://www.theherokuhackersguide.com/ "The Heroku Hacker's Guide"
  [Heroku's platform]: http://www.heroku.com/ "Heroku"
