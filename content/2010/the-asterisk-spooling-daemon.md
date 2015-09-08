---
title: "The Asterisk Spooling Daemon"
date: "2010-06-06"
tags: ["programming", "telephony", "asterisk", "c"]
slug: "the-asterisk-spooling-daemon"
description: "An informal code review and look at the Asterisk call file daemon (pbx_spool.so)."
---


![Daemon Sketch][]


While working on the new V2 release of [pycall][], I was doing some research on
the internal limitations of [Asterisk call files][], and thought I'd share some
interesting (technical) bits of information here.

All information below has been gathered from the [latest Asterisk release][]
(`v1.6.2.7`).  If you don't do any programming, you may want to skip this
article, as it is a bit geeky.


## Brief Overview of Call File Code

First of all, it is important to note that Asterisk call files only work when
the Asterisk module `pbx_spool.so` is loaded.

The `pbx_spool.so` module (the Asterisk spooling daemon), is a process which
runs and analyzes the Asterisk spooling directory (usually
`/var/spool/asterisk/outgoing/`) for new call files.  If a call file is found,
then the spooling daemon will process the call file (extracting the
directives), then executing the actions specified.

So, since we now know how the spooling daemon works, let's take a look at the
source code (in C), and figure out what actually goes on.

First of all, download the Asterisk source code if you want to follow along:
[asterisk v1.6.2.7 (tarball)][].  Once you extract the code, open up the file
`asterisk-1.6.2.7/pbx/pbx_spool.c` in your [favorite editor][].  This file
contains all of the Asterisk code used to parse, launch, and control call
files.

The first thing you'll notice (being a sensitive best-practices programmer!) is
that there are a *ton* of magic numbers being thrown around in here.  But let's
just ignore that for now (I'm sure the Asterisk guys are working on it) :)

The two sections of the code which we're going to look at today are the
`outgoing` struct, and the `apply_outgoing` function.  These contain the bulk
of the call file logic, and will help us learn a bit about call file internals.

Look them over briefly.  In the next section, we'll dive right in.


## The outgoing Struct

Let's start out by analyzing the `outgoing` struct, shown below (note: I've
re-done the formatting and comments so that it displays in proper 80-column
width):

```c
struct outgoing {
    int retries;        // current number of retries
    int maxretries;     // maximum number of retries permitted
    int retrytime;      // how long to wait between retries (in seconds)
    int waittime;       // how long to wait for an answer
    long callingpid;    // PID which is currently calling
    int format;         // formats (codecs) for this call

    AST_DECLARE_STRING_FIELDS (
        AST_STRING_FIELD(fn);       // file name of the call file
        AST_STRING_FIELD(tech);     // which channel technology to use for
                                    // outgoing call
        AST_STRING_FIELD(dest);     // which line to use for outgoing
                                    // call
        AST_STRING_FIELD(app);      // if application: Application name
        AST_STRING_FIELD(data);     // if application: Application data
        AST_STRING_FIELD(exten);    // if extension/context/priority:
                                    // extension in dialplan
        AST_STRING_FIELD(context);  // if extension/context/priority:
                                    // dialplan context
        AST_STRING_FIELD(cid_num);  // callerID information: number
        AST_STRING_FIELD(cid_name); // callerID information: name
        AST_STRING_FIELD(account);  // account code
    );

    int priority;               // if extension/context/priority: priority
    struct ast_variable *vars;  // variables and functions
    int maxlen;                 // maximum length of call
    struct ast_flags options;   // options
};
```

This struct holds the directives specified in each call file that the spooling
daemon reads.  This means that if your call file looks like:

```
Channel: Local/18002223333@from-internal
Application: Playback
Data: hello-world
```

Then the struct will set: `tech = "Local"`,
`dest = "18002223333@from-internal"`, `app = "Playback"`, and
`data = "hello-world"`.

Internally, Asterisk uses this struct throughout the `pbx_spool.c` module, as a
way to store individual call file states and track statuses.


## How The Spooling Daemon Works

Now, when users create a call file, the spooling daemon will process that file.
But how does it do it?  Now that we've seen `struct outgoing`, let's look at
the `apply_outgoing` function which parses call files, and populates an
`outgoing` struct while verifying that all lines are syntactically correct.

This will give us insight into which directives are allowed in call files (and
which variations raise errors).

Here is the `apply_outgoing` function cleaned up for clarity:


```c
static int apply_outgoing(struct outgoing *o, char *fn, FILE *f) {
    /*
     * Parse the `outgoing` struct, clean up any lingering whitespace, and
     * verify that all directives are syntactically correct. Logs errors as
     * it finds them.
     */

    char buf[256];
    char *c, *c2;
    int lineno = 0;
    struct ast_variable *var, *last = o->vars;

    while (last && last->next) {
        last = last->next;
    }

    while(fgets(buf, sizeof(buf), f)) {
        lineno++;

        // Trim comments.
        c = buf;
        while ((c = strchr(c, '#'))) {
            if ((c == buf) || (*(c-1) == ' ') || (*(c-1) == '\t'))
                *c = '\0';
            else
                c++;
        }

        c = buf;
        while ((c = strchr(c, ';'))) {
            if ((c > buf) && (c[-1] == '\\')) {
                memmove(c - 1, c, strlen(c) + 1);
                c++;
            } else {
                *c = '\0';
                break;
            }
        }

        // Trim trailing white space.
        while(!ast_strlen_zero(buf) && buf[strlen(buf) - 1] < 33)
            buf[strlen(buf) - 1] = '\0';

        if (!ast_strlen_zero(buf)) {

            // Split the directive into two parts. Command and value.
            c = strchr(buf, ':');
            if (c) {
                *c = '\0';
                c++;
                while ((*c) && (*c < 33))
                    c++;

#if 0
                printf("'%s' is '%s' at line %d\n", buf, c, lineno);
#endif

                // Analyze the command, and populate the outgoing struct.
                if (!strcasecmp(buf, "channel")) {
                    if ((c2 = strchr(c, '/'))) {
                        *c2 = '\0';
                        c2++;
                        ast_string_field_set(o, tech, c);
                        ast_string_field_set(o, dest, c2);
                    } else {
                        ast_log(LOG_NOTICE, "Channel should be in form "
                            "Tech/Dest at line %d of %s\n", lineno, fn);
                    }
                } else if (!strcasecmp(buf, "callerid")) {
                    char cid_name[80] = {0}, cid_num[80] = {0};
                    ast_callerid_split(c, cid_name, sizeof(cid_name),
                        cid_num, sizeof(cid_num));
                    ast_string_field_set(o, cid_num, cid_num);
                    ast_string_field_set(o, cid_name, cid_name);
                } else if (!strcasecmp(buf, "application")) {
                    ast_string_field_set(o, app, c);
                } else if (!strcasecmp(buf, "data")) {
                    ast_string_field_set(o, data, c);
                } else if (!strcasecmp(buf, "maxretries")) {
                    if (sscanf(c, "%30d", &o->maxretries) != 1) {
                        ast_log(LOG_WARNING, "Invalid max retries at line %d "
                            "of %s\n", lineno, fn);
                        o->maxretries = 0;
                    }
                } else if (!strcasecmp(buf, "codecs")) {
                    ast_parse_allow_disallow(NULL, &o->format, c, 1);
                } else if (!strcasecmp(buf, "context")) {
                    ast_string_field_set(o, context, c);
                } else if (!strcasecmp(buf, "extension")) {

                    ast_string_field_set(o, exten, c);
                } else if (!strcasecmp(buf, "priority")) {
                    if ((sscanf(c, "%30d", &o->priority) != 1) ||
                        (o->priority < 1)) {
                        ast_log(LOG_WARNING, "Invalid priority at line %d of "
                            "%s\n", lineno, fn);
                        o->priority = 1;
                    }
                } else if (!strcasecmp(buf, "retrytime")) {
                    if ((sscanf(c, "%30d", &o->retrytime) != 1) ||
                        (o->retrytime < 1)) {
                        ast_log(LOG_WARNING, "Invalid retrytime at line %d of "
                            "%s\n", lineno, fn);
                        o->retrytime = 300;
                    }
                } else if (!strcasecmp(buf, "waittime")) {
                    if ((sscanf(c, "%30d", &o->waittime) != 1) ||
                        (o->waittime < 1)) {
                        ast_log(LOG_WARNING, "Invalid waittime at line %d of "
                            "%s\n", lineno, fn);
                        o->waittime = 45;
                    }
                } else if (!strcasecmp(buf, "retry")) {
                    o->retries++;
                } else if (!strcasecmp(buf, "startretry")) {
                    if (sscanf(c, "%30ld", &o->callingpid) != 1) {
                        ast_log(LOG_WARNING, "Unable to retrieve calling "
                            "PID!\n");
                        o->callingpid = 0;
                    }
                } else if (!strcasecmp(buf, "endretry") || !strcasecmp(buf,
                    "abortretry")) {
                    o->callingpid = 0;
                    o->retries++;
                } else if (!strcasecmp(buf, "delayedretry")) {
                } else if (!strcasecmp(buf, "setvar") || !strcasecmp(buf,
                    "set")) {
                    c2 = c;
                    strsep(&c2, "=");
                    if (c2) {
                        var = ast_variable_new(c, c2, fn);
                        if (var) {
                            /*
                             * Always insert at the end, because some people
                             * want to treat the spool file as a script
                             */
                            if (last) {
                                last->next = var;
                            } else {
                                o->vars = var;
                            }
                            last = var;
                        }
                    } else
                        ast_log(LOG_WARNING, "Malformed \"%s\" argument. "
                            "Should be \"%s: variable=value\"\n", buf, buf);
                } else if (!strcasecmp(buf, "account")) {
                    ast_string_field_set(o, account, c);
                } else if (!strcasecmp(buf, "alwaysdelete")) {
                    ast_set2_flag(&o->options, ast_true(c),
                        SPOOL_FLAG_ALWAYS_DELETE);
                } else if (!strcasecmp(buf, "archive")) {
                    ast_set2_flag(&o->options, ast_true(c),
                        SPOOL_FLAG_ARCHIVE);
                } else {
                    ast_log(LOG_WARNING, "Unknown keyword '%s' at line %d of "
                        "%s\n", buf, lineno, fn);
                }
            } else
                ast_log(LOG_NOTICE, "Syntax error at line %d of %s\n", lineno,
                    fn);
        }
    }
    ast_string_field_set(o, fn, fn);
    if (ast_strlen_zero(o->tech) || ast_strlen_zero(o->dest) ||
        (ast_strlen_zero(o->app) && ast_strlen_zero(o->exten))) {
        ast_log(LOG_WARNING, "At least one of app or extension must be "
            "specified, along with tech and dest in file %s\n", fn);
        return -1;
    }
    return 0;
}
```

