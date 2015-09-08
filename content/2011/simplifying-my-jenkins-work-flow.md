---
title: "Simplifying My Jenkins Work Flow"
date: "2011-06-01"
tags: ["devops"]
slug: "simplifying-my-jenkins-work-flow"
description: "A quick hack to allow Jenkins to auto-accept all new SSH keys."
---


![Arrow Sketch][]


Up until recently, my [Jenkins][] work flow has been tedious.  It typically
went something like:

1.  Install Jenkins instance, fully configure it the way I want.
2.  Setup a few new projects to start building / testing / deploying.
3.  Spin up a new application server to deploy my project to.
4.  Watch my Jenkins deploy fail, as I forgot to accept my new server's SSH
    identity manually.
5.  Log into my Jenkins server as the `jenkins` user.
6.  Run `ssh <new_server_ip>`, and accept the stupid identity.

At work, we're constantly building out new servers--sometimes, automatically.
And Jenkins is a critical part of our infrastructure.  We use it to build,
test, then **deploy** all of our code straight into production.  When we spin
up new servers, the process looks like this:

1.  New server is booted.
2.  New server is bootstrapped with [puppet][] configurations.
3.  New server auto-configures itself according to our puppet node rules.
4.  Project deployment script is updated to include new server.
5.  We push an update to our code to GitHub.
6.  Jenkins pulls the latest code changes, tests the code, then attempts to
    deploy it to our new server.

This is where the problems happen--since we haven't manually verified the
identity of our new server, our Jenkins box will just start failing builds
since it won't SSH into a server before accepting the identity.


## The Fix

To remove the hassle of manually accepting each server's identity, we recently
decided to do away with the identity check all together to make our lives
easier.  This solution may not work for everyone (especially if security is a
real concern for your team), but for us it works great!

Just modify your `/etc/ssh/sshd_config` file and change

`ChallengeResponseAuthentication yes`

To...

`ChallengeResponseAuthentication no`

This will let your SSH client completely ignore the remote machine's identity
when ssh'ing into an unknown server.  This is great for us, since we're
constantly building out new servers automatically, and we're willing to accept
the associated risk.


  [Arrow Sketch]: /static/images/2011/arrow-sketch.png "Arrow Sketch"
  [Jenkins]: http://jenkins-ci.org/ "Jenkins"
  [puppet]: https://puppetlabs.com/ "puppet"
