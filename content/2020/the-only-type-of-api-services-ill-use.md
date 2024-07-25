---
aliases:
  - "/the-only-type-of-api-services-ill-use/"
date: "2020-02-17"
description: "How you price an API service is incredibly important. In this article I'll explain what good API pricing looks like, and why."
slug: "the-only-type-of-api-services-ill-use"
tags:
  - "programming"
  - "business"
title: "The Only Type of API Services I'll Use"
---


![Lady Justice Sketch][Lady Justice Sketch]

I love API services. It still feels *magical* each time I query an endpoint and get back some interesting data or cause some complicated functionality to occur.

I've built my entire career (and hobbies) around API services. I've only ever had one job (which only lasted several months) that *wasn't* focused on building or working with API services for other developers. To say I am heavily invested in developer services would be an understatement; it's essentially all I do.

With that being said, over these last ~15 or so years I've come to develop some strong opinions in regards to API businesses: how they should work, what they should look like, how they should be documented, how they should be priced, etc. And while all of these things can be done differently, there's one thing that I strongly believe all API services should do, and it's so important that if an API service doesn't do it, I refuse to use it. And that thing is *usage-based pricing with automatic volume discounts*.

## Why I Love Usage-Based Pricing

![Sand Clock Sketch][Sand Clock Sketch]

Usage-based pricing with automatic volume discounts is the only pricing model I believe API services should adopt. The concept is simple: the amount a customer pays for using an API service should depend on how much they use the service.

For example, if you're building an API service that stores data, you should price your service so that customers pay for the amount of data they store with you. Maybe you charge **$0.01** per gigabyte (up to 1TB), **$0.001** per gigabyte (up to 5TB), and **$0.0001** per gigabyte (for anything above 5TB).

I like this pricing model because:

- The more a customer uses your service, the more money you make
- If a customer is getting value out of your service, it's only natural their usage will increase, thereby increasing the amount of money you make
- If a customer decreases their usage of your service, you'll make less money and the customer will get less value from your service

But the most important reason I like this pricing model is that **it heavily incentivizes both the customer and the service provider to act in everyone's best interest**.

When API services have a usage-based pricing model, the service provider is *strongly incentivized* to improve their service (add features, improve stability, improve documentation, improve user experience, etc.) because they need to do whatever they possibly can to convince their customers to use their service more.

If your business relies on charging customers $0.01 for sending an SMS message, then you're going to make sure that:

