---
title: "Asterisk Expression Truthiness"
date: "2010-08-18"
tags: ["programming", "telephony", "asterisk"]
slug: "asterisk-expression-truthiness"
description: "A quick look at what Asterisk considers 'truth'.  We'll look at source code and plenty of examples."
---


![Stephen Colbert Sketch][]


Ever done any extensive [Asterisk][] dial plan coding?  If so, chances are
you've been frustrated with Asterisk expressions at one point or another.

If you're unfamiliar with Asterisk coding, you should read this
[awesome book][] on the subject.

**NOTE**: The following is written with Asterisk 1.6+ in mind.  If you're using
an older version of Asterisk, this may not be *completely* true.


## Asterisk Expression Basics

Asterisk [expressions][] are used in various Asterisk dial plan applications,
to help control the flow of your program.  They are typically used as if
statements to help branch logic.

Let's look at an example from the latest version of [FreePBX][], an extremely
popular open source Asterisk web front-end:

```ini
; Rings one or more extensions.  Handles things like call forwarding and
; DND. We don't call dial directly for anything internal anymore.
; ARGS: $TIMER, $OPTIONS, $EXT1, $EXT2, $EXT3, ...
; Use a Macro call such as the following:
;   Macro(dial,$DIAL_TIMER,$DIAL_OPTIONS,$EXT1,$EXT2,$EXT3,...)
[macro-dial]
exten => s,1,GotoIf($["${MOHCLASS}" = ""]?dial)
exten => s,n,SetMusicOnHold(${MOHCLASS})
exten => s,n(dial),AGI(dialparties.agi)
exten => s,n,NoOp(Returned from dialparties with no extensions to call and DIALSTATUS: ${DIALSTATUS})
```

In this short snippet, we see the Asterisk expression
`$["${MOHCLASS}" = ""]?dial`.  This short expression is the equivalent of the
following pseudo code (which looks curiously like python):

```python
def macro_dial(*args):
    global MOHCLASS

    if MOHCLASS:
        set_moh(MOHCLASS)

    dial(*args)
```

Makes sense so far, right?  Basically, if `MOHCLASS` is false, then the code
will not execute the `SetMusicOnHold` application before performing a dial.

And of course, expressions aren't limited to a single statement, they can be
used pretty much anywhere.  Here's another snippet from the latest version of
FreePBX:

```ini
exten => s,n,Set(DIALSTATUS=${IF($["${DIALSTATUS_CW}"!="" ]?${DIALSTATUS_CW}:${DIALSTATUS})})

exten => s,n,GosubIf($["${SCREEN}" != "" | "${DIALSTATUS}" = "ANSWER"]?${DIALSTATUS},1)
```

As you can see, expressions provide most common logical operators like `AND`,
`OR`, `NOT`, etc.


## Truthiness

In an attempt to demonstrate the truthiness of Asterisk expression, I'll
dissect the FreePBX code shown in the previous section.

Let's start by testing all aspects of the original FreePBX expression:

```ini
exten => s,1,GotoIf($["${MOHCLASS}" = ""]?dial)
```

In order to test it, let's run some dial plan code.

**NOTE**: I'm not showing the Asterisk output for any of the tests, because it
would take an enormous amount of space and be essentially useless.  So you can
take my answers to be true (I've tested them, I promise!), or test it for
yourself.


### Test 1

The first thing we'll test is what happens if the `MOHCLASS` doesn't exist?

```ini
exten => s,n,GotoIf($["${MOHCLASS}" = ""]?dial)
exten => s,n(dial),NoOp()
```

The output of our first test shows that the expression resolves to true (1).
That means that, `$["${MOHCLASS}" = ""]` can be used to test whether or not the
`MOHCLASS` variable exists.


### Test 2

In this test, we'll see what happens if `MOHCLASS` has been defined, and set to
a line of text.

```ini
exten => s,n,Set(MOHCLASS=hithere)
exten => s,n,GotoIf($["${MOHCLASS}" = ""]?dial)
exten => s,n(dial),NoOp()
```

This time, the expressions returns false (0).  This makes sense, as we wouldn't
expect Asterisk to think that both `""` and `hithere` are equal.


### Test 3

Now, let's see what happens if `MOHCLASS` is defined, and set to 0 (false).

```ini
exten => s,n,Set(MOHCLASS=0)
exten => s,n,GotoIf($["${MOHCLASS}" = ""]?dial)
exten => s,n(dial),NoOp()
```

Surprisingly, the expressions resolves to false.  Therefore, `0` != `""`.


### Test 4

How about if `MOHCLASS` is defined, but not assigned any value?

```ini
exten => s,n,Set(MOHCLASS=)
exten => s,n,GotoIf($["${MOHCLASS}" = ""]?dial)
exten => s,n(dial),NoOp()
```

This time, we get true (1).  So if a variable is set, but has no value, the
checking of the variable is equal to an empty string, e.g. `""`, will return
true.


### Test 5

And what if `MOHCLASS` is set to the empty string?

```ini
exten => s,n,Set(MOHCLASS="")
exten => s,n,GotoIf($["${MOHCLASS}" = ""]?dial)
exten => s,n(dial),NoOp()
```

Again, it resolves to true (1).  So, as expected, `""` = `""`.


## Truthiness Table

To summarize what we've learned, here's a simple truthiness table:

```console
expression      true?
----------      -----
"" = ""         1
0 = ""          0
= ""            1
blah = ""       0
undef = ""      0
```

As you can see, Asterisk is (for the most part) relatively easy to comprehend
when it comes to truthiness.  The only surprising expression we encountered was
the: `0 = ""` expression, which is *not* true.


## Questions?

Got any questions?  Feel free to [shoot me an email][] or message me on
[twitter][].


  [Stephen Colbert Sketch]: /static/images/2010/stephen-colbert-sketch.png "Stephen Colbert Sketch"
  [Asterisk]: http://www.asterisk.org/ "Asterisk"
  [awesome book]: http://www.amazon.com/gp/product/0596517343/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=0596517343&linkCode=as2&tag=rdegges-20 "Asterisk: The Definitive Guide"
  [expressions]: http://www.voip-info.org/wiki/view/Asterisk+Expressions "Asterisk Expressions Wiki Page"
  [FreePBX]: http://www.freepbx.org/ "FreePBX"
  [shoot me an email]: mailto:r@rdegges.com "Randall Degges' Email"
  [twitter]: https://twitter.com/rdegges "Randall Degges' Twitter"
