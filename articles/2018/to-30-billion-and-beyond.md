---
aliases:
  - "/to-30-billion-and-beyond/"
date: "2018-01-03"
description: "A story about building a scaling a web service in an extremely simple way using Heroku."
slug: "to-30-billion-and-beyond"
tags:
  - "programming"
  - "devops"
title: "To 30 Billion and Beyond"
---


![Buzz Lightyear Charging Sketch][]

Several years ago I created a free web service, [ipify](https://www.ipify.org/).
ipify is a freely available, highly scalable ip address lookup service. When you
query its REST API, it returns your public-facing IP address.

I created ipify because at the time I was building complex infrastructure
management software and needed to dynamically discover the public IP address of
some cloud instances without using any management APIs.

When I searched online for freely available reverse IP lookup services I didn't
find any suitable solutions:

- There were websites I could attempt to scrape my IP from (but this is bad
  form, and would likely result in complaints from the host)
- There were APIs for this that charged money (yuck!)
- There were APIs that allowed you to do a limited number of lookups per day
  (which scared me as I was managing a lot of instances at the time)
- There were APIs that appeared to be what I wanted, but upon using them they'd
  error out, go down randomly, or just otherwise not be of high quality. When I
  inspected the `dig` records of a particular provider, I noticed that the
  entire service was running on a single server (with an A record) that was
  terminating requests directly: not the most scalable/highly available service
  in the world.
- There was an API service that looked somewhat OK but was trying to raise money
  via donations to stay alive. Integrating with an API service on the brink of
  death didn't make me feel terribly comfortable.

Because of all these reasons I figured I'd just throw a small service together
myself and solve the problem for as many people as possible. After all: writing
software to return a single string isn't terribly hard: why *shouldn't* I do it?

I assumed that worst case I'd spend $30 bucks or so per month and treat it as a
public service.


## ipify v0

The first iteration of ipify was quite simple. I wrote an extremely tiny (< 50
LOC) API service in Node (I was playing around with Node a lot at the time).
Since the entire premise of the ipify service is returning a string, I figured
this was a perfect use case for Node as a technology: handling a lot of requests
with minimal CPU usage.

After I had the API service built in Node, I threw together a simple static site
to power the front-end and deployed it into an S3 bucket on Amazon. I then
configured a CloudFront origin (Amazon's CDN service) to sit in front of the S3
bucket and cache the pages for ultra-fast load times.

Now, I'm not a designer by any stretch of the imagination... But, with a little
[bootstrap](https://getbootstrap.com/) love things turned out half-decent =)

After getting everything working I did some quick testing and things seemed to
be working ok so I moved onto the next phase: deployment.


## Enter Heroku

![Heroku Logo][]

I'm a big [fan of Heroku](https://www.rdegges.com/2012/heroku-isnt-for-idiots/)
(I've even written [a book](https://www.theherokuhackersguide.com/) about it).
I've been using it for many years now and consider it to be one of the most
underrated services in the developer world. If you've never used it, go [check
it out](https://www.heroku.com/)!

I decided that if I wanted to run ipify in a scalable, highly available and
cheap way then Heroku was the simplest and best option: so that's what I went
with.

I deployed ipify to Heroku in a minute or two, ran it on a single dyno (web
server), and did some limited testing. Things again seemed to be working well
and I was feeling pretty happy with myself.

If you aren't familiar with Heroku, let me explain how ipify's infrastructure
was working:

- Heroku ran my ipify web service on a small dyno (web server) with 512M RAM and
  limited CPU
- If my process crashed or had any critical issues, Heroku would automatically
  restart it for me
- Heroku ran a load balancer that accepted all incoming requests for my app and
  forwarded them to my dyno (web server) to process the request

This is a nice setup because:

- Everything is highly available: Heroku's load balancers, my dyno, everything
- It requires no maintenance, configuration management, or any sort of
  deployment code. It's 100% automated.
- It's cheap: I paid ~$7/mo to run this single web server
- It's fast: Heroku runs on top of Amazon Web Services (AWS), so my
  infrastructure was running in one of the most popular cloud hosted
  destinations in the world: AWS us-east (Virginia). This means it is
  geographically running on the east coast of the US: just across the water from
  Europe, and not terribly far from the rest of the continental US. This means
  users from most parts of the world wouldn't have to make an enormous hop to
  reach the service.

At this point, I was feeling pretty good. This took < 1 day's worth of work to
build, setup, test, and move into production.

I then integrated ipify into my own infrastructure management code to solve the
problem I had initially needed to resolve.

Things were going great for about a month before I started noticing some
issues...


## Popularity... Ugh

![Spartan Warrior Sketch][]

I never marketed ipify, but it ended up ranking really high for the "ip address
api" search phrase on Google. I guess all those years working on copy editing
and SEO paid off.

Within a month or so, ipify was ranking near the top of Google search results,
bringing in thousands of new users. With the increased visibility of the
service, I started seeing some issues.

My Heroku load balancer was firing off warnings because my Node server wasn't
servicing incoming requests quickly enough. What ended up happening was:

- Too many users would make API requests to ipify
- My Node server would start responding to requests slowly so latency would rise
- The Heroku load balancer would notice this and start buffering requests before
  sending them onto my Node server
- Because my Node server wasn't servicing requests quickly enough, my load
  balancer would return a 503 to the user and the request would die off

Not a pretty picture.

So what I did was simple: I added another Heroku dyno. This way, I'd have twice
the capacity and things would run smoothly again. The downside is that running
two "production" dynos on Heroku spiked my cost up to $50. Once you've gone past
one dyno, you have to pay normal rates: $25/mo/dyno.

I figured that by now the service had likely capped out in popularity and I was
OK paying $50/mo, so I'd just do that and things would go back to normal.

But... Things didn't quite work out that way.

Before even a week had passed, I was already getting alerts from Heroku telling
me that I was having the same issue as before. When I looked at my stats, I
could see that my traffic had doubled, and again it appeared like ipify was just
simply getting too much usage.

I added another dyno (brining my monthly cost up to ~$75/mo), but decided to
investigate further. I'm a frugal guy -- the idea of losing > $50/mo seemed
unpleasant.


## The Investigation

![L Sketch][]

When I started investigating what was going on, the first thing I did was check
to see how many requests per second (rps) ipify was actually getting. I was
pretty surprised by the number: *it was low*.

If my memory serves me correctly, ipify was only getting around 10 rps at the
time. When I saw how small the number was, I figured something bad must be
happening in my code. If I can't service 10 rps across two small web servers, I
must be doing something horribly wrong.

The first thing I noticed was that I was running a single Node process. This was
an easy fix: I started using the Node [cluster
module](https://nodejs.org/api/cluster.html), and bam: I was immediately running
one process for each CPU core. This effectively doubled my throughput on my
Heroku dynos.

But 20 rps still seemed like a tiny number so I did some more digging. Instead
of doing load testing on Heroku, I did some load testing locally on my laptop.

My laptop was far stronger than a small 512M RAM Heroku dyno, so I figured I
should see much better throughput.

I did some testing using the [ab
tool](https://httpd.apache.org/docs/2.4/programs/ab.html) and was surprised to
see that even on my laptop I was unable to surpass a threshold of 30 rps from my
Node processes (I run Linux on my laptop and ab works effectively there). I then
did some basic profiling and found that Node was spending a lot of time
performing basic string manipulation operations (to extract the IP address from
the `X-Forwarded-For` header and clean it up). No matter what I experimented
with, I was unable to boost throughput up much above that limit.

At this point, the production ipify service was able to serve roughly 20 RPS
across two dynos. ipify was in total serving ~52 million requests/mo. Not
impressive.

I decided to rewrite the service in Go (which I started using a few months
before) for performance purposes to see whether or not I could get more
throughput out of an equivalent Go server.


## ipify v1

![Warrior Sketch][]

Rewriting ipify in Go was a short (but fun) experiment.

It gave me the opportunity to mess around with many different Go routing stacks:
Gorilla/mux, Martini, and
[httprouter](https://github.com/julienschmidt/httprouter). After benchmarking
and playing around with all three routing tools, I ended up using httprouter as
it performed significantly better than the other two more popular options.

On my laptop I was able to achieve ~2,500 requests/second from my Go server. A
massive improvement. The memory footprint was also much lower and hovered around
5M.

With my new found love for Go, I immediately took action and deployed my new
Go-based ipify service on Heroku.

The results were fantastic. I was able to get about ~2k RPS of throughput from a
single dyno! This brought my hosting back down to $25/mo and my total throughput
to ~5.2 billion requests/mo.

Several days later, while talking to a more experienced Go developer, I ended up
rewriting some of my string handling functionality which netted me an extra ~1k
RPS of throughput. I At this point I was able to sustain ~7.7 billion
requests/mo per dyno (give or take a bit).

I was thrilled to say the least.


## More Popularity

![Tyrael Sketch][]

Although I was able to cut back my hosting cost down to a reasonable range for a
short period of time, within roughly two months ipify started experiencing
issues once more.

It's growth had continued to rise at an astounding rate. Around this time I had
set up [Google Alerts](https://www.google.com/alerts) for ipify, so that I'd
know when people mentioned it.

I started getting notifications that more and more people started using ipify in
their personal and work projects. I then began receiving email from companies
asking if they can embed it in their products (including a large smart TV
provider, numerous media agencies, IoT vendors, etc.).

Before I knew it ipify was servicing around 15 billion requests/mo and I was now
back to spending $50/mo on hosting costs.

But that too didn't last for long.

I noticed rather quickly that ipify's traffic continued to rapidly increase.
There was a period of several months where it would add an additional billion
requests each month.

I also started having issues with burst traffic -- ipify would receive massive
amounts of burst traffic for a short period of time that would die off quickly.
I presumed this traffic was part of bootstrapping scripts, cron jobs, and other
similar timed operations.

I later discovered through user notifications that antivirus vendors started
blocking ipify because it started getting used in root kits, viruses, and other
nasty pieces of software. Attackers would use ipify to get the victim's public
IP address before firing it off to a central location to be used for malicious
purposes. I suppose this sort of usage was responsible for a large amount of
that burst traffic.

While I'm not a fan of helping VX authors or spending money to assist them, I
made the decision to keep ipify running neutrally to serve anyone who wants to
use it. I've never been a fan of developer services that pick and choose what
people use them for. I like to keep things simple.

Which left me to deal with the burst traffic problem. Dealing with burst traffic
was tricky because I primarily had two choices:

- Run additional dynos at a cost to myself and be always prepared for burst
  traffic, or
- Use an auto scaling tool like
  [Adept](https://elements.heroku.com/addons/adept-scale) to automatically
  create and destroy dynos based on traffic patterns on my behalf

I eventually decided to manually involve myself and go with option #1, simply
because I didn't want to spend any additional funds on Adept's service (even
though I've used it before, and it is fantastic). Around this time I was
spending $150/mo and ipify was servicing ~25 billion requests/mo.

Which brings us to the recent past.


## ipify Hits 30 Billion Requests

![Buzz Lightyear Proud Sketch][]

Over the past few months, ipify has hit a new record and surpassed 30 billion
requests/mo on several occasions. It was an exciting milestone to surpass and
something that has been fun to watch.

Today, ipify routinely serves between 2k and 20k RPS (which is almost never
consistent). Traffic is always variable and the usage is so routinely high that
I've completely given up on trying to detect traffic patterns in any meaningful
way. Average response time ranges between 1 and 20ms depending on traffic
patterns.

Today the service runs for between $150/mo and $200/mo depending on burst
traffic and other factors. If I factor that into my calculator (assuming a
$200/mo spend), it looks as if ipify is able to service each request for total
cost of $0.000000007. That's astoundingly low.

If you compare that to the expected cost of running the same service on
something like Lambda, ipify would rack up a total bill of: $1,243.582/mo
(compute) + $6,000/mo (requests) = ~$7,243.58. As a quick note, this is some
back-of-a-napkin math. I plugged ipify's numbers into a Lambda pricing example
from the AWS website here: https://aws.amazon.com/lambda/pricing/.

All in all, I'm *extremely satisfied* with ipify's cost. It's a frugal service
that serves a simple purpose.


## ipify's Future

Which leads me to the future. As ipify continues to grow, the service has gotten
requests for a lot of different things: ipv6 support (*something that Heroku
does not support :(*), better web design, other metadata about IP addresses,
etc.

As I'm incredibly busy with other projects nowadays, I ended up passing
ownership of ipify along to my good friends at
[https://www.whoisxmlapi.com](https://www.whoisxmlapi.com/).

Jonathan and team are good people working to build a portfolio of valuable and
interesting developer API services.

While I still help out with things from time-to-time, Jonathan and team are
currently implementing new features for ipify, and working hard to roll out some
pretty cool changes that I'm excited about (including an improved UI and more
data endpoint).

I look forward to seeing how [ipify](https://www.ipify.org/) continues to grow
over the coming years.

If you have any questions or would like to get in touch with me, please [shoot
me an email](mailto:r@rdegges.com).

-R


  [Buzz Lightyear Charging Sketch]: /static/images/2018/buzz-lightyear-charging-sketch.jpg "Buzz Lightyear Charging Sketch"
  [Heroku Logo]: /static/images/2018/heroku-logo.jpg "Heroku Logo"
  [Spartan Warrior Sketch]: /static/images/2018/spartan-warrior-sketch.jpg "Spartan Warrior Sketch"
  [L Sketch]: /static/images/2018/l-sketch.jpg "L Sketch"
  [Warrior Sketch]: /static/images/2018/warrior-sketch.jpg "Warrior Sketch"
  [Tyrael Sketch]: /static/images/2018/tyrael-sketch.jpg "Tyrael Sketch"
  [Buzz Lightyear Proud Sketch]: /static/images/2018/buzz-lightyear-proud-sketch.jpg "Buzz Lightyear Proud Sketch"