- Your service has a high amount of uptime (otherwise each second you're down you're missing out on revenue potential)
- Your service can support a high amount of throughput (otherwise you won't be able to earn as much revenue if you can't service the amount of usage customers demand)
- Your service has a high deliverability rate (because if you aren't able to deliver those SMS messages for customers then you aren't getting paid)
- Your service has great developer libraries and documentation (otherwise you won't be able to grow the usage of your service as much since integrating will be difficult for customers)
- Your service is actually providing value to your customers (otherwise they won't increase their usage of your service over time)

On the customer side, usage-based pricing also incentivizes good behavior:

- The more customers use your service, the more value they get
- If customers increase their usage of your service, they get a better deal (automatic volume discounts)
- If customers reduce their usage of your service, they get a worse deal (automatic volume discounts)

Usage-based pricing with automatic volume discounting incentivizes both parties to grow and win *together*. Neither party is in an adversarial position with the other.

With usage-based pricing models, customers feel like they are getting a good deal because they're paying for exactly what they use. They aren't getting "ripped off" by paying for something they aren't using. In fact, the more customers use your service, the cheaper it gets for them (automatic volume discounts)!

For service-providers, usage-based pricing can also be great because it gives companies a clear and measurable way to grow their business: *increase usage*. This means that companies can focus on the most important thing (the product) as opposed to hundreds of other metrics companies tend to obsess over that detract from focusing on the service.

## Problems With Other Pricing Models

![Grim Reaper Sketch][Grim Reaper Sketch]

I've seen lots of pricing models for API services, but there are only two I'd like to discuss with you today: *bucket-based* and *enterprise* (otherwise known as *contact-us*). These are the two pricing models I most frequently see used by API vendors.

### Problems With Bucket-Based Pricing

![Bucket Sketch][Bucket Sketch]

Bucket-based pricing is when you charge customers a set amount of money to purchase credits for your service.

For example, imagine you run an SMS-sending API and you have three pricing tiers available:

- **$10/mo**: which lets customers send up to 1,000 SMS messages
- **$50/mo**: which lets customers send up to 5,000 SMS messages
- **$100/mo**: which lets customers send up to 10,000 SMS messages

Bucket-based pricing creates an *adversarial* relationship between you and the customer because the customer is *always* going to pay more for your service than they want to. If the customer only needs to send 2,500 SMS messages, for example, they have no choice but to pay you $50/mo, which is twice as much as they'd like to spend, since you don't have a pricing plan that allows them to *only* purchase 2,500 SMS credits.

Because of this, customers who pay for bucket-based services are always getting slighted. The odds of a customer hitting 100% utilization of their plan is very slim, so they're essentially being charged more money for... Nothing.

Another side-effect of bucket-based pricing is that it incentivizes customers to *use your service less* so they can fall into a lower-tier bucket and minimize spend. This is unfortunate for both you *and* your customers because it incentivizes your customers to spend a lot of time and effort carefully planning how to use your service less (so they can maximize their value and fully utilize whatever bucket they're in) while you (the service provider) are going to get less overall usage (and therefore money) than you might have gotten otherwise.

On the service provider side, however, bucket-based pricing plans continue to be very popular. Some of the reasons companies like to structure their pricing in this way is that:

- **It generates more predictable amounts of revenue.** If you force customers to pay a set amount of money each month to use your service, you can easily predict how much money you're going to make. Venture capitalists love this. In usage-based pricing models, your top-line revenues will fluctuate much more as customer usage ebbs and flows.
- **It increases margins.** Because bucket-based pricing captures revenue even when customers don't use the service, companies are able to make more money while giving less service. This is great for companies that don't have strong engineering leadership as they can get by with less scalable services, more outages, and poor customer experiences as they'll still be making money regardless of whether or not these issues occur.

Bucket-based pricing incentivizes service providers to act poorly. Service providers are incentivized to discourage increased usage (to a point) as well as not make frequent updates and fixes to their service as they profit, to some extent, from the *lack of use* of their service.

Customers are also poorly incentivized when using bucket-based pricing plans. Instead of making the most out of an API service and increasing spend over time, they're incentivized to use as little service as possible to minimize spend and maximize value.

In addition to the obvious, bucket-based pricing plans encourage customers to have a [scarcity mindset](https://www.psychologytoday.com/us/blog/science-choice/201504/the-scarcity-mindset) which may impact the adoption of services.

### Problems With Enterprise Pricing

![Business Man Sketch][Business Man Sketch]

Enterprise pricing is an entire category of pricing models that lock customers into year-long (or multi-year) agreements where prices are fixed for the duration of the agreement and renegotiated when the contract comes up for renewal.

For example, imagine you're a web hosting company that hosts servers for your customers. An enterprise pricing model might involve you speaking with customers to negotiate prices such that a customer might pay 1M for a two-year contract which gives them the ability to run up to 100 16G RAM servers for the full two-years.

This model creates an *adversarial* relationship between you and the customer. You're incentivized to charge the customer as much as possible, for as little service as possible, for as long as possible. Customers know this, and are often apprehensive about these types of deal negotiations, so they tend to only go through this process if absolutely necessary as it's time-consuming, expensive, and generally understood to be a win-lose scenario (the service provider wins and the customer loses).

For customers, there really is no winning in an enterprise pricing scenario. Because prices are negotiable and private, this means service providers have an advantage in negotiations since their pricing isn't publicly available. It also means that customers need to be aggressive with their negotiations not just once, but every time a contract is up for renewal. This is time-consuming and expensive for both parties.

Furthermore, enterprise pricing plans lock customers into expensive long-term agreements that limit their ability to migrate to alternative providers without incurring substantial penalties. If I sign a two-year agreement to spend 1M with Amazon and am later offered the same level of service at half the cost by Google, I'll still be liable for paying Amazon the full value of that initial, two-year contract.

In my opinion, enterprise pricing is an *absolute racket*.

It's a lot like the way ISPs price their services here in the US. I might call Comcast for internet service at my home and be quoted a discounted rate of $75/mo if I sign a two-year agreement. Then, when my contract is coming up for renewal, the price will suddenly jump to $100/mo. This means each year I've got to negotiate with them so my costs don't increase substantially.

And in the case of ISPs like Comcast, what happens if I move? Let's say I move to another address where Comcast doesn't operate--I'm still going to be held liable for paying them for the full duration of my contract, even though I'll be unable to use their services.

As you can see, it's a win-lose scenario (great for Comcast, terrible for me).

Another reason I dislike enterprise pricing plans is that they generate a lot of unnecessary waste: the service provider has to hire sales reps to field customer inquiries and negotiate pricing while customers need to waste lots of time and energy going through a sales rep in order to access the service, negotiate pricing, etc.

Regardless of whether you're a service provider or a customer trying to purchase services, the enterprise pricing model significantly complicates matters as it requires lots more time, effort, and cost to complete a sale.

In my opinion, just about any type of pricing scheme is better than the enterprise pricing model as it substantially complicates selling and purchasing products -- something that is rarely necessary.

## My Thoughts On API Pricing

![Thinking Man Sketch][Thinking Man Sketch]

As both a consumer and provider of API services, the only type of pricing plan I'll use is usage-based pricing with automatic volume discounts. There are no negotiations, no misaligned incentives for either party, and nobody is being slighted.

When I'm evaluating potential API services, if they don't have a usage-based pricing model I'll immediately move on and look for other solutions. Other pricing models are a hard *no* for me as they incentivize poor behavior and put me in an adversarial position with whatever service provider I'm looking to utilize.

As a service provider, I *love* using usage-based pricing models as it means I can focus all my energy and effort on what I do best: running a service. It lets me focus on the quality of my service above everything else. Usage-based pricing also allows me to scale my service's revenues without hiring a large fleet of sales reps.

As my service gets better and usage increases, I make more money. Having a usage-based pricing model with automatic volume discounts incentivizes my users to use *more* of my service, thereby increasing revenues while making everyone happy. 

And, in addition to all the other reasons why I believe usage-based pricing is the way to go, there's another one that isn't as easy to quantify: *it just makes sense*.

API services exist to allow developers to outsource bits and pieces of their application logic. In my mind, API services are essentially the utility companies of the web.

And if you think of API services as utility companies, it only makes sense that they should charge based on usage. After all, imagine what would happen if you had to sign a two-year contract stipulating how much electricity you're going to use at home, or if you had to choose a bucket plan for electricity that forced you to purchase a set amount of kilowatt-hours of electricity.

I'm confident that in either scenario you would be upset because you'd almost certainly be paying for more electricity than you used.

With all that said, if you're thinking about how you should be pricing an API service, please consider usage-based pricing with automatic volume discounts. I believe that, more than any other pricing scheme, this will help set you and your customers up for success as well as a long, healthy business relationship.


  [Lady Justice Sketch]: /static/images/2020/lady-justice-sketch.png "Lady Justice Sketch"
  [Sand Clock Sketch]: /static/images/2020/sand-clock-sketch.png "Sand Clock Sketch"
  [Grim Reaper Sketch]: /static/images/2020/grim-reaper-sketch.png "Grim Reaper Sketch"
  [Bucket Sketch]: /static/images/2020/bucket-sketch.png "Bucket Sketch"
  [Business Man Sketch]: /static/images/2020/business-man-sketch.png "Business Man Sketch"
  [Thinking Man Sketch]: /static/images/2020/thinking-man-sketch.png "Thinking Man Sketch"