The first thing it seems to do (after storing some Asterisk variables for later
usage) is begin parsing the call file, 256 bytes at a time.  One thing we
immediately learn from this, is that any given line in your call file cannot
contain more than 256 bytes (characters).  If it does, then it will not be
parsed correctly.

The next thing that `apply_outgoing` does is remove any comments and trailing
whitespace.  This is pretty standard stuff.  I am a bit surprised, however,
that the Asterisk developers didn't use the utility function `ast_trim_blanks`
(in `include/asterisk/strings.h`), as re-writing this sort of stuff greatly
increases the size of the code base, making it harder to maintain.

Next, Asterisk attempts to detect the command and arguments for each call file
directive.  Since all call file directives are of the form
`command: arguments`, Asterisk splits the line at `:`, then tries to detect
which command is being called.  This is exactly what we would expect to happen.

In the process of splitting the lines into command and argument pairs, Asterisk
parses out the arguments as well, and populates the outgoing struct as
expected.  Along the way, if Asterisk finds any problems with the syntax, it'll
log the errors to the Asterisk log (usually `/var/log/asterisk/full`).

Lastly, after parsing all options, Asterisk verifies to make sure that the
minimum directives have been specified.

If everything worked OK, and the call file can be spooled, then
`apply_outgoing` will return `0`, otherwise, it'll return `-1`.


## What Did We Learn?

We've analyzed the core components that make call files work, and we've learned
a few things.

-   We have a complete understanding of which call file directives exist (as
    shown in the code above).  This is a big benefit, as the documentation on
    [VoIP Info][], and various other Asterisk documentation websites seems to
    be incomplete.  The exact call files directives allowed are:

    -   `channel`
    -   `callerid`
    -   `application`
    -   `data`
    -   `maxretries`
    -   `codecs`
    -   `context`
    -   `extension`
    -   `priority`
    -   `retrytime`
    -   `waittime`
    -   `retry`
    -   `startretry`
    -   `endretry`
    -   `delayedretry`
    -   `setvar`
    -   `account`
    -   `alwaysdelete`
    -   `archive`

    Note, some of these directives should not be directly entered into your
    call files (as Asterisk will automatically add them as necessary), but of
    course, if you're reading this you're probably the type of person who likes
    messing with that sort of stuff, so have at it. :>

-   We've learned how to put any amount of directives we want onto a single
    line.  Obviously this is totally useless, but it is nice to know that we
    CAN if we want to!

    We're able to do this because the spooling daemon reads 256 bytes at a time
    for parsing.  So we could write a call file that looks something like:

    `Channel: blah NextDirective: blah ...`


## Conclusion

I'm hoping to do a few more articles that demistify other parts of Asterisk in
depth (with code and examples).  This is my first, and I know it doesn't touch
on the complex topics like threading and synchronous / asynchronous channels,
but I assure you I'll write some future articles which cover those parts in
extreme depth.


  [Daemon Sketch]: /static/images/2010/daemon-sketch.png "Daemon Sketch"
  [pycall]: http://pycall.org/ "pycall"
  [Asterisk call files]: http://www.voip-info.org/wiki/view/Asterisk+auto-dial+out "Asterisk Call Files Wiki Page"
  [latest Asterisk release]: http://www.asterisk.org/downloads "Asterisk Downloads"
  [asterisk v1.6.2.7 (tarball)]: http://downloads.asterisk.org/pub/telephony/asterisk/old-releases/asterisk-1.6.2.7.tar.gz "Asterisk v1.6.2.7 Tarball"
  [favorite editor]: http://www.vim.org/ "Vim Editor"
  [VoIP Info]: http://www.voip-info.org/ "VoIP Info Wiki"
