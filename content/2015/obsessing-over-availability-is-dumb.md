---
date: "2015-12-29"
description: "Obsessing over availability and service uptime is dumb. Here's why."
slug: "obsessing-over-availability-is-dumb"
tags: ["programming", "devops"]
title: "Obsessing Over Availability is Dumb"
---


![Superman Sad Sketch][]

Over the past handful of years, as I've been building and working on several
very large and very public API services, I've noticed that almost everyone I
speak with is a *zealot* for availability.

> The API service must be up at all times!

> Availability is the number one most important thing at our company!

> We have an entire team of devops people working around the clock to ensure you
> get five nines of availability!

> Our customers can't tolerate even a single second of downtime in a year!

etc...

It actually comes up *so frequently* in conversation that I've started to
wonder if I'm not crazy for thinking that **obsessing over availability is
dumb**.  In my humble opinion, it's not only a complete waste of time, but
also a huge drain on the tech sector in general, and one of the largest
factors causing startups to go out of business early.

Think I'm crazy?  I'm *ok* with that.  But first, let me explain...


## It Just Doesn't Matter That Much

![Superman Angry Sketch][]

For 99.99999% of [*companies | products | websites | services*] out there right
now, availability really doesn't matter all that much.

Do you really think that your Wordpress blog is so critically important that it
needs to be up every single second of the year?  The most likely answer is *no*.

The same applies to your startup company: even though you might be providing a
[*cool | unique | valuable | important*] service to your customers, odds are --
your customers can live without your service for a few hours every quarter, and
still get along with their lives just fine.

Even if you're running an API company like...  Let's say: [Zencoder][] (*an
API service which transcodes video files*), and make 100% of your revenue from
developers building applications **on top** of your service -- it still just
doesn't matter all that much.

In the event that your application can't transcode a video immediately due to
Zencoder downtime, I'm sure the world won't end and all your customers won't
leave you.

Zencoder going down might be slightly inconvenient, but won't break your
business in twain.

Now, for certain services -- namely things that involve real-life repercussions:

- Healthcare
- Communication systems (*like the telephone network*)
- Banking

Of course availability is important!  It's important because having downtime
will *dramatically* affect a person in ways that may not be easily fixed.

If you place a call to 911 from your T-Mobile cell phone, and you get a
*ring-ring-ring* for 30 seconds, that's a **HUGE DISASTER** and could result in
a lot of horrible things happening.

But -- with that said, for 99.99999% of you reading this, the above is not
true.


## Availability is Technically Difficult

![Superman Scowl Sketch][]

There's a huge misconception out there that building highly available services
is somehow *"easy to do"*.  This isn't even remotely true in the slightest.

Let's think about what true availability means for a minute.

If you're building some API service that other developers will integrate into
their applications, then your service being highly available means:

- You need to have multiple web servers sitting behind a load balancer of some
  sort to handle incoming HTTP requests to your API service.  Your load balancer
  will need to be redundant, so in the event one no longer works, another can
  take over immediately.

- Your load balancers themselves need to be configured in a way such that any
  failed / incomplete HTTP requests will be resent from the load balancer to
  another operational web server before returning a response to the end user.
  This way incoming user requests are not dropped when issues occur.

- Any dependent services YOUR service depends on (*databases, caches, API
  services, etc.*) must be fully functional and have redundant options in place,
  as well as specialized fail over / retry software to handle issues when they
  occur.

- When you deploy changes to your software, you need to do so in such a way that
  no incoming requests (*whether in-progress or new*) will be negatively
  affected during the roll out.  This means your deployment procedures need to
  be very carefully implemented and automated, and all edge cases must be taken
  into account.  And don't forget about things like database migrations,
  rotating credentials, etc!

The above things are not easy to achieve in a technical way.  The reason?
Mistakes happen at all levels: hardware, software, and most of all -- *human*.
Trying to automate your way out of certain types of availability problems like
fail over is a very tricky game.

Even with thousands of hours invested writing configuration management and
automation scripts, the odds of technical failure are still very high -- and
let's face it: *if something can go wrong, it will*.


