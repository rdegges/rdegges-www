---
title: "My Desktop Environment"
date: "2011-02-12"
tags: ["programming"]
slug: "my-desktop-environment"
description: "A quick look at my standard work environment :)"
---


I love reading about the tools that other people use daily, what sort of
editors they use, what software they consider essential, how they use it, and
why.  I've never taken the time to do a write up about the tools I use, so I
figured this weekend would be as good a time as any.


## General Environment Information

-   **Computer**: Desktop (custom built). 16GB RAM, 2TB disk, wired Ethernet,
    quad core Intel core 7 CPU, nVidia GeForce GTX 285.
-   **OS**: [Kubuntu 10.10 64-bit][] (latest).
-   **Monitors**: 2x Hanns-G 26" 1080p LCD monitors.
-   **Speakers**: Creative 2.1.
-   **Keyboard**: [Logitech Illuminated Keyboard][].
-   **Mouse**: [Logitech Performance MX][].
-   **Amplifier**: [FIIO E9 / E7][].
-   **Headphones**: [Sennheiser HD598][].
-   **Reading**: [Kindle DX (latest)][].
-   **Phone**: [HTC G2][] (Android 2.2)

I prefer using a desktop over a laptop.  I've never really been a fan of
laptops.  They are annoying to carry around, I don't like plugging stuff into
them, and I don't like touch pads (they interfere with my typing).  I build a
new desktop every year, and the one I have now is great.  I've got a large desk
(6" wide) from Costco that I use, and it's large enough to house both of my 26"
monitors, speakers, a USB hub, and my amps with plenty of desk space left over.

I love having two monitors.  I'm a big fan of huge workspaces, it helps me
navigate work much easier.  I'll typically keep Vim full screen on one, and
chrome / music / TV on the other, depending on what I'm currently working on.

My keyboard and mouse are both Logitech.  Since I'm a programmer, I sit at a
computer most of the day.  I've used various types of keyboards and mice
through the years, but these are my favorites.  The illuminated keyboard is
perfect.  It's slim, has a full number pad, perfect lighting for night-time
hacking, and soft keys that have just the right amount of tension, so it feels
good to type on.  The Performance MX mouse is also a favorite.  I hate having
mouse cords run across my desk, but also hate most wireless mice because
they'll get periodically choppy--not this one.  The Performance MX is really
smooth, and responds perfectly even after long periods of inactivity.  It also
lasts a good three days on a single charge, and only takes about 10 minutes to
fully charge.

The Sennheiser headphones are awesome.  I only acquired them recently, but they
completely changed my coding experience.  They completely isolate your from the
outside world, and provide really smooth bass and a clear listening experience.
I often code wearing headphones through the day, and the difference between
these and my old 50$ makes it totally worth the cost.

For reading--I LOVE my Kindle.  I read a lot of books (30 minutes a day,
minimum), and the kindle has been a great way for me to save money and
consolidate my collection.  I've still got a rather large collection of
physical books, but I'm slowly phasing it out in favor of kindle books.  There
are very few books that I wouldn't read on a kindle (mostly fitness books, with
large pictures), but that's about it.  Most tech books I read display
perfectly, and it's become an essential part of my day.

And lastly, I use an HTC G2 phone.  I love Android OS, and couldn't really live
without it.  I keep all of my contacts in Gmail, which nicely syncs down to my
phone, and vice-versa, which really makes daily life simple.

And here's a picture of my workspace:

![My Workspace][]


## Operating System Details

I used to hate KDE, really hate it.  It was slow, choppy, and generally ugly.
The 4.x versions, however, are completely different.  I made the switch from
Ubuntu to Kubuntu about a year ago now, and have been incredibly impressed.

