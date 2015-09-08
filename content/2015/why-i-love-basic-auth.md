---
title: "Why I Love Basic Auth"
date: "2015-03-23"
slug: "why-i-love-basic-auth"
tags: ["programming"]
description: "I love HTTP Basic Authentication.  It's simple, secure, and a pleasure to use."
---


![Wall-e Sketch][]


One of the disturbing trends I've noticed over the past few years is that more
and more API services are slowly ditching support for HTTP Basic Authentication
(*aka: Basic Auth*) in favor of OAuth.

As someone who's been:

- Using REST API services for years.
- Has built numerous REST API services.
- Has built and ran a REST API company.
- Is currently working at a large developer-focused REST API company.

I can't help but feel like this is a *bad thing*.

It's a *bad thing* because OAuth (*as popular as it is*) is a huge pain in the
ass -- for both the people building the API services as well as the developers
consuming them.

OAuth is complex, misunderstood, widely misused, and lacking universal
implementations.  It most definitely has its uses, but in many cases feels
burdensome.

Basic Auth, on the other hand, is simple, very well understood, and has been
well supported in every language and framework since the 1990's.


## How Basic Auth Works

![Wall-e and Eve Sketch][]


Let's talk about Basic Auth:

- It's a well and clearly defined [specification][].
- It's been around since ~1996.
- It's super simple.

Here's the short version of how it works.

- You are a developer.
- You have an API key pair: an *API Key ID* and an *API Key Secret*.  Each of
  these is a randomly generated string (*usually a [uuid][]*).
- To authenticate against an API service, all you need to do is put your
  credentials into the [HTTP Authorization header][].

Here's an example showing how Basic Auth works on the command line using
[cURL][]:

```console
$ curl --user 'xxx:yyy' https://api.someapi.com/v1/blah
```

Here's some Python code showing how it works:

```python
>>> from requests import get
>>>
>>> api_key_id = 'xxx'
>>> api_key_secret = 'yyy'
>>>
>>> resp = get('https://api.someapi.com/v1/blah', auth=(api_key_id, api_key_secret))
>>> print resp.json()
```

And if that isn't enough, here's some Node.js code showing it as well:

```javascript
var request = require('request');

var api_key_id = 'xxx';
var api_key_secret = 'yyy';

request({
  url: 'https://api.someapi.com/v1/blah',
  auth: {
    'user': api_key_id,
    'pass': api_key_secret
  }
}, function(err, resp, body) {
  console.log(body);
});
```

Isn't that simple?

All Basic Auth lets you do (*at a high level of abstraction*) is specify your
credentials.  That's it.

**NOTE**: *Yes, I know that technically it's a little bit more complicated than
this.  There's base64 encoding, there's the HTTP Authorization header format,
etc., but for argument's sake I'm leaving that out as it's not important in this
context.*

Basic Auth is great for developers because it's simple, intuitive, and easy to
use.

Let's say you're integrating with an API service, all you do is create an API
Key Pair, and start making requests!

What do you do if you accidentally publicize your API Key Pair and it's
compromised?  Well...  You just create another API Key Pair, put that into your
application code, and get rid of the old one!

When used properly, Basic Auth can be a great choice for securing REST APIs.


## It's Simple

![Wall-e Eyes Sketch][]


My favorite thing about Basic Auth is that it's *simple*.

Unlike OAuth, there's no intermediary steps you need to go through to get an
access token: all you need are your API keys.

This makes a *huge* difference in development speed.

Instead of spending a lot of time figuring out what permissions and scopes you
need granted, setting up redirect URIs, web servers, and all this crap that
only serves to complicate matters -- all you need to do is put your damn API
keys into the HTTP Authorization header and *BAM*, shit works.

Because it's so simple, you can get a lot of work and testing done faster.

You also don't need to worry about things like:

- Token expiration.  *Cough, cough OAUTH!*
- Providers changing their implementations.  *Just about every single OAuth
  provider has changed their implementations numerous times, breaking thousands
  of developer applications.*
- Complex workflows for getting access to your data.  *OAuth2 has 4 different
  grant types, each of which is used in a different way and for different
  purposes.*

Every time I use a service like [Twilio][], I'm reminded how convenient Basic
Auth is to use: it's truly a pleasure to be able to:

- Generate and destroy API keys on command.
- Easily throw API keys into whatever apps I'm currently hacking on.
- Easily test my API requests out via the command line or an API explorer like
  [Runscope][].

I just love it.


## It's Secure

![Wall-e Upside Down Sketch][]


Basic Auth gets a bad reputation for being *"insecure"*, but this isn't
necessarily true.

There are several things you can do to ensure that your API service (*secured by
Basic Auth*) is as secure as possible:

- Always run all requests over HTTPs.  If you're not using SSL, than no matter
  what authentication protocol you use, you'll never be secure.  Unless you're
  using HTTPs, all of your credentials will be sent in plain-text over the wire:
  *a horrible idea*.

