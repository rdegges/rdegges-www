---
title: "postgression - A PostgreSQL Database for Every Test Case"
date: "2013-01-20"
tags: ["programming"]
slug: "postgression-a-postgresql-database-for-every-test-case"
description: "Introducing postgression: a free PostgreSQL database service."
---


![Monkey Sketch][]


The following are some facts about me:

-   I write a lot of software.
-   In order for me to write good software, I often write tests for my
    software.  Code that makes sure my business logic works on data from my
    database.  Code that makes sure my web requests return the right thing.
    You name it, I've probably tested it.
-   I do 100% of my development on a Linux laptop.
-   I usually run my tests on my laptop while I'm coding, as well as a remote
    [Jenkins][] server (and sometimes [Travis CI][] instance) that run all my
    tests to make sure I didn't forget to do so locally.
-   I hate running a database server on my laptop, I hate running a database
    server on my Jenkins instance, and I hate telling my test code how to run
    tests against my testing databases on all the different types of machines I
    use.

Over the past year or so, I've become really annoyed at having to configure my
database in all my environments.  I love [PostgreSQL][] (it's an *awesome*
database), but I can't stand the idea of running it locally on my laptop, just
so I can make some tests work.  I also can't stand the annoyance of having to
SSH into my Jenkins server, configure PostgreSQL, and then write code which
tells my tests to distinguish between my local PostgreSQL stuff and my Jenkins
PostgreSQL stuff--and don't even get me started on configuring it to work in
all 3 environments: locally, on Jenkins, and on Travis.  Ugh.

I think what annoys me about this is that setting up a database isn't hard, I
just think it's stupid to have to remember to do it for each new project.  It
feels like I'm repeating the same thing over and over again, and each time I do
it, I become slightly more annoyed.

So this past week, my buddy [Alven][] and I teamed up to solve this
mini-problem for ourselves.  The result is our new service, [postgression][].

postgression is a simple web service, built on top of [Heroku's platform][]
(Don't know about Heroku yet?  [Read my book.][]), that instantly provisions a
new PostgreSQL server (PostgreSQL 9.2.3, to be precise) for you to use in your
tests.

Here's how it works: you hit our public facing API (no account required), and
we give you back a PostgreSQL database URL that you can use in your
application.  For example:

```console
$ curl 'http://api.postgression.com'
postgres://username:password@hostname:port/dbname
```

Simple, right?  So now that you've got the database, you have your tests run
against this database (which is available in Amazon's US East region, in case
you're curious), and that's it!

Finally, after 30 minutes, this database will magically disappear.

So, why is this useful?  Well, using postgression to generate a database for
your tests means that:

-   You can run your tests locally without needing to install PostgreSQL
    server.
-   You can run your tests locally, remotely (on Jenkins / Travis / etc.) using
    all the same configuration--no need to do any custom scripting or
    environment checking.
-   It costs you nothing.

Is this the most useful service in the world?  Nope.  But I love it, I've been
using it, and it's made my testing quite a bit simpler.

Today I'm really happy to open postgression up to the public.  Alven and I have
created some handy tools on our [GitHub page][], which make using postgression
easier, and we've written some basic documentation on the
[postgression website][postgression] to help you get started.

If you've got any questions, comments, concerns, or otherwise, I'd absolutely
love to hear them.  I hope you'll give postgression a try!

[Check out postgression here.][postgression]


  [Monkey Sketch]: /static/images/2013/monkey-sketch.png "Monkey Sketch"
  [Jenkins]: http://jenkins-ci.org/ "Jenkins CI"
  [Travis CI]: https://travis-ci.org/ "Travis CI"
  [PostgreSQL]: http://www.postgresql.org/ "PostgreSQL"
  [Alven]: http://zaidox.com/ "Alven Diaz"
  [postgression]: http://www.postgression.com/ "postgression"
  [Heroku's platform]: http://www.heroku.com/ "Heroku"
  [Read my book.]: http://www.theherokuhackersguide.com/ "The Heroku Hacker's Guide"
  [GitHub page]: https://github.com/postgression "postgression"
