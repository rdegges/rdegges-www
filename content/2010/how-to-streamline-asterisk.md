---
title: "How to Streamline Asterisk"
date: "2010-08-16"
tags: ["programming", "telephony", "asterisk"]
slug: "how-to-streamline-asterisk"
description: "This article walks users through optimizing their Asterisk systems for maximum performance."
---


![Scuba Diving Sketch][]


So, you use [Asterisk][] professionally, for fun, or both, and you want to know
how to optimize the shit out of your Asterisk platform?  No problem, I've got
you covered.

Grab a beer, free up the next 2 hours of your time, and let's get to it!


## Why Do This?

**To speed up your Asterisk platform.**  Asterisk is a large and complex PBX
system with hundreds of features, commands, and various components.  Each
component that is in use adds additional overhead to your Asterisk system in
the form of RAM, CPU, and sometimes disk space.

To make your Asterisk PBX perform at its best, it is useful to strip out
everything you don't need, and force your Asterisk system to perform its best.


## Preparation

To make this quick, you should already have a box with Asterisk up and running,
ideally with some working call routing code of some sort.  If you manage an
Asterisk server at work, that will do just fine.

**WARNING**: Don't attempt this stuff live on production servers unless you
really like abuse.


## Approach

The approach I like to take with my Asterisk slimming, streamlining, or
whatever you want to call it, is to install Asterisk initially with as many
features as possible, disable everything, then selectively enable the features
I need, one at a time.

This is called a *whitelisting* approach, as you block everything by default,
and then manually allow only certain features (think network security).

This method requires more effort to setup and maintain, but leads to the best
possible performance.


## Install Asterisk

If you are familiar with Asterisk installation, you can go ahead and skip to
the next section.  Good work, smart guy!

If you've never installed Asterisk before, read [my guide][].

If you installed Asterisk from your OS's package manager (`yum`, `apt`, etc.),
then you can also skip this section.

So, I guess you installed Asterisk from source.  Nice.  That's the best way
(but you already know that).  Anyway, as I mentioned in the previous section, I
like to install Asterisk with as many features enabled as possible.  This way,
if I ever need to get some extra functionality, I can simply enable it, and not
have to completely re-install Asterisk from source.

If you aren't sure of how to selectively choose which features are installed
when you are compiling Asterisk, all you have to do is run `make menuselect` in
the Asterisk source directory (this also applies to `asterisk-addons`), after
running `./configure`, but before running `make`.

While installing Asterisk, you might run the following commands:

```console
$ cd asterisk-latest
$ ./configure
$ make menuselect
$ make
$ sudo make install
```

When you run `make menuselect`, you'll see an `ncurses` based GUI window, that
lets you use the arrow keys, enter, and tab to navigate around and choose which
components to install.  You should choose as many as possible.


## Figure Out Which Features You're Using

This step is **important**.  You need to figure out what parts of Asterisk you
**need** in order to do what you're doing before you can even think about
removing unnecessary junk.

Here are some helpful tips for figuring out what parts of Asterisk you need:

-   Read [this page][] on [voip-info][].  It has a pretty good list of module
    and configuration file dependencies.

-   Look at all of your code in `extensions.conf`, and write down all of the
    application names you use.  This would be stuff like `Plaback`, `Monitor`,
    etc.

-   Which sort of protocols does your system support?  SIP?  IAX?  DAHDI?
    ZAPTEL?

-   What sort of call codecs do you support?  ULAW, G729, etc.?

-   Which configuration files have you explicitly put code into?
    `indications.conf`?  `smdi.conf`?  etc.?

I suggest writing these all down somewhere.  It's not critical to have *all* of
them perfectly figured out at the start, you can always figure it out later via
trial-and-error.


## Get a List of All Modules

We now need to get a list of all the Asterisk modules that are currently
available on your system.  If you compiled Asterisk from scratch, and read my
*Installing Asterisk* section, you should have a ton.

On most Linux systems, you can get a list of all your Asterisk modules by
running the following command: `ls /usr/lib/asterisk/modules/`.  This *may* be
different for you, depending on what operating system you're using.


## Disable Everything

Before enabling the modules we need, we're going to disable everything.  This
is part of our *whitelisting* approach to Asterisk slimming.

To do this, open up your `modules.conf` file (usually located in
`/etc/asterisk/`).  Your file should look something like:

