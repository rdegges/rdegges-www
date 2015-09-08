---
title: "How Hard Can You Work?"
date: "2013-07-18"
tags: ["personal development", "programming"]
slug: "how-hard-can-you-work"
description: "Here's a trick to getting through those boring days at work: see how hard you can possibly work.  Make it a game."
---


![Shark Sketch][]


Lately I've been rereading one of my favorite books of all time:
[The Passionate Programmer][].  While every page of this book contains an
important lesson, I wanted to write about a particular one today.

**NOTE**: If you had to pick one book to read to become a better programmer (and
person), [The Passionate Programmer][] would be my recommendation.  Every
programmer should own a copy -- it's that good -- seriously.

Anyhow, onto the story.

I've been writing code since I was a kid.  When I first got started, I had zero
knowledge, and everything I learned was exciting and new.

As I've continued writing code and developing as a programmer over the past 13
years, I've had the opportunity to play with lots of different technologies,
learn new methodologies, and practice building lots of different tools.

It seems that over time, as I've learned new things, I've also become more and
more *elitist* when it comes to what I'm working on.  What I mean by this is
that instead of being content working on a simple project, I tend to quickly
rush my work when I'm finishing simple things, and instead focus all my *real
effort* on building parts of systems that I find interesting.

This has led to a bunch of problems:

- I feel frustrated and annoyed that I have to work on *simple problems* in my
  projects.
- I rush my work when doing simple tasks, leading to lots of bugs and poor
  quality code.
- I spend an inordinate amount of time working on a single part of a project
  (the core, complex part) and pay much less attention to polish and other
  important user-facing project components as they don't seem all that
  interesting technically.
- I end up losing interest in projects after getting the core functionality
  built, which leads to project decay and rot.

Obviously, the above are pretty bad.  I've spoken with lots of programmer
friends about this as well, and it seems that I'm not the only one who has this
problem.

Everyone I've spoken to about this (without exception) has had the same
experience after their first few years developing software -- it almost seems
natural that once you've learned something, it's just *not that interesting*
anymore and it becomes a chore to continue doing the same sorts of things over
and over again.

But, even though it may be natural to become a bit of a *software snob*, it's
definitely a problem that each programmer needs to tackle if they want to
continue making progress in this field -- programming isn't a field where you
can selectively pick and choose what you work on all the time, it's just not
possible.

Every project is going to require code to be written, and not all of that code
will be the most interesting thing in the world -- so if you'd like to continue
to up your skill set and deliver good products, you need to take a different
approach to your work once you've hit this roadblock.

This is where a mindset shift becomes necessary.

If you're experiencing any of the above problems, there is really only one good
solution.  You've got to ask yourself: **How hard can I work?**

The trick is to make your work a game.  The next time you need to build out a
simple part of a project, instead of feeling annoyed that you have to do it and
rushing your work, instead treat it as a personal challenge: *how good can I
possibly do this?*

This is a great way to keep yourself motivated for the task at hand, and allow
you to increase your skill set by giving even the simplest of tasks 100% of your
development effort.

Here are some simple things you can do to really challenge yourself regardless
of the complexity of a project, and ensure that you're not going to frustrate
yourself and do a poor job.

**Draw sketches of your project's functionality and architecture before getting
started.**  Go into detail and make sure you've laid things out in the most
optimal way possible.  This is a great way to ensure your systems will be
scalable and fault-tolerant -- and also forces you to think of the best possible
way to build your project.

**Try writing 100% test driven code.**  This is a great way to improve your TDD
chops, improve your internal APIs, and verify you've got no bugs in your code.
A good test suite also serves as great documentation for any future developers
looking at your code, and will earn you a great reputation among your peers.

**Automate testing and deployment.**  I find that a lot of the time, for simple
or basic tasks, I tend to do a lot of one-off process runs without putting much
thought into deployment and automation.  By automating your testing and
deployment (even for simple tasks) you'll work out any kinks in your
bootstrapping process, documentation, and re-usability.  This will also save you
(and your teammates) a lot of time in the long run, by avoiding any manual
intervention.

**Write great project documentation.**  This is especially true for internal
projects, where you know that not many people will be looking at your code in
the future.  By forcing yourself to write great documentation you'll not only
make your code more useful in the future, but you'll make maintenance easier,
and have something nice to show any higher ups who are wondering what you're
working on.  Writing great documentation also gives you a chance to think of
your code like a user would -- and improve your communication skills by clearly
and simply describing what your code does, and how to use it.  I've found that
many times, writing project documentation gives me a whole new perspective on my
project and helps me identify things I can do to simplify functionality,
usability, etc.

**Track execution metrics and stats.**  If the project you're working on
involves anything that has business value, you should consider hooking your
code up to a dashboard type service which aggregates important metrics (I like
[Ducksboard][]).  This can give you (and any other stakeholders) insight into
how well things are running, how much value your code is delivering, and how
much your project is being used.  Other than being a great motivator (*who
doesn't like seeing the fruits of their efforts?*) it's also a great way to
increase your skill as a developer and strategic leader by carefully monitoring
your development work.

I've found that by practicing the above strategies and asking myself, **How hard
can I possibly work on this?**, I've come to enjoy even the simplest of tasks
and dramatically improve not only my day-to-day happiness when working on
projects -- but also deliver more value with my work and greatly improve my
skill set, one day at a time.

The next time you're working on a project and feel frustrated that you have to
do some simple work, really push yourself to see *how good of a job you can do*,
and make a difference.


  [Shark Sketch]: /static/images/2013/shark-sketch.jpg "Shark Sketch"
  [The Passionate Programmer]: http://www.amazon.com/gp/product/1934356344/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=1934356344&linkCode=as2&tag=rdegges-20 "The Passionate Programmer"
  [Ducksboard]: http://ducksboard.com/ "Ducksboard"
