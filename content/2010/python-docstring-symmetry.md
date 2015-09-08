---
title: "Python Docstring Symmetry"
date: "2010-08-17"
tags: ["programming", "python"]
slug: "python-docstring-symmetry"
description: "A short PEP-257 rant about docstring style."
---


![Ruler Sketch][]


If you've been doing Python for more than a month, then I'm sure you're
familiar with [PEP-8][], the *official* Python style guide.  If you look at
PEP-8, it doesn't explicitly define any docstring style guidelines, but instead
recommends following [PEP-257][]'s rules.

In the Python community, it is considered a sin if you don't strictly follow
PEP-8.  This is one of the things I really enjoy about Python, the community
helps encourage best practices, and good coding style.  Nothing wrong with
that.

However, I hate to say it, but: **PEP-257 is bullshit**.


## What I Like About PEP-257

I don't hate *everything* about PEP-257, so before I get to the bad part, let
me start by talking briefly about what I like.

-   PEP-257 encourages developers to write docstrings for all modules,
    functions, and classes.  This is awesome.  I totally agree.  Docstrings are
    extremely useful for developers, and help show off some of Python's awesome
    self-documenting and introspection capabilities.

-   PEP-257 encourages the use of triple double quotes (`"""`) as docstring
    delimiters.  I agree again.  It is nice to have consistency across multiple
    programs.

-   PEP-257 suggests that very short one line docstrings be placed on a single
    line, but still use triple double quotes (`"""`) as delimiters.  Again,
    this rocks.  Let's say you're writing a private method for a class, and it
    is pretty self explanatory, don't kill yourself writing long docstrings:

```python
def _something_simple(x, y):
    """Adds x and y."""
    return x+y
```

-   PEP-257 says that you should NOT put your function signatures into your
    docstring, as they are already available through introspection.  Makes
    perfect sense: don't be redundant:

```python
# Don't do this, please.
def stupid_function(a):
    """stupid_function(a) -> int"""
    return 4
```

So, as you can (hopefully) see, I'm not some crazy rebel who hates standard
conventions or anything.  I love order just as much as the next programmer.


## Where PEP-257 Goes Crazy

The main bulk of PEP-257 is describing how multi-line docstrings should look,
and this is where things get ugly.

Basically, PEP-257 wants your multi-line docstrings to start immediately after
the opening triple quotes (`"""`), and end with a blank line.  Here's an
example:

```python
# This example was stolen directly from PEP-257.
def complex(real=0.0, imag=0.0):
    """Form a complex number.

    Keyword arguments:
    real -- the real part (default 0.0)
    imag -- the imaginary part (default 0.0)

    """
    ...
```

Here's another example with a more full docstring:

```python
def do_something(x=0.0, y=5):
    """Calculates your best friend's birthday by multiplying two numbers
    together, then returning 4.

    Keyword Arguments:
    x -- anything, I don't care
    y -- seriously

    """
    ...
```

Now, like most programmers I know, I'm a bit of an organizational freak.  I
like symmetry in my code, comments, and I have to have things perfectly
aligned.  PEP-257's suggested multi-line docstring format drives me crazy.

I have two big problems with PEP-257's suggested format:

1.  PEP-257 wants me to start my docstring **immediately** after the triple
    quotes.

2.  PEP-257 wants me to leave a blank line at the end of my docstring.

It doesn't look *clean* or *organized* putting your comments immediately after
the opening triple quotes.  It also seems unnecessary to add an extra blank
line at the end of each docstring.


## What I Propose

Instead of listening to PEP-257, I suggest that Python developers instead adapt
my style:

```python
def complex(real=0.0, imag=0.0):
    """
    Forms a complex number.

    :param real:    The real part (default 0.0).
    :param imag:    The imaginary part (default 0.0).
    :return:        An imaginary number, or False.
    """
    ...
```

This takes up the same amount of lines, except looks more symmetrical.  We now
have an uncluttered docstring, that is easier to scan over with your eyes, and
looks nicer.

The description of what you're documenting goes on the line directly below the
opening triple quotes, and there is no blank line before the end of the
docstring.


  [Ruler Sketch]: /static/images/2010/ruler-sketch.png "Ruler Sketch"
  [PEP-8]: http://www.python.org/dev/peps/pep-0008/ "PEP-8"
  [PEP-257]: http://www.python.org/dev/peps/pep-0257 "PEP-257"
