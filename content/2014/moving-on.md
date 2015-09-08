---
title: "Moving On"
date: "2014-02-03"
tags: ["startups", "programming", "personal development"]
slug: "moving-on"
description: "I'm officially moving on from my startup to do something new!  Here's my story."
---


![Barbarian Sketch][]


As I wrote [the other day][], my startup [OpenCNAM][] has been doing really well
over the past two years since it's launch, and lots of exciting things have been
happening.

While I will always love OpenCNAM and all the amazing things we've accomplished
over the past few years, I'd be lying if I said I was still the best person to
move the company forward.

Since I first got involved in the telephony industry roughly 5 years ago, I've
built tons and tons of services using all sorts of technologies.  I've become
intimately familiar with all the major PBX systems.  I've built pretty much
every possible telephony application that involves sending and receiving phone
calls and SMS messages.  I've built all sorts of interesting open and closed
source libraries, REST APIs, and consumer facing products.  I've written and
spoken about all sorts of things I've learned.  I even ended up inadvertently
helping someone in Syria perform a denial-of-service attack against a wide array
of [military phone lines][].

Although I've learned a ton and had a *LOT* of fun over these past 5 years, I've
been slowly getting tired of building telephony services, and have been much
more interested in non-telephony services (*APIs, in particular*).

I realized a while ago that when I wake up in the morning, what really motivates
me to get up and kick ass is the thought of building and working on the most
elegant API services around, with the intent of making the world a tiny bit
better by *completely solving* some annoying technical problem.

I've never been much of a consumer facing product guy, but I'm all about
building developer tools.  I honestly can't think of anything more fun than
spending all of my time hacking on programming products, hanging out with other
programmers, and learning new stuff.

With that said, I've officially stepped back from my day-to-day role as the CTO
of OpenCNAM, and will now only be doing advisory work as a board member.  The
rest of the team will continue shipping code, negotiating telco deals, and
building the best possible Caller ID service.


## Adventure Seeking

![Mountain Sketch][]


For the past year or so I've been keeping my eyes open for new, exciting
opportunities.  There are tons of cool tech companies around doing interesting
things, but as I was looking at my options, I realized there were actually very
few places I *really* wanted to work at (or jump into).

For a while, I was considering rolling another company from the ground up, but,
although I had a lot of ideas, I didn't really have anything that was calling me
with great INTENSITY.

So, after a lot of searching, I stumbled across [Stormpath][].

Several years back, I was reading [Hacker News][], and came across Stormpath for
the first time.  At the time, I was just discovering why [Service Oriented
Architecture][] is so useful, and was incredibly excited to see what I
considered an innovative and deeply useful API service come out.

Stormpath, for those of you that don't know, is a really neat API service: they
completely handle the user management and authentication portion of your
applications, and provide a flexible, scalable, and *secure* backend that lets
you create, manage, authenticate, authorize, and fully handle users.

When I first saw Stormpath, I thought it was a really great service because
they're handling what, in my experience, has always been one of the most
difficult parts of building applications: handling users and their data
properly, and effectively.

In almost every application I've built, the number one most difficult portion
has been handling users.  It doesn't matter how great the framework you're using
is: user management is a complicated burden.  You'll typically hit one of
several problems: slowness grabbing user data (due to complicated relationships
between users and their data on practically every system with more than 20
users), problems scaling your application as your user base grows, problems
storing user data securely (so many people mess this up, ugh), problems handling
authentication (SHA 512 won't help you), or problems sharing user state between
services (users and their data should be an independent service the rest of your
application can communicate with -- not a database table tied to your huge
monolithic applications).

Stormpath solves all of these problems (and more), which is why I thought that
it'd be incredibly fun (*and challenging!*) to get involved somehow.


## Joining Stormpath

![Stormpath Icon][]

After several months of talking with Stormpath and getting to meet their
incredibly great team (*and a whole lot of thinking*), I decided to take the
plunge and join Stormpath as their first Developer Evangelist -- and do
something completely different!

Since I was 12 I've been writing code every day.  When I first started working
in the industry, it felt like a dream: *"I get to code everyday, while getting
paid? FUCK YEAH!"*.  Now, after 13 years of being a straight up developer,
after working at medium, small, and startup companies, after building tons of
open source libraries, after writing tons of blog posts, writing a book, and
even giving a few talks: I'm going to be taking my first step out of my comfort
zone and doing all of the above in an entirely new context.

As odd as this sounds to me, I realize that while I've been having a lot of fun
since I started programming professionally, I've never really had to push myself
much.  Writing code all day was pretty natural, and not all that challenging.

I realized when I first started getting involved in the Python community years
ago that the times I felt the most alive and on the edge were the times I had to
get out in public and do stuff: give a talk, hang out with other developers way
smarter than myself, write articles about tech stuff, etc.

Whether it's because of my innate introversion or something else, I've always
seemed to get the biggest challenge out of community related stuff, while the
coding sessions have always come naturally.

While part of my excitement for joining Stormpath is due to their incredibly
awesome product and vision, I'm also really excited to challenge myself and push
myself in a bunch of new ways.

Over the next several months I'm going to be doing a whole lot of:

- Open source library hacking.
- Tool building (in lots of languages / frameworks / technologies).
- Speaking.
- Writing.
- Getting out into the community, making friends, and learning cool stuff from
  my peers.
- Helping other developers out, in whatever ways possible.

I'm really excited to be joining Stormpath, and opening a new chapter of my
life.

Over the next few months I'll also be writing about my experiences as a brand
new Developer Evangelist, about what I'm learning, and all the things that
involves.

As a side note: if you'd like to meet up and chat sometime, let me know!  Now
that part of my job is meeting developers, and getting out there into the
community even more -- I'm able to make time to do cool stuff more frequently
&gt;:)

If you'd like to get in touch, you can always hit me up on [Twitter][] or via
[email][].


  [Barbarian Sketch]: /static/images/2014/barbarian-sketch.jpg "Barbarian Sketch"
  [the other day]: {filename}/articles/2014/my-startup-a-retrospective.md "My Startup, a Retrospective"
  [OpenCNAM]: https://www.opencnam.com/ "OpenCNAM - A Simple Caller ID API"
  [military phone lines]: https://speakerdeck.com/rdegges/bring-down-the-system-1 "Bring Down the System! - Shutting down military phone lines to save lives, in Python."
  [Mountain Sketch]: /static/images/2014/mountain-sketch.jpg "Mountain Sketch"
  [Stormpath]: https://stormpath.com/ "Stormpath - User Management and Authentication for Developers"
  [Hacker News]: https://news.ycombinator.com/ "Hacker News"
  [Service Oriented Architecture]: http://www.rdegges.com/service-oriented-side-effects/ "Service Oriented Side Effects"
  [Stormpath Icon]: /static/images/2014/stormpath-icon.jpg "Stormpath Icon"
  [Twitter]: https://twitter.com/rdegges "Randall Degges on Twitter"
  [email]: mailto:r@rdegges.com "Randall Degges' Email"
