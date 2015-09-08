---
title: "Transparent Telephony - Part 3 - Making and Receiving Calls Using VoIP"
date: "2010-03-03"
tags: ["programming", "telephony", "asterisk"]
slug: "transparent-telephony-part-3-making-and-receiving-calls-using-voip"
description: "The third part of my telephony series.  In this installment we'll connect Asterisk to Flowroute, and make internet calls!"
---


![Old Telephone Sketch][]


Welcome back to the Transparent Telephony series.  If you're a new reader, you
may want to start at the beginning: [Part 1 - An Introduction][].

In the [previous installment][], we walked through installing Asterisk.  In
this article, we'll be picking up where we left off and configuring Asterisk to
make and receive phone calls using VoIP!

Specifically, we'll:

-   Register an account with a VoIP (voice over IP) provider.
-   Configure Asterisk to connect to our VoIP provider.
-   Create a SIP extension to make and receive calls from.
-   Configure Asterisk rules for making calls.
-   Configure Asterisk rules for receiving calls.
-   Connect a softphone (software phone) to our Asterisk server as an extension
    and use it to make real calls.

So let's get started!


## Getting a VoIP Account

The first thing we need to do is sign up with a VoIP (voice over IP) provider.
To quote from Part 1 - An Introduction,

> VoIP (voice over IP) is a relatively new way to connect to the PSTN using the
> Internet.  VoIP is extremely low-cost compared to other methods, and very
> easy to set up as it only requires an active Internet connection to use.
> More and more businesses are switching over to VoIP for cost reasons.

There are two main types of VoIP protocols that people use with Asterisk.
There is SIP (session initiation protocol) and IAX (inter-asterisk exchange).
While both of these protocols are still widely in use, SIP has become the
dominant VoIP protocol in today's world.  In fact, the term SIP has mostly
replaced VoIP.  When speaking to people in the telephony industry, it is common
to hear people say 'I have so and so as my SIP provider'.  So from now on,
we'll use that terminology as well.

Picking a SIP provider is a very important task.  If you Google for 'SIP
providers' you'll find thousands of options.  Here are the top few I recommend
(I've experimented with tons of different SIP providers):

-   [Flowroute][]
-   [voip.ms][]
-   [Vitelity][]
-   [Bandwidth][]
-   [Voicepulse][]

Flowroute is my favorite SIP provider because they have a great website, low
prices, and business-class reliability.  So instead of walking through the set
up for each of the above providers (that would take forever) I'll just cover
Flowroute.  If you choose to go with another provider, you can still follow
along with this article and get a sense of what to do.


## Create an Account

To create an account with Flowroute, visit their [sign up page][] and fill in
your information.  You don't need a credit card, and they'll give you 25 cents
of credit (enough to make approximately 30 minutes of calls).  If you want to
be able to receive calls as well as make them, then you'll have to deposit some
money into your account as you'll need to own a DID (more commonly known as
phone number) which costs a bit more than 25 cents.

Once your account has been created, you'll be directed to the account
dashboard, where, if you want, you can deposit some money via Amazon Payments.


### A Brief Note on Terminology

In the telephony world, SIP accounts are commonly referred to as SIP trunks.
Trunk meaning a single account connection to the PSTN.


## Connect Your SIP Trunk to Asterisk

Now that we've got a SIP trunk ready for us to use, we need to hook it up to
our Asterisk PBX.  To get started, go to your Flowroute account management
page, and navigate to the 'Interconnection' page, then click on the
'System Configurator' link towards the middle of the page.  Next click on the
drop down menu and select 'Asterisk' as this is what we're using.  The System
Configurator will give us all of the Asterisk settings we need to put into our
PBX (with only slight modifications required).


### A Brief Note on Security

Never ever give out any of your SIP account information!  If someone knows your
secret and account number, they can easily connect your SIP trunk to their PBX,
and begin placing calls on your tab!  This happens frequently as many system
administrators are not familiar with VoIP security, and don't know what
information is valuable, and what isn't.

