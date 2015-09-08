---
title: "Transparent Telephony - Part 1 - An Introduction"
date: "2009-08-31"
tags: ["programming", "telephony", "asterisk"]
slug: "transparent-telephony-part-1-an-introduction"
description: "The first part of my new series introducing technical folk to Asterisk and telephony."
---


![Telephone Sketch][]


So you've probably heard the word telephony thrown around from time to time.
Maybe you were hanging out in a certain IRC channel, wanted to root your cell
phone, or maybe, just maybe, you were actually interested in doing something
cool with your computers and phones.

This article is the first of a series.  I'm going to try my best to explain what
telephony is, how it works, and how to write cool programs that integrate voice
and data.  Telephony is a huge market, and used everywhere (think cell phones).
We are living in a time when telephony is casual, common, and popular.  While
being so huge, it often astounds me to think of how few programmers and tech
people ever get around to learning about it, or playing with it.  There are
very few telephony programmers, and even less proper documentation.  My hopes
are that these articles will give you a solid foundation in telephony and
inspire you to play around with it on your own, and do cool things.

Now that we've got the basics out of the way, let's get down to business...


## PSTN

Before we get into any setup or detailed information, we need to cover the
global network which allows interconnection between telephones.  This is
referred to as the PSTN (public switched telephone network).  The PSTN is much
like the Internet as it provides a system of routing to move calls from one
phone to another.  Traditionally, the PSTN consisted of analog devices and
relays which carried voice from phone A to phone B, but in recent years the
PSTN has been increasingly digitized.

The digital circuit in the PSTN is a 64 Kbps channel, and all audio is
digitized at 8 kHz.  That is, the highest quality voice you can get while
making phone calls across the PSTN is 8 kHz (horribly low compared to a
standard mp3, most mp3s are sampled at 48 kHz).

When you place a call from a home analog line, your call is sent to your LEC
(local exchange carrier) who then routes your call accordingly through the PSTN
to the desired destination.  Details beyond this point are not necessary for
the purposes of this article, but there is a lot of interesting information on
Wikipedia regarding the history and development of the PSTN.


## Connecting to the PSTN

There are many ways to connect to the PSTN.  Chances are, you've probably only
seen / used a few on a regular basis.

That phone sitting in your parent's house, hooked up to that analog line (or
maybe DSL) is a standard POTS (plain old telephone service) line.  These are
used all over the place, pretty much everyone uses these as 'house lines', and
many small businesses use them as well to get basic phone / fax service.

The next most popular way to connect to the PSTN is mobile lines (cell phones).
Everyone has a cell phone now-a-days.

Next we have T1 / E1.  These are primarily business lines, and are dedicated
for voice communications.  The T1 is the American version, and the E1 is the
European version.  T1 / E1 lines can carry 24 calls over them, which is what
makes them very appealing to businesses.  It's also a lot cheaper to use a
dedicated T1 / E1 line as opposed to purchased 24 separate analog lines.

A PRI / BRI line is very similar to a T1 / E1 line, except that it supports 23
calls max, and can handle more traffic due to it having a dedicated data
channel for performing call setup and tear downs, as well as passing caller ID
and other information, making it more efficient.  Again, the PRI is the
American standard, while the BRI is the European standard.

VoIP (voice over IP) is a relatively new way to connect to the PSTN using the
Internet.  VoIP is extremely low-cost compared to other methods, and very easy
to setup as it only requires an active Internet connection to use.  More and
more businesses are switching over to VoIP for cost reasons.

These are the basic types of lines people use to connect to the PSTN.  There
are others, but I don't think they are worth mentioning here.  Most businesses
use T1 / PRI lines because they are reliable.  VoIP is a great way to get phone
service, but is still a very new protocol.  One large problem with VoIP is
reliability, as it depends on the Internet for routing traffic.  This of course
causes problems as businesses who lose Internet connectivity will be unable to
place and receive calls, unlike analog or dedicated digital lines.

I personally use VoIP for everything: my home lines, programming, business
stuff, and everything in between.  I'd highly recommend that if you want to
experiment with telephony and programming, that you get a VoIP line (I'll cover
all this later).


## Phone Servers (PBXs)

A PBX (private branch exchange) is a device which provides phone service to
phones on a private network.  Think of a PBX as a router, it connects
telephones together to form a private network, and acts as a portal allowing
PSTN access for phones that it serves.  PBXs will be the focus of almost all my
future articles, as they are what allow us to do cool stuff with telephony.