KDE is a great desktop environment.  It's fast, can make use of all the normal
desktop effects (if you've got a decent GPU), and is highly customizable.

Here are some random screen shots of my desktop:

![Desktop Screenshot 1][]

![Desktop Screenshot 2][]

![Desktop Screenshot 3][]


## Software

The most important part of any environment is obviously the software.  Over the
years, I've tried numerous tools, and I routinely try new ones.  The ones that
follow are the ones I absolutely couldn't live without.


### Chrome

I love using [Google Chrome][].  It's got great developer tools built in for
working on your sites, has a lot of great plugins, and magically syncs your
bookmarks with your Gmail account.  It's also much faster to start and run than
Firefox, and has a really clean look to it.  The main killer feature for me is
the app sync.  Whenever you sign into your Google account on another chrome
browser, it will automatically install all of your apps--makes switching
computers simple as shit.

Plugins I use daily:

-   [TweetDeck][]: To view and use my Facebook and Twitter accounts.  It's the
    best client ever made.  Runs in a browser tab, and has sexy desktop
    notifications.
-   [Adblock][]: Who likes viewing ads?  Nobody, that's who.
-   [Google Voice][]: If you use Google Voice, this plugin is a must.  It lets
    you make calls from your browser, send SMS from your browser, listen to
    voicemails, etc.  It contains everything awesome about telephony in a
    single icon.
-   [Minimalist for Gmail][]: This plugin lets you pick and choose Gmail
    features to enable or disable.  Let's you clean up your Gmail interface and
    remove all the cruft you don't want to see.  Immensely pleasing.
-   [Vimium][]: For people like me who use Vim like crack, vimium is the
    perfect productivity tool.  It lets you use Vim key mappings inside chrome
    to navigate webpages without touching your mouse.
-   [Webpage Screenshot][]: Take screen shots of web pages.  Great for quickly
    sharing a screeny with some friends.


### Konsole

KDE's Konsole (terminal emulator) is by far my favorite terminal.  It has a
great GUI paired with lots of functionality and flexibility.  The default key
bindings work great, and are intuitive.  It meets pretty much all of my
terminal needs--with style.

Here's a couple screen shots:

![Konsole Screenshot 1][]

![Konsole Screenshot 2][]


### Vim

As I mentioned before--Vim is my editor of choice.  I code a lot, and Vim makes
coding easy.  I've messed around with lots of other options: emacs, eclipse,
gedit, kate, and some other tools, but Vim has always been my first choice.

The Vim key bindings are intuitive, and make editing simple.  I'm able to fly
through large sets of files, making small changes and frequently doing Git
commits with ease.  I've still got a long way to go before my Vim skills are
advanced level, but even at a beginner level, I still find myself extremely
happy with my productivity.

In addition to the (wide array) of basic Vim tools, I also use several plugins
which really improve the experience.  In no particular order:

-   [pathogen][]: Makes it easy to install new plugins and keep them organized.
-   [vim-puppet][]: Adds syntax highlighting for puppet files.
-   [vim-pyflakes][]: Magically interprets your python code as you write it,
    and gives you interpreter errors in your vim status window so that you can
    fix them without ever running the code.
-   [ropevim][]: Adds lots of handy vim key mappings for refactoring python
    code.
-   [snipmate][]: Lets you build (and use) code snippets for automatically
    populating code based on what you're typing.  For example, if you find
    yourself typing `for x in blah:` a lot, you can make a snippet for that,
    and when you start typing that statement it will automatically insert a
    template, and let you tab through the variables to update them.  Saves a
    TON of time.
-   [snipmate_django][]: Django snippets.
-   [trailing-whitespace][]: Removes all trailing whitespace from your files.
    I hate trailing whitespace.
-   [vim-fugitive][]: Adds Git support into Vim.  Never leave your Vim window
    again to use Git!
-   [vim-uninpaired][]: Adds key mappings for scrolling through files.
    Especially useful when using with vim-fugitive.  You can scroll through
    versions of a file controlled with git using hotkeys.

Obligatory screen shots:

![Vim Screenshot 1][]

![Vim Screenshot 2][]


### Screen

I only recently learned how to use GNU screen properly.  I will never go back.
Using screen has given me a huge productivity boost.  It lets you navigate
through windows quickly, mash windows together via splits, maintain copy+paste
buffers between screens, and do interactive sessions with other developers.

Before I started using screen, I would maintain at least 8 Konsole windows at
all times.  This was not optimal, because in order to switch between windows, I
would have to analyze ALT+TAB combinations carefully and slowly, or move my
hands off the keyboard to use the mouse.  Both of those solutions are slow and
annoying when you're trying to quickly navigate windows.  Using screen
completely changed my work flow.  Now I'll typically maintain a single Konsole
window full screen using GNU screen, and keep multiple screen windows open that
I'll switch through using `CTRL+a <numeric>` or `CTRL+a <p/n>` (previous and
next windows, respectively).  This makes switching windows quick, efficient,
and non-intrusive to my daily work flow.

Furthermore, I maintain a decent `.screenrc` file, which includes two status
lines that always display:

-   The `hostname` of the computer I'm working on.
-   The load average.
-   The date and time.
-   All screen windows that are open, and a special notation for the active
    screen window.

This makes it easy to identify my active windows, and keep track of what is
where:

![GNU Screen Screenshot][]


### Dropbox

