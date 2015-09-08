---
title: "What I Do At Work"
date: "2010-08-15"
tags: ["programming", "telephony"]
slug: "what-i-do-at-work"
description: "My best attempt at explaining what I actually do at work."
---


![Desk Sketch][]


I realized yesterday, while finishing some website updates, that I haven't
actually written a post about my new job, what I do, and how I do it.
Not that it is particularly amazing or anything like that, but I figured other
coders interested in startups, best-practices, telephony, python, or any
combination of those items may be interested.


## Where I Work

Several months ago (in early February, 2010), I took a job offer to work at
*RCG Communications, LLC*, which is a small (but highly profitable)
telecommunications company based in Georgia.

Now, not to be confusing, but I technically work for several companies:
*RCG Communications*, *RCI Telecommunications*, *GlobalRoute*, and several
others, which are all legally distinct for various encapsulation related
issues.  Although, we're currently forming a new company (whose name has not
yet been decided), that will become my primary employer, and will lease out
code and services to our other companies (this will make code ownership rights
far less confusing).


## Why I Took the Job

At my previous job with [Fonality][] (an awesome mid-size tech company), I
worked extensively with Asterisk, Linux, and all sorts of telephony stuff.  It
was my job to help customers, and write custom telephony software to complement
our Fonality PBX systems for companies who needed more functionality than our
base system provided.

Working at Fonality was really fun.  I got to know some of the coolest tech
people in the industry, got all the free information I wanted, got to do
extensive research and testing for Asterisk platforms, and had the pleasure of
working on some really awesome product lines.  All the while working on my own
open source code, libraries, projects, and friendships.

Despite enjoying working for Fonality, I had an urge to try something new, and
get involved in a fast moving company that would really push the boundaries of
my technical knowledge, and force me to become a better developer.

When I met [RCG's CEO][], and was given a job offer, I immediately knew that it
would be the opportunity I was looking for.  RCG really needed a lead
programmer with my qualifications, and I really needed a new project with lots
of challenges and opportunity.


## What Our Companies Do

*RCG Communications* and *RCI Telecommunications* both offer the same service:
a free telephone-based conferencing service with a hosted web portal.

*GlobalRoute*, one of our newest companies, is a back end termination provider
for other VoIP and telephony companies.  We offer domestic and international
termination (in bulk) for fractions of the cost of other large providers.


## Our Teleconferencing Platform

Our teleconferencing platform is currently the main focus of my work.  It is a
pretty large system, which has been written using the latest tech and best
practices available.

Basically, we provide callers with their own dedicated phone numbers to use
(upon request), and set them up with a private web portal login to begin
managing and using our services.

The conferencing platform we've engineered offers a lot of cool features:

-   Each conference line provides a wide array of statistics for line owners.
    Things like caller usage statistics, detailed call traffic information, and
    real time call statistics and usage.

-   Each conference line can have an (almost) infinite amount of sub-conference
    rooms, which allows a single line to be used for millions of simultaneous
    conference calls all happening separately from each other.

-   Line owners can customize the sounds, music, and other audio features that
    are standard on conferencing systems (music on hold, etc.).

-   Line owners can perform various moderator actions on their conference
    lines.  This includes muting, unmuting, banning, unbanning, etc.

-   Lines can provide outbound toll-free calls from withing the conference
    rooms, so that multiple callers can participate in outbound calls if
    needed.

-   Private conference rooms that two callers can join exclusively for
    mandatory private conversations.

-   Loads of other fun and stuff.

We have hundreds of users online at any given moment, and are madly trying to
solve our growing pains and scale efficiently.


## Current Status

Since I started working on the project, we've made a lot of changes.

The single largest project has been re-writing the web portal.  We completely
scratched the old PHP (CGI) website we had, and replaced it with a dynamic,
high performance Django web portal that can scale across multiple servers and
databases very well.

We also setup a very cool system that allows our Asterisk servers to directly
communicate with our Django site to get rid of redundant code, and allow us to
provide a database independent API for basically all of our various
interconnecting services.

The next item on the TODO list is to modularize our Asterisk platform (more
details on this coming soon), and provide a truly awesome telephony core that
will be easy to maintain, bug fix, and provide features for.


## Life is Good

I've really been enjoying these past few months.  I've had a chance to build
some really awesome software, learn a lot of new techniques and best-practices,
and help architecture what I think will be some of the most elegant telephony
services in the world.

I'm really excited to be working on all of our new advances and software,
especially now that we have a very cool core platform that will allow us to
re-define traditional telephony services, and let us build rock solid, high
performance telephony systems.


  [Desk Sketch]: /static/images/2010/desk-sketch.png "Desk Sketch"
  [Fonality]: http://www.fonality.com/ "Fonality"
  [RCG's CEO]: http://www.chrisbrunner.com/ "Chris Brunner"