```ini
;
; Asterisk configuration file
;
; Module Loader configuration file
;

[modules]
autoload=yes
;
; Any modules that need to be loaded before the Asterisk core has been
; initialized (just after the logger has been initialized) can be loaded
; using 'preload'. This will frequently be needed if you wish to map all
; module configuration files into Realtime storage, since the Realtime
; driver will need to be loaded before the modules using those
; configuration files are initialized.
;
; An example of loading ODBC support would be:
;preload => res_odbc.so
;preload => res_config_odbc.so
;
; res_phoneprov requires func_strings.so to be loaded:
preload => func_strings.so
;
; Uncomment the following if you wish to use the Speech Recognition API
;preload => res_speech.so
;
; If you want, load the GTK console right away.
;
noload => pbx_gtkconsole.so
;load => pbx_gtkconsole.so
;
load => res_musiconhold.so
;
; Load one of: chan_oss, alsa, or console (portaudio).
; By default, load chan_oss only (automatically).
;
noload => chan_alsa.so
;noload => chan_oss.so
noload => chan_console.so
;
```

Change the line that says `autoload=yes` to `autoload=no`.  This will
**prevent** Asterisk from automatically loading modules.

The next thing you need to do is `preload` any required modules.  As shown in
the sample config above, if you need `odbc` support, you should put
`preload => res_odbc.so` directly below your `autoload=yes` line.

After you've gotten all the `preload`s finished, **delete everything else** in
the file.  Seriously.  You won't need it anymore :)


## Enable Only What You Need

You should still be in your `modules.conf` file.  Now, remember before when you
got a list of all the Asterisk modules available on your system
(`ls /usr/lib/asterisk/modules/`)?  Do the following:

Below all of your `preload` lines in `modules.conf`, insert
`load => module_name.so` for each module that starts with `res_`, e.g.

```ini
;load => res_adsi.so
;load => res_agi.so
;load => res_clioriginate.so
;load => res_config_curl.so
;load => res_convert.so
;load => res_curl.so
;load => res_crypto.so
;load => res_indications.so
;load => res_limit.so
;load => res_monitor.so
;load => res_musiconhold.so
;load => res_phoneprov.so
;load => res_smdi.so
;load => res_timing_dahdi.so
;load => res_timing_pthread.so
```

Wondering why you need to do all of the modules with `res` first?  Because
these modules are special, they are `resources`.  Resource modules need to be
loaded before any other modules as they often satisfy dependency issues.

Now, feel free to insert `load => module_name.so` lines for your remaining
modules that don't start with `res_`, e.g.