A good deal of phone scams and telemarketing campaigns originate from hacked
SIP accounts, so be careful!


### Define Your SIP Trunk Registration String

If you read your System Configurator page, the first thing you'll notice is a
section labeled `sip.conf`.  The file `sip.conf` (located at:
`/etc/asterisk/sip.conf`) is the SIP configuration file that Asterisk uses to
define SIP trunks, and other SIP settings.  In order to connect our Flowroute
SIP trunk to Asterisk, we'll need to edit this file and add in the SIP trunk
information specified on the System Configurator page of the Flowroute account
dashboard.

The first bit of the Flowroute instructions say to add the following to
`sip.conf` right after general settings:

```ini
allow=ulaw
allow=g729
register => xxx:xxx@sip.flowroute.com
```

So go ahead and open `/etc/asterisk/sip.conf` in your favorite text editor (I
prefer vim).  You'll notice a lot of text, but ignore it for now.  These
configuration options will be covered in another article in this series.

Scroll down until you see a line that says only: `[authentication]`.  This line
marks the end of the `[general]` section (which is where we need to put the
settings mentioned above).  Now go ahead and insert the settings Flowroute gave
you directly above the `[authentication]` line.  Your configuration file should
now show something like:

```ini
allow=ulaw
allow=g729
register => xxx:xxx@sip.flowroute.com

[authentication]
```


### Define Your NAT Network Settings

If you are running your Asterisk PBX behind a router (e.g. your Asterisk system
has a private IP), then you'll need to add the following configurations to your
`sip.conf` file directly above the `[authentication]` line:

```ini
nat=yes
externip=xx.xx.xx.xx
localnet=192.168.0.0/255.255.255.0
```

Where `xx.xx.xx.xx` is your external IP (visit [IP Chicken][] if you don't know
it), `192.168.0.0` is your subnet, and `255.255.255.0` is your subnet mask.  In
this example, I'm allowing connections to my Asterisk PBX from any device on
the `192.168.0.x` network.

The reason we need to add our networking information here is because Asterisk
needs to modify the SIP packet headers to ensure that our SIP packets get to
the right destination.


### Define Your SIP Trunk

The next thing the Flowroute instructions tell us to do is to add the following
near the bottom of `sip.conf`:

```ini
[flowroute]
type=friend
secret=xxx
username=xxx
host=sip.flowroute.com
dtmfmode=rfc2833
context=inbound
canreinvite=no
allow=ulaw
allow=g729
insecure=port,invite
fromdomain=sip.flowroute.com
```

So go ahead and scroll to the bottom of your `sip.conf` file, and then insert
those settings along with a single addition: at the very bottom of your
configurations (on a new line after the `fromdomain=sip.flowroute.conf`) line,
insert the following: `qualify=yes`, as this will give us some additional
information about our SIP connection later on.


## Create a SIP Extension

Now that we've set up our SIP trunk, it's time to create an extension.  An
extension is just another term for 'phone'.  SIP extensions (IP phones) are the
most common type of extensions in use on modern phone systems.  Sure, you can
still hook up those old analog phones to your Asterisk PBX, but we'll save that
for another day.  Today we'll create a simple SIP extension which we will later
hook up a soft phone to and use to make and receive calls.

To define a SIP extension, we need to pick several things:

-   **An extension number.**  This is typically a numeric number, several
    digits in length.  I'll be using `1000` in the following examples.
-   **A secret password.**  This is generally an alphanumeric password of any
    length used to 'secure' your extension.  Any device which wants to make or
    receive calls from your extension need to know this password in order to
    authenticate.  This password does not need to be remembered, and should be
    globally unique.


### Creating the Extension

Now that you've picked your extension number and secret, let's create it!

Scroll down to the very bottom of your `/etc/asterisk/sip.conf` file, (below
the SIP trunk we created in the previous section), and insert the following
(make sure you swap out my extension number for yours, and my secret for
yours):

```ini
[1000]
type=friend
nat=yes
canreinvite=no
secret=mysecretpassword
qualify=yes
mailbox=1000@default
host=dynamic
dtmfmode=rfc2833
dial=SIP/1000
context=outgoing
```