There are tons of different kinds of PBXs.  Pretty much every business has a
PBX, or pays a company to host a PBX for them (just google PBX and you'll see
what I mean).  Why does anyone need a PBX?  Well, PBXs provide different
services to the phones it has connected to it.  Most PBXs offer services like:

-   Voice-mail.
-   Extensions (give each user a private phone number, kinda like a private
    IP).
-   Call forwarding (users can forward calls to their cell phones).
-   Auto attendants ('Welcome to My Company, press 1 for sales, 2 for support,
    ...').
-   Routing for phone numbers (you can have multiple phone numbers, and route
    them to different phones).
-   Paging and intercom ('Sale on soup on aisle 5').
-   Call recording.
-   And many other things.

The neat thing about PBXs is that they aren't as complex as you would think!
They are just computers, loaded with special software, and fully programmable.
Some of the most popular PBXs are Cisco, Avaya, and Asterisk. Cisco and Avaya
are proprietary and expensive, whereas Asterisk is free and open source.
Asterisk also supports all of the features of the proprietary PBXs, and many
more.


## Open Source Telephony With Asterisk

Back in 1999, Mark Spencer created Asterisk.  It's a free, open source PBX
system that is easily installable and usable on any Linux based operating
system.  Since it's creation, it has become one of the largest, most used PBX
systems in the world.  I'm a pro with Asterisk, and we will use it as our
official PBX for all of my tutorials.  You will master it.  Asterisk can
provide reliable call routing for thousands of calls simultaneously, which
makes it ideal not only for small business usage, but for medium, large, and
even enterprise usage.

In additional to being a great free PBX, Asterisk has also created a huge
market.  Tons of companies sell Asterisk-based phone systems to people, and
many more sell custom programs and setup services to businesses looking to save
money by going open source.

For programmers (like most of you), Asterisk provides many great features for
developing your own telephony applications.  Stuff like the AGI (asterisk
Gateway interface), AMI (Asterisk manager interface), dialplan (Asterisk core
scripting language), call files, and many other features.  I'll cover all of
these items later in this series.

As you've probably guessed, Asterisk makes integrating voice service with
pretty much anything else a breeze.  This is one of the reasons why Asterisk is
so powerful, and why telephony rules.  Not because it's 'cool' to talk on the
phone, but because we can integrate so many other things with it.


## Putting it All Together

Now that we've covered the core components that make telephony work, let's see
how it all works together in a nice diagram :) Excuse my horrible art skills,
this is the best I could come up with:

![PSTN Diagram][]

The PBX connects to the PSTN and acts as a gateway for all phones and programs
running on it to connect with the outside world.  The PBX provides services and
routing for calls via whatever PSTN connection you are using (PRI / BRI / T1 /
E1 / POTS / VoIP).


## Neat Things You Can Do With Telephony

When I first started learning about telephony, it was for my work, and I didn't
find it all that interesting.  That is, until I learned all the cool things
that you can do with it.  So I've listed some things below which are just basic
examples of things you can do (through simple telephony programming).  If you
have any interest in this stuff, be sure to read the rest of this series, and
*pwn* telephony!

-   Spoof your caller ID.
-   Change your voice.
-   DoS phone lines (cripple a business' phone line).
-   War dialing.
-   Snoop on other people's phone calls.
-   Encrypt phone conversations.
-   Automatically call people.
-   Add functionality to your cell phone (record calls, spoof numbers, reboot
    your home router, open your garage door, etc.)
-   Send text messages for free, receive text messages and do stuff based on
    the messages.
-   Setup advanced auto attendants.
-   Create conference calls.
-   Place / receive video calls.
-   Make international calls for cheap / free.


## Sounds Cool, What Next?

Dive right into the action.  The next article in the series will cover setting
up your very own Asterisk PBX system.  I'll have detailed setup information,
and we'll walk through a complete installation step-by-step.  You don't need a
dedicated computer for this (even though it does make things a bit simpler),
all you'll need is an Internet connection, and about 1 hour for setup.


## Motivation

My motivation for writing this series is to get people involved in the
telephony world.  There is a huge lack of telephony programmers, and as a
result, there aren't that many cool telephony-based services.  Also, the
phreaking scene has all but completely died off, and I think it is time to
reinvent the telephony hackers underground!


  [Telephone Sketch]: /static/images/2009/telephone-sketch.png "Telephone Sketch"
  [PSTN Diagram]: /static/images/2009/pstn-diagram.png "PSTN Diagram"
