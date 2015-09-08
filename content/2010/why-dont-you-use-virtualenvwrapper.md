---
title: "Why Don't You Use virtualenvwrapper?"
date: "2010-09-08"
tags: ["programming", "python"]
slug: "why-dont-you-use-virtualenvwrapper"
description: "virtualenvwrapper is such an amazingly useful Python tool.  This article shows you why it rocks so hard, and why you should be using it right now."
---


![Crumpled Paper Sketch][]


If you're a python programmer, you've most likely heard of [virtualenv][].  If
you haven't, then you need to check it out.

> virtualenv is a tool to create isolated Python environments.

In a nutshell, you can create as many *virtual environments* as you want.  Each
of these *virtual environments* is a small directory structure, which contains
a copy of your python interpreter(s), and provides a sandbox environment in
which you can install only the necessary packages you need to run your project,
as well as remove your programs' dependence on system packages and python
versions.


## virtualenvwrapper Rocks!

`virtualenvwrapper` (available via `pip` or `easy_install`), is a set of
scripts that makes managing multiple virtual environments easier-much easier.

In my day-to-day work, I typically use `virtualenv` to create various test
environments.  Let's say I want to test out a new package in my project, I may
do something like:

```console
rdegges@solitude:~/random_project$ virtualenv --no-site-packages env
New python executable in env/bin/python
Installing setuptools............done.
rdegges@solitude:~/random_project$ . env/bin/activate
(env)rdegges@solitude:~/random_project$ pip install nose
Downloading/unpacking nose
  Downloading nose-0.11.4.tar.gz (256Kb): 256Kb downloaded
  Running setup.py egg_info for package nose
    no previously-included directories found matching 'doc/.build'
Installing collected packages: nose
  Running setup.py install for nose
    no previously-included directories found matching 'doc/.build'
    Installing nosetests-2.6 script to /home/rdegges/random_project/env/bin
    Installing nosetests script to /home/rdegges/random_project/env/bin
Successfully installed nose
Cleaning up...
# do some testing here ...
```

I'll often repeat this process numerous times, as I don't want to clutter my
*official* virtual environment which has my list of good packages and their
respective versions.

The problem with this approach, of course, is that it becomes tedious to manage
a ton of virtual environments.  It also causes clutter in version control
environments, without careful exclusion rules.

This is where `virtualenvwrapper` comes into play.

`virtualenvwrapper` allows you to store as many virtual environments as you
want, in a single non-project location.  It provides convenient scripts for
creating, editing, switching, and removing virtual environments with ease.

Here's how I'd use `virtualenvwrapper` to create a new test environment and do
a bit of work in it:

```console
rdegges@solitude:~/random_project$ mkvirtualenv --no-site-packages testnose
New python executable in testnose/bin/python
Installing setuptools............done.
virtualenvwrapper.user_scripts Creating /home/rdegges/.virtualenvs/testnose/bin/predeactivate
virtualenvwrapper.user_scripts Creating /home/rdegges/.virtualenvs/testnose/bin/postdeactivate
virtualenvwrapper.user_scripts Creating /home/rdegges/.virtualenvs/testnose/bin/preactivate
virtualenvwrapper.user_scripts Creating /home/rdegges/.virtualenvs/testnose/bin/postactivate
virtualenvwrapper.user_scripts Creating /home/rdegges/.virtualenvs/testnose/bin/get_env_details
(testnose)rdegges@solitude:~/random_project$ pip install nose
Downloading/unpacking nose
  Downloading nose-0.11.4.tar.gz (256Kb): 256Kb downloaded
  Running setup.py egg_info for package nose
    no previously-included directories found matching 'doc/.build'
Installing collected packages: nose
  Running setup.py install for nose
    no previously-included directories found matching 'doc/.build'
    Installing nosetests-2.6 script to /home/rdegges/.virtualenvs/testnose/bin
    Installing nosetests script to /home/rdegges/.virtualenvs/testnose/bin
Successfully installed nose
Cleaning up...
# do some testing here ...
(testnose)rdegges@solitude:~/random_project$ deactivate
rdegges@solitude:~/random_project$
```

Nice, eh?  Now, let's say I want to work on another virtual environment that
I've already defined, it's as easy as:

```console
rdegges@solitude:~/random_project$ workon pycall
(pycall)rdegges@solitude:~/random_project$
```

Just use the `workon` command to instantly switch into an already defined
virtual environment.  And if I want to remove a virtual environment?

```console
(pycall)rdegges@solitude:~/random_project$ deactivate
rdegges@solitude:~/random_project$ rmvirtualenv testnose
rdegges@solitude:~/random_project$
```

And *bam*, just like that, `testnose` is gone.


## Give virtualenvwrapper a Try

It really is an awesome, extremely useful program.  If you use `virtualenv`
currently, you shouldn't write another line of code before installing and using
it.

`virtualenvwrapper` can be downloaded [here][].  The project website has great
[documentation][], and plenty of examples which show off the rest of the great
features that `virtualenv` has to offer.

Among other things, `virtualenv` also provides hooks for setting up virtual
environments, which allow you to get really creative, and save yourself a LOT
of time by automating common `virtualenv` tasks.


  [Crumpled Paper Sketch]: /static/images/2010/crumpled-paper-sketch.png "Crumpled Paper Sketch"
  [virtualenv]: https://pypi.python.org/pypi/virtualenv "Virtualenv on PyPI"
  [here]: http://www.doughellmann.com/projects/virtualenvwrapper/ "Virtualenvwrapper"
  [documentation]: http://www.doughellmann.com/docs/virtualenvwrapper/ "Virtualenvwrapper Documentation"
