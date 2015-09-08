---
title: "The Time I Accidentally Destroyed a Production Server"
date: "2011-04-30"
tags: ["programming", "devops"]
slug: "the-time-i-accidentally-destroyed-a-production-server"
description: "The story of the time I accidentally destroyed a live production server, and how I managed to recover from the disaster without too much bloodshed."
---


![Horseman Sketch][]


Over the past few years or so, I've learned a lot about software in
professional settings.  I learned that software development is not always all
it's cut out to be.  There are lots of points where software development will
make you want to rip your hair out, light it on fire, and then dance around the
fire screaming curse words.

Here's a story I've been saving up for a while.  It's a tale of the time I
accidentally destroyed a production server.  I hope you enjoy it :)


## What I Did

When I first came on board at BTS over year ago, I was working on production
servers.  We didn't have any development or staging environments set up at the
time, so I was a bit nervous.  We also didn't use any version control at the
time, so there was nothing to be done in case of emergencies.

In case you're not aware of what BTS does, we operate and build telephony
services of all sorts.  At the core of our software is the logging of phone
calls (stuff like `timestamp`, `duration`, etc.), which allows us to bill our
clients and telephone companies.  The way we handle this mission-critical
logging is via [freeradius][].  We have all of our telephony servers hooked up
to freeradius, so that it can take the call data and log it to our back end
databases for later retrieval and billing purposes.  This typically worked
great, and we had no issues with it.  However, if freeradius went down, it
meant that we'd not be collecting payment information, and would therefore lose
lots of money.

At the time, I was working on setting up new freeradius servers.  I had spun-up
two new [Rackspace][] servers: `r0` and `r1`.  The old radius server was named
`rad` I believe.  My plan was to install the latest and greatest version of
freeradius on `r0`, duplicate the setup to `r1` as a backup, point our servers
at the new primary and backup radius servers, and get rid of the old one.

I had three terminal windows opened side-by-side: `r0`, `rad`, and `r1`.  At
the time, I thought it made sense to have my reference (the original box) in
the middle of my other two windows, so I could easily switch focus to either of
the two new servers without shifting my eyes over two windows.

So after a while of reading the latest freeradius documentation, I start
installing the new version on the two new servers.  Then I go grab a glass of
water, and come back.  As I'm sitting down, I type:

```console
$ aptitude -y update
$ aptitude -y safe-upgrade
```

To update the new `r0` server before installing freeradius.  As I'm watching
the updates run, I notice that there are way too many updates for this to be
normal.  I frantically look at the system `hostname`, and realize that I just
updated the *only* production freeradius server.  Panic ensues.

It's about this time that I remember the version of freeradius running in
production was 1.x, which was completely incompatible with the later 2.x
versions that I had just accidentally upgraded to.  The config files were
different, and there was completely different documentation (*infact, the 1.x
versions had no official documentation*).  Now I'm panicking even more.

I then log into our database server and check to see if call records are still
being added--they are.  *Whew*.  No information lost yet.  Thankfully, the
update didn't replace any configuration files or restart the process.

So I frantically read through the documentation and default configuration files
for the new 2.x release I had just installed.  I sit down for literally 4 hours
straight intently staring and the screen and trying new configuration options.

Eventually I get the new freeradius server running 2.x configured as close as
possible to the way our old 1.x server was configured.  I sweat, and update the
call servers to point to the new radius server.

To my amazement, *it fucking works*.  We're back online, logging calls, and no
data was lost.  I then duplicate the working setup to `r1`, make tons of
backups of my configs, then get rid of the old freeradius server.


## What I Learned

-   No matter what, you always, **always** need to have a proper development
    environment.  If you don't, you're committing suicide.
-   Version control everything.  If you join a project with no version control,
    don't convince yourself that everything will be ok.  Refuse to do any work
    until you version control it.  Anything less is disasterous.
-   Never log into production servers via a shell.  Instead, write a script to
    do it.  And test your script in development first.

Immediately after this experience, I setup our development environment.  I
duplicated every server we had, and made sure that if something happened, we
would be able to recover.

Over the past few months working with [puppet][], [monit][], and other really
useful sysadmin tools, we've built up some pretty nice defenses to protect
against future problems like this.  However, I'll still never forget the
incredibly horrible sinking feeling in my stomach when I ran that update
command.


  [Horseman Sketch]: /static/images/2011/horseman-sketch.png "Horseman Sketch"
  [freeradius]: http://freeradius.org/ "FreeRADIUS"
  [Rackspace]: http://www.rackspace.com/index.php "Rackspace"
  [puppet]: https://puppetlabs.com/ "puppet"
  [monit]: http://mmonit.com/monit/ "monit"
