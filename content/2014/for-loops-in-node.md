---
title: "For Loops in Node"
date: "2014-09-23"
tags: ["programming"]
slug: "for-loops-in-node"
description: "A story in which I discover that writing simple for loops in Node.js isn't always so simple."
---


![Plague Sketch][]


As of late, I've been spending a fair amount of time writing Node.js code.
While I'm not a huge Node.js fan (*yey Python + Go!*), I find myself liking some
parts of the language quite a lot.

Over the past few months I've been working on a *really awesome* authentication
library for Node.js: [express-stormpath][], and have learned quite a lot about
Node as I've been working on it more and more.

Today I'd like to share a short, personal story with you, about my frustrating
experience trying to do something simple.


## The Story

Here's how it started: two weeks ago I was writing a web scraper for
[thepiratebay][].  My idea was simple: I wanted to get a JSON dump of all
torrent information available, so that I could later use it for some simple
data analysis.

After taking a look at the site, I realized that the simplest way to scrape all
the existing torrents would be to just loop through all integers, querying each
one sequentially -- this is because TPB allows you to access torrents via their
integer ID (*which is always increasing*):

- http://thepiratebay.se/torrent/1
- http://thepiratebay.se/torrent/2
- http://thepiratebay.se/torrent/3
- http://thepiratebay.se/torrent/...

The rules are simple: if you get a 404 skip it -- if you get a 200, the torrent
exists and can be scraped!

So, I sat down and wrote a first version that looked something like this:

```javascript
var request = require('request');

for (var i = 0; i < 10000000; i++) {
  request('http://thepiratebay.se/' + i, ...);
}
```

This is some pretty basic stuff:

- Iterate through numbers?  *CHECK!*
- Make HTTP requests?  *CHECK!*

But to my dismay, after running for a few minutes I noticed that this small
program was eating *all the RAM on my laptop!*  But why?!

I realized that Node.js blocks when running blocking code (*eg: a for loop*) --
but I figured that since I was making async requests from within things would
continue to work normally.

I was wrong.

So, being confused about what was happening, I decided to dig a bit deeper.  I
narrowed my case down to a simpler test:

```javascript
for (var i = 0; i < 10000000; i++) {
  console.log('hi:', i);
}
```

But alas, the same problem.  The program simply runs for a few minutes, then
crashes as it uses all the RAM on my computer.  Bummer.

So then I started Googling around to find potential solutions.  Surely this must
be a common issue?

Unfortunately, however, I didn't see much discussion about this, and all the
relevant Stack Overflow threads proposed solutions that didn't require looping
at all (*not an option in my case*).

Next, I turned to [async][] -- the really popular flow control library for Node.
After looking through the docs, I realized there was something that was
seemingly perfect for this!  The [forever][] construct! 

So I then tried the following:

```javascript
var async = require('async');

var i = 0;
async.forever(
  function(next) {
    console.log('hi:', i);
    i++;
    next();
  },
  function(err) {
    console.log('All done!');
  }
);
```

But again -- the same issue.  After a few thousand loops: crash.

After writing quite a few different iterations of this simple program, and a
significant amount of lost sleep (*I can't really sleep well knowing I don't
understand something -- grr*) -- my coworker [Robert][] proposed a working
solution:

```javascript
var Abstraction = function() {
  this.index = -1;
};

Abstraction.prototype.getIndex = function getIndex() {
  this.index++;
  return this.index;
};

Abstraction.prototype.isDoneTest = function isDoneTest() {
  return this.index > 10000000;
};

var list = new Abstraction();

function iterator(){
  var i = list.getIndex();
  console.log(i);
  if(list.isDoneTest()){
    clearInterval(interval);
  }
}

var interval = setInterval(iterator,1);
```

Brilliant!  I didn't even think of `setInterval` for some reason.

Anyhow: after a lot of discussion -- we both came to the agreement that using
`setInterval` is essentially the only way to solve this problem.

After thinking about this some more, I decided to write a small abstraction
layer to handle this -- so I created [lupus][].

`lupus` provides simple (*albeit, basic*) asynchronous looping for Node.js:

```javascript
var lupus = require('lupus');

lupus(0, 10000000, function(n) {
  console.log("We're on:", n);
}, function() {
  console.log('All done!');
});
```

Whatever you end up writing inside of the loop (*blocking or not*) -- `lupus`
doesn't care.


## The Moral

Performing asynchronous for loops in Node.js turned out to be quite a lot harder
than I expected.  I find it odd that it's so easy to crash my programs with the
simplest of looping examples.

Oh well!  Live and learn!


  [Plague Sketch]: /static/images/2014/plague-sketch.jpg "Plague Sketch"
  [express-stormpath]: https://docs.stormpath.com/nodejs/express/ "express-stormpath"
  [thepiratebay]: http://thepiratebay.se "The Pirate Bay"
  [async]: https://github.com/caolan/async "asyncjs"
  [forever]: https://github.com/caolan/async#forever "asyncjs forever"
  [Robert]: http://www.robertjd.com/ "Robert"
  [lupus]: https://www.npmjs.org/package/lupus "node-lupus"
