---
title: "Some Thoughts on Bitcoin"
date: "2013-04-28"
tags: ["bitcoin"]
slug: "some-thoughts-on-bitcoin"
description: "I started using Bitcoin a while back, here are my thoughts."
---


![Thinking Mask Sketch][]


Last month I started actually *using* bitcoin for the first time.  I've used it
in the past, but never had any serious interest in the stuff until recently.
Since I'm a relatively new bitcoin user (and software developer), I thought I'd
share my thoughts about bitcoin at this early stage, for any of you with similar
backgrounds and interest in bitcoin.


## Why I Decided to Give it a Try

I've been hearing about bitcoin since it was first mentioned way back in 2009.
At the time, I read some of the introductory articles explaining bitcoin (what
it was, how it worked, etc.), but almost immediately dismissed it as a passing
fad until sometime around 2010 when a lot of my programmer friends started
using bitcoin as a hobby and urging me to try it out.

After a month or so of hearing about it from friends, I downloaded the official
bitcoin client and gave it go, but had a really difficult time figuring out how
to use bitcoin for anything practical, how to back up my wallet, and a bunch of
other things.  If I remember correctly -- I mined bitcoin for a short time then
abruptly stopped using bitcoin and lost interest -- until last month.

What really inspired me to give bitcoin another try was all the recent tech
interest in bitcoin.  Over the past several months I've read countless articles
on bitcoin, seen a wide variety of new companies sprouting up offering bitcoin
services, and have heard more and more about bitcoin from strangers who are not
only using bitcoin for hobby purposes, but as a real alternate currency.

So, I decided to give it another go.


## My Experience Getting Started

Getting started with bitcoin last month was a *lot* easier than it was back in
2010 when I tried it initially.

The first thing I did was visit the [official bitcoin website][] and download
the official [Bitcoin-Qt][] wallet program, which allows you to send and receive
bitcoin from a variety of addresses.

After getting this set up, I created a new bitcoin address through the client
UI, and started my first Google search for *free bitcoin* :)  My reasoning at
the time was that: I'm still not sure whether I'm going to actually be using
bitcoin for anything, so why bother spending money on the stuff?  Might as well
see if there's a way to get a few free bitcoin and play around with the system.

Unfortunately, this is where things went from *good* to *messy*.  Most of the
sites I found under the *free bitcoin* search phrase were filled with ads,
scammy popups, and a variety of other eyesores that led me to question their
legitimacy.  After a couple of hours scouring the internet, I learned that this
is actually extremely common, and most of the *free bitcoin* sites are
essentially ad farms that pay you microscopic amounts of bitcoin in hopes that
you'll eventually miss a click and hit one of their ads.

So, after figuring out that these sites were, in fact, legitimate -- I ended up
getting my very first bitcoin payment (worth fractions of a cent), from:
[Daily Bitcoins][], one of the more reputable free bitcoin sites -- all I had to
do was fill out a captcha check and wait a few hours!

Over the next few days I read more about bitcoin, found more of the legitimate
free bitcoin sites, and filled out a ton of captcha checks to see deposits come
in -- it was actually pretty fun.


## Attempting to Buy Bitcoin

After I had some free bitcoin in my wallet, I decided to purchase a couple of
real bitcoin.  Unfortunately, this process was not nearly as easy as I thought
it would be.

I had assumed that since bitcoin had become so popular over the past couple of
years, there would be plenty of easy ways to buy (and sell) bitcoin without a
hassle -- how wrong I was.

The first thing I tried was using [Mt. Gox][], one of the largest (and oldest)
bitcoin exchanges.  Unfortunately, after I created an account I was greeted with
two big hurdles to overcome:

- An enormous red message telling me I must verify my account before I can use
  the service,
- An incredibly time consuming (and privacy destroying) process of entering my
  social security number, birthday, photos of my driver's license, and a bunch
  of other documentation as well.  If I hadn't been referred to Mt. Gox as being
  the largest and most reliable bitcoin exchange, I would have certainly figured
  it was a scam to get personal information.

Once I filled out their lengthy verification process, I was then informed it
could take anywhere up to 10 business days to have my account manually verified,
and that I couldn't use the service until the process was completed.  Boo :(

So, instead of going that route, I created an account with a new bitcoin
exchange I had recently heard about (backed by [ycombinator][]): [Coinbase][].

Coinbase allowed me to buy bitcoin almost instantly after creating an account,
by simply verifying my bank account.  Once that processed was finished (it only
took a few minutes), I put in an order for 3 bitcoin, and was greeted with a
friendly message telling me my order had been placed, and the bitcoin would be
in my account within 7 days (apparently Coinbase operates off some internal
delay for reasons of which I'm not aware).

A week later, I had my three bitcoin :)


## Playing With Bitcoin

After I got a few bitcoin, and played around with some of the sites and services
available, I immediately wanted to build some applications that use bitcoin (in
some way) to get a better feel for the currency.  While I still haven't really
accomplished this goal (you'll see what I mean below), I have gotten a lot more
familiar with the usage of bitcoin, and its properties for developers.

The first project I built was a command line bitcoin interface, [btc][], which
uses Coinbase's official API and allows users to buy, sell, and transfer bitcoin
in their terminal.

I use the command line all the time, so I figured this would be a good small
project to take on to help me get more acquainted with bitcoin usage, and fill a
software void at the same time.

The next tool I built was a very simple website:
[http://www.bestfreebitcoin.com/][], which is essentially just a curated list
of the best free bitcoin sites that allow you to earn bitcoin for doing work, or
filling out captcha checks.  Since I had such a hard time finding this stuff as
a new bitcoin user myself, I thought other new users might find it helpful as
well.

While I've still got some other bitcoin services I'd like to build in the near
future, I've learned quite a bit through playing around with existing services,
building some simple ones myself, and getting more involved in the bitcoin
community over the past few weeks.


## My Overall Impression of Bitcoin

After using bitcoin (buying, selling, and purchasing services with it) for a
little over a month, I've come to like bitcoin.

While it certainly isn't ready for mass market consumer usage due to lack of
services and supporting tools, it's definitely reached a point where the
currency is usable (clearly has value, has lots of press attention, is gaining
adoption, etc.), and it looks like it will be around for a long time.

While I can't predict the future, if I had to guess, I'd guess that in the next
couple of years there will be an enormous amount of growth around the bitcoin
ecosystem: new companies, simpler services, and more mainstream usage.

I can certainly envision a future in which a majority of people (at least in the
US) are familiar with bitcoin, and have at least a small amount of bitcoin
currency which they use for making online purchases, as using bitcoin to make
online purchases reduces a lot of the complexity associated with making online
payments now (PCI compliance, etc.).


  [Thinking Mask Sketch]: /static/images/2013/thinking-mask-sketch.jpg "Thinking Mask Sketch"
  [official bitcoin website]: http://bitcoin.org/en/ "Bitcoin Website"
  [Bitcoin-Qt]: http://bitcoin.org/en/download "Bitcoin-Qt"
  [Daily Bitcoins]: http://dailybitcoins.org/index.php?aff=edcd9fb07dcd67c574bee2b1c26ec781 "Daily Bitcoins"
  [Mt. Gox]: https://mtgox.com/ "Mt. Gox Bitcoin Exchange"
  [ycombinator]: https://news.ycombinator.com/ "YCombinator"
  [Coinbase]: https://coinbase.com/ "Coinbase"
  [btc]: http://rdegges.github.io/btc/ "btc - Command Line Bitcoin Client"
  [http://www.bestfreebitcoin.com/]: http://www.bestfreebitcoin.com/ "Best Free Bitcoin"
