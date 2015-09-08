---
title: "A Technical Introduction to the Asterisk Gateway Interface (AGI)"
date: "2010-02-16"
tags: ["programming", "telephony", "asterisk"]
slug: "a-technical-introduction-to-the-asterisk-gateway-interface-agi"
description: "Interested in the Asterisk AGI?  This article covers the AGI from the ground up: what it does, how it works, and when you should use it."
---


![Gate Sketch][]


The Asterisk Gateway Interface, commonly referred to as [AGI][], is a
language-independent API for processing calls.  It allows programmers to write
simple programs to manipulate and route calls on [Asterisk][] servers in a
simple, easy manner.

This article provides a technical introduction to the AGI, explaining how it
works, how it can be used, where you can find API documentation, and even
provides some basic code samples which demonstrate how to use the AGI.  The
intended audience is programmers, telephony enthusiasts, or IT people who want
to learn more about adding functionality to their Asterisk PBX systems.  This is
not a full programming reference, and will not explain how to write AGI
programs, it will merely teach you what the AGI provides and how to use it
high-level.


## Why Use AGI?

One question that arises frequently is *Why do I need to use the AGI?*  This is
a great question, worth discussing.  Asterisk provides several ways to perform
call logic, namely dial plan, AMI, and AGI.

[Dial plan][] is Asterisk's native scripting language which is parsed by
Asterisk and stored in memory to use for performing call logic.  Dial plan is
quick, efficient, and easy to learn.  There are, however, downsides associated
with dial plan.  It is very unsophisticated, and doesn't support standard
procedural language constructs (like loops).  This means that you will be doing
mostly assembly type coding using `Goto` statements and simple constructs.  This
makes writing large software tedious and difficult to maintain.

The [Asterisk Manager Interface][] (AMI) is a sophisticated, language
independent API for controlling Asterisk through TCP sockets.  The AMI is a
great solution for software that needs to be ran on remote servers as it can
interact with Asterisk across networks.  Many click-to-call programs are written
using the AMI, as are nearly all of the Asterisk manager programs like [HUD][],
[FOP][], and [Asterisk Assistant][].  The AMI is great because it allows remote
software to completely control the Asterisk PBX: get even status updates, make
calls, receive calls, route calls, etc.  The downside to using the AMI is that
it does not have any good documentation, is known to be buggy and error-prone,
and causes significant stress on the PBX.

The AGI is a middle man, lying somewhere between dial plan and the AMI in terms
of functionality.  The AGI can not be completely independent of the PBX, and
requires some dial plan modification to run (unlike the AMI), is not bound to a
specific programming language (like the AMI), and can be used either locally or
across networks (like the AMI).  The AGI is usable only for incoming calls, and
is thus no good for purely outbound telephony development.  The AGI uses little
overhead compared to the AMI, and is a good solution for developers who want to
write a module or plugin for Asterisk which can be used on any PBX and
implemented quickly and simply without stressing the server.  AGI is also a
great solution for developers who would like to create telephony programs
without learning the Asterisk dial plan.  It lets you build applications in
whatever programming language you are comfortable with, which can rapidly
decrease development time.


## The Four Types of AGI

The AGI actually has four ways in which it can be used, each different from the
other.  There is the standard AGI, dead AGI, fast AGI, and enhanced AGI.

[Standard AGI][AGI] is the simplest, and most widely used form of AGI.  Standard
AGI scripts run on the local PBX and communicate with Asterisk through socket
descriptors (namely `STDIN` and `STDOUT`).  The standard AGI allows for usage of
all AGI commands, and is what this article will be discussing.

The [dead AGI][] is a simplified form of AGI which continues to run after the
call has been hung up.  This is useful in situations where programming logic
needs to be performed after a call has hung up.  As dead AGI allows developers
to control logic after the call, certain AGI commands are not permitted in its
usage.  Dead AGI is also deprecated as of Asterisk 1.6, and should not be used.