## Availability is Expensive

![Superman Question Sketch][]

So, since availability is so hard to technically achieve, what does that equate
to?  You probably already guessed: *cost*!

**Availability is very, very expensive.**

Here's how it costs you:

- Hiring multiple full-time operations people to help write Chef / Puppet /
  Ansible / Salt rules to manage infrastructure, configure / tweak services, and
  test / automate / mess around with things like fail over, clustering, and
  graceful degradation.

- Having your developers spend lots of time doing the operations work
  themselves, instead of writing quality code.  I've gone this route myself in
  the past, and have spent many thousands of hours doing devops work.  No matter
  what anyone else says: doing devops work in addition to your normal
  development duties is a losing battle -- you will never have enough time to
  do a good job at both (*unless you follow my advice later on*).

- Spending tons of money on very expensive outsourced services.  There are most
  definitely tools out there than can improve your availability, but they cost a
  great deal of money.  Running redundant servers, paying incredible premiums
  for special hardware, etc. -- it all costs lots of money, time, and *usually*
  ongoing maintenance.

- Doing a shitty job.  If you claim that availability is important to you, but
  you aren't willing to spend actual time working on it -- then the cost is
  going to be your customers and your reputation.  Selling five nines of
  availability to customers and under-delivering won't put you out of business
  immediately, but will drain your reputation and slowly bleed your user base
  over time.

No matter what you've heard: availability ain't cheap: so don't forget it!


## Availability Will Cost You Your Company

![Superman Bold Stance Sketch][]

As a pretty active member of the development community over the last 10 years,
I've had the pleasure of getting to know lots of different people in the startup
scene -- and not just in the bay area.

I've spent tons of time going to meetups and meeting other developers in Los
Angeles, the Bay Area, Portland, Denver, New York, and quite a few other places.

And, no matter where I go or who I speak with: I continue to meet startups
building their MVPs who are **already spending lots of time and money
architecting their services for availability**.

I can tell you right now that if you're a startup building an MVP and don't yet
have a lot of customers, **you're wasting your time, money, and most likely
dramatically increasing the odds your company will fail** by spending time and
effort worrying about availability.

If you aren't making money, and are already worried about redundant load
balancers, you should probably be working over at Google instead of running a
startup.

Spending time, effort, and in many cases: limited funding will dramatically
increase your [Death Rate][], putting you out of business that much sooner.
It's hard to come up with generic rules (*I'm not a VC or anything*), but if I
*had* to come up with a formula, I'd say that if your company is less than 10
people, and you've got a dedicated operations person, you're doing it all
wrong.

If you're a startup and you're deploying your web services anywhere other than
[Heroku][], [AWS Elastic Beanstalk][], or some other incredibly simple PaaS,
you've probably already wasted too much time.


## Winning by Least Effort

![Superman Stare Sketch][]

In my opinion, there's only one way to *win* at product development: doing the
simplest possible thing at every possible level.

**NOTE**: This is a lot different than taking the *"easy way out"* -- this is
all about taking the path of least effort.

And, as with everything else in this world, the simplest possible thing often
involves trade-offs.  You can trade a little bit of availability for a *LOT* of
convenience, or you can trade a lot of availability for a large *inconvenience*.

I prefer to go with the former.

Here's what I like to do when I'm starting new projects, regardless of how
ambitious they are:

Firstly, I'll build retry logic into the core of my products, so that any
failed HTTP requests / DB queries / etc. are retried using
[exponential backoff][] a set amount of times (*usually 3*), ensuring that
failed requests are retried and downtime is *hopefully* avoided for transient
issues.  This strategy requires very little development effort, and greatly
improves *apparent* availability even when issues are present.

Secondly, I'll build my MVP using tools and services that make my life
dramatically simpler, with the knowledge that in the future, if I absolutely
*need* to architect my project for availability, I can always do so.

This typically involves me using services like:


### Heroku

![Heroku Icon Black][]