```ini
;load => app_addon_sql_mysql.so
;load => app_adsiprog.so
;load => app_alarmreceiver.so
;load => app_amd.so
;load => app_authenticate.so
;load => app_cdr.so
;load => app_chanisavail.so
;load => app_channelredirect.so
;load => app_chanspy.so
;load => app_controlplayback.so
;load => app_dahdibarge.so
;load => app_dahdiras.so
;load => app_dahdiscan.so
;load => app_db.so
;load => app_dial.so
;load => app_dictate.so
;load => app_directed_pickup.so
;load => app_directory.so
;load => app_disa.so
;load => app_dumpchan.so
;load => app_echo.so
;load => app_exec.so
;load => app_externalivr.so
;load => app_festival.so
;load => app_flash.so
;load => app_followme.so
;load => app_forkcdr.so
;load => app_getcpeid.so
;load => app_ices.so
;load => app_image.so
;load => app_macro.so
;load => app_meetme.so
;load => app_milliwatt.so
;load => app_minivm.so
;load => app_mixmonitor.so
;load => app_morsecode.so
;load => app_mp3.so
;load => app_nbscat.so
;load => app_page.so
;load => app_parkandannounce.so
;load => app_playback.so
;load => app_privacy.so
;load => app_queue.so
;load => app_read.so
;load => app_readexten.so
;load => app_readfile.so
;load => app_record.so
;load => app_saycountpl.so
;load => app_sayunixtime.so
;load => app_senddtmf.so
;load => app_sendtext.so
;load => app_setcallerid.so
;load => app_sms.so
;load => app_softhangup.so
;load => app_speech_utils.so
;load => app_stack.so
;load => app_system.so
;load => app_talkdetect.so
;load => app_test.so
;load => app_transfer.so
;load => app_url.so
;load => app_userevent.so
;load => app_verbose.so
;load => app_voicemail.so
;load => app_waitforring.so
;load => app_waitforsilence.so
;load => app_while.so
;load => app_zapateller.so

;load => cdr_addon_mysql.so

;load => chan_agent.so
;load => chan_dahdi.so
;load => chan_iax2.so
;load => chan_local.so
;load => chan_mgcp.so
;load => chan_ooh323.so
;load => chan_oss.so
;load => chan_phone.so
;load => chan_sip.so
;load => codec_adpcm.so
;load => codec_alaw.so
;load => codec_dahdi.so
;load => codec_g726.so
;load => codec_gsm.so
;load => codec_lpc10.so
;load => codec_ulaw.so

;load => format_g723.so
;load => format_g726.so
;load => format_g729.so
;load => format_gsm.so
;load => format_h263.so
;load => format_h264.so
;load => format_jpeg.so
;load => format_mp3.so
;load => format_pcm.so
;load => format_sln.so
;load => format_sln16.so
;load => format_vox.so
;load => format_wav.so
;load => format_wav_gsm.so

;load => func_audiohookinherit.so
;load => func_base64.so
;load => func_blacklist.so
;load => func_callerid.so
;load => func_cdr.so
;load => func_channel.so
;load => func_curl.so
;load => func_cut.so
;load => func_db.so
;load => func_enum.so
;load => func_env.so
;load => func_extstate.so
;load => func_global.so
;load => func_groupcount.so
;load => func_iconv.so
;load => func_lock.so
;load => func_logic.so
;load => func_math.so
;load => func_md5.so

;load => func_module.so
;load => func_rand.so
;load => func_realtime.so
;load => func_sha1.so
;load => func_shell.so
;load => func_strings.so
;load => func_sysinfo.so
;load => func_timeout.so
;load => func_uri.so
;load => func_version.so
;load => func_vmcount.so
;load => func_volume.so

;load => pbx_config.so
;load => pbx_loopback.so
;load => pbx_spool.so
```

Now, go through the list of modules you have in your `modules.conf`, and
uncomment the ones that you absolutely can't live without.

I realize that the above steps aren't exactly super descriptive, so keep
reading.  The next section will give you some additional pointers.


## Tips for Slimming

At some point during this article, you've probably thought to yourself, *How do
I know which modules are absolutely essential to my setup?*.

If you aren't able to figure it out, there's one foolproof way to figure it
out: trial-and-error.

Don't feel bad about doing trial-and-error here either, Asterisk can be
complex.

1.  Configure your `logger.conf` to output with maximum verbosity to the full
    logfile.  Your `logger.conf` file should have a line that looks like:
    `full => notice,warning,error,debug,verbose`.

2.  Try to restart Asterisk: `/etc/init.d/asterisk restart`.  Then check your
    full logfile: `tail /var/log/asterisk/full`, and look for lines that
    contain **WARNING** or **ERROR**.  Asterisk provides great error messages.
    So if you aren't loading a necessary module, it will tell you.

3.  Load the modules you were missing, and go back to step 1.

You know you're done when you've gone through every single module on your
system, and know exactly which ones you need to have enabled to make your
system run.


## Results

Streamlining your Asterisk installs has great benefits.  Not only will your
system run much faster, and more efficiently than before, but you'll also know
a lot more about Asterisk, how it works, and how to modify its behavior.

One of the great strengths of Asterisk is its module system, which is extremely
dynamic and provides a great interface for developers to add functionality.

Got any questions? Feel free to [shoot me an email][], I'd be happy to help.


  [Scuba Diving Sketch]: /static/images/2010/scuba-diving-sketch.png "Scuba Diving Sketch"
  [Asterisk]: http://www.asterisk.org/ "Asterisk"
  [my guide]: {filename}/articles/2010/transparent-telephony-part-2-installing-asterisk.md "Transparent Telephony - Part 2 - Installing Asterisk"
  [this page]: http://www.voip-info.org/wiki/view/Asterisk+Slimming "Asterisk Slimming Wiki Page"
  [voip-info]: http://www.voip-info.org/ "VoIP Info Wiki"
  [shoot me an email]: mailto:r@rdegges.com "Randall Degges' Email"
