---
title: "Easy Fuzzy Text Searching With PostgreSQL"
date: "2013-06-12"
tags: ["programming"]
slug: "easy-fuzzy-text-searching-with-postgresql"
description: "PostgreSQL has a really useful extension which allows you to easily do full text fuzzy search."
---


![Monster in Disguise Sketch][]

I've been using PostgreSQL for the past few years as my primary database of
choice.  I figured I'd take a moment to write about one of the coolest features
I use on a daily basis, that you may find interesting (if you're not already
using it).

**NOTE**: I use [Heroku Postgres][] to host all my PostgreSQL instances -- so
these instructions will work for you if you're using Heroku Postgres.  If you're
not, your mileage may vary (depending on your server setup).


## Fuzzy Text Searching

Fuzzy text searching is *fucking awesome*.  Let's say you've got a table in your
database that contains a list of people and their names, for example:

```sql
d51job1rstb2g=> SELECT first_name FROM people WHERE first_name LIKE 'Gar%' LIMIT 9;
 first_name
------------
 Gary
 Gary
 Gary
 Garden
 Gary
 Gary
 Garfield
 Gar
 Gary
(9 rows)
```

Now, let's say you now want to grab everyone whose name is similar to `Gary`.
This could be tricky to do unless you have fuzzy text searching available in
your database -- right?

There's no built in way to tell your database *"Hey!  Give me a list of all the
people whose first name is similar to 'Gary'"*.

This is where fuzzy text searching rocks -- it does the similarity matches for
you, so that you can tell your database something like the above.

It'd be ideal if we could do something like:

```sql
d51job1rstb2g=> SELECT first_name FROM people WHERE first_name % 'Gary' LIMIT 10;
 first_name
------------
 Gary
 Gary
 Calgary
 Gary
 Gary
 Gary
 Geary
 Gar
 Garage
(10 rows)
```

As you can see above, I just used a made up operator (`%`) which allowed me to
select a bunch of fuzzily matched text strings similar to the word `Gary` --
and it worked!


## PostgreSQL Fuzzy Text Searching

So now the question is: *How can we make PostgreSQL support fuzzy text
searching?*  The answer is actually pretty simple: [pg_trgm][].

`pg_trgm` is a PostgreSQL extension which ships with PostgreSQL, and only needs
to be activated once on your database so that you can use it.

To activate it, just run:

```sql
CREATE EXTENSION pg_trgm;
```

On your PostgreSQL server -- and *bam* -- you now have fuzzy text searching
capabilities!

What's especially awesome about the `pg_trgm` extension is that it works
anywhere a `LIKE` statement would work.  This means that you can make use of
fuzzy text searching pretty much anywhere you want -- and it involves very
few changes to your code base!

Let's say you've got a table of businesses, and one of the columns in your
`businesses` table is `categories` -- an `ARRAY` column which stores business
categories:

```sql
d51job1rstb2g=> SELECT name, categories from businesses WHERE 'Zoos' = ANY(categories) LIMIT 5;
                         name                          |                                                            categories
-------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------
 ANIMAL HOUSE EXOTIC ANIMALS & OSTRICH FARM            | {Zoos}
 LITTLE ROCK ZOO                                       | {Zoos,"Zoos & Wildlife Conservancies"}
 TURPENTINE CREEK WILDLIFE REFUGE                      | {"Wildlife Refuges & Sanctuaries","Campground & Recreational Vehicle Parks","Amusement Places",Zoos,"Wedding Ceremony Locations"}
 U S 65 THE ZOO                                        | {Zoos}
 RIDDLE'S ELEPHANT BREEDING FARM & WILD LIFE SANCTUARY | {"Wildlife Services","Wildlife Refuges & Sanctuaries","Wildlife Removal & Preservation",Zoos}
(5 rows)
```

In the example above, we did an exact search to find any businesses who have a
category that is equal to the string `Zoos`.

Now, if we want to enable fuzzy text searching on our `ARRAY` search, we can do
so easily (just like we did in our previous example):

```sql
d51job1rstb2g=> SELECT name, categories from businesses WHERE 'zoo' % ANY(categories) LIMIT 5;
                         name                          |                                                            categories
-------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------
 ANIMAL HOUSE EXOTIC ANIMALS & OSTRICH FARM            | {Zoos}
 LITTLE ROCK ZOO                                       | {Zoos,"Zoos & Wildlife Conservancies"}
 TURPENTINE CREEK WILDLIFE REFUGE                      | {"Wildlife Refuges & Sanctuaries","Campground & Recreational Vehicle Parks","Amusement Places",Zoos,"Wedding Ceremony Locations"}
 U S 65 THE ZOO                                        | {Zoos}
 RIDDLE'S ELEPHANT BREEDING FARM & WILD LIFE SANCTUARY | {"Wildlife Services","Wildlife Refuges & Sanctuaries","Wildlife Removal & Preservation",Zoos}
(5 rowss
```

This time, we did a fuzzy text search for the word `zoo`, and got back the same
results!  Nice, right?

The thing to keep in mind here is that you can use the fuzzy text search
operator (`%`) anywhere you would a `LIKE` statement (or any other selection
type statement).


## Performance Considerations

Using the built in `pg_trgm` extension is a great way to quickly support fuzzy
text searching on your existing data without having to do any special work.  The
drawback, of course, is that this method is a lot slower than using an external
search service with proper indexes ([Solr][], [Elastic Search][]).

In my experience, if you're running small to mid-sized services, however,
`pg_trgm` is a perfectly suitable solution -- it's easy, adds no additional
maintenance work, no additional servers, etc.

The next time you're looking to do fuzzy text searching, don't stress it!  Just
use `pg_trgm` and move on with your life >:)

Got any questions?  Feel free to [shoot me an email][], would be happy to help.


  [Monster in Disguise Sketch]: /static/images/2013/monster-in-disguise-sketch.jpg "Monster in Disguise Sketch"
  [Heroku Postgres]: https://postgres.heroku.com/ "Heroku Postgres"
  [pg_trgm]: http://www.postgresql.org/docs/9.2/static/pgtrgm.html "PostgreSQL Fuzzy Text Searching"
  [Solr]: https://lucene.apache.org/solr/ "Apache Solr"
  [Elastic Search]: http://www.elasticsearch.org/ "Elastic Search"
  [shoot me an email]: mailto:r@rdegges.com "Randall Degges' Email"
