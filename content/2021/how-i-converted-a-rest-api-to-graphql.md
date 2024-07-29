---
aliases:
  - "/how-i-converted-a-rest-api-to-graphql/"
date: "2021-10-03"
description: "A short guide to REST API -> GraphQL conversion using StepZen."
slug: "how-i-converted-a-rest-api-to-graphql"
tags:
  - "programming"
title: "How I Converted a REST API I Don't Control to GraphQL"
---


![REST API to GraphQL][]

I've been building and working with REST APIs for many years now. Recently, however, I've been spending more and more of my time working with (and building) GraphQL-based APIs.

While GraphQL has generally made my life easier, especially as I've been building and consuming more data-heavy APIs, there is still one *extremely* annoying problem I've run into over and over again: lack of GraphQL support for third-party APIs I need to consume.

If I'm trying to use a third-party API service that *doesn't* have a GraphQL endpoint, I either need to:

1. Download, install, configure, and learn how to use their custom REST API clients (which takes a lot of time and means my codebase is now a bit cluttered), or
2. Build my own GraphQL proxy for their service… But this is a big task. I've got to read through all their REST API docs and carefully define GraphQL schemas for everything, learning all the ins and outs of their API as I go.

In short: it's a lot of work either way, but if I really want to use GraphQL everywhere I have to work for it.

In an ideal world, every API service would have a GraphQL endpoint, this way I could just use a single GraphQL library to query all the API services I need to talk to.

Luckily, one of my favorite developer tools, [StepZen][] (disclaimer: I advise them), has made this problem a lot less painful.


## What StepZen Does

StepZen is a platform that lets you host a GraphQL endpoint to use in your applications. But, more importantly, they've designed a schema system that lets you import (or build your own) GraphQL wrappers for just about anything: REST APIs, databases, etc. It's really neat!

Using the StepZen CLI, for example, I can create a new GraphQL endpoint that allows me to talk with the [Airtable][] and [FedEx][] APIs, neither of which support GraphQL natively. The beautiful thing is, I don't even need to write a GraphQL wrapper for this myself since someone else already did!

Here's what this looks like (assuming you've already got the [StepZen CLI][] installed and initialized):

```console
$ stepzen import airtable
$ stepzen import fedex
$ stepzen start
```

Using the `import` command, StepZen will download the publicly available GraphQL schemas for these services (Airtable and FedEx) to your local directory. The `start` command then launches a GraphQL explorer on localhost, port 5000, which you can use to interactively query the Airtable and FexEx APIs using GraphQL! Pretty neat!

![StepZen Query Dashboard][]


## How to Access Public GraphQL Schemas

So, let's say you want to use GraphQL to query an API service that doesn't support GraphQL. If you're using StepZen, you can find all the publicly available (official) schemas on the [StepZen Schemas repo][] on GitHub. This repo is namespaced, so if you see a folder in the project, you can use the `stepzen import` command on it directly. At the time of writing, there are 24 publicly available GraphQL schemas you can instantly use.

StepZen currently has support for lots of popular developer services: [Disqus][], [GitHub][], [Shopify][], etc.

You can, of course, create your own GraphQL schemas as well.


## The Problem I Ran Into with GraphQL

Several months ago I was working on a simple user-facing web app. The entire backend of the app was using GraphQL and I was trying to keep the codebase as pure as possible, which meant not using any REST APIs directly.

In all my years of building web apps, I've *always* used a REST API at some point. So this was a bit of an experiment to see whether or not I could build my app without cluttering my codebase with REST API clients or requests.

As I was working on the app, I went to use one of my favorite free API services, [Random User][]. If you haven't heard of it before, it's a publicly available REST API you can hit to generate realistic-looking fake users. It's incredible for building a development environment, using seed data in an app, or creating real-world-looking MVPs. I use it all the time.

I knew going into this process that the Random User API didn't have a GraphQL endpoint, so I figured I'd spend some time creating one for them.


## How to Convert a REST API to GraphQL

My goal, as I mentioned above, was to build a GraphQL endpoint for the Random User REST API.

In order to make this work, what you have to do is translate your REST API so the [StepZen service][] can understand which endpoints you are hitting and what types of inputs and outputs they require.

