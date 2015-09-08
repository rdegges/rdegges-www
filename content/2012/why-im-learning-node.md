---
title: "Why I'm Learning Node"
date: "2012-04-07"
tags: ["programming", "javascript", "nodejs"]
slug: "why-im-learning-node"
description: "I'm learning node.js because not only is it awesome, but it's a great way to improve my Javascript chops while concurrently writing backend code.  It's a two for one deal."
---


![Ninja Warrior][]


As many (if not all) of you know, I'm a Python guy.  I program every single
day, and most days, that involves using Python.  I write Django code for fun
and profit, and also do a fair amount of "raw" Python coding (no frameworks).

Unfortunately, while I do a lot of kick ass back end coding, I don't often get
a chance to practice my front-end kung fu.  Since I'm fairly knowledgeable
about the back end stuff I work on (telephony services, web services, etc.), it
doesn't often make sense for me to also build the front end code (I'm looking
at you: HTML, CSS, Javascript).  As a result of this lack of front-end coding
practice, I suck at it.

I suck at HTML, CSS, and most of all, Javascript.

Over the past few years, my lack of front end knowledge has really began to
bother me.  I enjoy doing full-stack development.  I like taking projects from
conception to completion.  Something about the creation process resonates
really well with me.  What I don't like, however, is feeling crippled when I
have an idea, write the back end for it, and then have to spend months fiddling
around with the front-end to make it look even half decent.

Since I first started writing websites, Javascript has really changed a lot.
While Javascript used to be a toy language for moving navigation elements on a
page, it's now usable everywhere: server side (nodejs), client side (backbone),
and even in the database (mongo).

So, after many years of not properly learning Javascript--I decided to take it
seriously and dive in.  My goal is to become a proficient Javascript
programmer, so that I can:

-   Use some of the new Javascript frameworks and tools that are out there
    (node, backbone, knockout, etc.).
-   Contribute to Javascript projects that I like.
-   Write my own Javascript code (server side and client side) without feeling
    like an idiot.
-   See what all the fuss is about.

Since I'm already familiar with programming concepts, the first thing I did was
pick up the highly recommended book: [Javascript: The Good Parts][].  I read
through that a few weeks ago, and subsequently failed to find a good way to
apply my newly found Javascript knowledge to anything practical.

**NOTE**: If you're an experienced programmer looking to learn Javascript, you
probably can't do any better than reading [Javascript: The Good Parts][].
It's extremely short, concise, and enjoyable to read.  Highly recommended.

To actually practice my newly learned Javascript-fu, I decided to give
[nodejs][] a try.  Since I learn best by writing command line applications
(who actually enjoys reloading their browser to test code?), I figured node
would be a good choice.

If you aren't familiar with node (why are you reading this?), it's a
server-side Javascript interpreter.  That means you can use it just like
Python, ruby, or perl--directly from the command line (no browser required).
It also comes with an extremely elegant package manager ([npm][]), that makes
building and sharing reusable node modules extremely simple.

After reading so many [negative things about nodejs][], I'm completely
surprised to report that it is actually pretty damn cool.  While I'm not
(currently) using it for building websites or anything like that, it really
makes Javascript a lot simpler for people like me: back end developers who want
to learn Javascript without all the barriers to entry (I'm looking at you, web
browsers).

node has a great package manager, tons of extremely awesome modules, a large
developer community, and great documentation.  I was able to write my first
reusable nodejs module ([node-opencnam][]) in less than 1 hour.  That's pretty
insane.

I went from 0 knowledge of nodejs to a working, publicly available, reusable
module, in less than 60 minutes.  Booya.

After playing around with nodejs a bit, I've decided to continue learning it.
So far it has been extremely useful in my quest to learn Javascript, and as
I've continued to build things using it, I've been slowly getting more and more
familiar with Javascript as a language.

As I learn more about Javascript, I'll keep you all updated!

**NOTE**: I'm going to start reading through the [Node Beginner Book][] this
weekend.  You should check it out.


  [Ninja Warrior]: /static/images/2012/ninja-warrior.png "Ninja Warrior"
  [Javascript: The Good Parts]: http://www.amazon.com/gp/product/0596517742/ref=as_li_ss_tl?ie=UTF8&tag=rdegges-20&linkCode=as2&camp=1789&creative=390957&creativeASIN=0596517742 "Javascript: The Good Parts"
  [nodejs]: http://nodejs.org/ "nodejs"
  [npm]: http://npmjs.org/ "npm"
  [negative things about nodejs]: http://teddziuba.com/2011/10/node-js-is-cancer.html "nodejs is cancer"
  [node-opencnam]: https://github.com/telephonyresearch/node-opencnam "node-opencnam"
  [Node Beginner Book]: http://www.nodebeginner.org/ "Node Beginner"
