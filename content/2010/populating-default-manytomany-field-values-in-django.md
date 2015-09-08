---
title: "Populating Default ManyToMany Field Values in Django"
date: "2010-06-25"
tags: ["programming", "python", "django"]
slug: "populating-default-manytomany-field-values-in-django"
description: "A quick article discussing how populate ManyToManyField default values for Django applications."
---


![Pony Sketch][]


At work, I'm the lead developer of a rather large, complex web application
which interacts with many different technologies ([Asterisk][], [Freeswitch][],
Cisco routers, [Python][], XML-RPC, [JSON][], [Django][]--to name a few).  A
few days ago, while implementing a ban system, I bumped into an interesting
problem that was not trivial to find a solution to.  So, here it is :)


## Background

The web application I'm developing is a private portal which allows users to
manage teleconference lines real time.  Since all of our telephony services are
free of charge, we often get callers onto certain teleconference lines who want
to abuse services (think of those trolls on the internet, except over the
phone).  As you can probably imagine, without strict regulation & technology in
place, telephone trolls could cause huge problems for normal users.

To combat this, I wrote a relatively simple ban system which allows web admins
to remove abusive callers from specific teleconference lines.  Each
teleconference line is represented by a Django model class, which looks
something like:

```python
class Teleconference(models.Model):

    name = models.CharField('Teleconference name.', max_length=50)
    did = PhoneNumberField('Teleconference phone number.', unique=True)
    owner = models.ForeignKey(User)
    bans = models.ManyToManyField(Caller, blank=True, null=True)

    def __unicode__(self):
        return '%s:%s' % (self.name, self.did)
```

The newly added `bans` field stores a list of `Caller` objects which map to
individual callers, and allow the web users to ban specific callers if they're
causing trouble.


## Problem

The problem came up when I was trying to finish the view which allows web
admins to select which callers they want to ban.

The view code (originally) looked something like:

```python
def edit_teleconference(request, id=None):
    teleconference = get_object_or_404(Teleconference, id=id)

    if request.method == 'POST':
        form = TeleconferenceForm(request.POST, instance=teleconference)
        if form.is_valid():
            if 'name' in form.cleaned_data:
                teleconference.name = form.cleaned_data['name']
            if 'did' in form.cleaned_data:
                teleconference.did = form.cleaned_data['did']
            if 'owner' in form.cleaned_data:
                teleconference.owner = form.cleaned_data['owner']
            if 'bans' in form.cleaned_data:
                teleconference.bans = form.cleaned_data['bans']

            teleconference.save()
    else:
        defaults = {
            'name': teleconference.name,
            'did': teleconference.did,
            'owner': teleconference.owner.id
        }
        if teleconference.bans:
            defaults['bans'] = teleconference.bans.id

        form = TeleconferenceForm(request.POST, instance=teleconference)

    variables = RequestContext(request, {'form': form})
    return render_to_response('portal/teleconf/edit.html', variables)
```

The problem in the code above resides on line 24.  Attempting to populate the
default values for a ManyToMany field using the `id` attribute does not work.

After a bit of playing around, I was unable to find a solution, so I checked
Google.  After ~20 minutes of Google, I was still stuck with the same problem.


## Solution

To resolve the issue, and successfully populate the default `bans` field
values, I had to do:

```python
def edit_teleconference(request, id=None):
    teleconference = get_object_or_404(Teleconference, id=id)

    if request.method == 'POST':
        form = TeleconferenceForm(request.POST, instance=teleconference)
        if form.is_valid():
            if 'name' in form.cleaned_data:
                teleconference.name = form.cleaned_data['name']
            if 'did' in form.cleaned_data:
                teleconference.did = form.cleaned_data['did']
            if 'owner' in form.cleaned_data:
                teleconference.owner = form.cleaned_data['owner']
            if 'bans' in form.cleaned_data:
                teleconference.bans = form.cleaned_data['bans']

            teleconference.save()
    else:
        defaults = {
            'name': teleconference.name,
            'did': teleconference.did,
            'owner': teleconference.owner.id
        }
        if teleconference.bans:
            defaults['bans'] = [t.pk for t in teleconference.bans.all()]

        form = TeleconferenceForm(request.POST, instance=teleconference)

    variables = RequestContext(request, {'form': form})
    return render_to_response('portal/teleconf/edit.html', variables)
```

Which basically passes a list of `Caller` `id` attributes to the form.  While
this now seems an intuitive solution to me, I had a great deal of trouble
initially figuring it out.

The way that form defaults work for `ForeignKey` and `ManyToMany` fields is
that they take in either a model's `id` attribute for `ForeignKey`s, or a list
of model `id`s for `ManyToMany` fields.


## Conclusion

Populating Django `ManyToMany` field default values can be a bit confusing, and
somewhat undocumented.  Hopefully the code presented above helps clarify how to
do it properly, and why it works the way it does.


  [Pony Sketch]: /static/images/2010/pony-sketch.png "Pony Sketch"
  [Asterisk]: http://www.asterisk.org/ "Asterisk"
  [Freeswitch]: http://freeswitch.org/ "Freeswitch"
  [Python]: http://python.org/ "Python"
  [JSON]: http://json.org/ "JSON"
  [Django]: https://www.djangoproject.com/ "Django"