I like to use [Heroku][] for hosting my web servers and workers.  Not only is
Heroku a platform that [enforces best practices][], but it is built on top of
open technologies, has been around for years, and has an incredible team of
people behind it.

It's also very competitively priced, and free for small projects (*like most
of mine!*).

Furthermore, [history shows][] that Heroku gets you at *least* 99.99% uptime,
for no cost, with zero operations work and maintenance involved.  I currently
run an API service on Heroku ([ipify][]) which serves > 12 billion of requests
per month, and it hasn't once involved maintenance, woken me up with alerts,
or inconvenienced me *in the slightest*.

Lastly, worth a mention, is the fact that Heroku comes with an awesome
collection of [addon services][] which are incredibly high quality.  Heroku also
runs the absolute best hosted database service that has ever existed:
[Heroku Postgres][].  Using anything else in comparison makes you realize just
how absolutely amazing the Heroku Postgres service really is.


### Select AWS Services: S3, SQS, Dynamo, Redshift

![AWS Icon][]

[AWS][] is an incredibly complicated hosting service.  More than a hosting
provider, it's a suite of low-level building blocks for developing modern web
applications.

It consists of a vast array of services, all of which have distinct purposes and
use cases.

Out of all the current services AWS provides, several are worth a mention: S3,
SQS, Dynamo, and Redshift.  These services require 0 maintenance, do their
jobs incredibly well, and get you incredibly high amounts of uptime for low / no
cost.

If you haven't heard of [Amazon S3][], I don't know how you found this blog.
But anyhow: S3 is a very reliable file storage service that gets you a
durability percentage of 99.999999999% (*you read that correct, 9 nines of
durability*), and 99.99% availability yearly.  This is probably the most widely
used of the AWS services, and, side note: I've never see anyone complain about
their 99.99% availability guarantees.

Next up: [Amazon SQS][].  SQS is an incredibly simple to use queueing service
that costs next to nothing, has a high record of history availability, requires
no maintenance or hackery over time, and supports and *unlimited* amount of
concurrent messages.

[Dynamo][] is a very high performance NoSQL database that requires no
maintenance, is inexpensive to use, has a very simple API, and allows you to
retrieve data in a variety of ways for speed and accuracy.  I've had incredible
results using it as a first-tier cache for API services that require incredibly
low latency responses.

Finally, [Amazon Redshift][] is an excellent data warehousing service.  It
requires no maintenance, is very fast, has a PostgreSQL compliant API for
querying data, and can store an unlimited amount of data.  If you're building
any sort of analytics tools, aggregating all your data into one place before
generating useful metrics and graphs is a perfect use case for Redshift, and
it has a number of amazing features to make this sort of workflow even simpler.

I've built several projects now that have used Redshift for data warehousing
with great success.


### Other Services

![Service Logos][]

For some non-hosting related services, I really enjoy using:

[Mailgun][] for sending out email.  They have a simple API, competitive
pricing, and a 99.99% uptime guarantee.  It's also a hell of a lot easier than
handling email yourself.

[Twilio][] for handling any sort of telephony stuff: phone calls, SMS messages,
etc.  They have a great API, cheap pricing, and a 99.95% uptime guarantee.

[Algolia][] for searching data.  It's simple to use, fast, and has a 99.99%
uptime guarantee.  It's also way easier than running Elastic Search clusters of
your own, and dealing with all the madness that entails.

[Pusher][] for anything that requires websockets.  It provides a simple API to
handle websocket stuff, without the hassle of running socketio servers and
scaling / running / worrying about those in production.  They also have an
amazingly transparent uptime model you have to [read for yourself][]:  *+1 for
respect.*


## Pride, Ego, and Hubris

![Superman Proud Sketch][]

Lastly, I wanted to quickly mention that the only reason people tend to drone on
endlessly about availability in the first place is that caring about
availability over almost everything else to a fault has become *popular* in the
tech community.  Building a highly available service has become something of a
*badge of honor*.

People who give conference talks about their *war stories* building highly
available services, and brag about their efforts to improve availability 0.0001%
are lauded with praise, even under ridiculous circumstances.

