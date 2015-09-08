---
title: "Auto Generate Forms with Django's ModelForm"
date: "2010-03-12"
tags: ["programming", "python", "django"]
slug: "auto-generate-forms-with-djangos-modelform"
description: "Django's ModelForm class is pretty useful.  Here we'll take a quick look at using ModelForm appropriately."
---


![Mannequin Sketch][]


In this short article, we'll analyze a better way (in some cases) to create
forms for your Django models.

If you've ever worked with Django forms, then you know that there is a lot of
repetitive code involved in the process of writing a form to create your model.
Take, for instance, the following model, which represents a physical server
(somewhere):

```python
from django.db import models

class Server(models.Model):
    """This class represents a physical server."""
    hostname = models.CharField('Server Name',
        help_text = 'Hostname of the server.',
        max_length = 50
    )
    ip = models.IPAddressField('Server IP Address',
        help_text = 'Public IP of the server.',
        unique = True
    )
    disk_space = models.IntegerField('Disk Space on Server',
        help_text = 'Total disk space in MB.'
    )
    ram = models.IntegerField('RAM on Server',
        help_text = 'Total RAM in MB.'
    )
    cpu = models.IntegerField('Processing Power',
        help_text = 'Total Processing Power in MHz.'
    )

    def __unicode__(self):
        """Make the model human readable."""
        return self.hostname
```

Our `Server` model contains several attributes which define a `Server` object.

If you want to create a `Server` object, you can generate a form class which
can be used to create a new `Server` model and store it in the database.  This
isn't very difficult, but is a bit repetitive.  Here's how you would generate a
form to create a new `Server` model using Django's forms:

```python
from django import forms

class CreateServerForm(forms.Form):
    """Create a new Server model."""
    hostname = forms.CharField(
        label = 'Server Name',
        max_length = 50,
        required = False
    )
    ip = forms.IPAddressField )
        label = 'Public IP',
        required = False
    )
    disk_space = forms.IntegerField(
        label = 'Disk Space in MB',
        required = False
    )
    ram = forms.IntegerField(
        label = 'RAM in MB',
        required = False
    )
    cpu = forms.IntegerField(
        label = 'CPU in MHz',
        required = False
    )
```

As you can see, there's a lot of repetitive code in there.  This is great when
you need maximum control of your forms, but is overkill if you're just trying
to build a simple view to create an instance of your model class.

What if there was a way to auto-generate a form class without re-writing all of
that code?  Well, there is!  Django's `ModelForm` class allows you to create a
very simple `ModelForm` without ever touching form code.

Here's our `models.py` code re-written using `ModelForm`:

```python
from django.db import models
from django.forms import ModelForm

class Server(models.Model):
    """This class represents a physical server."""
    hostname = models.CharField('Server Name',
        help_text = 'Hostname of the server.',
        max_length = 50
    )
    ip = models.IPAddressField('Server IP Address',
        help_text = 'Public IP of the server.',
        unique = True
    )
    disk_space = models.IntegerField('Disk Space on Server',
        help_text = 'Total disk space in MB.'
    )
    ram = models.IntegerField('RAM on Server',
        help_text = 'Total RAM in MB.'
    )
    cpu = models.IntegerField('Processing Power',
        help_text = 'Total Processing Power in MHz.'
    )

    def __unicode__(self):
        """Make the model human readable."""
        return self.hostname

class ServerForm(ModelForm):
    """Auto generated form to create Server models."""
    class Meta:
        model = Server
```

Look how much simpler that is!  Instead of writing a `forms.py` file, and
manually creating a form, we just use `ModelForm` to specify a model class that
Django should magically create a form from.

Lastly, let's see how we can use this new `ModelForm` class in an actual view.
It's easy, I promise:

```python
from myapp.models import Server
from myapp.models import ServerForm

from django.template import RequestContext
from django.shortcuts import render_to_response

def create_server(request):
    """Create a new Server model."""
    if request.method == 'POST':
        form = ServerForm(request.POST)
        if form.is_valid():

            # Create a new Server object.
            form.save()
    else:
        form = ServerForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('path/to/template/create.html', variables)
```

See how easy that is?  In only a few lines, we were able to auto-generate a
form from our model class, and then write a simple view which creates a new
`Server` model by using the auto-generated form.

If you're interested in Django's `ModelForm`, read the
[official documentation][], it will answer all of your more in-depth questions.


  [Mannequin Sketch]: /static/images/2010/mannequin-sketch.png "Mannequin Sketch"
  [official documentation]: https://docs.djangoproject.com/en/dev/topics/forms/modelforms/ "Django ModelForms"