Once you've defined all this, StepZen will be able to create a GraphQL endpoint for your app. When your app queries the StepZen GraphQL endpoint, StepZen will translate your GraphQL request into the proper REST API call, execute the request, then translate the response and send it back to your app in standard GraphQL format.

Here's how you can convert any REST API to GraphQL using StepZen, step-by-step.


### Step 1: Read Through the REST API Docs and Identify Endpoints to Convert

The first part of converting any REST API to GraphQL is to fully understand what endpoints you want to convert from REST to GraphQL.

In my case, the Random User API only has a single endpoint, so this isn't complicated. But, let's say you're converting a large, popular API like [Twilio][] that has many endpoints... This can be much more difficult.

To make things simpler, here's what I recommend: when converting a REST API to GraphQL, identify the endpoints you *actually need* and ignore the rest. Trying to build an entire abstraction layer for a massive API like Twilio would be difficult, so instead, focus only on the key endpoints you need to use. In the future, if you need to use additional endpoints, you can always add support for them.

**NOTE**: This is especially true if you're using StepZen. It's incredibly easy to support additional endpoints in StepZen once you have a basic schema going, so don't feel bad about focusing on the important ones and ignoring the rest.

Following this just-in-time pattern will help save you time and get you back to working on the important stuff.


### Step 2: Understand the REST Endpoint's Schema

Every API endpoint has some sort of schema. For example, the Random User API, when queried, returns a blob of JSON similar to the following:

```json
{
  "results": [
    {
      "gender": "male",
      "name": {
        "title": "mr",
        "first": "brad",
        "last": "gibson"
      },
      "location": {
        "street": "9278 new road",
        "city": "kilcoole",
        "state": "waterford",
        "postcode": "93027",
        "coordinates": {
          "latitude": "20.9267",
          "longitude": "-7.9310"
        },
        "timezone": {
          "offset": "-3:30",
          "description": "Newfoundland"
        }
      },
      "email": "brad.gibson@example.com",
      "login": {
        "uuid": "155e77ee-ba6d-486f-95ce-0e0c0fb4b919",
        "username": "silverswan131",
        "password": "firewall",
        "salt": "TQA1Gz7x",
        "md5": "dc523cb313b63dfe5be2140b0c05b3bc",
        "sha1": "7a4aa07d1bedcc6bcf4b7f8856643492c191540d",
        "sha256": "74364e96174afa7d17ee52dd2c9c7a4651fe1254f471a78bda0190135dcd3480"
      },
      "dob": {
        "date": "1993-07-20T09:44:18.674Z",
        "age": 26
      },
      "registered": {
        "date": "2002-05-21T10:59:49.966Z",
        "age": 17
      },
      "phone": "011-962-7516",
      "cell": "081-454-0666",
      "id": {
        "name": "PPS",
        "value": "0390511T"
      },
      "picture": {
        "large": "https://randomuser.me/api/portraits/men/75.jpg",
        "medium": "https://randomuser.me/api/portraits/med/men/75.jpg",
        "thumbnail": "https://randomuser.me/api/portraits/thumb/men/75.jpg"
      },
      "nat": "IE"
    }
  ],
  "info": {
    "seed": "fea8be3e64777240",
    "results": 1,
    "page": 1,
    "version": "1.3"
  }
}
```

Since the purpose of the Random User API is to return random user data, I can clearly see in the JSON data many of the fields I might be interested in working with: `email`, `cell`, `username`, etc.

Once you've clearly identified the fields you want to make use of, move on to the next step.


### Step 3: Create a Corresponding GraphQL Schema

Once you've figured out which fields you want to make use of, you need to define a [GraphQL schema][] that will tell the StepZen service how to *understand* the endpoint's response.

You don't need to be a wizard to do this, just pick out the important fields (and their types) from a REST API response, then build a corresponding GraphQL type.

For example, here's the `RandomUser` type I defined based on the REST API output above:

