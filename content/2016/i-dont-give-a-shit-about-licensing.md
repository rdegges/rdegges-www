---
aliases:
  - "/i-dont-give-a-shit-about-licensing/"
date: "2016-07-14"
description: "Software licensing is stupid. Let's take a look at why."
slug: "i-dont-give-a-shit-about-licensing"
tags:
  - "programming"
title: "I Don't Give a Shit About Licensing"
---


![Sad Stick Figure Sketch][]


Every now and then I'm reminded of just *how much* I hate software licensing.
Instead of doing what I normally do and silently complaining to myself, I
figured I'd mix things up a bit and write a good old fashioned rant >:)

A few days ago I got an email from a developer working at some enormous
corporation:

> Hi Randall,
>
> I am trying to use your flask-dynamo project at &lt;big corporation here&gt;.
> Can you please tell me what license this code is written under?  I need to
> send it to the legal department before I can use it.
>
> Please advise.

I've changed the wording slightly here, but hopefully you get the idea.

Now...  This is a perfectly valid question.  This guy works for some big company
that has very strict policies, and needs to know whether or not my code can be
*LEGALLY* used at his workplace.

That's all fine and dandy, except for one thing: I simply don't care about
licensing.  If you told me I had to choose between picking up dog shit all day
or having another conversation about software licensing, I'd happily go pick up
dog shit.  That's how much I hate licensing.

I find the whole discussion around software licensing to be completely
pointless.  It's one of the stupidest, most awful, and most incredibly redundant
conversations in the entire tech world.  And why is that?  Well...

It's redundant because it just DOESN'T FUCKING MATTER.  If you can already
find or view my code, then guess what -- you have the ability to use it!
Whether I want you to or not, you can already view my code, so copying pieces of
it (*or the whole fucking thing*) is totally possible.

Even if I decide to put a license on all my Github projects that says:

> COPYRIGHT Randall Degges.  Nobody else in the world is legally allowed to use
> this code or copy it in any way, shape, or form. Otherwise I'll sue you.

It just doesn't matter.

I simply refuse to believe this developer works at a company where his boss
constantly reviews every single commit he makes, googling each line of code,
checking to see where he might have copied it from, and whether or not it is
legal.

**NOTE**: If you do work at a place like that: do yourself a favor and resign.
There are so many places to work where you can leave an impact, get paid
sufficiently well, and not be treated like a child.

As a developer, the very thought of having to ask permission to use a piece of
code you can find freely online is insane.  I mean, how many ways are there to
do something, after all?

There's really only a couple of ways to write a for loop, increment an integer,
and store some data in a database.  Everything else is just details.

The idea of having some public code that's legally unusable is akin to a writer
not being able to use a dictionary while writing.  It just doesn't make any
sense at all.

I mean -- I understand the other side of this too: you write some code and you
don't want anyone to use it!  It's your project, after all.  You thought of it,
you wrote it, and you can license it however you want to stop whoever you want
from using it, right?

It sort of makes sense when viewed from that angle: if you're the creator of
something, you should have control over it!

But let's get real for a minute: if you build something and you don't want other
people to use it, the solution is a lot simpler than licensing: just don't
fucking make it publicly accessible!

Spend some damn time ensuring your code is stored privately, and not easily
accessible.  Keep it on locked down servers, use Github Enterprise, or for
fuck's sake: just run your code as a service and charge people money to use it!

All of those are fine options.

But whatever you do, don't bother publishing it online with a stupid license
that tells other people they can't use your code, because guess what: I'll use
your code.  I'll use it, and I won't even bother to check the license.  *And I'm
not the only one.*

This is what makes the internet great.  The ability to share information with
anyone, instantly, without restriction.  As developers, we should be on the
absolute forefront of encouraging this sort of thing.

After all: everything we do is built on top of thousands of layers of
abstraction of the programmers that came before us.  It's our job to contribute
forward and ensure that the next generation of developers can build cool and
powerful things in a simple way.

And the only way that will ever happen is if we all get our heads out of our
asses, and stop acting like we own thoughts and ideas.

Programming is a creative endeavour.  If you can't stand the idea that something
you spent time and energy creating and putting onto the *public internet* can
be used by anyone else for free, then maybe this isn't the right field for you.

Programming, by its very nature, is something that's meant to be shared.  The
amount of complexity needed to build modern applications would not be possible
without a tremendous amount of publicly accessible code.

Instead of viewing the code you write as *"your property"*, you should instead
look at it as your child.  When you create some code, you release it in the
world, and hope that it grows up to be useful to other people in some way.  You
don't keep it locked inside, and selfishly control all access to it.

It might bring you some happiness, some sorrow, and a lot of things in between:
but it's your *ethical* responsibility to let it out into the world and let it
make its own mark.

<hr/>

The next time you decide to publish some open source software, I'd encourage you
to seriously consider what software license you choose.  If you'd like to ensure
as many people as possible can use your code without restriction, then either:

- Use a public domain license like [UNLICENSE][], or
- Don't include a license at all.

By releasing your software into the public domain, you're consciously making a
decision to make your software truly public.  You're giving ANYONE who can find
your project the right to use it however they want.  This means they can copy
a piece of it, or the whole thing.  They can even copy it and say they wrote
it.  In short: anyone who gets a hold of it can do absolutely anything they
want with it.

And...  If you have an existing project that's been released under another
license?  Maybe it's time to consider changing things.  Releasing your code into
the public domain not only helps the corporate developers who want to use your
software: it helps the entire development community world wide.

**NOTE**: If you are a developer trying to use a project inside a big company,
and you actually care about what license a project has, please spend a minute
actually *looking* in the project to see what license it has before blindly
emailing the author of the project.

&lt;EOF&gt;


  [Sad Stick Figure Sketch]: /static/images/2016/sad-stick-figure-sketch.png "Sad Stick Figure Sketch"
  [UNLICENSE]: http://unlicense.org/ "UNLICENSE"
