---
title: "CD"
date: "2013-05-14"
tags: ["programming"]
slug: "cd"
description: "Some thoughts on continuous delivery, and why it is awesome."
---


![Tron Light Cycle Sketch][]


There are certain practices every programmer learns at one point or another,
which greatly improve their productivity.  All the best productivity hacks for
programmers are obvious things (in retrospect), but sometimes having them
explained to you and presented in a direct way will trigger the *Oh yeah! I
should be doing that!* light bulb which eventually leads you to implementing
these practices.

Continuous Delivery ([CD][]) is one of those practices.

When I first *learned* about CD (via [The Pragmatic Programmer][]), the light
bulb clicked in my head.  While the concept is certainly not *special* in any
way -- after all, everyone knows and understands that automatically deploying
code you write into production is something that's possible -- it never really
hit home to me as being incredibly useful until I read the book and got the
full concept explained to me in simple terms.

CD is something every programmer should be using 100% of the time, without
exception.


## Preface

From the time I first learned about CD (~4 years ago) until last week, I
honestly never thought I'd be writing about the subject.  When I first learned
about the concept of deploying your code automatically into production, it
immediately seemed obvious to me why this was such a great idea, and I never
even questioned in afterwards.

The concept seemed so simple that I figured everyone *except* for me must have
known this all along, and that there was never a reason to share the practice
with anyone else since it's so obvious (in retrospect).

It wasn't until last week when I was working on a small work project, without
practicing CD, that I realized how annoying programming without CD is, and how
important it is that every programmer know about (and practice) CD for all
their projects, all the time.

With that said, here we go :)


## Continuous Delivery

The concept of CD is simple: each time you write code, it is deployed
automatically into your production environment.