Caring a lot about availability has become a source of pride for many
developers, in the same way that code quality is a source of pride.  If you
*don't* care about it as much, people think you're insane!

**NOTE**: For the record, I *do* care about code quality more than almost
anything else =)

The next time you end up in a conversation where availability comes up, try to
approach the conversation from a logical place: is availability necessary for
this?  Is the cost worth it?  Can you get by with 99.99% availability and *no
operations work whatsoever* instead of spending hundreds of thousands of dollars
for an extra nine of availability?

As a programmer, you should always be analytical about this stuff.  Don't
blindly hop onto the *"me too!"* train just because everyone else is.


## Closing

![Superman Back Sketch][]

I hope that by this point I've convinced you that I'm at least *not crazy*, and
that obsessing over availability isn't exactly the smartest thing to do in most
cases.

Now, excuse me while I go back to hacking on my latest API service which will be
happily sitting at 99.99% availability with zero effort on my part.  I'm a busy
guy, after all.


  [Superman Sad Sketch]: /static/images/2015/superman-sad-sketch.png "Superman Sad Sketch"
  [Superman Angry Sketch]: /static/images/2015/superman-angry-sketch.png "Superman Angry Sketch"
  [Superman Scowl Sketch]: /static/images/2015/superman-scowl-sketch.png "Superman Scowl Sketch"
  [Superman Question Sketch]: /static/images/2015/superman-question-sketch.png "Superman Question Sketch"
  [Superman Bold Stance Sketch]: /static/images/2015/superman-bold-stance-sketch.png "Superman Bold Stance Sketch"
  [Superman Stare Sketch]: /static/images/2015/superman-stare-sketch.png "Superman Stare Sketch"
  [Heroku Icon Black]: /static/images/2015/heroku-icon-black.png "Heroku Icon Black"
  [AWS Icon]: /static/images/2015/aws-icon.png "AWS Icon"
  [Superman Back Sketch]: /static/images/2015/superman-back-sketch.png "Superman Back Sketch"
  [Superman Proud Sketch]: /static/images/2015/superman-proud-sketch.png "Superman Proud Sketch"
  [Service Logos]: /static/images/2015/service-logos.png "Service Logos"
  [Zencoder]: https://zencoder.com/en/ "Zencoder"
  [Heroku]: https://www.heroku.com/ "Heroku"
  [AWS Elastic Beanstalk]: https://aws.amazon.com/elasticbeanstalk/ "AWS Elastic Beanstalk"
  [Death Rate]: http://startupdeathclock.com "Startup Death Clock"
  [enforces best practices]: {{< ref "2012/heroku-isnt-for-idiots.md" >}} "Heroku Isn't for Idiots"
  [history shows]: https://status.heroku.com/uptime "Heroku Uptime"
  [ipify]: https://www.ipify.org/ "ipify - A Simple Public IP Address API"
  [exponential backoff]: https://en.wikipedia.org/wiki/Exponential_backoff "Exponential Backoff"
  [addon services]: https://elements.heroku.com/addons "Heroku Addons"
  [Heroku Postgres]: https://elements.heroku.com/addons/heroku-postgresql "Heroku Postgres"
  [AWS]: https://aws.amazon.com/ "AWS"
  [Amazon S3]: https://aws.amazon.com/s3/ "Amazon S3"
  [Amazon SQS]: https://aws.amazon.com/sqs/ "Amazon SQS"
  [Dynamo]: https://aws.amazon.com/dynamodb/ "Amazon DynamoDB"
  [Amazon Redshift]: https://aws.amazon.com/redshift/ "Amazon Redshift"
  [Mailgun]: http://www.mailgun.com/ "Mailgun"
  [Twilio]: https://www.twilio.com/ "Twilio"
  [Algolia]: https://www.algolia.com/ "Algolia"
  [Pusher]: https://pusher.com/ "Pusher"
  [read for yourself]: https://pusher.com/legal "Pusher Legal"
