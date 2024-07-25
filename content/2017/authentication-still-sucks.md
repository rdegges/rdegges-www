---
aliases:
  - "/authentication-still-sucks/"
date: "2017-08-29"
description: "Authentication hasn't improved much in the last several years.  Here's the current state of things."
slug: "authentication-still-sucks"
tags:
  - "business"
  - "programming"
title: "Authentication Still Sucks"
---


![Upset Owl Sketch][]


I currently own 47 domain names. I know it sounds like a lot, but that's down
quite a bit from my all-time high of 78 ~two years ago.

I'm constantly thinking about fun websites and businesses to build; I can't help
it. For the last ten years or so, I've probably acquired around ten domains per
year as a way to satisfy my never-ending need to build silly things.

My most shameless domain name purchase (as my wife will gladly tell you) was
back in ~2010 when I purchased the subtly named "checkonoldpeople.com". At the
time, it was around 4am and I was hyped up on Rockstar (no-carb) energy drinks.
I thought I had a revolutionary idea: a simple website that would call your
aging parents for you automatically (using Twilio's API) once per day, prompting
them to press "1" if they were still alive. Tactful, I know.

I wish I could tell you I didn't spend the next two days building out the
service; but I won't lie to you: I did.

Several years ago I was scrolling through a credit card statement and couldn't
help but gulp when I saw my yearly domain renewal bill. I think seeing the
numbers there in that black-and-white PDF are what put really my insanity into
perspective for me. After that experience I was finally able to let several
dozen expire (including "checkonoldpeople.com").

Most of the projects I start building are motivated by some small online void.
Here's how it happens:

- I'm working on a real-world project trying to figure something out
- I come across a solution and start implementing it
- Once I'm done implementing it, I wonder why it was so hard to figure it out in
  the first place
- This is where I immediately start thinking of project names, buy a domain
  name, and spend a minimum of one full night locked away hacking on the idea

It's a vicious cycle.

The funny part of the whole thing is that 99% of these projects never see the
light of day. 99% of them never have a single user (other than myself). You
might think someone who is that driven and motivated would surely launch more
than a few websites after so many years of building things: but you'd be
incorrect.

For the most part, once I've found a reasonable working solution to my problem
and built out the core functionality of the service, I struggle to finish the
"other stuff" that makes projects and businesses successful:

- Allowing users to sign up for the service
- Building a polished website
- Handling billing (for paid services)
- Covering all odd edge-cases that a user might run into (404 pages, mobile
  design, etc.)

My typical workflow (as a backend developer) is to get the core functionality
working, then refactor relentlessly until it meets my personal quality
standards. After that's done, I'll start working on the customer facing website.

This is where I run into problems. Every. Single. Time.

After I throw together a basic bootstrap template, I choke when designing the
user flows:

- User registration
- User login
- Password reset
- User permissions

You know: authentication and authorization.

It's something that "sounds" so easy to do, but always ends up frustrating me in
every possible way. I'm surprised more people in the software world don't
complain about it.

If something so fundamental and so critically important to almost every single
website was as incredibly hard to implement and figure out as authentication,
you can bet your ass there'd be half-a-million [r/programming][] and
[Hacker News][] threads about it in a heartbeat.

If you woke up tomorrow and discovered that something as simple as implementing
a contact page on your website took more than 40 hours to implement, you'd
probably freak out.

"What is going on?! Why is this so hard? I thought this only took a minute.
FUCK!"

That's the way I've been feeling about authentication for the last 15 years or
so. Over all the time I've spent programming, authentication and authorization
are still as complex as ever. Maybe even moreso.

Back in the day, the only sort of authentication you really had to worry about
as a developer was simple username/password authentication to a webpage. The
idea was relatively simple:

- A user will send you their username/password
- You hash the user's password (to keep it safe), and store it in a database
- When the user logs in, you compare their username/password with the username
  and hashed password in the database to log them in

While you still had to worry about things like database security, SSL, password
hashing, etc. -- the concept was at least easy to grasp and understand.

Nowadays things are significantly more complicated. For any given project you
might need to authenticate:

- A user to a simple server-side web page
- A user to a client-side web page
- A user to a third party provider (like Facebook, Google, etc.)
- A program to an API

Each form of authentication requires different trade-offs, and potentially
costly decisions.

Logging a user into a traditional server-side web page is mostly a solved
problem. Web frameworks support secure user sessions, user serialization, and
lots more. Depending on the programming language/web framework you're using,
however, you might be in for a lot of work. Not every language/framework is
created equal.

If you're a Node.js developer, for instance, you'll likely find that trying to
authenticate a user into even the most simple web application can become a
painful experience in low-level security concepts.

Most Node applications use the [passport library][] to handle authentication,
and end up:

- Setting up and configuring their own session support
- Hashing their own user passwords
- Writing their own user serialization/deserialization logic
- And lots more

It seems insane to me that in 2017, if I want to build even a simple website
that supports user registration and login, I'm still required to know and
understand low level authentication concepts as well as implement these concepts
in a secure and reliable way to protect the most critical data in my
application: my users' personal information.

And that may not sound like a lot of work at first: I'm certainly guilty of
thinking that. There have been many occasions where I've said to myself:

"Oh, that doesn't sound so hard! I know a decent amount about security! I'll set
up my session library, I'll use the bcrypt hashing algorithm, I'll write my user
serialization code. I can get that working in a few hours!"

But what happens when you start implementing everything and realize:

- There are numerous options for session libraries, many of which support
  different configuration options, hashing algorithms, and encryption options --
  which one is the right choice?
- Your choice of hashing algorithm will need to be set to the correct "work
  factors" to prevent brute force attacks with current hardware constraints, and
  that in a year or two this algorithm will need to be upgraded transparently to
  prevent security issues?
- Your user model changes and breaks your serialization code, so you then need
  to modify it?
- You realize you need to implement password reset functionality, so you plug in
  an email API provider like [Mailgun][], create your
  templates, and write the logic to securely enabled password reset?
- You realize you need to support login via other mechanisms than just plain old
  username/password, so you start plugging in Facebook login, Google login,
  etc., each of which takes a reasonable amount of effort to get started and
  maintain over time?
- You realize you need to also authenticate users to your mobile app, and begin
  researching OAuth2 and OpenID Connect, looking for solutions that allow you to
  run a secure OAuth2 server, while at the same time making it easy to
  authenticate users to this new server?
- Etc... I could endlessly list all the authentication issues I've ran into.

And that doesn't even begin to cover the massive surface area that authorization
covers -- namely, how do you assign user permissions, groups, and roles in an
efficient and secure way? How do you segment user data into different "tenants"
to keep customer information logically (or physically) isolated?

What I'm getting at is this: almost every time I sit down to build the
authentication and authorization piece of my websites, mobile apps, and API
services, I get overwhelmed.

Even when I'm building projects using a "complete" framework like Django that
gets me 90% of the way, I still have a number of concerns to worry about:

- How do I expose my users to other services in my backend?
- How do I handle "user flows" like requiring a user to click an email link to
  verify their account? Or reset their password?
- How do I handle multi-factor authentication across a variety of channels?
  Yubikey? SMS? Google Authenticator? Etc.?
- How do I enable single sign-on for my users into *other* applications?
- How do I enable single sign-on for *other* application users *into* my
  application?

And the list goes on and on.

It doesn't matter what programming language I use -- the experience is more or
less the same: I (as a developer) am expected to implement a ton of redundant
logic that is mission-critical, deals with highly sensitive information, and can
result in massive business losses if I screw it up.

I think that is unreasonable.

And that is why, almost four years ago now, I joined a tiny company called
[Stormpath][].

At the time, I had just spent a year building and maintaining my own
authentication API service internally for a company project, and had learned a
ton about modern web security along the way. I really enjoyed working on it, and
web security quickly became one of my favorite subjects.

When I ran into the Stormpath founders at a tech conference in SF, I initially
thought they were a weather company -- but what they told me was much more
interesting than the weather: they were building the first developer focused
authentication-as-a-service company.

I was floored.

I thought about my past experiences building this stuff myself, and how much I
learned and struggled along the way. I thought about how much time and effort
I'd put into authentication and authorization problems, and how much I
underestimated them. After just a single conversation, I knew I had to get
involved.

I reached out to the Stormpath team and told them why I'd be a good addition,
and why I  *needed* to join the crusade.

Before I knew it I was spending my days building open source security software.
I was having a blast! As we continued to iterate on the Stormpath core API
service, the developer libraries, and everything else that makes a developer
service great (docs, tools, support, etc.), we started to see some real
traction!

Developers enjoyed using our service. When they plugged our Flask library into
their Flask web apps, it solved *almost* all of their authentication problems.

Things weren't perfect, of course, but I was really proud of the tools we made,
and was proud that our service allowed us to simplify authentication and
authorization issues for so many developers around the world.

Now, for the sad part of the story.

Back in February of this year, Stormpath (the API service I had spent years of
my life caring for and nurturing) was acquired. Everyone on the team was unsure
of whether this was a good or bad thing.

When we joined forces with [Okta][], we were nervous. Okta
acquired us to help build our initial Stormpath vision into a much larger and
more scalable company, but most of us were afraid (at least I was).

I was afraid that we'd have to start over from scratch, and try to rebuild the
great technology we already had. I was afraid that we'd ruin the goodwill we'd
built with developers worldwide over the past few years, and burn our bridges.
And more than anything: I was afraid that we'd lose the ability to build
something truly magnificent: *an authentication and authorization API service
that is built FOR developers BY developers*.

Since the acquisition, we've all gone through a lot.

We've made good decisions and bad. We've struggled to build and rebuild tools,
libraries, documentation, and more. But through all the sleepless nights we've
put in over the last six months, we've never compromised on one thing: the
original vision.

This is why I'm genuinely excited to announce that today, we're officially
re-launching the *new and improved* [Okta Identity Platform][].


![New Okta Developer Site][]


Everything has been molded to our vision, and we're aiming to do something we
could not before: build the world's largest authentication-as-a-service platform
for developers of all shapes and sizes.

The new Okta Identity Platform is our attempt to make authentication and
authorization problems a relic of the past. We want to provide beautiful
developer libraries across every programming language and framework to make
adding things like...

- User registration
- User login
- Password reset
- Social login
- Single Sign-On
- API authentication
- And lots more

...a thoughtless five minute task.

Okta handles things like user credential storage, password hashing, data
isolation, best practices, etc. If you use one of our new developer libraries,
we'll do our very best to solve all your user management problems.

While the Okta service isn't perfect, and certainly has some rough edges, it's
something we're all incredibly passionate about, and working hard every single
day to improve. It will get better.

So today, it's exciting to start fresh. I'm happy to have a second chance to
build something that I love and care about.

For me, this is personal. I'm still working on fun side projects, and I'm still
struggling through authentication problems. I won't be satisfied until Okta
fills the void that exists in the web world right now, and provides the absolute
best platform for developers of all different types to scratch their user
management itch.

This means we're building the service to cater to actual developers of all
types: students, hobbyists, 10pm - 4am hackers (like myself), startups, and even
large enterprises. We're aiming to build an extremely low-cost, usage-based
service that anyone can use without the need to commit to expensive plans and
upsells. We want to make something that WE would want to use in our next passion
project.

For applications with fewer than 1,000 active monthly users, this means the
service will be absolutely free. For applications with more active users than
that, we've got inexpensive usage-based plans.

I think it's time for authentication to no longer suck.

I'm happy to say that myself (and the rest of the former Stormpath team) will
still be working on what we love most, and doing our absolute best to build
something that we hope you will love as well.

Anyhow, thanks for hearing me out. If you're interested in trying out the new
Okta Identity Platform that I've been working on with the rest of the team,
please [sign up today][] and [hit me up][] if you've got questions, comments,
or feedback.

Finally, if you'd like to follow along with the Okta journey, we're doing
everything we can as transparently and publicly as possible. We've recently
started writing on the [Okta developer blog][], and tweeting through our
[Okta Developer][] account. If you're interested in seeing what it takes to
launch a service like this, and how we're improving things, you may find those
interesting!


  [Upset Owl Sketch]: /static/images/2017/upset-owl-sketch.jpg "Upset Owl Sketch"
  [r/programming]: https://www.reddit.com/r/programming/ "Reddit Programming"
  [Hacker News]: https://news.ycombinator.com/ "Hacker News"
  [passport library]: https://github.com/jaredhanson/passport "Passport.js"
  [Mailgun]: https://www.mailgun.com/ "Mailgun"
  [Stormpath]: https://stormpath.com/ "Stormpath"
  [Okta]: https://www.okta.com/ "Okta"
  [Okta Identity Platform]: https://developer.okta.com/ "Okta Identity Platform"
  [New Okta Developer Site]: /static/images/2017/okta-developer-screenshot.png "Okta Developer Screenshot"
  [sign up today]: https://developer.okta.com "Sign Up For Okta"
  [hit me up]: https://twitter.com/rdegges "Randall Degges on Twitter"
  [Okta developer blog]: https://developer.okta.com/blog/ "Okta Developer Blog"
  [Okta Developer]: https://twitter.com/oktadev "Okta Developers on Twitter"
