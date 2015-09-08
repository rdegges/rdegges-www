---
title: "My Experience as a New Developer Evangelist"
date: "2014-02-22"
tags: ["startups", "programming", "personal development"]
slug: "my-experience-as-a-new-developer-evangelist"
description: "Reflections and thoughts about my first three weeks as a Developer Evangelist at Stormpath."
---


![Blah Sketch][]


Three weeks ago I joined [Stormpath][] as a Developer Evangelist.

This is my first Developer Evangelist job, and so far it's been a lot different
than anything I've done before.  As many of you know (if you've read my blog),
I'm a programmer, and have been programming almost every day since I was 12.

To say that being a Developer Evangelist is different than being a programmer
would be an understatement.

As a programmer, I'd typically wake up, grab some caffeine, then spend the rest
of the day focusing on a single task: building a feature, fixing a bug, or
handling some combination of the two.

As a Developer Evangelist, I wake up, pick from one of the 100 available tasks,
then start knocking stuff off the todo list.

In short, it's crazy!  If I had to sum up Developer Evangelism for any
interested programmers, I'd call it a lifestyle rather than a job.


## What I Actually Do All Day

![Large Robot Sketch][]

I think the biggest change for me in the first few weeks has been getting used
to what I actually do everyday.

For the first 2 weeks, in particular, although I was doing a lot of stuff, if
felt as though I was slacking off and not accomplishing anything -- mainly
because I wasn't churning out code like I'm used to doing.

I suppose all these years of development have made me feel as if when I'm not
writing code, I'm not really doing anything.

Although I'm still struggling with this concept a bit, I'm beginning to
understand that there are definitely other things I can do to provide value in
my work, other than obsessively focusing on product :)

The first week at work I ended up doing an array of tasks:

- Writing a simple [blog post][] about me joining the team :)
- Getting access to all our internal systems (we use Atlassian for most internal
  stuff: JIRA, Confluence, etc.)
- Discussing what the goals will be for the first month (what stuff we're going
  to be doing -- how we're doing to do it -- and why).
- Lobbying for GitHub access so I could hack up our official [Python SDK][] :)
- Hacking up the Python SDK: cleaning some stuff up, preparing for an official
  1.0.0 release (which happened in week 2).
- Going to a nodejs meetup with my coworkers and building some random programs
  for fun.
