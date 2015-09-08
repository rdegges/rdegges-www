---
title: "Essential Tools for Pythonistas"
date: "2011-04-17"
tags: ["programming", "python"]
slug: "essential-tools-for-pythonistas"
description: "A list of essential tools that all Python programmers should be using on a daily basis."
---


![Python Sketch][]


[Pythonistas][] need a lot of good tools in order to work efficiently.  I'd
like to take a few minutes to enumerate some of my favorite tools that help me
write better Python code faster.


## GitHub

Although you're likely already using [Github][] for hosting all of your
projects (both open source, and closed source), if you aren't, you need to
seriously reconsider what you are doing with your life.  GitHub is an extremely
useful platform for hosting [Git][] projects.  It provides lots of great tools
for making your project easy to work on, easy to get assistance with, easy to
discover, and tons of other things.


## Vim + pyflakes

Ok, so [Vim][] may not be entirely necessary, but [pyflakes][] definitely is.
pyflakes is an awesome python project that integrates with Vim, and allows you
to check for interpreter errors in your python code live (as you are coding).
This is immensely useful when working on large projects, as you almost never
need to actually run your code to find basic errors--your Vim terminal will
simply highlight the problematic source line red, and provide you with a nice
little error description so that you can fix it without ever running it.

Furthermore, pyflakes is fast.  As you code it'll show exceptions in a
non-invasive way, which makes it excellent for fixing errors quickly without
disturbing your train of thought.

Here's a little screen shot of pyflakes in action:

![pyflakes Screenshot][]


## Sphinx

Writing good documentation is essential for good projects.  Good technical
documentation is what separates decent projects from amazing projects.  If you
provide clear, useful documentation for your project's users, then you are far
more likely to get good involvement from other programmers, and are much more
likely to get positive exposure.

[Sphinx][] (a [pocoo][] project) is the best tool around for generating
beautiful documentation for technical projects.  It allows you to write simple
[reStructuredText][] markup (a plain text format), which it compiles into
beautiful HTML pages and PDF documents.  It comes with several built-in themes,
so you can even choose a look that suits your project's personality.
Furthermore, extending Sphinx and writing custom themes is very simple--just
add a CSS file, and you can easily change the entire look and feel of your
documentation.


## Read The Docs

[ReadTheDocs][] is a relatively new (and highly regarded) Sphinx documentation
hosting site.  It provides free documentation hosting for Sphinx projects,
which makes sharing your project's documentation even easier.

Having great documentation is awesome, having great and *easily accessible*
documentation is even more awesome.

ReadTheDocs allows you to host all of your projects' documentation in a single
location, as well as automatically build your project documentation whenever
you make updates, and lots of other goodies.  If you aren't using it, you
should be.


## virtualenv

As any frequent Python programmer will tell you, having tons of Python packages
installed on your OS of choice is a *pain-in-the-ass*.  Projects all require
various versions of dependencies, and having your OS cluttered with conflicting
versions of packages is incredibly frustrating [virtualenv][] makes this problem
go away.

`virtualenv` provides isolated package environments that you can install Python
packages to.  This way, each project you work on can have its own mini working
environment, completely isolated from the rest of your system.

Ideally, you should be using `virtualenv` with the infamous
[virtualenvwrapper][].


  [Python Sketch]: /static/images/2011/python-sketch.png "Python Sketch"
  [Pythonistas]: http://python.net/~goodger/projects/pycon/2007/idiomatic/presentation.html "Code Like a Pythonista"
  [GitHub]: https://github.com/ "GitHub"
  [Git]: http://git-scm.com/ "Git"
  [Vim]: http://www.vim.org/ "Vim"
  [pyflakes]: https://github.com/kevinw/pyflakes "pyflakes"
  [pyflakes Screenshot]: /static/images/2011/pyflakes-screenshot.png "pyflakes Screenshot"
  [Sphinx]: http://sphinx.pocoo.org/ "Sphinx"
  [pocoo]: http://www.pocoo.org/ "pocoo"
  [reStructuredText]: http://docutils.sourceforge.net/rst.html "reStructuredText"
  [ReadTheDocs]: http://readthedocs.org/ "readthedocs"
  [virtualenv]: http://www.virtualenv.org/en/latest/ "virtualenv"
  [virtualenvwrapper]: http://www.doughellmann.com/projects/virtualenvwrapper/ "virtualenvwrapper"
