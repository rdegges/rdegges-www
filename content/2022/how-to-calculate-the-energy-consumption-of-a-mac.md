---
aliases:
  - "/how-to-calculate-the-energy-consumption-of-a-mac/"
date: "2022-01-30"
description: "A look at the various ways to track the energy consumption of a Mac."
slug: "how-to-calculate-the-energy-consumption-of-a-mac"
tags:
  - "programming"
title: "How to Calculate the Energy Consumption of a Mac"
---


![Macbook Sketch][]

I'm a bit of a sustainability nerd. I love the idea of living a life where your carbon footprint is neutral (or negative) and you leave the world a better place than it was before you got here. 

While it's clear that there's only [so much impact](https://www.epa.gov/ghgemissions/sources-greenhouse-gas-emissions) an individual can have on carbon emissions, I like the idea of working to minimize my personal carbon footprint. This is a big part of the reason why I live in a home with solar power, drive an electric vehicle, and try to avoid single-use plastics as much as possible.

During a recent impact-focused hackathon at [work](https://snyk.io) ([come work with me!](https://snyk.io/careers/)), I found myself working on an interesting sustainability project. Our team's idea was simple: because almost all Snyk employees work remotely using a Mac laptop, could we measure the energy consumption of every employee's Mac laptop to better understand how much energy it takes to power employee devices, as well as the amount of carbon work devices produce?

Because we know (on average) [how much carbon](https://www.eia.gov/tools/faqs/faq.php?id=74&t=11) it takes to produce a single kilowatt-hour (kWh) of electricity in the US (0.85 pounds of CO2 emissions per kWh), if we could figure out how many kWh of electricity were being used by employee devices, we'd be able to do some simple math and figure out two things:

1. How much energy is required to power employee devices
2. How much carbon is being put into the atmosphere by employee devices

Using this data, we could then donate money to a [carbon offsetting service](https://www.investopedia.com/best-carbon-offset-programs-5114611) to "neutralize" the impact of our employee's work devices.

**PROBLEM**: Now, would this be a perfectly accurate way of measuring the true carbon impact of employees? Absolutely not -- there are obviously many things we cannot easily measure (such as the amount of energy of attached devices, work travel, food consumption, etc.), but the idea of being able to quantify the carbon impact of work laptops was still interesting enough that we decided to pursue it regardless.


## Potential Energy Tracking Solutions

The first idea we had was to use smart energy monitoring plugs that employees could plug their work devices into while charging. These plugs could then store a tally of how much energy work devices consume, and we could aggregate that somewhere to get a total amount of energy usage.

I happen to have several of the [Eve Energy](https://www.evehome.com/en/eve-energy) smart plugs around my house (which I highly recommend if you use Apple's HomeKit) that I've been using to track my personal energy usage for a while now.

![Eve Energy Screenshot][]

While these devices are incredible (they work well, come with a beautiful app, etc.), unfortunately, they don't have any sort of publicly accessible API you can use to extract energy consumption data.

We also looked into various other types of smart home energy monitoring plugs, including the [Kasa Smart Plug Mini](https://amzn.to/341CXQt), which does happen to have [an API](https://github.com/python-kasa/python-kasa).

Unfortunately, however, because Snyk is a global company with employees all over the world, hardware solutions were looking less and less appealing as to do what we wanted, we'd need to:

- Ship country-specific devices to each new and existing employee
- Include setup instructions for employees (how to configure the plugs, how to hook them up to a home network, etc.)
- Instruct employees to always plug their work devices into these smart plugs, which many people may forget to do


## Is It Possible to Track Mac Energy Consumption Using Software?

When [someone on the team](https://www.linkedin.com/in/seanmclarke/) proposed using software to track energy consumption, I thought it'd be a simple task. I assumed there were various existing tools we could easily leverage to grab energy consumption data. But boy, oh boy, I was wrong!

As it turns out, it's quite complicated to figure out how many watt-hours of electricity your Mac laptop is using. To the best of my knowledge, there are no off-the-shelf applications that do this.

Through my research, however, I stumbled across a couple potential solutions.


### Using Battery Metrics to Calculate Energy Consumption

The first idea I had was to figure out the size of the laptop's battery (in milliamp-hours (mAh)), as well as how many complete discharge cycles the battery has been through (how many times has the battery been fully charged and discharged).

This information would theoretically allow us to determine how much energy a Mac laptop has ever consumed by multiplying the size of the battery in mAh by the number of battery cycles. We could then simply convert the number of mAh -> kWh using a simple formula.

After a lot of Google-fu and command-line scripting, I was able to get this information using the [ioreg command-line tool](https://developer.apple.com/library/archive/documentation/DeviceDrivers/Conceptual/IOKitFundamentals/TheRegistry/TheRegistry.html), but in the process, I realized that there was a critical problem with this approach.

The problem is that while the variables I mentioned above will allow you to calculate the energy consumption of your laptop over time, when your laptop is fully charged *and* plugged into a wall outlet it isn't drawing down energy from the battery -- it's using the electricity directly from your wall.

This means that the measuring approach above will only work if you *never* use your laptop while it is plugged into wall chargers -- you'd essentially need to keep your laptop shut down while charging and only have it turned on while on battery power. Obviously, this is not very realistic.


### Using Wall Adapter Information to Calculate Energy Consumption

After the disappointing battery research, I decided to take a different approach. What if there was a way to extract how much energy your laptop was pulling from a wall adapter?

If we were able to figure out how many watts of electricity, for example, your laptop was currently drawing from a wall adapter, we could track this information over time to determine the amount of watt-hours of electricity being consumed. We could then easily convert this number to kWh or any other desired measure.

And… After a lot of sifting through `ioreg` output and some help from [my little brother](https://www.linkedin.com/in/jdegges/) (an engineer who helps build [smart home electric panels](https://www.span.io)), I was able to successfully extract the amount of watts being pulled from a plugged-in wall adapter! Woo!


## The Final Solution: How to Calculate the Energy Consumption of Your Mac Using Software

After many hours of research and playing around, what I ended up building was a small shell script that parses through `ioreg` command-line output and extracts the amount of watts being pulled from a plugged-in wall adapter.

This shell script runs on a cron job once a minute, logging energy consumption information to a file. This file can then be analyzed to compute the amount of energy consumed by a Mac device over a given time period.

I've packaged this solution up into a small GitHub project you can check out [here](https://github.com/rdegges/energy-tracker).

The command I'm using to grab the wattage information is the following:

```console
/usr/sbin/ioreg -rw0 -c AppleSmartBattery | grep BatteryData | grep -o '"AdapterPower"=[0-9]*' | cut -c 16- | xargs -I %  lldb --batch -o "print/f %" | grep -o '$0 = [0-9.]*' | cut -c 6-
```

Here it is broken down with a brief description of what these commands are doing:

```console
/usr/sbin/ioreg -rw0 -c AppleSmartBattery | \  # retrieve power data
  grep BatteryData | \                         # filter it down to battery stats
  grep -o '"AdapterPower"=[0-9]*' | \          # extract adapter power info
  cut -c 16- | \                               # extract power info number
  xargs -I %  lldb --batch -o "print/f %" | \  # convert power info into an IEEE 754 float
  grep -o '$0 = [0-9.]*' | \                   # extract only the numbers
  cut -c 6-                                    # remove the formatting
```

The output of this command is a number which is the amount of watts currently being consumed by your laptop (I verified this by confirming it with hardware energy monitors). In order to turn this value into a usable energy consumption metric, you have to sample it over time. After thinking this through, here was the logging format I came up with to make tracking energy consumption simple:

```text
timestamp=YYYY-MM-DDTHH:MM:SSZ wattage=<num> wattHours=<num> uuid=<string> 
```

This format allows you to see:

- The timestamp of the log
- The amount of watts being drawn from the wall at the time of measurement (wattage)
- The number of watt hours consumed at the time of measurement (wattHours), assuming this measurement is taken once a minute, and
- The unique Mac UUID for this device. This is logged to help with deduplication and other statistics in my case.

Here's an example of what some real-world log entries look like:

```text
timestamp=2022-01-30T23:41:00Z wattage=8.37764739 wattHours=.13962745650000000000 uuid=EDD819A5-1409-5797-9BE4-22EAAC75D999
timestamp=2022-01-30T23:42:01Z wattage=8.7869072 wattHours=.14644845333333333333 uuid=EDD819A5-1409-5797-9BE4-22EAAC75D999
timestamp=2022-01-30T23:43:00Z wattage=9.16559505 wattHours=.15275991750000000000 uuid=EDD819A5-1409-5797-9BE4-22EAAC75D999
timestamp=2022-01-30T23:44:00Z wattage=8.49206352 wattHours=.14153439200000000000 uuid=EDD819A5-1409-5797-9BE4-22EAAC75D999
timestamp=2022-01-30T23:45:00Z wattage=7.45262718 wattHours=.12421045300000000000 uuid=EDD819A5-1409-5797-9BE4-22EAAC75D999
```

To sum up the amount of energy consumption over time, you can then parse this log file and sum up the `wattHours` column over a given time period. Also, please note that the script I wrote will NOT log energy consumption data to the file if there is no energy being consumed (aka, your laptop is not plugged into a wall adapter).

**PROBLEMS**: While this is the final solution we ended up going with, it still has one fatal flaw: this approach only works if the script is ran once a minute. This means that if your laptop is shut down or sleeping and this code is not running, there will be no way to log energy consumption data.


## What I Learned About Tracking Energy Consumption on Macs

While building our short sustainability-focused hackathon project, I learned a lot about tracking energy consumption on Macs.

1. Your laptop doesn't always use its battery as a power source, so tracking battery metrics is not an ideal solution
2. It's possible to track energy consumption by measuring the draw from wall adapters, although this approach isn't perfect as it requires your computer to be on and running code on a regular interval
3. While using hardware energy trackers isn't convenient in our case, this is certainly the simplest (and probably the best) option for personal energy tracking

If you'd like to see the software-based energy tracking solution I built, please [check it out on GitHub](https://github.com/rdegges/energy-tracker).

I'm currently in the process of following up with Snyk's IT department to see if this is something we could one day roll out automatically to employee devices. I still think it would be incredibly interesting to see a central dashboard of how much energy Snyk employees are using to "power" their work, and what that amount of carbon looks like.

**PS**: The creation of this blog post took precisely `19.972951810666647` watt-hours of electricity and generated `.016977009039067` pounds of CO2.


  [Macbook Sketch]: /static/images/2022/macbook-sketch.png "Macbook Sketch"
  [Eve Energy Screenshot]: /static/images/2022/eve-energy-screenshot.png "Eve Energy Screenshot"
