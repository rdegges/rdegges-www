---
title: "Simple Continuous Integration / Deployment With Jenkins"
date: "2011-04-10"
tags: ["programming", "devops"]
slug: "simple-continuous-integration-deployment-with-jenkins"
description: "A quick walkthrough showing you how to get Jenkins up and running."
---


![Butler Sketch][]


At work we rely heavily on continuous integration and deployment to help us
deliver lots of code into production and staging environments quickly.  In a
typical day, we'll make something like 15 deployments to at least one or two of
our projects.

The software we use to manage this is crucial to us, as programmers, because it
makes our lives much easier.  Instead of manually running large test suites
against remote servers, we just let our CI system run the tests as soon as we
push our code to [GitHub][], and once our tests pass, deploy the code live :)

Today I'm setting up a new [Jenkins CI][] server for work, to move off our old
[Hudson][] server, so I figured this would be a good time to blog about the
process, as it's so extremely helpful to us that I can't imagine ever
programming without it again.

For the rest of this tutorial, I expect that you:

-   Are using Ubuntu server or Debian server as your operating system.
-   Are familiar with the Linux command line.
-   Know what [continuous integration][] and continuous deployment are.
-   Have some code to test deploy.


## Installing Jenkins

Installing Jenkins is ridiculously easy on Debian systems:

```console
$ wget -q -O - http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key | sudo apt-key add -
$ sudo echo "deb http://pkg.jenkins-ci.org/debian binary/" > /etc/apt/sources.list.d/jenkins.list
$ sudo aptitude -y update
$ sudo aptitude -y install jenkins
```

Congratulations, you now have Jenkins running!  To visit your new Jenkins
instance, just visit `http://youserverip:8080/`.  If you want to update it, you
can do so with the rest of the system (via
`aptitude -y update; aptitude -y safe-upgrade`).


## Configure a HTTP Proxy With NGINX

Since Jenkins by default runs on port `8080`, I like setting up an HTTP proxy
so to that I can access it on port `80`.  My weapon of choice for proxying is
NGINX, so let's set that up now:

```console
$ sudo aptitude -y install nginx
$ cd /etc/nginx/sites-available
$ sudo rm default
$ sudo cat > jenkins
upstream app_server {
    server 127.0.0.1:8080 fail_timeout=0;
}

server {
    listen 80;
    listen [::]:80 default ipv6only=on;
    server_name ci.yourcompany.com;

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;

        if (!-f $request_filename) {
            proxy_pass http://app_server;
            break;
        }
    }
}
^D # Hit CTRL + D to finish writing the file
$ sudo ln -s /etc/nginx/sites-available/jenkins /etc/nginx/sites-enabled/
$ sudo service nginx restart
```

Now you should be able to visit `http://ci.yourcompany.com/` and see your
Jenkins instance on the default HTTP port `80`.


## Secure Jenkins

Jenkins has built-in user account management, which makes it easy to lock your
interface down.  Below, we'll create two accounts: `admin` and `rdegges`.
`admin` will have full permissions to the projects, and `rdegges` will only be
able to view project statuses, but not update any settings or make project
changes.  Changing the security rules for your environment are pretty
intuitive, once you see how it works:

1.  Click the **Manage Jenkins** link on the left side of your page.
2.  Click the **Configure System** link.
3.  Check the box labeled **Enable security**.
4.  Select the bubble labeled **Jenkins's own user database**.
5.  Select the bubble labeled **Matrix-based security**.
6.  Enter **admin** in the text box labeled **User/group to add** then click
    **Add**.
7.  Enter **rdegges** in the text box labeled **User/group to add** then
    click **Add**.
8.  For **admin**, check all the square boxes that run horizontally.  This
    allows the **admin** user to do anything.
9.  For **rdegges**, check only the square boxes labeled **Read**.
10. Scroll to the bottom of the page and click the **Save** button.

If you did everything properly, your page should look something like this:

![Jenkins Configuration][]

Now that you've applied some rules, you need to actually create the two user
accounts you supplied rules for.  On the main Jenkins page, click the **Create
an account** link, and create two accounts--one for `admin`, and one for
`rdegges`.  Note that when you log into each of these accounts, they have the
permissions you supplied earlier.  If you want to change permissions, just log
in as the `admin` user, and go through the same steps above.