[Fast AGI][] is the AGI over TCP sockets protocol.  It allows for all AGI
functionality except EAGI, and is provided as a solution to developers who need
to run resource intensive AGI programs.  By running the bulk of the AGI logic on
another server, the Asterisk server itself can process calls and not worry about
handling complex computation for other services.  This is the recommended
protocol for large applications.

Last is the [EAGI][].  The EAGI communications through file descriptors on the
local machine using `STDIN` and `STDOUT`, and provides developers a way to
access the audio channel directly for the calls being processed.  This is rarely
used, but gives developers a way to analyze raw audio data.


## How to Run an AGI Program

When calls come into the Asterisk server, the dial plan rules process the call
and determine where to route it.  To launch an AGI program and hand off call
processing the AGI program, you will need to use the Asterisk dial plan command
AGI.  Below is an extremely simple example dial plan which passes all calls to
an AGI script for processing.

```ini
; This dial plan code passes all call processing to the call-processor.sh shell
; script.

[incoming]
exten => _X.,1,AGI(call-processor.sh)
```

By default, if no path is specified, Asterisk will look for the script, in this
case `call-processor.sh`, in the directory `/var/lib/asterisk/agi-bin`.  This is
the default location for all AGI programs, and should probably be used to store
your AGI software.  If your program resides in another directory, you may
specify an absolute path to the program for Asterisk to use instead.

The program must be executable (on Linux systems that means that the executable
bit must be set on your program).  You can do this by using the Linux command
`chmod +x` to add the executable bit to your program.

The program must also be readable by Asterisk, this means that it must be in a
public directory tree, or a tree that is owned by the user account under which
Asterisk runs.  Also, don't forget that your AGI program will be ran by
Asterisk, so permissions are necessary to plan out in advance.  A common problem
new Asterisk developers run into is that they will have their AGI programs write
files to a system location, like `/etc/`, but Asterisk will be running in a
restricted environment, so their programs will fail and they will not know why.


## Testing AGI Scripts (live)

Running AGI scripts, as explained in the previous section is a simple task.
Sometimes, however, debugging AGI scripts can be difficult and time consuming.
Often, it is difficult to test AGI programs as you cannot simply print output to
the screen as you normally would for debugging purposes.  This section briefly
covers using the Asterisk command line to watch and debug AGI applications live.

To get started, log into the asterisk console via the `asterisk -r` command from
the shell.  Once inside the CLI, run the `agi set debug on` command to enable
verbose AGI output.  This will come in handy when troubleshooting your programs.
Below is an AGI debug of an AGI application which shows a wide array of
information about my AGI application.  Take a close look at this debug, and try
to make sense of it.  I'll explain what each bit means below.

```console
AGI Tx >> agi_request: hello-world.sh
AGI Tx >> agi_channel: SIP/flowroute-ac10d3c8
AGI Tx >> agi_language: en
AGI Tx >> agi_type: SIP
AGI Tx >> agi_uniqueid: 1266365654.10672
AGI Tx >> agi_version: 1.6.1.1
AGI Tx >> agi_callerid:
AGI Tx >> agi_calleridname: unknown
AGI Tx >> agi_callingpres: 0
AGI Tx >> agi_callingani2: 0
AGI Tx >> agi_callington: 0
AGI Tx >> agi_callingtns: 0
AGI Tx >> agi_dnid:
AGI Tx >> agi_rdnis: unknown
AGI Tx >> agi_context: inbound
AGI Tx >> agi_extension:
AGI Tx >> agi_priority: 1
AGI Tx >> agi_enhanced: 0.0
AGI Tx >> agi_accountcode:
AGI Tx >> agi_threadid: 1097206080
AGI Tx >>
AGI Rx << ANSWER
AGI Tx >> 200 result=0
AGI Rx << NOOP hello, world!
AGI Tx >> 200 result=0
AGI Rx << HANGUP
AGI Tx >> 200 result=1
```

