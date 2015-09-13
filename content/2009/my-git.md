---
date: "2009-12-04"
description: "A short, personal review of Scott Chacon's new book: Pro Git.  TLDR?  It's awesome, and you should read it."
slug: "my-git"
tags: ["git"]
title: "My Git"
---


![Pro Git Book Cover][]

A few days back I ordered a copy of [Scott Chacon][]'s book: [Pro Git][], which
I am really enjoying reading.  Scott is an excellent writer, and really does
justice to [Git][].  I was reflecting on his enthusiasm, and thinking about my
own.  Here are my thoughts on Git, and my experience with it over the years.

I started using Git around 2 years ago when I saw a screencast discussing it
online.  What initially drew me to Git was that it was created by [Linus][] (who
was very enthusiastic about it), and that my previous experiences with version
control systems ([VCS][]) were horrible.  Naturally, I wanted to give it a try,
and get back to the best-practices way of doing things (using a VCS).

When I first learned about VCS, pretty much everyone used [SVN][] or [CVS][].
When I researched them both, there was no doubt in my mind that SVN was clearly
the most popular, and so that's what I decided to learn.  I started using SVN
for all of my code (most of it was hosted on [SourceForge][] at some point or
    another), and learned it well enough to push periodic updates to my projects
    and do basic collaboration with a few other people.

However, I never really liked SVN.  It was always slow and time consuming to
perform commits (something that you should do extremely frequently), so I just
stopped doing them often.  This got me into the bad habit of only performing a
commit for a release, something that is definitely frowned upon, and completely
nullifies any benefits that you get from using a VCS in the first place!  To
make the situation even worse: at the time, a good portion of the code I was
writing was offline.  This meant that I was unable to make commits when working
on my code, as without an internet connection I couldn't connect to the remote
repository.

Using SVN also imposed limits on my work with others.  A lot of the projects I
worked on required collaboration with several other people.  Using SVN slowed
the process down.  Performing merges, managing access rights, and doing SVN
updates always took a lot of time.  Also, if the SVN repository was down, it
meant that nobody could access the source or project history, which made team
effort difficult.

The other large issue I had (and still have) with SVN is that there are no good
project hosting websites out there which meet my needs.  SourceForge, which is
probably the largest and most popular SVN project hosting site is slow, filled
with ads, and has an unintuitive interface.  It also requires approval for every
project which can sometimes take hours.  What I want in a project hosting site
is something that:

-   Has a clean and pretty interface with no (or few) ads.
-   Allows developers to instantly create a new project and get to work.
-   Makes managing access rights and collaboration simple.
-   Allows private projects, which are necessary for proprietary code.
-   Has an issue tracker for each project, which allows advanced categorization
    of bugs and fixes.  Something that makes it easy for both users to submit
    issues (and propose fixes), and developers to close bugs and keep it
    organized.
-   Allows you to store large projects and releases.
-   Has a pretty source viewer so that users can casually browse any version of
    your source code through a simple navigation window, and can permalink to
    any piece of code at their whim.
-   Allows users to embed snippets of code in their web pages for display on
    other sites.
-   Has pretty URLs, none of that `?p=155` stuff.
-   Has a wiki system that looks nice and is simple to navigate for users.
-   Has detailed graphs and statistics for each project.
-   Has some sort of 'watch' or 'follow' functionality which allows users to
    monitor the status of a project over time.

Enter Git.  *Git felt like it was designed for me.*

As a developer who works on many projects small and large, I need a VCS which
will be as flexible as I am.

Git is fully distributed, so no matter where I am or how many people are working
on a project, I always have complete access to all revisions of the source.
There are no file deltas (Git stores the entire file), and I can instantly see
what the source looked like at any given time in the project's history whether
I'm online or offline.  This gives me the flexibility to get work done wherever
I am, whether it be on a plane, at the beach, or in the park.  When you perform
commits in Git, the files are checked into your local repository.  Once you have
internet access, you can push to your remote repository and add your full
history straight into the project as if you were online the entire time.

Git also makes collaboration a simple process.  I don't have to manage a Git
database and allow access to certain users: when someone makes a patch or adds
code, they can simply link me to their Git repository, and I can merge it into
the project at my leisure.  This has the added benefit of being able to see all
of the source contributor's history in my project once I have merged the
branches together.  This makes working with other people extremely easy and
reduces the hassle of managing a large monolithic SVN repository.

Git also handles merging and re-basing beautifully.  When conflicts arise I am
notified, and the current working revision is put on hold until these errors are
fixed or stashed.  Git adds the appropriate conflict information to my files so
I can see exactly what is conflicting, and how it needs to be changed to
progress.

Lastly, Git has an great community, and [GitHub][].  GitHub is the ultimate
project hosting site.  You can create projects instantly and store large files.
You can also store all of your SSH keys for the various systems you work on,
thereby showing different commit users and / or messages.  GitHub has a simple
and intuitive web interface which looks great, and has clean functionality for
users, developers, and people exploring the site.

The GitHub source viewer is nice as well.  It lets you browse the entire history
of the project, you can see a full snapshot of exactly what the source looked
like at any given time.  It also allows you to get a direct permalink to any
particular source file from any revision in the project's history.  This is
extremely useful for source review and any sort of online publishing /
collaboration tools.

One of my favorite GitHub features is the ability to instantly 'fork' a project.
Forking a project is extremely easy, simply click the 'fork' button on the
project you'd like to fork.  GitHub will instantly copy the projects source /
history to your account, and automatically create your own Git repository for
the project which you can change and modify all you like.  This is very useful,
as if you see a project you'd like to make a patch for, you can fork it, make
the patch, and link the real project owner to your forked repository, where they
can then merge in your changes!  It's also useful for people who just want to
make their own modifications to a project.  GitHub's forking provides an elegant
solution to a common problem.

Yet another nice feature of GitHub is it's social networking type feel.  Every
account can 'watch projects', send private messages, add and remove friends, and
get instant updates when your friends add / remove code to their projects.
GitHub is also releasing a resume searching tool on their site at some point in
the near future, and they have already implemented resume pages for each user
who wishes to add to them.  This means that in addition to providing project
hosting, they'll also be able to help companies find talented programmers based
on their actual work!

GitHub also has many other neat features including a wiki system, statistics
system for gathering project stats, and a language browsing feature which makes
finding new projects in your favorite programming languages fun.

Since learning Git, and discovering all the nice features that it offers (in
addition to the general awesomeness of GitHub), I think that I've definitely
become a better programmer.  Git has helped me remedy my bad habits by making
the committing and merging systems thoughtless, and has given me the ability to
really get the most out of my coding experiences.  Git has also made running an
contributing to open source projects fun again, and that what it is all about.


  [Pro Git Book Cover]: /static/blog/images/2009/pro-git-book-cover.png "Pro Git Book Cover"
  [Scott Chacon]: http://scottchacon.com/ "Scott Chacon"
  [Pro Git]: http://www.amazon.com/gp/product/1430218339/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=1430218339&linkCode=as2&tag=rdegges-20 "Pro Git"
  [Git]: http://git-scm.com/ "Git"
  [Linus]: http://en.wikipedia.org/wiki/Linus_Torvalds "Linus Torvalds"
  [VCS]: http://en.wikipedia.org/wiki/Revision_control "Revision Control"
  [SVN]: http://subversion.apache.org/ "Subversion"
  [CVS]: http://cvs.nongnu.org/ "Concurrent Versions System"
  [SourceForge]: http://sourceforge.net/ "SourceForge"
  [GitHub]: https://github.com/ "GitHub"