- Getting to know my coworkers (they're all awesome, by the way).
- Planning an internal company hackathon (which is taking place this coming
  week!).

In the next two weeks, I ended up picking up the pace and doing quite a few
other things:

- Going to roughly two meetups per week (Python, Django, and nodejs stuff so far).
- Taking ownership over our Python SDK, planning out feature sets, reviewing
  code, and merging pull requests.
- Working on talks for upcoming events (I'm giving a talk on Service Oriented
  Architecture at Rackspace in a couple weeks, and another talk on Password
  Security at [Rocket Space][]).
- Talking with lots of developers and learning what problems they're having with
  authentication stuff (you'd be surprised how hard this is).
- Helping developers out with their Python projects (I've dived into 3 code
  bases in the past week, alone, helping people get various things working).
- Speaking with everyone at Stormpath about what they're working on, and what
  they like about it (these are interesting things to know, and make for good
  articles / etc.).
- Building a new [Flask SDK][] for Stormpath, as well as a pretty neat
  [sample application][] which demonstrates how to use it.
- Planning out our soon-to-be Go SDK and command line utility.
- Lots of other stuff I'm probably forgetting.

Overall, there's essentially a huge backlog of things that need to be done.
Right now this mainly consists of:

- Improving our client libraries.
- Writing better client library docs.
- Publishing interesting blog articles on our tech stack / etc.
- Building various sample applications to make our implementation simpler for
  developers.
- Working on talks and presentations.
- Going to meetups, hackathons, and events, and just generally being a nice guy.

Overall, it appears that almost every day will be different from here on out --
some days I'll be traveling, some days I'll be going to events and meeting
people, some days I'll be in the office writing all day, and some days I'll be
writing code.

It's definitely a change from what I'm used to, and while I'm slowly beginning
to get the hang of things, I've definitely got a long way to go before I get
used to things.


## The Challenges

![Bodybuilder Sketch][]

So far, the biggest challenge as a new Developer Evangelist has been figuring
out how to maintain a workable schedule.

I realized after week 2 that going to multiple meetups per week, while also
trying to maintain a healthy sleep and gym schedule, as well as work from 9 -> 6
is almost impossible.

Fortunately, I'm getting slightly better at this now, but maintaining a healthy
schedule is definitely looking like a challenge.  I've heard from some other
evangelists I've spoken with that their health has gone down the drain as a side
effect of the job, but I refuse to let that happen to me.

My biggest priorities in life at the moment right now are health, friends and
family, then work.

Over the next month I'll be doing my best to balance commitments better to
ensure things can work sustainably!  This might involve changing up work hours
on some days, or maintaining a consistent sleep schedule and only scheduling
events around that -- not sure yet.

Aside from the scheduling problems, the next biggest challenge is trying to
prioritize work effectively.  Right now there are simply so many things to do
(articles to write, events to attend, talks to give, libraries to build, etc.)
that it's really difficult deciding what to do, and when.

Although I realize evangelism is a long-term game, I'd like to maximize the
effect I have, so I'm still trying to figure out what stuff is most effective,
and what stuff is valuable.


## The Good

![Happy Moose Sketch][]

Although I'm still figuring things out, being a Developer Evangelist for
Stormpath is definitely one of the most fun things I've ever done.

It's been pretty awesome.  For years I've loved coding, loved being part of the
community, and loved writing -- but now I get to do all of those things, all
day long, and get paid for it!

It's pretty insane.

It's also really great to be able to do 100% of my work out in the open (on
GitHub), as opposed to building product in private repositories.  Since I'm a
big open source guy myself, it's really nice to be fully able to develop out
in the open, without worrying about needing to keep certain things closed
source.

So far, this job has been great, and it's really growing on me more as time
passes.


## Things I'd Like to Change

![Beast Sketch][]

While Stormpath is really great as a company, there are definitely some things
I'd like to change.

One of the things I'd like to do is remove some of the process around shipping,
and get to a point where balancing content quality with delivery speed is a bit
better.

Right now, we use a pretty heavy process of pushing all tasks through JIRA.  Any
sort of task (product bugs, features, todos, etc.), any sort of work (writing
articles, adding stuff to docs, etc.), and any sort of review (code review,
article review, pull request review, etc.) all gets pipelined through a complex
set of JIRA rules and processes.

As a brand new JIRA user, I'm pretty surprised by how *heavy* this system feels.

Creating tasks in JIRA, and moving through the defined Kanban process takes
seemingly forever, even for handling very minor things: adding links to the
website, cleaning up small documentation fixes, etc.

I understand the need for process, but I think that in a lot of ways, by adding
too much process around tasks you end up with an overload of management
responsibility which just kills time.

What I'd like to do is move non-critical stuff out of our existing system, and
into a more *free* system: [Trello][].

This coming week I'm going to be setting up a few simple Trello boards:

- Articles.
- Sample Applications.

And begin moving my tasks out of JIRA and into Trello.  I think that by
offloading these less-critical, non-engineering tasks into Trello I'll be able
to speed up the delivery of content, and make things move a lot quicker.

The other thing I'd like to do is find a way to get everyone at Stormpath more
involved in the community at large: meetups, conferences, etc.  I realized that
while everyone at Stormpath is incredibly awesome at engineering, most of them
aren't used to getting out into community events, participating in fun stuff
outside of work, etc.

I think that since I'm quite familiar with this stuff, it'll be fun to get
everyone involved, and bring them into the awesomeness that is the development
community in the bay area.


## Closing Thoughts

![Door Sketch][]

The first few weeks as a Developer Evangelist have been pretty crazy.  I've
learned a ton of things, and have been getting more familiar with not only what
I need to be doing, but also what works and what doesn't.

While I still have a long way to go before I'm satisfied with myself, I think
the past few weeks have been a good indicator that I not only really love what
I'm doing here, but that I'm doing a half-decent job.

I'm looking forward to the next month or two, as I plan to solve some of the
problems I've been having, build a bunch of awesome stuff, and make a lot of
people happy.

And oh yeah, have a lot of fun :)

-Randall


  [Blah Sketch]: /static/images/2014/lion-face-sketch.jpg "Lion Face Sketch"
  [Stormpath]: https://stormpath.com "Stormpath - Simple Authentication and User Management for Developers"
  [Large Robot Sketch]: /static/images/2014/large-robot-sketch.jpg "Large Robot Sketch"
  [blog post]: http://stormpath.com/blog/hello-stormpath "Hello, Stormpath!"
  [Python SDK]: https://github.com/stormpath/stormpath-sdk-python "Stormpath Python SDK"
  [Rocket Space]: http://rocket-space.com/ "Rocket Space"
  [Flask SDK]: https://github.com/stormpath/stormpath-flask "Stormpath Flask SDK"
  [sample application]: https://github.com/stormpath/stormpath-flask-sample "Stormpath Flask Sample Application"
  [Bodybuilder Sketch]: /static/images/2014/bodybuilder-sketch.jpg "Bodybuilder Sketch"
  [Happy Moose Sketch]: /static/images/2014/happy-moose-sketch.jpg "Happy Moose Sketch"
  [Beast Sketch]: /static/images/2014/beast-sketch.jpg "Beast Sketch"
  [Trello]: https://trello.com/ "Trello"
  [Door Sketch]: /static/images/2014/door-sketch.jpg "Door Sketch"
