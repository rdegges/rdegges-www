---
title: "A Developer's Conundrum - Dev / Prod Parity"
date: "2012-07-10"
tags: ["programming"]
slug: "a-developers-conundrum-dev-prod-parity"
description: "Want to make your life easier when writing production quality software?  You should try to keep your development environment as similar to your production environment as possible."
---


![Grim Reaper Bust][]


As a [passionate developer][], I constantly try to write the best code
possible.  I *love* my craft.

For me, this means that I:

-   Read lots of books on new and emerging technologies, trying to learn as
    much as possible about them as a hobby.
-   Write lots of open source code which solves problems in a reusable way.
-   Maintain old code, and periodically update it to new quality standards.
-   Rewrite software that needs to be rewritten, using whatever new knowledge
    I've obtained to do the job better.
-   Talk with a variety of developers in other fields with other skill sets,
    and learn from their experience.
-   Keep up with industry best practices, and do my best to adhere to them
    where possible.
-   Write maintainable code to make my life (and that of my fellow developers)
    as painless as possible.

None of these things are unusual amongst the friends I have, and people I know.
Every good developer wants to follow best practices, write better code, and
become better at their craft.

In general, I find that current best practices largely make sense.  I primarily
develop web software, and possibly the most famous best practices are all
contained within [The Twelve-Factor App][], a document detailing the 12 factors
which should be followed while building web software.  If you strictly follow
these 12 factors of good application design, it would be hard to go wrong.

Many of the 12 factors make perfect sense when you read them.  They are
undisputed as software guidelines.

To summarize:

-   Keep your system in version control.  Deploy it as many times as needed--
    from the same codebase.
-   Ensure all your project dependencies are explicitly stated.  You should be
    able to provision a working instance of your application on demand.
-   Store your application configuration as environment variables--this way you
    can easily move your application around, keeping sensitive data safe.
-   Treat all backing services as attached resources.
-   Separate your build, release, and run processes.
-   Ensure instances of your app are stateless, this way you can scale your app
    as needed.
-   Export your services via port binding.
-   Allow your services to run concurrently, allowing you to scale your system
    horizontally across many machines.
-   Keep your services quick to start up, and quick to shut down.
-   Keep development, staging and production as similar as possible to avoid
    unexpected deployment errors.
-   Treat your log files as event streams.
-   Run admin and management tasks as one-off processes.

Unfortunately, while I continuously do my best to follow the 12 factors of good
application design, I'm constantly battling with myself over factor 10,
[dev-prod parity][].


## Dev / Prod Parity

When you write software (web software in particular), the environment you're
writing your code in is often very different from the environment which you're
deploying your code in.

If I'm writing a website, for instance, I'll often need many infrastructure
tools to make it run successfully in production:

-   PostgreSQL, for storing application data.
-   Amazon S3, for hosting my static assets (CSS, JS, images).
-   Memcache, for storing cached data.
-   Amazon SQS, for storing messages that need to be processed asynchronously.
-   etc.

The best practices way for me to handle this situation would be to use all of
the tools above locally while I'm developing the website, so that when I'm
actually ready to deploy my application in a production environment I already
know that everything will work as expected.

And when I think about this, it makes perfect sense.  If you want to build your
application in the best way possible, avoiding as many issues as you can, you
should probably make sure that your development environment (in my case, a
laptop) is identical to your production environment ([Heroku][], [AWS][], or
whatever you use to host your sites).

*Unfortunately, this is my conundrum--I find it nearly impossible to both
write good code, and minimize dev / prod parity.*


## The Difficulty

The difficult thing about minimizing dev / prod parity (for me), is minimizing
*pain*.  It is really painful, for example, to develop a site locally (on my
laptop) and not be able to get instantly see how my web pages look when
rendered.

If I were to only use S3 for hosting my CSS, for example, I'd have to:

-   Commit my changes to Git.
-   Push my code to Heroku.
-   Push my static assets (CSS) to S3.
-   Open my browser, visit my staging environment's website
    (`http://myapp-staging.herokuapp.com`).

That's a lot of pain to go through to see if my CSS change fixed what I wanted
it to, or not.

In the same way that manging static assets sucks with no dev / prod parity,
managing other infrastructure components is equally frustrating.

If I were to actually use Amazon SQS locally while developing my website, I'd
have to (among other things):

-   Always be online to test even the most trivial of my application changes.
-   Run two separate processes locally (my web worker, as well as much
    background task worker).
-   Ensure I have a test SQS queue created for each of my applications in
    addition to my production queue.
-   Make sure that I consume all of my messages while testing, otherwise I'll
    have messages sitting in SQS until they expire, costing money.

Ugh.


## Complexity

I realize that complexity is a major issue here.

If your development and production environments are identical, deployment
complexity goes down (because you already know things work).

If your development and production environments are very different, coding
complexity goes up because you have to manage multiple application
configurations: one for development, and one for production.

But which is worse?


## What I'm Doing

Up until now, I've always found it a lot *cleaner* to maintain different
application environments: one for development and one for production.  This
way, I can develop sites locally without issue, and deploy them (usually)
without issue.

Sure, there are drawbacks to this approach (e.g. more code to worry about), but
as a result, I'm able to develop my sites quite a bit quicker (instant
feedback), as opposed to a more delayed (slow feedback) process.

Every time I talk to my developer friends, however, I'm constantly reminded of
the rule: minimize dev / prod parity!

**This is my conundrum.**

I'd love to hear your opinions (please leave a comment), so that I can make a
decision about what to do from now on in my quest to consistently improve my
development skills >:)


  [Grim Reaper Bust]: /static/images/2012/grim-reaper-bust.png "Grim Reaper Bust"
  [passionate developer]: http://www.amazon.com/gp/product/1934356344/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=1934356344&linkCode=as2&tag=rdegges-20 "The Passionate Programmer"
  [The Twelve-Factor App]: http://www.12factor.net/ "The 12 Factor App"
  [dev-prod parity]: http://www.12factor.net/dev-prod-parity "Dev / Prod Parity"
  [Heroku]: http://www.heroku.com/ "Heroku"
  [AWS]: http://aws.amazon.com/ "Amazon Web Services"
