---
title: "How to Instantly Fix Problematic Deployments on Heroku"
date: "2012-01-08"
tags: "programming, devops"
slug: "how-to-instantly-fix-problematic-deployments-on-heroku"
description: "Instantly fix broken Heroku deployments with the awesome rollback tool."
---


![Broke Production][]


**NOTE**: Have no idea what [Heroku][] is?  I feel sorry for you.  You should
create an account with them immediately, then come back and read this post!

Today I was working with my new co-worker on one of our company's [Django][]
projects, and after deploying some code, noticed that our [New Relic][] panel
was spitting out loads of `DatabaseErrors`.

**Oh shit!**

In situations like this, Heroku's fabulous [releases][] add-on can really save
the day.  While the releases add-on is still in beta, it is indispensable to
any serious project.  Using the releases add-on, I simply ran the command:
`heroku rollback` in the terminal, and everything was fine.  How awesome is
that?

The releases add-on gives you an extremely useful `rollback` command to use,
that instantly swaps your deployed Heroku code with the most recent deployed
copy.  This is a lifesaver.  Without the releases application, you have only a
few choices available to you should a disaster occur:

-   Revert all of your previous commits in your local Git repository, then push
    your changes to Heroku.  This works--but takes a while to do, and can be
    error prone (do you know what the most recent deployed Git commit was on
    Heroku vs. your local repo?).
-   Slowly go through your most recent commits, looking to find the problem
    area.  Once you've found the problematic code--update it, then re-push to
    Heroku.  Again, this is time consuming and error prone.
-   Freak out, and run away.

All three of those options suck. The releases add-on is a developer safety net,
and a good one.  Instead of wasting time worrying about stuff, just `rollback`
your Heroku application, and casually debug your application looking for the
problems.

In addition to the awesomeness of the simple `rollback` command, the advanced
releases add-on (`heroku addons:add releases:advanced` gives you even more
power: the ability to instantly deploy any revision of code previously deployed
to Heroku.

Let's say you deploy several times before realizing your application is broken,
and there is already an army of angry users with pitchforks heading to your
Cheeto covered dungeon.

![Cheeto Hands][]

The last thing you want to do is throw on your chain mail, grab your longsword,
and fight them off.  Let's face reality here: you'd much rather be watching
[The IT Crowd][] and guzzling mountain dew.  So instead of going to war, you
decide to simply roll back to the last working release.

**But wait!**  Your rollback command isn't working!  You forgot that the last
working release was several deployments ago.  Damn.

Luckily, you remember that since you're using the releases add-on, you can
simply run `heroku releases` and view a list of all your previous releases:

![Heroku Releases][]

Oh yes, you think. Release `v304` was the last working release.  Just to
confirm, you then run the `heroku releases:info v304` command, and after taking
a look to make sure, you decide that you've found the correct release to
rollback to.

To finish your rollback, you simply run `heroku rollback v304` and *bam*,
everything is working again.  Now you can spend the rest of the afternoon
writing a [Twilio][] script that sends text messages to each of your users
en-route to your Cheeto dungeon to destroy you, informing them that the problem
has been solved, and asking them to return to their lairs.

Whenever you're working on production projects, problems will arise.  Being a
developer is no easy task!  Luckily for us, Heroku is on our side.

If you're interested in using the Heroku releases add-on, you should read
through the [official documentation][], it's really great.

**UPDATE**: So, I actually wrote a book on Heroku!  If you liked this post, you
should check it out: [http://www.theherokuhackersguide.com/][]


  [Broke Production]: /static/images/2012/broke-production.png "Broke Production"
  [Heroku]: http://www.heroku.com/ "Heroku"
  [Django]: https://www.djangoproject.com/ "Django"
  [New Relic]: http://newrelic.com/ "New Relic, the Best Fucking Application Monitoring Software Ever Written"
  [releases]: http://addons.heroku.com/releases "Heroku Releases Addon"
  [Cheeto Hands]: /static/images/2012/cheeto-hands.png "Cheeto Hands"
  [The IT Crowd]: http://www.imdb.com/title/tt0487831/ "The IT Crowd"
  [Heroku Releases]: /static/images/2012/heroku-releases.png "Heroku Releases CLI Screen Shot"
  [Twilio]: http://www.twilio.com/ "Twilio"
  [official documentation]: http://devcenter.heroku.com/articles/releases "Heroku Releases Addon Documentation"
  [http://www.theherokuhackersguide.com/]: http://www.theherokuhackersguide.com/ "The Heroku Hacker's Guide"