```
type RandomUser {
  gender: String!
  title: String!
  firstName: String!
  lastName: String!
  streetNumber: Int!
  streetName: String!
  city: String!
  state: String!
  country: String!
  postcode: String!
  latitude: String!
  longitude: String!
  timezoneOffset: String!
  timezoneDescription: String!
  email: String!
  uuid: String!
  username: String!
  password: String!
  salt: String!
  md5: String!
  sha1: String!
  sha256: String!
  dateOfBirth: Date!
  age: Int!
  registeredDate: DateTime!
  registeredAge: Int!
  phone: String!
  cell: String!
  largePicture: String!
  mediumPicture: String!
  thumbnailPicture: String!
  nationality: String!
}
```

As you can see, I simply defined the fields I care about from the REST response, along with their type.

**NOTE**: The exclamation point after many of these fields is to mark these fields as non-nullable. This means that no matter what, these fields should always be present in a response.

What you'll want to do is create a new folder in your project and put this code into a file named `<servicename>.graphql`. In my case, I created the following directory tree and put the code into the `randomuser.graphql` file.

```text
randomuser
└─ randomuser.graphql
```


### Step 4: Define a GraphQL Query

Once your data modeling is complete and you've defined your type(s), it's time to define a special `Query` type that will tell the StepZen service how to communicate with the REST API you're converting.

To get started, edit the `<servicename>.graphql` file and add the following `Query` definition:

```
type Query {
  randomUser: RandomUser
    @rest(
      endpoint: "https://randomuser.me/api"
      resultroot: "results[]"
    )
}
```

This is a barebones query that essentially tells StepZen the `randomUser` query will return data of type `RandomUser` (which we defined in the previous step) and will get data by hitting the `https://randomuser.me/api` endpoint, then parsing the data out of the `results` JSON array field.

But… That's not all! We still have more work to do.

When I defined the `RandomUser` type above, I decided to make all the data flat, and not nested like it was in the original REST API. This is because I don't need any special nested fields when I generate a random user, I just want the data!

So, the next thing we need to do is explain to StepZen how to convert the nested JSON key/values into the custom schema I defined. To do this, we'll use the `setters` REST directive StepZen provides:

```
type Query {
  randomUser: RandomUser
    @rest(
      setters: [
        { field: "title", path: "name.title" }
        { field: "firstName", path: "name.first" }
        { field: "lastName", path: "name.last" }
        { field: "streetNumber", path: "location.street.number" }
        { field: "streetName", path: "location.street.name" }
        { field: "city", path: "location.city" }
        { field: "state", path: "location.state" }
        { field: "country", path: "location.country" }
        { field: "postcode", path: "location.postcode" }
        { field: "latitude", path: "location.coordinates.latitude" }
        { field: "longitude", path: "location.coordinates.longitude" }
        { field: "timezoneOffset", path: "location.timezone.offset" }
        { field: "timezoneDescription", path: "location.timezone.description" }
        { field: "uuid", path: "login.uuid" }
        { field: "username", path: "login.username" }
        { field: "password", path: "login.password" }
        { field: "salt", path: "login.salt" }
        { field: "md5", path: "login.md5" }
        { field: "sha1", path: "login.sha1" }
        { field: "sha256", path: "login.sha256" }
        { field: "dateOfBirth", path: "dob.date" }
        { field: "age", path: "dob.age" }
        { field: "registeredDate", path: "registered.date" }
        { field: "registeredAge", path: "registered.age" }
        { field: "largePicture", path: "picture.large" }
        { field: "mediumPicture", path: "picture.medium" }
        { field: "thumbnailPicture", path: "picture.thumbnail" }
        { field: "nationality", path: "nat" }
      ]
      endpoint: "https://randomuser.me/api"
      resultroot: "results[]"
    )
}
```

Using the `setters` directive, we're able to tell StepZen which fields in our `RandomUser` type can be supplied by which nested paths from the raw REST API JSON data. Neat!

