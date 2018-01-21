---
aliases:
  - "/how-the-eu-cookie-law-affects-authentication/"
date: "2018-01-22"
description: "The EU Cookie Law has had a massive negative impact on website security. Here's why."
slug: "how-the-eu-cookie-law-affects-authentication"
tags:
  - "programming"
  - "security"
title: "How the EU Cookie Law Affects Authentication"
---


![Cookie Monster Sketch][]

Over the last few years you might have noticed banners like this one popping up on a lot of web pages:

![EU Cookie Law Banner][]

These banners are a direct result of the passage of the EU directive, sometimes
known as the Cookie Law, back in 2011. The EU passed this directive to improve
consumer awareness about how their data is being used by websites and give
consumers the option not to participate in the data collection and tracking
practices that many websites utilize.

The Cookie Law got its name because at the time a majority of the data websites
collected about users was stored in cookies.

Unfortunately, there's a lot of confusion and misinformation in the developer
community around the EU Cookie Law and how it applies to *web authentication*, a
topic that I care deeply about. =)

After all: if you need to log users into and out of your web application, you
*have* to store session information someplace. Does this mean if you're storing
authentication information inside a cookie you need to display the EU Cookie Law
banner on your website?

Today I'm going to clear up any misconceptions you might have about the law and
explain exactly what you need to know to be in compliance.


## The Cookie Law Isn't About Cookies

![Cookie Monster Cookie Sketch][]

The first thing we need to talk about is cookies.

As crazy as it may seem, **the EU Cookie Law has absolutely nothing to do with
cookies**. Shocking, right?

The EU Cookie Law is about storing any data about a user that isn't strictly
necessary for the operation of your website, regardless of where that data is
stored.

For instance: let's say you're building an online store like Amazon. Before a
user can purchase goods, they are required to create an account. When a user
creates their account with you, you log them in with a session cookie.

In this scenario, your website is using a cookie to do something that's required
for your website to operate, so no cookie banner is needed.

If you then decided to add a marketing tool for analytics tracking such as
Google Analytics, Kissmetrics, Optimizely, etc., you would now be collecting
and storing user information in a non-essential way, so you would then need to
implement a cookie banner on your site to remain compliant with the EU Cookie
Law.


## Who Does the EU Cookie Law Apply To?

![Confused Elmo Sketch][]

Legally speaking, the EU Cookie Law only applies to companies and websites owned
by a person or entity who resides in an EU country.

However, if your company is based in the EU or has an EU subsidiary then you are
required to comply with the EU Cookie Law if your website is primarily targeted
at an EU audience. This means that if you're an EU company running a website
that only serves US customers, you are exempt.

To sum it up: the EU Cookie Law only applies to you if you have a presence in
the EU and your website targets EU visitors.


## Is Local Storage Exempt from the EU Cookie Law?

![Elmo Waving Sketch][]

The biggest myth floating around the developer world right now regarding the EU
Cookie Law is that if you decide to store non-essential user information in HTML
local storage as opposed to cookies, then you are compliant with the EU law and
don't need to worry.

This is, of course, completely false.

Regardless of where you store user information for purposes like tracking and
marketing, you are only compliant if you show a cookie banner on your website.
Just because the EU Cookie Law has “cookie” in the name, it doesn't mean that
using an alternate place to store information will make you compliant!


## The Biggest Problem with EU Cookie Law Myths

![Oscar the Grouch Sketch][]

The biggest problem I see as a developer entrenched in the security world is
that many web developers are compromising their website security in massive ways
through their misunderstanding of the legislation. Let me explain.

A majority of the developers I've spoken with over the last few years mistakenly
believe that:

- User authentication data (session information) falls under the EU Cookie Law
  for regulation
- If they store session information in HTML local storage instead of cookies,
  they can get around the law entirely

Mixing these two pieces of misinformation together creates a dangerous recipe
that has the potential to dramatically affect the security of many websites in
the EU.

Here's where the root of the problem lies: developers trying to outsmart the EU
Cookie Law by storing their user's session information in HTML local storage
instead of cookies.

**NOTE**: My worry here is not unfounded. There are many, many websites in the
EU *right now* that are following this pattern and are not only
out-of-compliance, but are also risking major security breaches of their user's
personal information.

The problem is that **HTML local storage is not a safe place to store sensitive
information like a user's session data**. HTML local storage is designed to be
accessible to client-side Javascript code, which puts you at risk for
[cross-site scripting attacks][] (XSS) which just so happen to be one of the
most common attacks ([pdf][]) (and one of the hardest to prevent!) across the
entire internet!

In short: when handling sensitive information like user session info, you must
always store that data in cookies (with the [httpOnly][] and [SameSite][] flags
set). If you don't, you're opening yourself up to a massive surface area of
potential attacks, all of which have the capacity to allow attackers access to
your most sensitive information: user details.


## EU Cookie Law Summary

It's unfortunate that the EU Cookie Law is named like it is. The name of the law
has confused tons of developers across the EU and is responsible for a lot of
misinformation about compliance.

Please make sure that you do the following things if you're an EU website owner
running a service targeted at EU visitors:

1. Only store session information for your users in cookies (not local storage!)
   with the [httpOnly][] and [SameSite][] flags set
2. If you have any services on your website that collect non-essential user
   information (usually marketing and advertising tools) in any way (via local
   storage, an API, cookies, etc.) *then* you are required to display a cookie
   banner on your site

If you follow the two rules above, you'll be OK.


  [Cookie Monster Sketch]: /static/images/2018/cookie-monster-sketch.jpg "Cookie Monster Sketch"
  [EU Cookie Law Banner]: /static/images/2018/eu-cookie-law-banner.png "EU Cookie Law Banner"
  [Cookie Monster Cookie Sketch]: /static/images/2018/cookie-monster-cookie-sketch.jpg "Cookie Monster Cookie Sketch"
  [Big Bird Sketch]: /static/images/2018/big-bird-sketch.jpg "Big Bird Sketch"
  [Confused Elmo Sketch]: /static/images/2018/confused-elmo-sketch.jpg "Confused Elmo Sketch"
  [Elmo Waving Sketch]: /static/images/2018/elmo-waving-sketch.jpg "Elmo Waving Sketch"
  [Oscar the Grouch Sketch]: /static/images/2018/oscar-the-grouch-sketch.jpg "Oscar the Grouch Sketch"
  [cross-site scripting attacks]: https://www.owasp.org/index.php/Cross-site_Scripting_(XSS) "Cross Site Scripting OWASP"
  [pdf]: https://www.owasp.org/images/7/72/OWASP_Top_10-2017_%28en%29.pdf.pdf "OWASP Top 10 List"
  [httpOnly]: https://www.owasp.org/index.php/HttpOnly "httpOnly Cookie Flag OWASP"
  [SameSite]: https://www.owasp.org/index.php/SameSite "SameSite Cookie Flag OWASP"
