---
title: "Successful GitHub Development"
date: "2012-04-14"
tags: ["programming"]
slug: "successful-github-development"
description: "A guide to being a successful GitHub hacker and open source developer."
---


![Octocat][]


I've been using GitHub for several years now, and it has drastically changed my
development work flow, mindset, and collaboration efforts.  Over the time I've
used GitHub, I've contributed to many projects, started many of my own, and had
the opportunity to interact with a wide range of developers (from novices to
professionals).

This article is my attempt to explain GitHub best practices that you can
practically apply to your everyday coding, which will make you:

-   A better programmer.
-   A better collaborator.
-   A more reputable programmer (that everyone likes).

For clarity, this article is broken up into two separate components,
**maintainers** and **contributors**.

The **maintainers** section explains best practices for running your own open
source project on GitHub.  If you've ever published your own library, you
should check it out.

The **contributors** section explains how to best contribute to already
existing open source projects.

I highly recommend that regardless of whether you primarily maintain or
contribute, you read both sections thoroughly.  Open source development is a
staple of modern society, and in order to ensure that the open source ecosystem
remains friendly, accessible, and effective--we (as developers) need to do all
we can to promote best practices and effective collaboration.


## Maintainers

Maintaining open source projects is hard--it requires time, energy, and good
communication.  The principles outlined here should be applied to all open
source projects (large and small), as they will ensure that your life (and the
life of your contributors) is as simple as possible.

All of the practices mentioned below **only apply to projects once they've made
an initial release**.  If you are still working on implementing the basic
functionality of your software--you may choose to ignore any of these rules,
and work in whatever way is most effective for you personally.

I've tried to list these rules in order of importance, so as a project
maintainer you can use this list as something of a checklist for new projects,
going through and crossing off each requirement until your project is fully
compliant.


### 1. Write Official Documentation

The first requirement for any open source project is that it has good
documentation for prospective users.  There is absolutely no excuse for not
having good documentation.

Your official documentation should (at a minimum) include:

-   **What your project's purpose is, and who is its indended audience.**  For
    example, if your project provides a Python library for controlling the Mars
    Rover spacecraft, you should explain that your project is meant to be used
    by NASA scientists on the rover project, and that you need at least a PhD
    in Physics to get started.
-   **How to properly install your project.**  Ideally, your project should be
    installable via a common (simplistic) method: PyPI for Python, PEAR for PHP,
    CPAN for Perl, RubyGems for Ruby, etc.
-   **A quickstart guide which walks new users through building a working
    application.**  This piece is critically important, as it will determine
    what new users think of your project.  Having a good quickstart guide shows
    users that you care for them, and ensures that both you (as a maintainer)
    and your users have a good understanding of your project.
-   **A topic guide explaining specific components not referenced in the
    quickstart guide.**  This should include extra bits of information, code
    samples, and topic-specific documentation.  For example, if your project
    provides a simple IRC bot library, you may want to put documentation on
    managing multiple server connections here (as that information is probably
    too in-depth for a quickstart guide).
-   **How to contribute to your project.**  This section should include (in
    detail):
    -   How to check out your project's source code.
    -   Which branch to use for development.
    -   What style rules to follow when adding code.
    -   How to run all of the project's unit tests, integration tests, etc.
    -   An example work flow.

-   **Where to get help.**  If your user is stuck, and can't figure something
    out--where should they go for help?  A mailing list?  A forum?  An IRC
    channel?  A personal email account?

Having good official documentation is probably the single most important thing
you can do (as a maintainer) to ensure the long-term success of your project.
Good documentation encourages new users to use your code, encourages
contributors to contribute to your project, and gives you a positive reputation
in the developer community.

Some things to take note of:

-   A wiki does NOT qualify as official documentation.  If possible, avoid
    wikis entirely.  Having a wiki gives off a bad impression to new (and
    existing) users.
-   If you have a very small project (such as a simple command line utility
    with a single purpose), it is ok to combine your quickstart guide with your
    topic guide.
-   If you have a small project, use GitHub's new [project page generator][]:
    to host your documentation.
