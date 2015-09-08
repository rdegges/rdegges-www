---
title: "Tools I Use - tmux"
date: "2012-01-06"
tags: ["programming"]
slug: "tools-i-use-tmux"
description: "tmux is an amazingly useful tool.  Here's a quick look at what makes it awesome."
---


![Tools][]


I love reading about tools other programmers use in their day-to-day existence.
There are so many great pieces of software out there that it's impossible to
hear about them all.  Whenever I read articles (or watch screencasts) that
other developers make, I tend to learn a lot.

So, I decided to start my own series here on my site, dedicated to talking
about the tools I use, and how I use them.  Unfortunately, I probably don't
have much useful information to give in this area--but I figure that if I start
writing about it, I'm bound to learn more about the tools I use along the way.
So this is a win-win for me.

As this is the first article in the series, I figured what better time to
discuss [tmux][], my favorite terminal multiplexer!


## Terminal Multiplexers

If you've ever had the need to run multiple terminal windows inside an existing
terminal window, you've probably heard of [GNU screen][].

GNU screen is one of the most popular terminal multiplexers of all time.  What
it allows you to do is have a large amount of virtual terminals that you can
create, move around, and use at will.  What's great about tools like GNU screen
is that they allow you to quickly move between your terminal windows using
keyboard shortcuts, which can often times be a lot quicker than alt+tab'ing to
a new terminal window on your OS.

The other great thing about terminal multiplexers like GNU screen and tmux is
that they give you the power to tile your windows as you please.  For instance,
you can run two terminals side by side, one window with code, and another with
a shell for testing your code on the command line.  This can be a great help in
many situations.

When I first made the jump from using my OS terminal program to using GNU
screen a few years ago, my productivity shot up enormously, as I was able to
quickly move around through terminals like I never could before.  I instantly
started writing code faster, finding problems quicker, and spending much less
time creating and moving terminal windows around on my desktop.


## tmux - A Cool Terminal Multiplexer

While I was using GNU screen for a few years, I always had some issues with it
that didn't sit well with me.  For one, while I had my GNU screen software
highly configured, I was still unable to perform some seemingly basic tasks
like create horizontally split windows.  This meant that I could only open
columns of terminals, restricting the usefulness of my terminal.

Furthermore, GNU screen had a lot of complex key bindings that tended to make
it difficult for me to get used to.  I remember spending quite a bit of time
when first learning GNU screen just memorizing the basics.

One frustrating day while I was struggling to adjust some screen key bindings,
I decided to look for alternatives.  After a bit of research I stumbled upon
tmux.  What a great day that was.

tmux, just like screen, is a terminal multiplexer. What's great about tmux is:

-   It's a lot simpler than GNU screen.  It has sane defaults configured, and
    requires much less configuration to be useful.
-   It supports both vertical AND horizontally split windows.
-   It has a really awesome key binding that allows you to magically rearrange
    your terminal windows in a variety of patterns.  This is extremely useful
    for situations where you open multiple windows, and then want them to be
    moved to a decent looking pattern, but don't want to configure each window
    manually.
-   It has great documentation.


## tmux in Action

A picture is worth a thousand words.  I won't bore you any further, here are
some screenies of tmux in action.

This first picture is just a simple display of tmux with multiple windows open
(note the window names at the bottom):

![tmux Multiple Windows][]

Next, we have a single tmux window open, broken into three panes: one is
vertically split, while the other is horizontally split. As you can see, this
makes coding quite convenient since I can code, look at tests, and browse
documentation all in the same window:

![tmux Multiple Panes][]

Here I just hit a single key, and had tmux automatically re-arrange my panes a
few times in a row.  Nice, huh?

![tmux Gallery 1][]

![tmux Gallery 2][]

![tmux Gallery 3][]


## tmux - Configuration

One of the great things about tmux is that it requires almost no configuration
to be useful.  Unlike GNU screen which requires quite a bit of tweaking (in my
opinion) to be useful, tmux has sane defaults out of the box.

Below is my `~/.tmux.conf` file.  As you can see, it's very simple:

```text
set -g prefix C-a
unbind %
bind \ split-window -h
bind - split-window -v
bind-key k select-pane -U
bind-key j select-pane -D
bind-key h select-pane -L
bind-key l select-pane -R
```

The changes I made are simply to remap keys for my own preferences.  Here's
what my changes do:

-   Set the tmux command key to `CTRL+a` (just like GNU screen).  That means
    all tmux commands are prefixed with `C-a`.
-   To create vertical split windows, I setup key mappings for `C-a |`.  To me,
    since the pipe key (`|`) looks like a vertical split, it makes sense to
    have that key open a new split window.
-   Likewise, I also bound the horizontal split key to `C-a -` (the dash key),
    since the dash key looks like a horizontal split.
-   The last few changes make moving between split windows easy.  To navigate
    through windows, I assigned vim-like keybindings. e.g.
    -   `C-a h` will move you one window to the left.
    -   `C-a j` will move you one window down.
    -   `C-a k` will move you one window up.
    -   `C-a l` will move you one window right.

As you can see, I had to make very few changes to tmux in order for it to be
useful to me.


## tmux - Resources

If you'd like to give tmux a try, here are some resources to get you going.
tmux has become one of my favorite and most used tools since I started using it
earlier last year.  I'd highly recommend it to anyone who does a lot of
terminal work.

-   [The main tmux website.][tmux]
-   `man tmux` has great information and is highly readable.
-   [tmux crash course][], a really great introduction to using tmux.
-   [tmux series][], a series of blog posts explaining tmux in depth.  A great
    read.


  [Tools]: /static/images/2012/tools.png "Tools"
  [tmux]: http://tmux.sourceforge.net/ "tmux"
  [GNU screen]: http://www.gnu.org/software/screen/ "GNU screen"
  [tmux Multiple Windows]: /static/images/2012/tmux-multiple-windows.png "tmux Multiple Windows"
  [tmux Multiple Panes]: /static/images/2012/tmux-multiple-panes.png "tmux Multiple Panes"
  [tmux Gallery 1]: /static/images/2012/tmux-gallery-1.png "tmux Gallery 1"
  [tmux Gallery 2]: /static/images/2012/tmux-gallery-2.png "tmux Gallery 2"
  [tmux Gallery 3]: /static/images/2012/tmux-gallery-3.png "tmux Gallery 3"
  [tmux crash course]: http://robots.thoughtbot.com/post/2641409235/a-tmux-crash-course "tmux Crash Course"
  [tmux series]: http://blog.hawkhost.com/2010/06/28/tmux-the-terminal-multiplexer/ "tmux Series"