## Install and Configure Git

The core functionality of Jenkins is to use some form of version control
software (I use [Git][]) to check out some release of code, and then do stuff
with it.  Below, we'll setup Git on our server, and in Jenkins, so that we can
check out all of our Git projects.

Firstly, you'll want to run the following commands on your server to install
Git.  You'll obviously need to make changes to this code for your environment:

```console
$ sudo aptitude -y install git
$ sudo su - jenkins
$ git config --global user.name "Jenkins CI"
$ git config --global user.email "ci@yourcompany.com"
$ ssh-keygen -t rsa -C "ci@yourcompany.com" # Use all the default options, don't specify
                                          # a password.
$ cat .ssh/id_rsa.pub # Grant this SSH key access to your Git repositories.

# If you're using github, you'll also want to do:
$ ssh git@github.com
# And accept the connection so that you add github.com to your known_hosts file.
```

Once you've done all that, all you need to do is follow the next few steps in
the web panel:

1.  From the main page, click the **Manage Jenkins** link.
2.  Click the **Manage Plugins** link.
3.  Click the **Advanced** tab.
4.  Click the **Check Now** button.
5.  Click the **Back to Dashboard** link.
6.  Click the **Manage Jenkins** link.
7.  Click the **Manage Plugins** link.
8.  Click the **Available** tab.
9.  Check the box labeled **Git Plugin** (it's towards the bottom of the
    page).
10. Scroll to the bottom of the page and click the **Install** button.
11. Once the plugin has been installed, click the **Restart When No Jobs Are
    Running** button.

You've now got Git ready to roll.


## Configure a Project

In this step we'll configure Jenkins to check out the latest copy of our
project's code, run the test suite, and then deploy our code live into
production.  It's a lot easier than it sounds, let's take a look:

1.  Click the **New Job** link.
2.  Enter your project's name into the **Job name** box.
3.  Select the **Build a free-style software project** link.
4.  Click the **OK** button.
5.  Under the **Source Code Management** section, select the bubble next to
    **Git**.
6.  Enter the URL of your Git repository. This is usually something
    like: `git://github.com/rdegges/django_project.git`.
7.  Under the **Build Triggers** section, select the box labeled **Poll SCM**.
8.  In the **Schedule** box that appears, enter `* * * * *` (don't
    include the quotes).  This instructs Jenkins to check your Git repository
    for changes every minute.  If you want to change the frequency, feel free
    to do so using [crontab format][].
9.  Under the **Build** section, click the **Add Build Step** button, then
    select **Execute shell**.
10. In the **Command** box that appears, enter your commands to build, test,
    and deploy your software.
11. Scroll to the bottom of the page and click the **Save** button.

That's it!  Jenkins will now automatically poll your Git repository every
minute for changes.  If any code was changed, it will check out the latest
version of your code, then execute the commands you specified as build
steps--which should be testing and deploying your code.

If you go back to the main page, you'll be able to view the status of all your
projects, and click through to see detailed information about builds, errors,
and lots of other neat stuff.


## RTFM

Obviously, a 5 minute walk-through is no excuse for not learning how to use
Jenkins properly.  If you want to learn how to make the best use of Jenkins,
and experiment with the hundreds of awesome plugins that it has, be sure to
read the [official documentation][].


  [Butler Sketch]: /static/images/2011/butler-sketch.png "Butler Sketch"
  [GitHub]: https://github.com/ "GitHub"
  [Jenkins CI]: http://jenkins-ci.org/ "Jenkins CI"
  [Hudson]: http://hudson-ci.org/ "Hudson CI"
  [continuous integration]: http://en.wikipedia.org/wiki/Continuous_integration "Continuous Integration Wiki Page"
  [Jenkins Configuration]: /static/images/2011/jenkins-configuration.png "Jenkins Configuration"
  [Git]: http://git-scm.com/ "Git"
  [crontab format]: http://adminschoice.com/crontab-quick-reference "crontab reference"
  [official documentation]: http://jenkins-ci.org/ "Jenkins Documentation"
