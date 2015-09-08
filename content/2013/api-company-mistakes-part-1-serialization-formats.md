---
title: "API Company Mistakes - Part 1 - Serialization Formats"
date: "2013-03-25"
tags: ["programming", "startups"]
slug: "api-company-mistakes-part-1-serialization-formats"
description: "Some mistakes I've made while building my API company, OpenCNAM."
---


![Angry Dragon Sketch][]


Over the past few years I've been spending more and more time building and
working with web APIs.  To me, APIs are absolutely fascinating, and they've
quickly become my favorite branch of technology to work on.

Last year, I even built a quite successful API company ([OpenCNAM][]), which
allows developers to easily get Caller ID data.  I've also built a good number
of other APIs over the past several years:

- An API that allows users to create, edit, and modify teleconferencing
  chat rooms.
- An API that allows users to instantly create an ephemeral PostgreSQL database
  ([postgression][]).
- An API for compressing HTML pages.
- An API for storing, approving, and displaying programming quotes.
- And quite a few others.

Through my experiences, I've had some successes and some failures.  Each time I
bring these points up with friends, they always tell me to *write about it*, so
I thought it'd be interesting to chronicle my mistakes here in hopes that
you'll learn from my mistakes.


## The Story

This first lesson comes from my experiences building [OpenCNAM][] last year.

When I started working on OpenCNAM, my goal was to make the simplest, easiest to
use Caller ID API in the world.  If you're at all involved in the telephony
world, you probably know how complex something so simple can be.  While
retrieving Caller ID data sounds straightforward, due to legal issues and big
companies, there were practically no options available to developers before
OpenCNAM.

Anyhow, after I built out the initial minimum viable product (MVP) and launched
it to the world, I started getting lots of user email asking for various bits of
functionality.

You see, initially I had tried to keep things simple and had OpenCNAM return
only JSON responses.  Soon after launch, I got several email from developers
asking for other serialization formats: XML, JSONp, and YAML.

Not wanting to let potential users down, I immediately got to work and quickly
added support for the serialization formats listed above, as well as several
others (an HTML format to make users testing queries in their web browser
happy, and a plain text format to make integration with certain phone systems
simpler).

Unfortunately, these additional serialization formats ended up causing numerous
problems, one of which was that various third party libraries I used to support
these formats had issues:

-   The XML library was clunky.  Instead of requiring me to add a line of code
    to output my object as an XML object, I had to spend a full day figuring
    out that I needed 30 additional lines of code to properly build the XML
    tree response manually.  Ugh.
-   The YAML library had conflicting dependencies with my web application, which
    took a long time to debug and eventually caused me to revert back to an
    older version (with less documentation).

In addition to my annoyance of working with the above third party libraries, I
also realized that many users were mistakenly using the HTML serialization
format on accident in production (after having tested it out in their web
browser), which ended up generating a lot of support emails from users confused
that their applications were displaying HTML error messages when Caller ID data
couldn't be found.

After answering many support email and rewriting my developer documentation to
sufficiently explain the new serialization formatting options, I also noticed
another discouraging problem with my newly supported formats: almost nobody was
using them!

Despite initial email I received asking for XML, JSONp, and YAML formatting
options, I noticed that they were getting very little usage.

Which brought my to my realization: *I've made a big mistake*!  I wasted several
days (and lots of time) adding support for numerous serialization formats that:

- Confused my users.
- Made my documentation much more complex for the average user.
- Were very rarely used!

My first thought was to just remove the new serialization formats, clean up my
code base, and simplify things.  After thinking this through, however, I
realized that one of the largest mistakes an API company can make is to remove
previously advertised functionality (why would developers trust you to provide
data to them if you're so quick to remove functionality?).

My final decision was to endure the annoyance I had created for myself, and
maintain the serialization formats I'd created, despite their added
complexities.


## The Lesson

What you can take away from my mistake is simple: if you're building an API
company, try to keep things as simple as possible.  In my case, I should have
simply picked a serialization format and stuck with it (e.g. JSON), especially
since JSON is becoming more and more ubiquitous in the web API world, and other
formats are slowly dying out.

While serialization formats are sure to come and go, it's a far better idea to
pick one and go with it for a while than it is to attempt to keep everyone
happy and support everything under the sun.

Having a more restricted feature set will make your product code simpler, your
product documentation simpler, your client libraries much simpler, and will most
definitely save you a headache or two.


  [Angry Dragon Sketch]: /static/images/2013/angry-dragon-sketch.png "Angry Dragon Sketch"
  [OpenCNAM]: https://www.opencnam.com/ "OpenCNAM - A Simple Caller ID API"
  [postgression]: http://www.postgression.com/ "A PostgreSQL Database for Every Test Case"