I'll skip over the configuration options for now, I'll cover these in great
depth in a later part of the series.  If you want to read more about them now,
check out the [VoIP Info page][] which describes them in detail.

At this point we've fully configured a Flowroute SIP trunk and a SIP extension
with Asterisk.  The next thing for us to do will be configuring our network so
that our SIP trunk works.  So keep reading!


## Configure the Network

Before our SIP set up is finished, we need to configure our network to pass SIP
and RTP (voice traffic) to our Asterisk server.  If your server is not behind a
router, you can skip this section.

To do this, configure port forwarding on your router to forward ports `5060`
UDP, and `10,000` -> `20,000` UDP to your Asterisk server.

Port `5060` UDP is used for SIP traffic.  Ports `10,000` -> `20,000` UDP are
used to pass voice traffic (audio).

If your router has any SIP options such as SIP ALG (application layer gateway)
or SIP fixup, you'll want to disable them.


## Testing the SIP Trunk

Before moving on to the actual call configuration, let's make sure our SIP
trunk is actually connected to Asterisk and working.

From the command line, type the following: `asterisk -rx 'sip reload'`, which
will force Asterisk to reload our SIP configuration file that we just edited
(`/etc/asterisk/sip.conf`).

Next, let's check to make sure that our Flowroute trunk is registered
(connected and in service): `asterisk -rx 'sip show registry'`. If your state
shows registered:

```console
[root@localhost asterisk]# asterisk -rx 'sip show registry'
Host                    Username  Refresh State   Reg.Time
sip.flowroute.com:5060  xxxxxxxx  105 Registered  Tue, 02 Mar 2010 09:34:23
1 SIP registrations.
```

Then you know that your SIP trunk is connected and working!


## Configure the Dial Plan

Since we have our SIP trunk working, we now need to program Asterisk, and teach
it how to route calls for us.  There are two things that we need to teach
Asterisk to do: how to route outgoing calls, and how to route incoming calls.
Each of these requires separate Asterisk configuration to work.

Our goal will be to write the following two rules:

1.  When we dial an 11-digit US phone number from our soft phone, it should
    call that phone number.
2.  When someone calls our SIP DID (phone number), we should connect that call
    to our soft phone so we can talk to the person who called us.

There are several ways to program Asterisk to handle call routing, but the
simplest (and native) way to do it is via 'dial plan'.  Dial plan is the name
of Asterisk's own scripting language.  It is very simple, and easy to
understand (even for non-programmers).

In the next few sections, we'll write dial plan code to route calls according to
our rules above.


### Asterisk Dial Plan Basics

All Asterisk dial plan code resides in the file
`/etc/asterisk/extensions.conf`.  So when working on dial plan code, always
have this file open.

There are two main sections of the `extensions.conf` file that are always
present.  There is a `[general]` context which contains dial plan settings.
These settings control Asterisk dial plan parsing options for the most part.
The other context is `[globals]` which contains a list of global variables that
can be accessed by any dial plan code.

All Asterisk dial plan code is kept in contexts (much like the SIP
configuration we walked through earlier).  You can create as many contexts as
you like.

Each context should have a clear, meaningful name, which describes what the
code inside of it does.

Each line of dial plan code is of the form:
`exten => extension,priority,application`, where:

1.  `extension` is a regular expression or literal value which is used to
    determine routing logic.
2.  `priority` is a numeric value (or variable) which tells Asterisk in what
    order to execute the code.
3.  `application` is a function that Asterisk executes to perform some
    functionality.

If you don't understand all of this now, don't worry!


### Start With a Clean Slate

Before we begin writing our code, let's quickly create a nice clean
`extensions.conf` file to work in.  Remove your current dial plan file
(`/etc/asterisk/extensions.conf`) and replace it with the following:

```ini
[general]
static=yes
writeprotect=no
clearglobalvars=no

[globals]
TRUNK=flowroute
```