-   If you have a project with any sort of real complexity, use
    [http://readthedocs.org/][] to host your documentation.  Read the Docs
    provides free documentation hosting, with a lot of useful features,
    including:
    -   A beautiful default theme (with many other themes to choose from).
    -   GitHub hooks to automatically build your documentation whenever your
        project is updated.
    -   The ability to generated PDF downloads for your documentation.
    -   The ability to support multiple versions of documentation for your
        project (v0.1, v0.2, etc...).


### 2. Use Git Flow

[git-flow][] is a popular Git branching model (and add-on) that provides a
simple way to work with stable projects.  The idea of git-flow is that each
project should have two branches at all times: a `master` branch which always
contains stable, production-ready code--and a `develop` branch which contains
the latest development code.

Using git-flow should encourage:

-   The master branch to only receive updates when there is a new (stable)
    release of your application (or library) ready.
-   The develop branch to receive all updates from you (as the project
    maintainer), and your fellow core contributors.

By agreeing upon a stable Git branching model, you can ensure your users are
never confused as to:

-   Which branch to use in production.
-   Which branch to use for development.
-   Where to submit their pull requests.

To learn more about git-flow, read the following posts (in order):

-   [http://jeffkreeftmeijer.com/2010/why-arent-you-using-git-flow/][]
-   [http://nvie.com/posts/a-successful-git-branching-model/][]
-   [http://buildamodule.com/video/change-management-and-version-control-deploying-releases-features-and-fixes-with-git-how-to-use-a-scalable-git-branching-model-called-gitflow][]
-   [http://codesherpas.com/screencasts/on_the_path_gitflow.mov][]


### 3. Publish Test Runs

If you don't write tests for your code, [read this][] before you go any
further.  As I'm sure you know, tests are essentially worthless if they aren't
ran--after all, what's the point of having tests if nobody cares about them?

For open source projects, simply running your tests isn't enough.  In addition
to running your tests, you also need to publicize your test results so that
your users and contributors know what the status of your test suite is.

While this is not commonly practiced--publicizing test builds is a great way to:

-   Inspire confidence in your code base.
-   Ensure that all code submissions adhere to a certain level of quality (and
    don't cause breakage).
-   Make errors transparent, so that things can get fixed quicker.
-   Make your tests more valuable, as people will see them and instantly know
    that testing is important in your project.

If possible, you should always attempt to use [Travis CI][] to run the tests
for your project.  Travis CI is "A hosted continuous integration service for
the open source community."  At the time of writing, Travis CI supports a wide
array of programming languages, frameworks, databases, caching services, and
many other infrastructure components which allow you to successfully run your
test suite, regardless of its complexity.

To get started with Travis CI, read their [official documentation][].

**NOTE**: If you are using Travis CI to run your project's tests--make sure you
use their sharing functionality to embed your project's build status in your
official documentation.  The recommended way to do this is embed the Travis CI
markdown code into your project's `README.md` file, this way GitHub will
display it prominently on your project page.

If you can't use Travis CI for any reason, you should use [Jenkins][].  Jenkins
is a simple continuous integration server that you can easily configure to
build your projects.  If you are using Jenkins, be sure to link users (from
your documentation) to your Jenkins web page so they can view your test builds.


### 4. Use GitHub Issues

GitHub issues is the best way to track issues for your project, and you should
encourage your users (and contributors) to use it for:

-   Feature requests.
-   Documenting bugs (or weird behavior).
-   Listing TODO entries for development.
-   Referencing issues from Git commits.

Having all of your project's issues in one place makes it easy for users and
contributors to submit problems, comment on other people's problems, find
things to do, and generally keep organized.

Ensuring your project's issue tracker is always kept up-to-date and well
maintained also strongly encourages new contributors to work on the project, as
they can easily find issues and fix them for you.


## Contributors

Contributing code to open source projects can be difficult, exciting, scary,
and rewarding.  This section is aimed at helping you successfully contribute
code to projects you like, while minimizing the odds of failure along the way.

If you stick to these tips, you can't go wrong.  As with the maintainers
section--the tips below are ordered by importance, and can be followed as a
checklist.


### 1. Read the Project Documentation

If the project you're attempting to contribute to has any official
documentation, be sure to read all of it before submitting any code.  Often
times the code submission you have in mind is already part of the project, and
can be found somewhere in the documentation.

Reading through the official documentation will also typically give you a good
feel for the project's purpose, scope, and ideals.  These are incredibly
important, as possibly the most critical factor in having your code accepted to
a project is that it meshes well with the existing code base.  It is highly
unlikely, for instance, that an IRC bot maintainer will accept a pull request
containing code which adds Skype support--as the project is most likely
focusing entirely on IRC.


### 2. Look at the Issue Tracker

Before writing your first line of code, be sure to scan through the project's
issue tracker.

If you are planning on fixing a bug, and you don't see it listed in the issue
tracker yet--create a new issue for it!  The best type of code is code that is
never written.  The bug you're attempting to fix may be another problem
unrelated to the project, so filing an issue before submitting code is
typically a good idea as it will save you (and the project maintainer) lots of
time and confusion.

If you are considering submitting a new feature to the project--create an
issues for it first, and explain the feature you'd like to submit and why you
think it would be useful.  This gives the project maintainer the ability to
discuss the feature with you, and figure out what the best way to move forward
is.  Often times, having feature discussions before submitting code greatly
increases the chance your code will be accepted, as the maintainer already
expects you to submit code, and has a good idea of what to look for and
inspect.


### 3. Comply to Style Guidelines

Almost every project has a distinct style of code.  Whenever you submit code to
a project, be sure that your code complies with the already existing style.

Not only will writing code in the same style as the project make the code
easier for you to understand--it will make it easier for the project maintainer
to review, accept, and publish!

Regardless of whether or not you like the style of the existing code base,
complying with the author's style guidelines makes everyone happier as all the
code will be uniform, easier to scan through, easier to debug, and easier to
maintain over time.


### 4. Unsure? Ask!

If you're unsure about anything--whether it be coding style, development work
flow, wording, whatever--try not to make assumptions, ask!

Quite possibly the greatest benefit of open source software is that it brings
people together to create amazing things.  If you're not sure about something,
have a chat with one of the project maintainers--they'll most likely be really
happy to talk to you.

Project maintainers don't want to waste time (theirs or yours), and will
usually be more than happy to explain why something is (or isn't) a good idea.
Discussing questions before submitting code is a great way to make new friends,
learn cool things, and generally enjoy your open source experience a lot more.


## Have Fun

Maintaining and contributing to open source projects is a lot of fun.  There's
nothing quite like the rush you get by creating something entirely new, and
sharing it with the world. Whether you're starting a project or contributing to
one, enjoy your work, meet new people, and have a good time.

If you ever find yourself in a situation where you aren't having fun, stop what
you're doing immediately and re-think things.

I hope the guidelines above were useful to you.  If you have any questions or
suggestions, please leave a comment and I'll update the post as needed.


  [Octocat]: /static/images/2012/octocat.png "Octocat"
  [project page generator]: https://github.com/blog/1081-instantly-beautiful-project-pages "GitHub Project Page Generator Documentation"
  [http://readthedocs.org/]: https://readthedocs.org/ "Read the Docs"
  [git-flow]: https://github.com/nvie/gitflow "git-flow"
  [http://jeffkreeftmeijer.com/2010/why-arent-you-using-git-flow/]: http://jeffkreeftmeijer.com/2010/why-arent-you-using-git-flow/ "Why Aren't You Using Git Flow?"
  [http://nvie.com/posts/a-successful-git-branching-model/]: http://nvie.com/posts/a-successful-git-branching-model/ "A Successful Git Branching Model"
  [http://buildamodule.com/video/change-management-and-version-control-deploying-releases-features-and-fixes-with-git-how-to-use-a-scalable-git-branching-model-called-gitflow]: http://buildamodule.com/video/change-management-and-version-control-deploying-releases-features-and-fixes-with-git-how-to-use-a-scalable-git-branching-model-called-gitflow "A Video Introduction to Git Flow"
  [http://codesherpas.com/screencasts/on_the_path_gitflow.mov]: http://codesherpas.com/screencasts/on_the_path_gitflow.mov "On the Path to Git Flow"
  [read this]: http://www.codinghorror.com/blog/2006/07/i-pity-the-fool-who-doesnt-write-unit-tests.html "WRITE UNIT TESTS, FUCK!"
  [Travis CI]: https://travis-ci.org/ "Travis CI"
  [official documentation]: http://about.travis-ci.org/docs/ "Travis CI Documentation"
  [Jenkins]: http://jenkins-ci.org/ "Jenkins"