Now, the first thing to note is that every line starts with the channel ID of
the call, this way, calls can be traced even on very busy servers.  If you have
a lot of call traffic, filtering out lines by their channel ID can help improve
visibility.  A great way to do this is to use `grep`, ex: `asterisk -r | grep`
from the command line.

AGI applications send commands to Asterisk via `STDOUT`, and Asterisk sends data
to your AGI programs via `STDIN`.

After the channel ID, you'll see AGI followed by either `Tx` or `Rx`. `Tx`
stands for transmit, and means that Asterisk is transmitting the following
information into the `STDIN` buffer for your AGI program to use if it desires.
Lines which begin with `Rx` (receive) display information that your AGI program
is sending to Asterisk into the `STDOUT` buffer.  If you ever find yourself
wondering what response you are getting after sending a command to Asterisk via
AGI, you can always look at the `Tx` lines to see what Asterisk says.

The first 21 lines of output are all transmissions from Asterisk, which are sent
into the `STDIN` buffer for your program to use if it wishes.  Each of these
lines defines a call variable which contains information about the call that is
currently being processed.  This information may be used by your programs to
figure out things like what caller ID the person calling is using, what number
they called, what dial plan context were they in before hitting your AGI
application, what language the call is in, what version of Asterisk is being
used, etc.

Note that this initial list of variables is terminated by a single empty line.
So when writing software to parse in these variables, always keep parsing until
you read in an empty line.  That is how you can tell that there is no further
input.

The next few lines are dialog between our AGI application and Asterisk.  The
`Rx` lines show AGI commands which were sent to Asterisk for processing, and the
following `Tx` lines show Asterisk responses.


## AGI Hello World Application

In the previous section, we looked at an AGI call log.  Now let's examine the
AGI application which ran and generated that call log.  What follows is an
extremely simple AGI application which simply outputs `hello, world!` to the AGI
debug output.

```bash
#!/bin/bash

echo "ANSWER"
echo "NOOP hello, world!"
echo "HANGUP"
```

This program completely disregards all of the variables that Asterisk passed
into `STDIN` when it spawned a new thread for our AGI application, and only
writes three AGI commands to `STDOUT` (which is how our application communicates
with Asterisk).

The first command we send is [ANSWER][], which does nothing but answer the call
(establishes an audio connection with the remote end, so that the call starts
getting billed).  The second command we send is a [NOOP][], which only outputs
the text that follows it onto the AGI debug screen of the CLI.  Lastly, we send
the [HANGUP][] command which ends the call.

Simple enough?  Now, go ahead and try to run this program yourself.  Test it
out, understand what is happening, and make it work.

One thing you may notice is that you may get some errors on the CLI while
watching your program run.  Usually they look something like this:

```console
[Feb 16 19:14:15] ERROR[25770]: utils.c:1126 ast_carefulwrite: write() returned error: Broken pipe
[Feb 16 19:14:15] ERROR[25770]: utils.c:1126 ast_carefulwrite: write() returned error: Broken pipe
```

Feel free to ignore those errors.  Those are generated when your AGI application
does not read in *all* data from `STDIN` before your program closes.

In most real world applications, you'll want to read in Asterisk responses so
that you know whether or not your commands executed successfully, and can grab
important information about the call being processed, but for this example, we
don't care, so we didn't.


## Passing Arguments to Your AGI Application

Now that you know how to write and use basic AGI scripts, let's get a little
more advanced.  Many complex AGI applications may need more advanced data given
to them than what Asterisk natively provides.  Luckily, the Asterisk dial plan
command AGI allows for us to pass up to 127 arguments to our AGI application.
This should be sufficient for most needs.

To pass arguments from the dial plan to your AGI script, you can simply add them
in a comma delimited list after your AGI application path is specified:

```ini
exten => s,1,AGI(hello-world.sh,arg1,arg2,arg3)
```

As you'll notice in the above example, I did not put spaces after each comma.
That is because if you add spaces, Asterisk will interpret them literally and
your program will receive the argument with a space character prepended to it.
This may (or may not) be desirable, based on your application specifications.