All I did here was remove all comments and clutter from the file, so that we
can clearly see what we're doing.  I also added a global variable called
`TRUNK` which contains the name of our SIP trunk defined earlier in the
article.  We'll use this global variable later on to make outbound calls.


### Configure Outbound Routing

The goal here is to allow our extension to dial an 11-digit US phone number,
and connect it to the PSTN via our Flowroute SIP trunk.

Remember when we configured our SIP extension?  One of the keys we specified in
the configuration file was: `context=outgoing`.  The context field of an
extension determines what dial plan context the pattern matching will start at.
This is similar to the main() function in most programming languages.

The context specified in our SIP extension plays an important role in routing
outbound calls.  It says (in human English):

> When any extension who's `context` key is equal to `outgoing` dials a number,
> send the number that was dialed to the `[outgoing]` context to be processed.
> Let the `[outgoing]` context determine what to do at this point.

So now that we know what context we need to create (the `[outgoing]` context),
let's make it!

Open your `extensions.conf` file and add the following code to it at the
bottom:

```ini
[outgoing]
exten => _1NXXNXXXXXX,1,Dial(SIP/${EXTEN}@${GLOBAL(TRUNK)})
```

Let's go through the code and analyze exactly what is happening.

The first bit: `exten =>` is standard.  All Asterisk dial plan code starts with
this bit.  The extension: `_1NXXNXXXXXX` is a regular expression that Asterisk
will use to pattern match the number dialed.  Remember above how we said that
we're going to route all 11-digit US telephone numbers outbound?  This pattern
represents an 11-digit US telephone number.  Since all 11-digit US telephone
numbers begin with the number `1`, we hard-code that number.  The variable `N`
represents a number (2 through 9), and the variable `X` represents a number (0
through 9).  Therefore, the pattern `_1NXXNXXXXXX` will match any 11-digit US
telephone number.

After the extension (pattern), you'll see a comma character followed by the
number `1`.  The number `1` is the priority.  Asterisk dial plan code can
contain more than a single line of instructions.  In cases where there are
multiple lines of code that need to be executed, Asterisk relies on the
priority number to determine what to do first.

Imagine that we had code which looked like:

```ini
exten => _1NXXNXXXXXX,2,Dial(18002223333@flowroute)
exten => _1NXXNXXXXXX,1,Dial(19999999999@flowroute)
```

In this case, Asterisk would execute the code at priority number 1 first, then
the code at priority number 2.  So always check for priority numbers when
looking at code as they will help determine what is going on.

The last part of the code you see is the called application:
`Dial(SIP/${EXTEN}@${GLOBAL(TRUNK)})`.  The application we're using here is the
`Dial()` command.  This application instructs Asterisk to dial the phone number
out of our Flowroute SIP trunk and connect the call to our extension (e.g. make
an outbound call)!

Everything inside of the `${}` characters is a variable reference.  Asterisk
has several pre-defined 'channel variables' which are always accessible.  In
our `Dial()` code, we reference the `${EXTEN}` channel variable, which contains
the number that was dialed and pattern matched.  If we dialed the number
`18002223333`, then `${EXTEN}` would expand to `18002223333`.

The `${GLOBAL(TRUNK)}` code references the global variable `TRUNK` which we
defined at the top of our `extensions.conf` file.  This code will expand to
`flowroute` before executing the `Dial()` application.

So after all of the variable expansion is finished, Asterisk actually sees the
following (assuming that we dialed the number `18002223333`):
`Dial(SIP/18002223333@flowroute)`, which is a lot easier to understand!  The
first part of the line that says `SIP/` tells Asterisk that the number we're
going to dial should be sent out of our SIP trunk.  The `@flowroute` part tells
Asterisk to dial the number `18002223333` on the `flowroute` SIP trunk,
specifically.  Doing it this way gives us flexibility.  Imagine if we had many
SIP trunks on our Asterisk system, and wanted to route certain calls through
certain SIP trunks.


### Outbound Routing, a Full Walk Through

