---
title: "On Programming Deadlines"
date: "2011-06-23"
tags: ["programming"]
slug: "on-programming-deadlines"
description: "Programming deadlines are the stuff of nightmares.  Luckily, I've found some ways to make them a little less scary."
---


![Computer Sketch][]


There are a lot of differences between programming, and programming
professionally.  The most notorious of which, is deadlines.


## Deadlines

When you're writing code for yourself, you can spend as much (or as little
time) on it as you please--but when you're writing code for *other* people,
you've got only a limited amount of time and resources to get the job done.
In my experience, this typically leads to one of two situations:

-   You've got to extend the deadline to finish the job properly.
-   You've got to write some dirty hacks to finish the job.

If you've ever done professional programming, you know what I mean.  Very few
projects are agile enough to allow for both sufficient time and resources to
get the job done.  This leads to tough decisions for programmers.

No self-respecting programmer wants to deliver sub-par code; but it's difficult
to consistently deliver high-quality code when dealing with time obligations,
especially in professional environments where you're dealing with non-engineers
who don't necessarily understand the concept of technical debt.

Luckily, there are some guidelines you can follow to help minimize the amount
of 'hackery' you have to do when writing code on a deadline.  They aren't
necessarily quick-fixes, but can certainly be helpful to anyone who needs to
consistently push out top-notch code, day after day.


## Rule 1: Setup Continuous Deployment Before Writing ANY Code

This is a tip I picked up from [The Pragmatic Programmer][] book (definitely
required reading for any programmer).  Always, and I mean always, setup your
continuous deployment system before writing code.

What do I mean by continuous deployment?  Well, before you start coding your
project, you should have a system set up that lets you deploy your project code
into production (and preferably staging and development environments as well).
This way, as you write your code, you'll have the peace of mind that comes with
knowing your project can be deployed at any moment.

In a lot of programming work flows, this can save tons of development time.
Instead of `scp`'ing your project to some testing environment (or worse, coding
directly on a live server), you can just push your code to your preferred
source control system, and let your continuous deployment system take care of
the rest.  It may not seem like much of a time saver--but if you consider the
amount of time it takes, day after day, to copy your code over and do testing
manually, it can quickly add up and save hours of time each month.


## Rule 2: Write Tests First

If you've never heard of test-driven development (TDD), please read the
[Wikipedia article][] on it immediately.  If someone is paying you to write
software, and you've got a deadline, then you need to be practicing TDD at all
times.

The basic concept of test-driven development is that before writing project
code, you write a simple piece of code that tests your hypothetical project
code for desired behavior.  For example, let's say your project requires you to
write a function that adds two numbers, and returns the sum of these numbers.
Before writing that piece of code, you should write a test function,
`test_add_two_numbers`, that calls your `add_two_numbers` function with various
inputs, and verifies through assertions that the results you get back are
proper.

This may seem like a bit of a hassle, but it has numerous benefits:

-   Writing tests first help you clarify your application architecture.
-   You have the peace of mind that comes with knowing your code is
    operational.
-   You're able to easily refactor parts of your project without worrying about
    breaking code.
-   You can avoid releasing low-quality code, and tarnishing your reputation.

Writing tests certainly takes time and effort, but can save time in the long
run by avoiding emergency bug-fixes, system crashes, etc.  Especially when
you're on tight deadlines, you don't want the added stress and worry of buggy
code.


## Rule 3: Be Transparent

Transparency can be difficult to achieve (depending on your work environment),
but can be greatly beneficial.

In order to be transparent, you need to make sure that you have a clear line of
communication with the clients receiving your code.  You need to keep them
updated regularly as to what is being worked on, and how far along progress is.
Bonus points if you can continuously deploy your code to a staging system where
clients can view the unfinished project and see how it is changing day after
day.

If you're able to maintain transparency with your boss(es), they're much more
likely to be understanding if deadlines need to be pushed back.  Non-engineers
often don't understand software development, and view it as a black-box art.
By maintaining clear communication and transparency with your clients, and
getting them involved in the process, they'll be more understanding of your
work, and they'll feel happier about the product they're getting developed.


## Rule 4: Maintain Daily TODO Lists

Time management is definitely out of the scope of this article, but I will
mention that maintaining a daily TODO list is one of the best things you can do
as a programmer to ensure things are progressing forward at all times.

Software development is an immensely complex task.  It requires years of
practice, patience, and discipline to become a good programmer, and you are
never finished learning.  When writing software on a deadline, more often than
not, you're writing a complex system.  In order to keep your head clear, and
allow you the maximum amount of programming power, you should maintain a daily
TODO list consisting of each individual task that needs to be accomplished
(code-wise) in the day.

Don't make overly vague TODO items such as "debug sound problem", really think
it through, and write out the full task in numerous steps.  For example:

-   Write a unit test for the `load_soundfile` function that checks to see if
    mp3s are playable.
-   Write a unit test for the `load_soundfile` function that checks to see if
    wav files crash when loading.
-   Create new feature branch, `design_update`, to hold the new web design
    templates.
-   Update `style.css` using the new web design templates.

Having a clear list of actionable items gives you the power to focus on a
single task at a time, without having to balance 100 or so next-steps in your
head.  Writing software is complex enough already, don't make your life more
difficult!


## Rule 5: Do the Right Thing

There will undoubtedly be circumstances that arise which make you nervous and
uncomfortable.  Did you procrastinate yesterday and skip writing the unit tests
for your new features?  When these situations arise, don't go with your
instinct.  Instead--do the right thing.

Whether you need to double back and revisit some old code, write some more test
cases, or even delay a deadline--do it.  As a professional engineer, it's your
job to deliver working code consistently, even if that means you've got to make
tough choices.


## Conclusion

Being a software developer is no easy task.  Our world is filled with constant
challenge and hardship, and only our discipline and preparedness can help us
push through the hard times, and prosper in the good times.  Always use your
best judgement, and beat the deadlines by using steadfast engineering
practices, and never giving in to anything less.

You can do it.


  [Computer Sketch]: /static/images/2011/computer-sketch.png "Computer Sketch"
  [The Pragmatic Programmer]: http://www.amazon.com/gp/product/020161622X/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=020161622X&linkCode=as2&tag=rdegges-20 "The Pragmatic Programmer"
  [Wikipedia article]: http://en.wikipedia.org/wiki/Test-driven_development "test-driven Development Wiki"