The arguments will be available to your AGI application both via the standard
argument list *and* via the initial Asterisk variable list.  Each programming
language handles it differently.  Here is an AGI log which shows our old
`hello-world.sh` program being called with 3 arguments:

```console
AGI Tx >> agi_request: hello-world.sh
AGI Tx >> agi_channel: SIP/flowroute-ac10d3c8
AGI Tx >> agi_language: en
AGI Tx >> agi_type: SIP
AGI Tx >> agi_uniqueid: 1266365654.10672
AGI Tx >> agi_version: 1.6.1.1
AGI Tx >> agi_callerid:
AGI Tx >> agi_calleridname: unknown
AGI Tx >> agi_callingpres: 0
AGI Tx >> agi_callingani2: 0
AGI Tx >> agi_callington: 0
AGI Tx >> agi_callingtns: 0
AGI Tx >> agi_dnid:
AGI Tx >> agi_rdnis: unknown
AGI Tx >> agi_context: inbound
AGI Tx >> agi_extension:
AGI Tx >> agi_priority: 1
AGI Tx >> agi_enhanced: 0.0
AGI Tx >> agi_accountcode:
AGI Tx >> agi_threadid: 1097206080
AGI Tx >> agi_arg_1: arg1
AGI Tx >> agi_arg_2: arg2
AGI Tx >> agi_arg_3: arg3
AGI Tx >>
AGI Rx << ANSWER
AGI Tx >> 200 result=0
AGI Rx << NOOP hello, world!
AGI Tx >> 200 result=0
AGI Rx << HANGUP
AGI Tx >> 200 result=1
```

As you can see, after the initial arguments have been passed, Asterisk simply
adds a new line with for each additional argument passed to the AGI script.
This makes reading in these variables easy and doesn't require any extra effort
on your part.


## Where to Get AGI Information

Now that we've introduced and explained how AGI programs work, there is nothing
left to do except start writing some for yourself!  The definitive reference to
AGI commands and functions can be found on [VoIP Info's AGI page][AGI].

If you are comfortable with Asterisk dial plan, you'll easily pick up the AGI
commands.  If you have no prior experience, then look for some references /
examples in the VoIP info page as they have numerous examples and help
available.


  [Gate Sketch]: /static/images/2010/gate-sketch.png "Gate Sketch"
  [AGI]: http://www.voip-info.org/wiki/view/Asterisk+AGI "Asterisk Gateway Interface Wiki Page"
  [Asterisk]: http://www.asterisk.org/ "Asterisk PBX"
  [Dial plan]: http://www.voip-info.org/tiki-index.php?page=Asterisk%20config%20extensions.conf "Asterisk Dial Plan Wiki Page"
  [Asterisk Manager Interface]: http://www.voip-info.org/wiki/view/Asterisk+manager+API "Asterisk Manager Interface Wiki Page"
  [HUD]: http://www.fonality.com/solutions/heads-up-display "Fonality HUD"
  [FOP]: http://fop2.com/ "Flash Operator Panel"
  [Asterisk Assistant]: http://blogs.digium.com/2008/12/22/asterisk-desktop-assistant-windows-click-to-call-and-more/ "Asterisk Desktop Assistant"
  [dead AGI]: http://www.voip-info.org/tiki-index.php?page=Asterisk+cmd+DeadAGI "Dead AGI Wiki Page"
  [Fast AGI]: http://www.voip-info.org/wiki/view/Asterisk+FastAGI "Fast AGI Wiki Page"
  [EAGI]: http://www.voip-info.org/wiki/view/Asterisk+EAGI "Enhanced AGI Wiki Page"
  [ANSWER]: http://www.voip-info.org/wiki/view/answer "Asterisk AGI Answer Command Wiki Page"
  [NOOP]: http://www.voip-info.org/wiki/view/noop "Asterisk AGI NoOp Command Wiki Page"
  [HANGUP]: http://www.voip-info.org/wiki/view/hangup "Asterisk AGI Hangup Command Wiki Page"