Let's quickly perform a full walk through of what happens when we dial the
number `18002223333` on our extension.  (Don't worry that we haven't set up the
soft phone yet, we'll get to that later.)

1.  Asterisk receives a SIP call from our extension (`1000`) which has dialed
    the number `18002223333`.
2.  Asterisk looks at the context key in our extension's configuration
    settings, and sees that it is set to outgoing.
3.  Asterisk sends the number `18002223333` to the `[outgoing]` context,
    defined in `/etc/asterisk/extensions.conf` to be pattern matched.
4.  Once Asterisk finds a match for the number, it begins looking for the first
    application to execute by looking for priority `1`.
5.  Asterisk finds priority `1`, and then beings performing variable expansion
    in the application field to prepare for execution.
6.  Asterisk finishes variable expansion, then executes:
    `Dial(SIP/18002223333@flowroute)`.
7.  Asterisk then calls the number `18002223333` on the `flowroute` SIP trunk,
    and connects the call to our extension so that both ends can talk to each
    other.

That's it for outbound routing!  Simple right?


### Configure Inbound Routing

In order to route calls inbound, you will need a DID (phone number) with your
SIP provider.  This way, you can call your number, and it will direct to your
Asterisk PBX system.  A phone number is a lot like an IP address, each one is
unique, and routes to a specific location.

Unfortunately, DIDs cost money (just like you pay for cell phone service and
house phone service, you need to pay for VoIP service to rent a DID).  If you
would like to try out the code that follows, you'll need to deposit some money
into your Flowroute account, and then purchase a DID from the web panel.  At
this point in time, a single DID from Flowroute costs approximately $1.39 per
month.

Once you've purchased a DID, write the number down somewhere.  It will be an
11-digit phone number.  For the code that follows, simply substitute in your
DID where necessary, as I will be using the fictitious DID `18182223333`.

Open your `/etc/asterisk/extensions.conf` file and add a new context called
`[inbound]` to the bottom of your file (it can go beneath the `[outgoing]`
context we created in the last section).  The context should look like:

```ini
[inbound]
exten => 18182223333,1,Dial(SIP/1000)
```

The code here should look familiar to the code in the previous section.  All
we're doing is dialing the SIP extension `1000` (which is the extension we
created earlier).  You've probably noticed that there is no `@trunk` syntax at
the end of our `Dial()` application.  If you look back at your SIP
configuration file (`/etc/asterisk/sip.conf`) you'll notice that when we
created our extension, one of the keys we defined was: `dial=SIP/1000`, which
tells Asterisk that in order to connect a call to that extension, we have to
dial `SIP/1000`.


### Inbound Routing, a Full Walk Through

Let's quickly perform a full walk through of what happens when someone calls
our DID (`18182223333`) from the PSTN.

1.  First our SIP provider will receive the call, and check to see what
    customer the DID belongs to.
2.  The SIP provider will then check to see if we are registered to their SIP
    server.
3.  Once they've confirmed our registration, they'll forward the call to our
    Asterisk system.
4.  Asterisk will receive the call from our Flowroute SIP trunk, and check to
    see what context it should use to route the call.
5.  Asterisk will see that our `[flowroute]` trunk is configured to use the
    context 'inbound', and will send the DID number, `18182223333` to the
    `[inbound]` context for pattern matching.
6.  Asterisk will match the pattern `18182223333` in our `[inbound]` context,
    and begin looking for priority `1`.
7.  Asterisk will find priority `1`, and then execute the `Dial(SIP/1000)`
    command.
8.  Asterisk will connect the incoming call to our extension, so that both
    parties can talk.

Not too bad!  We've set up the ability to receive incoming calls in only a
single line of code!

At this point, we've created dial plan rules for both the outgoing and incoming
call routing.  Save your `extensions.conf` file, and let's move on.


## Apply Your New Dial Plan Rules

Now that we've finished writing our dial plan code, we need to reload Asterisk
to have it re-scan our `extensions.conf` file.  To do this, simply type:
`asterisk -rx 'dialplan reload'` from the command line.

