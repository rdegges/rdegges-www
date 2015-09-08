---
title: "My Startup, A Retrospective"
date: "2014-01-31"
tags: ["startups"]
slug: "my-startup-a-retrospective"
description: "A quick look back at my startup: what things worked, what didn't, and what I learned along the way."
---


![Cute Monster Sketch][]


Wow, the past ~2 years have been totally crazy.

Almost two full years ago I launched my startup, [OpenCNAM][], with [this
post][] here on my blog.  Since then I've learned a ton, and wanted to take some
time to reflect on what things I did right, what things I did wrong, and
hopefully share an interesting story along the way.

If you've got any questions, feel free to [drop me an email][].


## Launching OpenCNAM

![Rocket Ship Sketch][]

When [Mike][], [Chris][] and I decided to build OpenCNAM, we did so because the
Caller ID industry was horrible.

There was no good way (as a developer) to grab Caller ID information and use it
without going through a ton of hoops.  If you wanted to get Caller ID
information, you had to:

- Setup expensive phone company contracts.
- Have your own hardware servers.
- Have custom cards in your servers to talk to the phone companies.
- Setup a PBX system and do all sorts of custom coding to get things working
  properly.

We weren't satisfied with that.  It sucked!

Our vision for OpenCNAM was to have a purely developer-drive site where users
could easily query a REST API endpoint and get back Caller ID information for
any phone, instantly.

So that's what we set out to build.

What we ended up doing was launching a very, very small MVP of OpenCNAM in a
single weekend.  The strategy was simple: load up on energy drinks and knock the
entire thing out as quickly as possible.

I spent the entire weekend building a Django site and API service (using
[Tastypie][]), and desperately hacking up a theme from [ThemeForest][] that
looked suitable.  In the end, everything came together nicely and the first
version of OpenCNAM was live!

It consisted of:

- A two page website (a home page, an about page).
- A [Sphinx][] documentation site (docs.opencnam.com), which contained all of
  our developer facing documentation.
- And lastly, a simple API service that returned Caller ID given a phone number
  (in JSON, JSONP, YAML, XML, and plain text).
- No user accounts or signup whatsoever.  Users could only query our API
  endpoint directly (with no credentials).

Overall, it equated to about 20 hours of hacking.

After it was ready, I randomly threw the link up on [Hacker News][] and
[/r/startups][] tailed our Heroku logs >:)

To my surprise, people liked it!

We received hundreds of email from programmers who found us through both Hacker
News and Reddit, asking us questions, giving us suggestions, etc.  In the first
48 hours we did several hundred thousand API requests -- it was insane!


## Post Launch

![The Thinker Sketch][]

After the initial launch, we knew OpenCNAM had some potential.  So I immediately
went back to work.

For the next two weeks I added user authentication, billing, integrated a new
custom design (we hired a designer to build a nicer looking website), rewrote
our documentation, and cleaned up the code base.

I also built out several client libraries, and started writing integration
software for existing business phone systems (to give phone system
administrators a way to enable Caller ID for their users).

The entire time I was living through the biggest adrenaline rush ever.
Constantly coding, feeling great, and (for the most part) living the dream!
There's almost no better feeling in the world than working on something that
you really love, and having other people enjoy your product!

Once those two weeks were over, I relaunched the site, and emailed all of the
people who messaged us about OpenCNAM previously.  We immediately started to see
user signups -- a great feeling.

Within a day or so we had our first few paid users (and profitability!).  From
there, the service just kept on growing.


## Scaling Issues

![Skeleton Warrior Sketch][]

A few weeks after our 'real' launch, we started having issues keeping up with
customer demand.  The Django site and API service I had built were hacked
together quickly, and were not scaling properly.

To keep things running smoothly, I scaled up our Heroku Dynos, but quickly
realized that things needed to be rewritten as soon as possible to avoid major
problems.  Not only were there issues with customizing Tastypie for our specific
use case, but there were also problems optimizing our authentication and
authorization workflow, which led to us hammering our database and caching
servers far more than necessary.

For the next two months I spent a lot of time carefully rewriting the entire
OpenCNAM code base, and converting the systems from a single, monolothic Django
project, into multiple, totally independent, Flask API services.