There are lots of other things you can define using StepZen, so even if you have an incredibly complex endpoint there are always ways to support it. To learn more about this, you might want to read through the [StepZen docs](https://stepzen.com/docs/connecting-backends/how-to-connect-a-rest-service) on the subject.


### Step 5: Define the API Metadata

Once you've finished defining the data model and query, the next thing you'll want to do is prepare your GraphQL API schema for production!

In my case, I wanted to contribute my schema back to the StepZen developer community, so I forked the [stepzen-schemas repo][] and created a new top-level folder named `randomuser` in which I put my query/data model from above.

I then wrote up a README and created  a `stepzen.config.json` file which provides details about this schema:

```json
{
  "name": "RandomUser",
  "description": "Generates random users for testing purposes using the randomuser.me API.",
  "categories": ["Dev Tools"]
}
```

Notice how all I'm providing is a `name`, `description`, and any relevant `categories` this schema fits into.

Finally, I opened a pull request to the StepZen repo and the maintainers tested and merged my schema into the repo so anyone could use it!

Now, if you have no interest in creating a public GraphQL schema for the REST API you're converting, you can obviously skip this step. So long as you have a folder with your service name and your data model/queries defined, you can use StepZen to run your endpoint regardless of whether or not your schema is publicly available to the world.


## Using Your Converted REST API

Once you've built a schema that teaches StepZen how to talk to the REST API, how do you actually use it?

Well, in the example above, I built a public-facing StepZen schema and contributed it back to the community. In this case, I can simply use this schema like I would any other:

```console
$ stepzen import randomuser
$ stepzen start
```

This will download and install the schema I built, then deploy the code in the current directory to my personal StepZen GraphQL endpoint. It'll also watch the directory for changes and automatically deploy them if I tweak any of the schema code, etc.

In addition to the above, the `start` command will open a browser window with the StepZen Schema Explorer that will allow you to test your API by exploring the queries and types available and querying the API running on StepZen.

If you want to start querying your new GraphQL endpoint directly from an application, read through the [Connecting to Your StepZen API Guide][] which shows some examples of how to connect/query your new GraphQL API.


## Recap: How to Convert a REST API You Don't Control to GraphQL

If you're trying to find a way to use GraphQL on a REST API, here's what you should do.

First, check StepZen's list of [publicly supported schemas][] to see if a schema already exists. This means you can use GraphQL to access the API of your choice without doing much.

If there isn't a public schema available, go build your own! To do this:

1. Figure out what endpoints you need to use
2. Figuring out what data your endpoints take as input/output
3. Define a GraphQL type to reflect what your endpoints look like in GraphQL
4. Define a StepZen query to explain how the StepZen service can interact with the REST API

Once you have a schema, you can easily deploy it live to the StepZen service, which will give you a dedicated GraphQL endpoint/explorer you can query. And bam, you're now able to use GraphQL to talk to any REST API, even ones you don't own/control/etc!


  [REST API to GraphQL]: /static/images/2021/rest-to-graphql.gif "REST API to GraphQL GIF"
  [StepZen]: https://stepzen.com/ "StepZen"
  [Airtable]: https://www.airtable.com/ "Airtable"
  [FedEx]: https://www.fedex.com/en-us/home.html "FedEx"
  [StepZen CLI]: https://stepzen.com/docs/cli "StepZen CLI"
  [StepZen Query Dashboard]: /static/images/2021/stepzen-query-dashboard.png "StepZen Query Dashboard"
  [StepZen Schemas repo]: https://github.com/steprz/stepzen-schemas "StepZen Schemas on GitHub"
  [Disqus]: https://disqus.com/api/docs/ "Disqus API"
  [GitHub]: https://docs.github.com/en/rest "GitHub API"
  [Shopify]: https://shopify.dev/api/admin/rest/reference "Shopify API"
  [Random User]: https://randomuser.me/ "Random User"
  [StepZen service]: https://stepzen.com/ "StepZen"
  [Twilio]: https://www.twilio.com/docs/usage/api "Twilio API"
  [GraphQL schema]: https://graphql.org/learn/schema/ "GraphQL Schema"
  [stepzen-schemas repo]: https://github.com/steprz/stepzen-schemas "StepZen Schemas Repo"
  [Connecting to Your StepZen API Guide]: https://stepzen.com/docs/connecting-frontends/connecting-to-stepzen "Connecting to Your StepZen API"
  [publicly supported schemas]: https://github.com/steprz/stepzen-schemas "StepZen Publicly Supported Schemas"