The next section which will teach you how to hook up a soft phone to your
Asterisk system so you can actually test your system!


## Set Up a Softphone

In this section, we'll set up a soft phone to use to make calls.  Soft phones
are just SIP clients that can connect to Asterisk and act as normal phones.
Asterisk can work with normal analog telephones as well as fancier (and more
expensive) SIP phones, but SIP phones are much easier to set up, so we'll be
configuring a soft phone today.  If you want to hook up your analog phone to
your Asterisk server-don't despair-that will be covered in another article in
this series.

There are tons of soft phones to choose from, but I'll be walking you through
using X-Lite, as it is one of the most popular and widely used.

First thing you'll want to do is [download and install X-Lite][] on your
computer (it runs on all platforms).

Once you've got it installed, open it up.  If you don't have your extension
information in front of you, open up your SIP configuration file
(`/etc/asterisk/sip.conf`) and look at your extension definition.

Right click on the main window display in X-Lite and click on 'SIP Account
Settings'.  Now click 'Add...' to add a SIP account.

Here are the values you should fill in:

-   **Display Name**: Set this to anything you like.  I prefer `1000` (the
    extension I'm using).
-   **User Name**: Set this to your extension number (`1000`).
-   **Password**: Set this to your secret.
-   **Authorization User Name**: Set this to your extension number (`1000`).
-   **Domain**: Set this to the IP address of your Asterisk server.
-   Make sure the box next to 'Register with domain and receive incoming calls'
    is checked.

Once you've configured all those settings, press OK and then close out of the
configuration menu.

If your network and SIP configuration files have been properly configured, your
X-Lite phone will now say 'Registered' at the top of the window!  If it is not
working, read back through the setup instructions and make sure you didn't miss
anything.  If you are using a virtual machine, also make sure your host network
settings have been configured to receive incoming traffic.


## Making and Receiving Your First Call

Now that we've gotten everything set up, let's actually make some calls!

On your X-Lite soft phone, go ahead and dial any 11-digit US telephone number
(since this is the rule that we configured for outbound routing).  When you hit
dial (the green button) you'll make a call just like you would on a normal
phone, and you'll be connected to the phone number you dialed!

If you want to receive a call, use your cell phone to call your DID, and
Asterisk will route the call directly to your X-Lite phone.  You will see and
hear you X-Lite phone ring, and you can pick up the call by clicking the green
button.


## Conclusion

This was a very large article, and took a considerable amount of time to write.
I hope that if you got this far, you were able to clearly configure and
understand the basic Asterisk setup required to make outbound calls, and to
receive inbound calls.

The material covered in this part of the series is bulky, but very important in
understanding the way Asterisk works.  In future parts of the Transparent
Telephony series, we'll have significantly shorter, more targeted articles, so
following along should be easier.


  [Old Telephone Sketch]: /static/images/2010/old-telephone-sketch.png "Old Telephone Sketch"
  [Part 1 - An Introduction]: {filename}/articles/2009/transparent-telephony-part-1-an-introduction.md "Transparent Telephony - Part 1 - An Introduction"
  [previous installment]: {filename}/articles/2010/transparent-telephony-part-2-installing-asterisk.md "Transparent Telephony - Part 2 - Installing Asterisk"
  [Flowroute]: http://www.flowroute.com/ "Flowroute"
  [voip.ms]: http://voip.ms/ "Voip MS"
  [Vitelity]: http://vitelity.com/ "Vitelity"
  [Bandwidth]: http://bandwidth.com/ "Bandwidth"
  [Voicepulse]: http://www.voicepulse.com/ "Voicepulse"
  [sign up page]: https://www.flowroute.com/accounts/signup/ "Flowroute Sign Up Page"
  [IP Chicken]: http://ipchicken.com/ "IP Chicken"
  [VoIP Info page]: http://www.voip-info.org/wiki/view/Asterisk+config+sip.conf "Asterisk sip.conf Wiki Page"
  [download and install X-Lite]: http://www.counterpath.com/x-lite.html "X-Lite Download Page"
