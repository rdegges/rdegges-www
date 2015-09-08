---
title: "Why You Might Enjoy Using DNSimple"
date: "2012-11-27"
tags: ["reviews"]
slug: "why-you-might-enjoy-using-dnsimple"
description: "DNSimple is the greatest DNS provider in the history of the universe.  You'd be crazy not to use them.  Here's why."
---


![Saturn Sketch][]


Practically everyone I know involved in the tech industry has a preferred
domain name registrar / DNS provider.  I've used quite a few different
companies myself over the years, and have come to really, *really* like
[DNSimple][].

DNSimple is, in my experience, the simplest, most elegant, and best all around
domain name registrar and DNS provider.  Since I often get the *What registrar
do you use?* question when talking with friends online, I figured I'd chronicle
my experiences with DNSimple here.

If you're already a DNSimple customer, you may enjoy this article regardless.
If you're not yet a DNSimple customer, but are already sold, you can
[sign up here][] and both you and I will get a free month of service.


## Interface

DNSimple has an awesome interface.  The company is built around the idea that
DNS should be simple, and their interface reflects this.

Below are some screenshots of my personal DNSimple account.

![DNSimple Account][]

![DNSimple Contacts][]

![DNSimple Add Domain][]

![DNSimple Apply Domain Template][]

![DNSimple Domains][]

![DNSimple Templates][]

![DNSimple Domain Editor][]

![DNSimple Domain Page][]

I love their interface.  Their UI is simple and elegant.  You can easily
register and transfer domains.  You can easily update DNS records manually
using their advanced editor (which is, by far, the simplest DNS editor I've
ever used), and you can even use their pre-built DNS templates to instantly add
DNS records to your domain (for stuff like Google Apps, Heroku, Cloudflare,
etc.).

If you find yourself frequently applying similar DNS rules, you can even create
your own custom DNS templates, which allows you to perform one-click DNS record
additions to as many domains as you'd like.

Lastly, DNSimple doesn't try to up-sell you additional services.  Purchasing a
domain name takes two clicks, and there are no spammy ads or any other junk
preventing you from doing what you want to do: purchase your damn domain name!


## URL Forwarding

What has quickly become one of my favorite lesser known DNSimple features is
their URL forwarding service.  This allows you to create a DNS 'URL' record
which redirects users to your desired location.

This works great for instances where your site runs under the `www` sub-domain,
and you'd like to force all users who visit your naked domain (e.g.
`mysite.com`) to be redirected to your `www` sub-domain (e.g.
`www.mysite.com`).  If you're wondering why I use `www` instead of naked
domains, see [this article][] (it's worth your time).

Below is a screen shot from one of my domains--you can see my URL record and
how it forwards.

![DNSimple URL Forwarding][]


## SSL

Another great thing about DNSimple is their excellent SSL handling.

For some reason, every registrar I've ever used has made purchasing SSL
certificates a confusing, frustrating, and slow experience.  DNSimple is the
only company I've worked with that actually makes purchasing and using SSL
certificates simple and straightforward.

Below is what their SSL certificate purchasing page looks like.  See how simple
that is?

![DNSimple SSL][]

Once you've purchased a certificate, DNSimple adds a nice SSL certificate
section to your domain page, which allows you to easily download or copy and
paste your SSL details for usage with your provider.  If you're using Heroku,
there's [a guide you can follow][] to get up and running with SSL and DNSimple.


## API

Another thing that really bugs me about most registrars is that they have no
easily accessible API.  Since domain names are primarily managed by
programmers, this has always felt completely unacceptable to me.

Luckily, DNSimple has a really great REST API, along with excellent
[API documentation][] and a bunch of [client libraries][].

There are even some [great tools][] you can use, built on top of the DNSimple
API--worth checking out if you'd like to see some real-world DNSimple API
examples.


## Price

DNSimple is very reasonably priced.  They charge a small per-month membership
fee depending on how many domains you have (see their [plan page][] for
details), and they support a long list of TLDs (see their [TLD pricing page][]
here).


## Support

Among registrars I've used, DNSimple has, by far, the best support.  I've sent
them several support emails with questions over the past year or so, and each
time I've received an email answer immediately (from a developer).

Each time I've talked with someone at the company, I've been extremely
impressed by the speed (and accuracy) of service.


## Final Thoughts

DNSimple is, without question, my favorite domain name registrar and DNS
provider.  They've been able to live up to their name and really make
DNS--*simple*.

If you're shopping around for a new registrar, I'd highly recommend you give
DNSimple a shot, I guarantee you'll like them.

The only gripe I have about DNSimple is only that they don't (yet) have an
Android app!  (They do have an [Iphone app][], if you're an IOS guy.)

Anyhow, if you'd like to give DNSimple a shot, create an account
now: [https://dnsimple.com/][DNSimple].


  [Saturn Sketch]: /static/images/2012/saturn-sketch.png "Saturn Sketch"
  [DNSimple]: https://dnsimple.com/r/d9a8f0b92dfb78 "DNSimple"
  [sign up here]: https://dnsimple.com/r/d9a8f0b92dfb78 "sign up here"
  [DNSimple Account]: /static/images/2012/dnsimple-account.png "DNSimple Account"
  [DNSimple Contacts]: /static/images/2012/dnsimple-contacts.png "DNSimple Contacts"
  [DNSimple Add Domain]: /static/images/2012/dnsimple-add-domain.png "DNSimple Add Domain"
  [DNSimple Apply Domain Template]: /static/images/2012/dnsimple-apply-domain-template.png "DNSimple Apply Domain Template"
  [DNSimple Domains]: /static/images/2012/dnsimple-domains.png "DNSimple Domains"
  [DNSimple Templates]: /static/images/2012/dnsimple-templates.png "DNSimple Templates"
  [DNSimple Domain Editor]: /static/images/2012/dnsimple-domain-editor.png "DNSimple Domain Editor"
  [DNSimple Domain Page]: /static/images/2012/dnsimple-domain-page.png "DNSimple Domain Page"
  [this article]: https://devcenter.heroku.com/articles/avoiding-naked-domains-dns-arecords "Avoid Naked Domains"
  [DNSimple URL Forwarding]: /static/images/2012/dnsimple-url-forwarding.png "DNSimple URL Forwarding"
  [DNSimple SSL]: /static/images/2012/dnsimple-ssl.png "DNSimple SSL"
  [a guide you can follow]: https://devcenter.heroku.com/articles/ssl "Heroku SSL Guide"
  [API documentation]: http://developer.dnsimple.com/ "DNSimple API Documentation"
  [client libraries]: http://developer.dnsimple.com/libraries/ "DNSimple API Libraries"
  [great tools]: http://developer.dnsimple.com/tools/ "DNSimple Tools"
  [plan page]: https://dnsimple.com/plans "DNSimple Plans"
  [TLD pricing page]: https://dnsimple.com/tld-pricing "DNSimple TLD Pricing"
  [Iphone app]: https://itunes.apple.com/app/dnsimple-app/id507299306?mt=8 "DNSimple Iphone App"