[Dropbox][] just makes everything easier.  I use it to sync all of my desktop
files: code, music, pictures, configuration files, etc.  Most of my `/home`
directory is synced there somewhere.  Dropbox (if you haven't heard of it),
allows you to sync files between multiple computers.  I put all of my files
into my `/home/rdegges/Dropbox` folder, and then symlink to major folders from
there, e.g. `ln -s /home/rdegges/Dropbox/Documents /home/rdegges/Documents`.
Makes all of my stuff sync transparently.

The main benefits with Dropbox are that all my files are always backed up, and
that I can easily switch computers.  Let's say I need to use my laptop
somewhere, as soon as I turn it on, it'll sync all my desktop files to my
laptop, and essentially fully configure my data for me.  No work necessary.


### Amarok

I listen to a lot of music.  [Amarok][] is my favorite music player for Linux.
It has lots of great plugins (including [last.fm][] support), album art,
lyrics, streaming servers, and lots of other goodies.  It also has a great UI
which cleanly integrates with my KDE desktop, and the globally configurable
hot keys allow me to quickly sort through music without ever touching the
mouse.

Screen shot below.

![Amarok Screenshot][]


### IRSSI

If you've ever used IRC, you've likely heard of [IRSSI][].  It's probably the
best IRC client for command line users.  It provides tons of configuration
options, a clean interface, and intuitive key mappings for navigating the UI.
I use IRC all the time (have been IRC longer than I've been using Linux,
actually), and IRSSI is my weapon of choice.

Screen shot:

![IRSSI Screenshot][]


## Conclusion

Those are my tools in a nutshell.  I'm specifically not including my coding
tools here (Judson, fabric, Python, etc.) because that should really be in a
separate post.


  [Kubuntu 10.10 64-bit]: http://www.kubuntu.org/ "Kubuntu 10.10 64-bit"
  [Logitech Illuminated Keyboard]: http://www.amazon.com/gp/product/B001F51G16/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B001F51G16&linkCode=as2&tag=rdegges-20 "Logitech Illuminated Keyboard"
  [Logitech Performance MX]: http://www.amazon.com/gp/product/B002HWRJBM/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B002HWRJBM&linkCode=as2&tag=rdegges-20 "Logitech Performance MX"
  [FIIO E9 / E7]: http://www.amazon.com/gp/product/B004M172FY/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B004M172FY&linkCode=as2&tag=rdegges-20 "FiiO E9 / E7"
  [Sennheiser HD598]: http://www.amazon.com/gp/product/B0042A8CW2/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B0042A8CW2&linkCode=as2&tag=rdegges-20 "Sennheiser HD598"
  [Kindle DX (latest)]: http://www.amazon.com/gp/product/B002GYWHSQ/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B002GYWHSQ&linkCode=as2&tag=rdegges-20 "Kindle DX"
  [HTC G2]: http://www.amazon.com/gp/product/B004ZF0E16/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B004ZF0E16&linkCode=as2&tag=rdegges-20 "HTC G2"
  [My Workspace]: /static/images/2011/my-workspace.png "My Workspace"
  [Desktop Screenshot 1]: /static/images/2011/desktop-screenshot-1.png "Desktop Screenshot 1"
  [Desktop Screenshot 2]: /static/images/2011/desktop-screenshot-2.png "Desktop Screenshot 2"
  [Desktop Screenshot 3]: /static/images/2011/desktop-screenshot-3.png "Desktop Screenshot 3"
  [Google Chrome]: http://www.google.com/chrome "Google Chrome"
  [TweetDeck]: http://www.tweetdeck.com/ "TweetDeck"
  [Adblock]: https://chrome.google.com/webstore/detail/gighmmpiobklfepjocnamgkkbiglidom "Adblock"
  [Google Voice]: https://chrome.google.com/webstore/detail/kcnhkahnjcbndmmehfkdnkjomaanaooo "Google Voice"
  [Minimalist for Gmail]: https://chrome.google.com/webstore/detail/oddhbkghjoccbljmagcgoklbfdjeiinb "Minimalist for Gmail"
  [Vimium]: https://chrome.google.com/webstore/detail/dbepggeogbaibhgnhhndojpepiihcmeb "Vimium"
  [Webpage Screenshot]: https://chrome.google.com/webstore/detail/ckibcdccnfeookdmbahgiakhnjcddpki "Webpage Screenshot"
  [Konsole Screenshot 1]: /static/images/2011/konsole-screenshot-1.png "Konsole Screenshot 1"
  [Konsole Screenshot 2]: /static/images/2011/konsole-screenshot-2.png "Konsole Screenshot 2"
  [pathogen]: https://github.com/tpope/vim-pathogen "pathogen"
  [vim-puppet]: https://github.com/rodjek/vim-puppet "vim-puppet"
  [vim-pyflakes]: https://github.com/kevinw/pyflakes-vim "vim-pyflakes"
  [ropevim]: https://github.com/gordyt/rope-vim "ropevim"
  [snipmate]: https://github.com/msanders/snipmate.vim "snipmate"
  [snipmate_django]: https://github.com/robhudson/snipmate_for_django "snipmate_django"
  [trailing-whitespace]: https://github.com/vim-scripts/trailing-whitespace "trailing-whitespace"
  [vim-fugitive]: https://github.com/tpope/vim-fugitive "vim-fugitive"
  [vim-uninpaired]: https://github.com/tpope/vim-unimpaired "vim-unimpaired"
  [Vim Screenshot 1]: /static/images/2011/vim-screenshot-1.png "Vim Screenshot 1"
  [Vim Screenshot 2]: /static/images/2011/vim-screenshot-2.png "Vim Screenshot 2"
  [GNU Screen Screenshot]: /static/images/2011/gnu-screen-screenshot.png "GNU Screen Screenshot"
  [Dropbox]: http://db.tt/nP9tpb2 "Dropbox"
  [Amarok]: http://amarok.kde.org/en "Amarok"
  [last.fm]: http://www.last.fm/home "last.fm"
  [Amarok Screenshot]: /static/images/2011/amarok-screenshot.png "Amarok Screenshot"
  [IRSSI]: http://www.irssi.org/ "IRSSI"
  [IRSSI Screenshot]: /static/images/2011/irssi-screenshot.png "IRSSI Screenshot"