When I finally pushed these new services live, and shut down the old Django
site, I was incredibly surprised to see how much of a difference it made.  Our
new service oriented architecture was able to serve thousands of requests per
second (for both free and paid users) with only two Heroku Dynos, reducing our
hosting costs to almost nothing.

**Fun Fact**: To this day, OpenCNAM only needs roughly 5 Heroku Dynos, and
handles billions of requests.  Something I'm incredibly proud of.

Our new Flask backend also proved to be a lot simpler and more maintainable.
The code base shrunk about 50% in size, and our projects became so simple that
apps / blueprints / etc. weren't even needed -- a nice side effect of building
simple, isolated services.


## Getting Customers

![Handshake Sketch][]

After getting the product side of things running smoothly, I was talking with
Mike and Chris about the next move, and we all decided that now would be a
perfect time to go out there and acquire customers.

**Side Note**: I'm a bit of an introvert.  I do *OK* talking with other
programmers, but I've never considered myself a marketing or salesperson, so I
had absolutely no idea how to "get a customer".

Anyway, it was around this time that I decided to get out of my comfort zone and
try to bring in some new customers myself!  I figured that if sales guys can do
it, it can't be all that hard, so I might as well give it a go.

Since Chris is an experienced customer facing guy, I spoke with him and got some
advice about talking with potential customers and reaching out to people
directly.

After a few days of trial-and-error, I found a marketing solution that ended up
working pretty well!


### Identify Your Targets

The first thing you want to do when looking for customers is identify who your
customers actually are.

In our case, I figured that we had several groups of potential customers:

- Mobile developers wanting to build Caller ID applications for Android / iOS.
- IT guys working in small companies who managed the company phone system, and
  wanted to get Caller ID support for their users.
- Voice over IP companies who provide IP based phone service to many customers
  at scale.

