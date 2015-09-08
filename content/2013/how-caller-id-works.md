---
title: "How Caller ID Works"
date: "2013-12-18"
tags: ["telephony", "programming", "startups"]
slug: "how-caller-id-works"
description: "An in-depth look at how Caller ID works.  TLDR: Caller ID is horribly broken and totally sucks."
---


![Demon Horse Sketch][]

Oh man.

I don't do this often, but, I'm going to do a bit of ranting >:)


## Why?

I've been working with telephony stuff for almost 5 years now, and have a
pretty decent understanding of how things work.  Truth be told: the entire
telephony industry is one huge hack.  All the big players are using old
technologies and standards which are frustrating to work with, and cause loads
of unnecessary grief for anyone working with stuff!  **Ugh!**

I'm also quite invested in this topic.  Almost two years ago I started an API
company ([OpenCNAM][]) which makes getting Caller ID information easy for
developers.

Since I've been doing this for a while, and have seen almost every imaginable
problem and roadblock, I figured it'd be nice to get all this off my shoulders,
and share some interesting technical information with the rest of the internet
at the same time.


## What is Caller ID?

Caller ID is an old telco standard for NANPA countries (any country whose phone
numbers begin with a +1):

- US
- Canada
- American Samoa
- Bermuda
- Guam
- Northern Marianas
- Puerto Rico
- Sint Maarten
- US Virgin Islands

Essentially, the standard (which doesn't seem to be published anywhere on the
internet *sigh*) says that every assigned phone should have a Caller ID string
which is represented as a 15 character, ASCII string.

The way this works is simple.  Every phone company (think Verizon, T-Mobile,
AT&T, etc.) maintains a database that contains three columns:

- phone number
- Caller ID
- private? (yes / no)

So, each time a phone company gets a new customer and assigns them a phone
number, that phone company is responsible for collecting the user's name and
inserting it into their central Caller ID database.

The idea is that if each carrier has a Caller ID database, then when people make
calls to and from one another, this information can be used to display the
Caller ID name of the person making the call -- this way the called party can
see who is calling them.

**NOTE**: Caller ID works differently in other countries, so I'm only going to
cover the NANPA stuff (which applies to all US readers).


## How Caller ID is Stored

Now that you've got a very high level understanding of what Caller ID is, let's
talk about how it is stored.

When phone companies sign on new customers, they insert the new user's Caller ID
into a [LIDB][] database.  Each carrier typically has their own LIDB database
that centrally stores all Caller ID for a given company.

For simplicity's sake, you can think of an LIDB database as a relational
database (think PostgreSQL).  Now, in actuality, I have no idea what underlying
technologies power an actual LIDB database -- I can only guess.  The reason for
this is that there is *no information* on this technology anywhere online (as
far as I can tell) -- and all the books I've read on the subject seem to skip
this bit of information.

The important part is that LIDB databases are where Caller ID information is
stored.

Now, here's the thing -- since there are so many different phone companies
around the US (and Canada) -- including many rural (small) phone companies,
what's ended up happening is that many of the little guys have done one of two
things:

- Decided not to maintain any LIDB database records at all.
- Decided to outsource their Caller ID data to an LIDB provider -- a company
  which provides a single LIDB database and stores Caller ID for numerous
  different providers themselves.

Now, as you can see, the above two points have caused a lot of side effects:

- Each carrier is no longer guaranteed to have an LIDB database of their own.
- When calls are made, the location of the Caller ID data is now tricker to
  find.
- Some phone numbers will never have Caller ID since some phone companies don't
  have the staff / ability to handle that stuff.

I'll get into these points more later on, but it's important to understand what
is happening.


## Final Thoughts

Caller ID is a horribly old, legacy standard that is hard for both consumers and
businesses to use and work with.  Furthermore, all of the Caller ID players
(with the exception of [OpenCNAM][]) are only making the problem worse, and
causing further pain in the industry.

Got any questions?  Feel free to [shoot me an email][], would be happy to help.


  [Demon Horse Sketch]: /static/images/2013/demon-horse-sketch.jpg "Demon Horse Sketch"
  [OpenCNAM]: https://www.opencnam.com/ "OpenCNAM - A Simple Caller ID API"
  [LIDB]: http://en.wikipedia.org/wiki/LIDB "LIDB Database on Wikipedia"
  [shoot me an email]: mailto:r@rdegges.com "Randall Degges' Email"
