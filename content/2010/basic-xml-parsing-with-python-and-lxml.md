---
title: "Basic XML Parsing With Python and LXML"
date: "2010-03-16"
tags: ["programming", "python"]
slug: "basic-xml-parsing-with-python-and-lxml"
description: "The simplest way to parse basic XML code with Python (hint: use LXML)."
---


![Lumberjack Sketch][]


Recently I've been developing an API using python and [Django][] for work,
which uses XML responses to speak to clients.  One of my goals for the client
was to be able to easily parse the XML responses that the server sends, so that
I could appropriately handle errors.

Fortunately, python has many tools for building and parsing XML.  During my
research, I tested several options, but found that the well supported library
[LXML][] was a perfect match for what I needed.  Unfortunately, I had a hard
time figuring this out, as examples to just parse XML content was lacking in
the official tutorial, and there were no good resources online with code
samples.

So let's take a quick peek at a sample XML document, then we'll analyze some
simple LXML code to see how it works.  Of course, before you can run any of
these code samples, you'll need to download and install LXML (there are
packages available on most Linux systems already).

Here's are two sample XML responses that our server may send to the clients:

```xml
<?xml version="1.0" encoding="utf-8"?>
<response version="1.0">
  <code>200</code>
  <id>50</id>
</response>
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<response version="1.0">
  <code>400</code>
  <errors>
      <error>This API call requires a HTTP POST.</error>
  </errors>
</response>
```

The first XML document shows a successful response.  The `code` tag contains an
HTTP `200 OK` code, which means the operation succeeded, and the `id` tag
contains an identification number which the client needs to store for later
processing.

Now, let's quickly analyze the situation.  We have an XML tag which will be
available whether the operation succeeds or fails, which is the `code` tag.
So, for the client to be able to distinguish between a success or failure, it
needs to first figure out what `code` was returned.

Let's write some `python-lxml` code to quickly output the value of the `code`
tag:

```python
from lxml import etree

response = 'some xml response here'

try:
    doc = etree.XML(response.strip())
    code = doc.findtext('code')
    print code
except etree.XMLSyntaxError:
    print 'XML parsing error.'
```

In our code, we first build a XML document from our XML response string, then
use the `findtext()` method (provided by LXML) to retrieve the value of the
`code` tag.  Run this example, play around with it, and you'll see that you can
pull up any value you want from the XML document.

In my client code, the program flow looks something like:

```python
from sys import exit
from lxml import etree

response = 'some xml response here'

try:
    doc = etree.XML(response.strip())
    code = doc.findtext('code')
    print code
except etree.XMLSyntaxError:
    print 'XML parsing error.'
    exit(1)

if code == '200':
    # store the id somewhere
    id = doc.findtext('id')
else:
    # handle errors, do more stuff
    print doc.findtext('error')
    exit(1)

exit(0)
```

This lets me perform error checking on the XML response to make sure that
everything went smoothly.  If something goes wrong during the API call, then I
will know about it, and can perform other actions to fix any problems or report
errors.

If you'd like to do more advanced XML parsing with LXML, read the
[official tutorial][].  It is very verbose, but contains excellent examples
which clearly demonstrate how to both parse and generate XML.

So the next time you're looking for a quick way to process XML, check out LXML.


  [Lumberjack Sketch]: /static/images/2010/lumberjack-sketch.png "Lumberjack Sketch"
  [Django]: https://www.djangoproject.com/ "Django"
  [LXML]: http://lxml.de/ "LXML"
  [official tutorial]: http://lxml.de/tutorial.html "LXML Tutorial"
