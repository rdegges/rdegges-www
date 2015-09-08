---
title: "Quickly Extract XML Data with Python"
date: "2013-09-04"
tags: ["programming", "python"]
slug: "quickly-extract-xml-data-with-python"
description: "The simplest way to extract XML data with Python."
---


![Broken Demon Sketch][]


Today I had the unfortunate luck of having to integrate an XML web service into
an application I'm working on.

As you might already know, parsing JSON data with Python is really simple thanks
to some great built in tools.  I wish I could say the same thing for working
with XML!  Unfortunately, while Python *does* include built in XML processing
tools, they're not exactly the easiest thing in the world to work with.

I've [written][] about XML parsing in Python before (a really long time ago!),
but after spending an hour hunting around for the most elegant solution earlier
today, I figured I'd write a quick post as future reference to myself.

When I last worked with XML in Python, I recommended that users try to use the
[lxml][] library.  LXML is pretty great because it allows you do some advanced
things with XML, but on the downside: it requires C libraries (yuck!) that are
annoying to install locally, and adds another dependency to your project.

Instead of going the LXML route, I'd like to suggest using Python's built in
[xml.etree][] module.  It's got a (relatively) simple interface that makes
parsing simple XML documents fairly easy -- and since that's all I needed to do,
it seemed like a good solution.

If you're looking for a quick way to extract XML data, read on.

Anyhow, let's say you've got a simple XML document that looks something like the
below:

```xml
<?xml version='1.0' encoding='UTF-8'?>
<!DOCTYPE xgdresponse SYSTEM 'xgdresponse.dtd'>
<xgdresponse version='1.0'>
  <transid>2771709</transid>
  <errorcode>0</errorcode>
  <response>
    <result>
      <element>666</element>
      <errorcode>0</errorcode>
      <value>SOMETHING IMPORTANT!</value>
    </result>
  </response>
</xgdresponse>
```

Now, let's say you need to extract the `value` element out of this XML tree.
After lots of experimentation, this is the simplest way I found to do the data
extraction:

```python
"""Extract the `value` element from the XML tree, if it exists."""


from xml.etree import ElementTree as ET


xml = """
<?xml version='1.0' encoding='UTF-8'?>
<!DOCTYPE xgdresponse SYSTEM 'xgdresponse.dtd'>
<xgdresponse version='1.0'>
  <transid>2771709</transid>
  <errorcode>0</errorcode>
  <response>
    <result>
      <element>666</element>
      <errorcode>0</errorcode>
      <value>SOMETHING IMPORTANT!</value>
    </result>
  </response>
</xgdresponse>
""".strip()

value = ET.fromstring(xml).find('response/result/value')
if value:
    print 'Found value:', value.text
```

Which outputs:

```console
$ parse.py
Found value: SOMETHING IMPORTANT!
```

The way this works is that we:

- Load our XML document into memory, and construct an XML `ElementTree` object.
- We then use the `find` method, passing in an [XPath selector][], which allows
  us to specify what element we're trying to extract.
- If the element can't be found, `None` is returned.
- If the element can be found, then we'll use the `.text` property on our
  element object to grab the data out of the desired XML element.

All in all, not so bad!

The next time you're looking to quickly extract some data out of an XML
document, give it a try!

Got a better method?  [Drop me a line][].


  [Broken Demon Sketch]: /static/images/2013/broken-demon-sketch.png "Broken Demon Sketch"
  [written]: {filename}/articles/2010/basic-xml-parsing-with-python-and-lxml.md "Basic XML Parsing With Python and LXML"
  [lxml]: http://lxml.de/ "Python LXML"
  [xml.etree]: http://docs.python.org/2/library/xml.etree.elementtree.html "Python xml.etree"
  [XPath selector]: http://docs.python.org/2/library/xml.etree.elementtree.html#elementtree-xpath "XPath Selector"
  [Drop me a line]: mailto:r@rdegges.com "Randall Degges' Email"
