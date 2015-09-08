---
title: "Deployment System Requirements"
date: "2010-12-18"
tags: ["programming"]
slug: "deployment-system-requirements"
description: "Just some personal thoughts to myself about what my continuous deployment systems need to look like to be successful."
---


![Robot Sketch][]


Over the past month, my colleague Kurtis and I have been engineering a fully
environment.  This article discusses the requirements that we had for our
deployment system.  I eventually hope to discuss the entire thing, how we
built it, and what revisions we make.


## Why Deploying Can Be Painful

Most programmers hate deploying code.  I certainly did until this past year.
Deploying code is (often times) much harder than writing the code itself.
Deploying requires a great deal of knowledge: OS configuration and setup, cloud
provider APIs or physical server installation quirks, numerous software
components, system monitoring, access lists, and a lot of other things.

It's a pain.

At my work, we operate with a variety of technologies and tools, which makes
deployment even more complex, as there is no one-solution-fits-all approach to
managing our various components easily.

Since it can be difficult and frustrating (especially for small teams like
mine, where we don't have any dedicated sysadmins), many people tend to ignore
deployment, or put it off till the last minute.  This is the way I used to
operate--I would work on my code for weeks at a time, and then once I had some
features finished and bugs removed I would manually copy my code over to each
production server, carefully update my project files, and then restart the
necessary services and manually test like crazy to make sure I wasn't breaking
anything.

The approach I used to take was awful for numerous reasons.  Among other
things:

-   It made me scared to deploy code frequently.  This means users get slower
    updates, bugs get fixed slower, and every suffers.
-   Deploying code would often cause downtime.  One accidental `cp` or `rm`,
    and your code is gone.  It's hard to recover from production mistakes.
-   It is time consuming.  Deploying code shouldn't take hours.
-   It made it difficult to test for code correctness.  Infrequent deployment =
    infrequent testing = infrequent integration with other team member's code.
    When we deployed, it would often cause other code issues that were unseen
    in our development environments.

When Kurtis and I started discussing these issues, we decided it was time to do
something about it.  We wanted to build a deployment system to make our lives
easier, our coding more effective, and our company more efficient.


## Our Requirements

When we started planning out our deployment system and doing research, we
generated a list of requirements that (more or less) must be met by the system
of our choosing. Here they are:

-   We should have three distinct environments: development, staging, and
    production.  There should never be any versions of code running on the
    incorrect systems.
-   Our development systems should always be running the latest version of or
    `develop` git branch.
-   Our staging systems should always be running the latest version of our
    `master` branch.
-   Our production systems should always be running the latest version of our
    `master` branch (but only if tests pass on staging).
-   We should have a continuous integration system watch our git repositories,
    and when changed, check out the latest version of our code, run tests on it
    and if the tests pass deploy it to the appropriate environment.
-   We should be able to run multiple levels of tests: unit tests, integration
    tests, performance tests, and deployment tests, with each commit.
-   We should be able to get meaningful statistics and notifications when we
    break stuff, so that we can get it working again.
-   Our system should be as self-healing as possible.  If something goes wrong,
    it should try to fix it, and only if it can't figure out what to do should
    we be notified.

Those are the main requirements we had.  And I'd like to think that they are
still pretty solid.  With those features, we should be able to focus on code,
and let everything else happen naturally.

The three distinct environments are important.  They can vary greatly from
organization-to-organization.  For us, our development environment is local for
each developer.  We write and test most of our code on our home boxes with a
combination of Rackspace boxes and Virtualbox environments as helpers.  Our
staging and production environments are both in the same cloud, and identical
in almost every way.  We use our staging as a live fail over for production,
and it serves as a great test bed for production code before putting it live.

We use [git flow][] at work, which explains our git branching model.
Basically, all our branches have standard naming convention, which allows us
to do stuff like say that all code in the `master` branch should be deployed
straight to staging / production, and that all code in `develop` should be
deployed straight to development.

The continuous integration (and deployment) system should be able to run tests
and deploy code.  This step has the biggest impact on our work flow.  Knowing
that every time I `git commit`, my code is automatically tested and deployed to
all development, staging, and production boxes (depending on the git branch) is
an awesome feeling.  This enables us to do a lot of cool things.  Push bug
fixes out immediately, push features out immediately, instantly test for
problems, discover pain points earlier, etc.

The ability to run multiple levels of tests is also extremely important.  Most
folks (those who do any sort of testing, anyhow) will stop at unit tests.
However, especially when you are designing large scale systems with databases,
you need to test for concurrency problems, and many other factors that simple
unit tests won't catch.  This means that we need the ability to launch
performance test suites, and other remote tests that MUST run against a live
development or staging environment to be useful.

Our requirement to get feedback is a no-brainer.  What is the point of
automating stuff if you can't get reports when things don't work?

And lastly, we chose to build in the self-healing requirement so that we would
not end up wasting our time dealing with issues that are best solved
automatically.


## Conclusion

What are your experiences with deployment?  I'm extremely glad that we decided
to tackle this issue recently.  We've still got quite a while to go before our
system is perfect, but we're making a lot of good progress, and have already
saved hundreds of man hours with some fairly simple automation.

Sometime in the next week or so I'll throw up another article on our deployment
system, and dive into some technical details.


  [Robot Sketch]: /static/images/2010/robot-sketch.png "Robot Sketch"
  [git flow]: http://jeffkreeftmeijer.com/2010/why-arent-you-using-git-flow/ "git flow"