This can mean a lot of things (so I'll elaborate).

Let's say you're writing a web application and using [Git][] to store your
source code.  If you wanted to start using CD, you'd need to set up your
environment such that each time you push code to your Git repository, that code
is automatically deployed to your web servers so that your new code is running
live.

Let's say you're writing some desktop software, something like iTunes -- In
this case, CD might mean that every time you push new changes of your code to
your Git repository, a new binary of your software is built, and distributed to
your download servers, such that all customers who are checking for updates
will automatically download the latest release.

Regardless of the type of software you're writing, CD has several enormous
benefits that will help you become a better (more productive) programmer.


### Don't Break the Build

One of the most obvious benefits of using CD is that it forces you to *not break
the build*.  This is something that (horrifyingly) seems to happen in
programming projects all over the world, which can (for the most part) be
easily solved with CD.

Let's say you're working on a project with three other developers.  Your goal is
to add a couple of features to the company website.  Each of you starts working
on one feature.

You notice that one of the developers has been pushing lots of code to your
[GitHub][] repository, but that all of his commits are breaking the main
website.  This is causing problems for you, as before you can push your changes
to GitHub, you have to merge his unfinished (broken) changes into your code,
which makes you unable to test your changes out to see if they're working or
not.

*Frustrating.*

When you're using CD, pushing broken code to your repository is unacceptable, as
these changes will be immediately deployed live (for the world to see!).

Imagine running an enormous website and pushing a change that crashes the site
and prevents you from getting 500,000 new visitors -- *that's a huge mistake*!

Using CD forces you to make small, functional, incremental changes to your
code base.  Not only will this practice ensure your code base is *always* in a
usable, working state, it will greatly improve the overall quality of your
project, reduce frustration in team settings, and force you to improve your
programming skills by always keeping your code base in working condition.

Maintaining a working code base is hard work!  But it's fun, challenging, and
extremely useful to all involved.


### Less Shit Work

Last week, I started working on a small project for work.  Specifically, I was
writing a web scraper which iterates over millions of web pages and downloads
the content in structured form.

When I started the project, I was aiming to get things going as quickly as
possible, and so, for the first time in a long while, I decided to just start
hacking the code locally on my laptop and ignore all the other stuff I normally
do (setting up CD, etc.).

Once I had a very basic program in working order, I created an [EC2][] server to
run my code, logged into the server, copied my new code over to the server, and
started running the scraper.

All was good!  ...  Until the next day.

The next day I realized I had forgotten to do some important type conversions --
the latitude and longitude data points I was scraping were being stored as
strings, which ended up feeding poor data into my consuming applications.

So, naturally, I:

- Went back onto my laptop and fixed the issue.
- Tested the change on my laptop.
- Opened up the EC2 web console to find the server credentials.
- Logged into the server I provisioned the day before.
- Manually copied my updated code over onto the server.
- Stopped the running copy of the old web scraper.
- Ran my new web scraper code.
- Logged out of the server.

All in all, that took about 45 minutes, 20 of which were spent moving my code
from my laptop back to the server and re-running my web scraper (and then making
sure it didn't crash).

Over the next several days, I ended up making several more changes to my web
scraper, each time requiring me to spend about 20 minutes deploying my code to
the server manually.

After the 5th day of this, I was dreading making anymore changes to the project.
It was then that I remembered one of the golden rules of software development:
*use CD*!

30 minutes later I had configured my CD software, [Jenkins][], to automatically
deploy my code every time I pushed changes to the project.  *What a relief.*

The rest of the week was a *lot* nicer.  In just 30 minutes I had automated 4
hours of manual labor -- that's a lot of time to save (for just 5 days of
work!).  Imagine how much time you can save using CD if your project is being
developed for weeks -- or months!

In addition to the removal of a lot of shit work from your day, you're also
freeing your mind up for more important tasks.

As I was working on my project, even though I spent about 20 minutes deploying
my code each time I made a change -- the reality is that those 20 minutes of
wasted time were probably more like an hour.  Each time I went to manually
deploy my new code I had to get *out of the flow* of my work to do the
deployment, then had to spend some time afterwards to get back *into the zone*
and resume whatever important task I was working on next.

Over the past 4 years or so, using CD in my projects has likely saved me from
thousands of hours of shit work, and greatly increased my personal productivity
on a day to day basis.


### Clear Value

Another (more public) benefit of using CD in your projects is that you're able
to clearly deliver value to whatever stakeholders you may have.

If you're building a project that customers use, for instance, each time you
push changes to your code your customers will see the fruits of your labor.  Not
only will they be seeing the value for which they're paying you quicker, but
they'll likely be more engaged with your product as they can see it evolve right
before their eyes.

If you're doing freelance work, using CD is an excellent way to clearly show
your customers exactly what they're paying for, and help prevent frequent
*update meetings* which are primarily a drain on time (for everyone involved).


## Continuous Delivery Suggestions

We've talked about why CD is great, and *hopefully* I've convinced you to start
practicing CD with all your projects.  If you've never before set up any CD
software, you're likely curious about how to do so -- so let's talk about that.


### Software Choices

You've got a lot of different options out there when it comes to setting up CD
for your projects.

At the simple end of the spectrum, your source control software probably
supports simple hooks (for instance: [Git Hooks][]).  Stuff like this will allow
you to write a small script that will fire each time you commit code to your
repository -- a great (simple) way to ensure that every time you push code, your
code is deployed live.

The downside to using simple hooks described above is that they'll frequently
slow down your work -- if I had to wait 5 minutes for my software to deploy each
time I committed code, I'd go insane!

A slightly more complicated (but not by much) approach is to use a service like
[Travis CI][].  Travis will automatically download your projects every time you
commit code, and then run a script to do stuff (usually run your unit tests,
etc.).  This gives you a relatively simple (free) way to deploy your code live
after each commit.  Neil Middleton wrote a [great post][] on the topic which you
can use as a guide.

At the end of the spectrum, you've got open source options like [Jenkins][].  If
you'd like to privately deploy code in as asynchronous a manner as possible,
Jenkins really can't be beat.

To use Jenkins, you'll need to install it on a server, then use the Jenkins web
interface to add each of your projects and configure them.  Much like Travis CI,
Jenkins will download your code after each commit, and then run arbitrary
commands on your code to run tests, deploy it, etc.

For all my work, I tend to use Jenkins to automatically deploy my projects, as
it's cheap (free), reliable, and easy to configure.


### Other Resources

If you're looking for other resources which talk about CD in depth, you may want
to give the following books a read -- they're extremely great books, and I'd
highly recommend them to any software developer who hasn't already read them:

- [The Pragmatic Programmer][]
- [Continuous Delivery][]
- [Continuous Delivery and DevOps][]
- [Continuous Integration][]


While the concept of continuous delivery is a simple one, it's an extremely
practical, simple, and useful tool that every programmer should have in their
arsenal.  The next time you start a project, be sure to get continuous delivery
working from the very beginning, and save yourself from a lot of wasted time.


  [Tron Light Cycle Sketch]: /static/images/2013/tron-light-cycle-sketch.jpg "Tron Light Cycle Sketch"
  [CD]: https://en.wikipedia.org/wiki/Continuous_delivery "Continuous Delivery"
  [The Pragmatic Programmer]: http://www.amazon.com/gp/product/020161622X/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=020161622X&linkCode=as2&tag=rdegges-20] "The Pragmatic Programmer on Amazon"
  [Git]: http://git-scm.com/ "Git"
  [GitHub]: https://github.com/ "GitHub"
  [EC2]: https://aws.amazon.com/ec2/ "Amazon EC2"
  [Jenkins]: http://jenkins-ci.org/ "Jenkins CI"
  [Git Hooks]: http://git-scm.com/book/ch7-3.html "Git Hooks"
  [Travis CI]: https://travis-ci.org/ "Travis CI"
  [great post]: http://www.neilmiddleton.com/deploying-to-heroku-from-travis-ci/ "Deploying to Heroku from Travis CI"
  [Continuous Delivery]: http://www.amazon.com/gp/product/0321601912/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=0321601912&linkCode=as2&tag=rdegges-20 "Continuous Delivery on Amazon"
  [Continuous Delivery and DevOps]: http://www.amazon.com/gp/product/1849693684/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=1849693684&linkCode=as2&tag=rdegges-20 "Continuous Delivery and DevOps on Amazon"
  [Continuous Integration]: http://www.amazon.com/gp/product/0321336380/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=0321336380&linkCode=as2&tag=rdegges-20 "Continuous Integration on Amazon"