- Give your developers the ability to generate as many API key pairs as they'd
  like.  This makes it easy for developers to *isolate* their usage of an API
  key pair to a single application or service.

- Give your developers the ability to revoke API key access when they need to.
  For instance: if a developer accidentally leaks his API keys on Github, he
  should be able to revoke that API key pair, thereby guaranteeing it can't be
  used by anyone else.

- Generate random API key pairs using [uuids][].  This ensures API key pairs
  aren't *guessable*.

Furthermore, for developers *using Basic Auth*, there are a few things you
should always keep in mind:

- Store your API keys securely.  If you're using an API service that supports
  Basic Auth, be sure to not do things like store your API keys in your public
  Github repo.

- Don't use an API service that isn't run over HTTPs -- you're guaranteed to
  have problems in the future.

- Use a unique API key pair for each application you write.  This way, if you
  accidentally lose an API key or leak it publicly, you only need to revoke
  *that specific API key*, and you only need to update *a single codebase that
  relied on that API key*.  This will make your life much easier in the long
  run.

If you're looking for a good example of an API company that handles API keys the
right way, check out [AWS][].


## Universally Supported

![Wall-e Happy Sketch][]


Another great thing about Basic Auth is that there's only one implementation
everyone uses -- this means that there's never any ambiguity about how to craft
requests or server-side components: it's always the same.

The way it works is like this:

- You take the API Key ID and the API Key Secret, and you put them into a
  colon-separated string like so: `'xxx:yyy'`.
- You then prepend the word `'Basic '` to the string, so that you have: `'Basic
  xxx:yyy'`.
- You then [base64][] encode the API key portion of the string, so you end up
  with: `'Basic eHh4Onl5eQ=='`.
- Lastly, you set this value as your HTTP Authorization header when you make
  your HTTP requests.

When the web server receives your request, it then:

- base64 decodes the header value.
- Splits the string by the colon character.
- The left-hand portion is the API Key ID, the right hand portion is the API Key
  Secret.
- The server then validates these credentials, and either allows you access or
  returns an *HTTP 401 UNAUTHORIZED* response.

There's nothing ambiguous about Basic Auth.  This means every programming
language has top-notch support for the standard, and it's easy to find well
audited libraries for using Basic Auth as both a producer and consumer.


## My Hope

![Wall-e Love Sketch][]


My hope is that while OAuth continues to rise in popularity, developers continue
to support Basic Auth to the maximum possible extent.

Not only does this make my life as a developer easier, but it also makes it more
enjoyable.

For any API services out there that trust their developers, you really can't go
wrong by supporting Basic Auth.

And...  Even for those services that *don't trust their developers* -- namely
consumer services like Google, Facebook, Fitbit, etc. -- it's still a good idea
for them to support Basic Auth.  This, at the very least, empowers their users
to pragmatically access their *own data* without jumping through the OAuth
hoops.

**NOTE**: *I realize this is a somewhat controversial topic.  I've ended up
writing numerous drafts of this article, only to throw them away as their scope
has grown too much.  In the future, I plan to write many more articles
discussing the various pitfalls of both OAuth and Basic Auth, diving into more
in-depth technical reasons for my opinions.*


  [Wall-e Sketch]: /static/images/2015/wall-e-sketch.jpg "Wall-e Sketch"
  [Wall-e and Eve Sketch]: /static/images/2015/wall-e-and-eve-sketch.jpg "Wall-e and Eve Sketch"
  [Wall-e Eyes Sketch]: /static/images/2015/wall-e-eyes-sketch.png "Wall-e Eyes Sketch"
  [Wall-e Love Sketch]: /static/images/2015/wall-e-love-sketch.jpg "Wall-e Love Sketch"
  [Wall-e Happy Sketch]: /static/images/2015/wall-e-happy-sketch.jpg "Wall-e Happy Sketch"
  [Wall-e Upside Down Sketch]: /static/images/2015/wall-e-upside-down-sketch.jpg "Wall-e Upside Down Sketch"
  [OAuth]: http://oauth.net/ "OAuth"
  [specification]: http://tools.ietf.org/html/rfc2617 "HTTP Basic Auth / Digest Auth Spec"
  [uuid]: http://en.wikipedia.org/wiki/Universally_unique_identifier "UUID on Wikipedia"
  [HTTP Authorization header]: http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html "HTTP Headers Spec"
  [HTTP Basic Auth]: http://tools.ietf.org/html/rfc2617 "HTTP Basic Auth / Digest Auth Spec"
  [cURL]: http://curl.haxx.se/ "cURL"
  [Twilio]: https://www.twilio.com/ "Twilio"
  [Runscope]: https://www.runscope.com "Runscope"
  [uuids]: http://en.wikipedia.org/wiki/Universally_unique_identifier "UUID on Wikipedia"
  [base64]: http://en.wikipedia.org/wiki/Base64 "Base64 on Wikipedia"
  [AWS]: http://aws.amazon.com/ "Amazon Web Services"