I figured that since the last group is the smallest (there are a lot less VoIP
companies than there are mobile developers and IT guys), it would be
advantageous to reach out to them first (and of course, it doesn't hurt that
they'd likely be the biggest spenders).


### Find Your Targets

Once you know who you need to contact, the next step is to find them!

In my case, I literally opened up Google and searched for *voip companies*, *SIP
providers*, and a few other related phrases, then spent a day or two going
through every page of results and making a spreadsheet with several columns:

- The company name.
- The company URL.
- The company size (estimated).
- The owner (or CTO's) email address.

The main goal here is to get an email address of the highest ranked technical
person.  For small companies, this is usually the CEO / CTO.  For larger
companies, you might have to find something like the lead programmer / lead tech
/ etc.

In the end you should have roughly ~500 contacts.


### Send Personal Email

Once you have enough contacts, it's time to get busy writing email!

What I decided to do at first was send 3 email per day, first thing in the
morning, to three different potential customers.

My reasoning was that 3 email is easy to do, and ensures that you won't get
overwhelmed with phone calls / email in the following few days -- this way you'll
be able to devote as much time to each customer as needed.

Although I tweaked my email wording quite a bit, what ended up working well for
me was something similar to the following (your mileage may vary):

> Hi &lt;name&gt;!
>
> I'm a big fan of your company, &lt;company&gt;.  I love how you guys do &lt;something&gt;,
> and love your product.
>
> I'm the CTO at a small tech startup, OpenCNAM (https://www.opencnam.com/).  We
> just built an experimental new Caller ID API service.  The way it works is
> simple: you query our public API endpoint with a phone number (ex:
> https://api.opencnam.com/v2/+16502530000), and we'll give you back that phone's
> Caller ID ("GOOGLE INC" in this case).
>
> I'd love to get your feedback on our service.  You can try it for free without
> even creating an account!  Just hit our public API endpoints directly.
>
> I'd love to know how we compare to your current Caller ID provider(s) if you
> have any.
>
> Thanks for your time, I realize you're incredibly busy.
>
> Best,
>
> -Randall

The key things that worked were:

- I always wrote each email personally, and included company-specific stuff in
  each email (this requires time).
- I took the time to find out what this company does *BEST*, and complement them
  on it.  This was totally genuine, and helped me get to know what products my
  potential customers were building.
- I gave the person example URLs to test against.  I think this is super
  important -- nobody cares for reading a bunch of documentation and stuff.
  People want to see results.  What better way to win someone over than give
  them what they want?
- Don't mention anything about pricing / etc., it makes people feel like they're
  being sold to.
- Ask for feedback.  If the person likes your product / company, they'll sign
  up.  If they don't like your product, you'll get some negative feedback you
  can use to make things better.  Win / win.
- Lastly, everyone is really busy and hates wasting their time.  I always
  mentioned that I know they are very busy to let them know that I *really do*
  appreciate them taking the time to read my email and possibly respond.

The method above resulted in a roughly 75% conversion rate -- it was incredibly
successful.


### Things to Keep in Mind

![Brain Sketch][]

The people you reach out to are just like you: they're busy, they want to save
money, and they want to use quality products.  If you can show them a superior
product and make it look nice and easy, people will usually like you and your
company.

In our case, we got extremely lucky -- either we had perfect timing, or we had
perfect wording, but for one reason or another, we were able to convert an
incredible amount of large phone company providers into customers in a very
short period of time.

The best thing you can do when reaching out to potential customers is just be
yourself -- don't worry about being professional or pretending to be a *big
company*, just be genuine and treat people with respect.


## Keeping Busy

![Bee Sketch][]

After bringing on a couple thousand customers, I decided to release a V2 API and
make several improvements to the data layout / features we provided.

I ended up spending a month or two releasing supplementary features and finally
pushing out a nice new V2 API (and related docs, libraries, and software
integrations).

Since our hosting costs were very low, we decided to keep things simple and make
iterative improvements to the product, and run as lean as possible.  This
allowed us to build up quite a bit of funding to invest in our other projects
(we have several other large products).

Unfortunately, it was about this time when things started to run smoothly and
everything seemed excellent that we decided to devote more time to our other
projects and spend less time working on OpenCNAM directly (which in retrospect,
was a big mistake).

For the next year I spent most of my time working on our other projects, and
only making small improvements to OpenCNAM at the behest of our customers.
During this time OpenCNAM continued to grow steadily, but I had a ton of project
guilt for not spending enough time adding all the cool things I wanted to add to
the project.


## Bringing on Help

![Heart Sketch][]

I'm happy to report that as of two weeks ago, we brought on our first new
OpenCNAM hire: [Avery Max][].  Avery is going to be 100% dedicated to OpenCNAM
and will be launching all of the awesome features I didn't get a chance to
release, and making the product a lot better in the coming months.

In the two years since OpenCNAM started, we've served up billions of API
requests, brought on thousands of new (and happy!) customers, and made the
Caller ID industry a little bit better.

I'm super proud of everything that's been done over the past few years, and
can't wait to see how the product develops over the next few years (*there
are lots of amazing things in the pipeline*).


## Retrospective (the Good)

![Lion Roar Sketch][]

While I'm pretty confident the main reason OpenCNAM was successful was luck, I
do think that we made some good decisions early on which helped improve that
luck a bit.

Firstly, we decided to get the MVP going as quick as possible.  I know this is
common knowledge, but you really should get your product out there as soon as
you possibly can, even if it's just hacked together.

Secondly, we actually launched a product for our MVP, not just a landing page or
a 'coming soon' type thing.  While I realize the best way to validate your
product is to have customers lined up in advance, I think that in most cases,
that's just a waste of time.  In the amount of time it takes to get your
domains / email / landing page setup and configured properly, then to do all
the marketing for your product, you might as well build a functional MVP!

The other thing I think we did well was to stay true to the company's goal.  We
set out to build the best Caller ID API service possible, and I think we did
exactly that.  Along the way, we received tons of email from customers asking us
if we could do other things like:

- Give them email addresses from phone numbers.
- Give them social network information from phone numbers.
- etc.

But I'm glad that we turned those requests down and kept our goal as simple and
straightforward as possible.  Having a single, unifying goal makes it easy for
everyone on the team to get involved and make decisions without worrying about
whether or not what they're doing is right.  Whenever we received requests, or
had tricky technical issues crop up, the question we always asked was "Will
doing this make OpenCNAM the best Caller ID company out there, or not?"

Lastly, we did a great job with customer support.  We went out of our way to
help new customers use and integrate OpenCNAM into their products, sometimes
even committing code directly into a customer's code base!  I think it's pretty
important to do just about anything for your customers.  If they need help --
get out there and help them!  Don't worry about politics, procedure, etc., just
make people happy!


## Retrospective (the Bad)

![Angry Dinosaur Sketch][]

While I'd like to say we made no mistakes running OpenCNAM, I can't!  All of us
made a ton of mistakes along the way.

I think the single largest mistake we made was to not invest more time into
OpenCNAM as it was growing.  Instead of devoting time to other projects, we
should have doubled down and focused on developing the product even more, and
made it into the best possible product.

At the time, it seemed like a good idea -- but in retrospect, I believe that if
we would have really focused on adding more features to the API service,
cleaning up the user dashboard, and fixing some UI elements -- we could have won
a lot more potential customers over.

Secondly, we realized too late that the product we built was for the wrong
audience!

We started OpenCNAM with the idea that it would be an API company for
developers.  What we realized many weeks after launch (based on customer email)
was that most of our users were NOT developers at all!  As it turned out, most
of our users were companies with internal phone systems (PBXs) who just needed
to get Caller ID hooked up for their users.

Since our company / branding / UI was totally developer driven, this made things
a lot more complicated and confusing for potential users, and often resulted in
email questions, and integration questions about various phone systems.

If we would have realized this sooner, and either:

- Pivoted the company to cater to phone system users, or
- Launched a separate product to cater to phone system users.

Then I think we could have been far more successful, and made our customers far
happier.

Of course, it's never too late to do these things, but it would have been nice
to have identified and taken care of these things immediately after learning
about them.


## Closing Thoughts

Running a successful startup has been a crazy two year experience.  It's had
it's ups and it's downs -- but mostly ups.  I feel incredibly lucky to both
succeed on the first try as well as build something that thousands of people
use and love!

In the next few years, I expect OpenCNAM to continue to grow and evolve, and
make even more of an impact on the telephony industry.

If there's anything else you'd like to know, feel free to [shoot me an email][].
I'm probably going to be writing several follow up articles in the coming weeks
/ months, so if you think of any interesting topics let me know!

-Randall


  [Cute Monster Sketch]: /static/images/2014/cute-monster-sketch.jpg "Cute Monster Sketch"
  [OpenCNAM]: https://www.opencnam.com/ "OpenCNAM - A Simple Caller ID API"
  [this post]: {filename}/articles/2012/im-working-on-a-startup.md "I'm Working on a Startup"
  [drop me an email]: mailto:r@rdegges.com "Randall Degges' Email"
  [Rocket Ship Sketch]: /static/images/2014/rocket-ship-sketch.jpg "Rocket Ship Sketch"
  [Mike]: http://michaelrwally.blogspot.com/ "Michael Wally"
  [Chris]: http://www.chrisbrunner.com/ "Chris Brunner"
  [Tastypie]: http://tastypieapi.org/ "Django Tastypie"
  [ThemeForest]: http://themeforest.net/ "ThemeForest"
  [Sphinx]: http://sphinx-doc.org/ "Sphinx"
  [Hacker News]: https://news.ycombinator.com/ "Hacker News"
  [/r/startups]: http://www.reddit.com/r/startups "Reddit Startups"
  [The Thinker Sketch]: /static/images/2014/the-thinker-sketch.jpg "The Thinker Sketch"
  [Skeleton Warrior Sketch]: /static/images/2014/skeleton-warrior-sketch.jpg "Skeleton Warrior Sketch"
  [Handshake Sketch]: /static/images/2014/handshake-sketch.jpg "Handshake Sketch"
  [Brain Sketch]: /static/images/2014/brain-sketch.png "Brain Sketch"
  [Bee Sketch]: /static/images/2014/bee-sketch.jpg "Bee Sketch"
  [Heart Sketch]: /static/images/2014/heart-sketch.jpg "Heart Sketch"
  [Avery Max]: https://twitter.com/averymax "Avery Max on Twitter"
  [Lion Roar Sketch]: /static/images/2014/lion-roar-sketch.jpg "Lion Roar Sketch"
  [Angry Dinosaur Sketch]: /static/images/2014/angry-dinosaur-sketch.jpg "Angry Dinosaur Sketch"
  [shoot me an email]: mailto:r@rdegges.com "Randall Degges' Email"
