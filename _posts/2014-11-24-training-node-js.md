---
layout: post
title: "Delivering a node.js training"
date: 2014-11-24
permalink: "/2014/11/24/training-node-js/"
description: "On a short notice a big training company had approached me - A trainer of them had dropped out of a planned training and they needed someone to deliver a…"
tags: []
og_type: article
original_source: "Dissident Trainings"
original_url: "http://dissident-trainings.de/2014/11/24/Training-node-js.html"
canonical_url: "http://dissident-trainings.de/2014/11/24/Training-node-js.html"
render_with_liquid: false
---
On a short notice a big training company had approached me - A trainer of them had dropped out of a planned training and they needed someone to deliver a introduction to the node platform in the context of web development for one of the bigger agencies here in hamburg.

As always: The participants already had a good idea about Javascript and knew basics of the node platform. It was all more about filling the gaps than teaching all “from the ground up”.

## The content

We had a Training in [2 Parts aka days](https://github.com/DissidentTrainings/node-js-training/blob/master/Agenda.md)

- Day 1: Introduces to node.js, npm and packages
  - How node works and some look into npm
  - Debugging and monitoring Node apps
- Day 2: Express JS, TDD, Grunt
  - Creating a CommonJS module
  - Creating a ExpressJS app

## The results

It was pretty nice to see the training unfold. The beginning was a bit rough, since I had to go into areas that I had rarely touched before and these were a bit bumpy at least.

I had created a simple repo for the first day, that reflects the progress of the workshop and introduces basic techniques like “git tag”, semver and such tools. All this is required later on and helps.

Surprisingly the participants wanted to code more (and even more) so that I changed the second day to just Pairprogramming/Coding-Dojo/Mob programming (I do not differ that so much).

We started with 2 repos on github (which saw one or the other commit these days):

- [The “Workshop” Repo](https://github.com/DissidentTrainings/) - Containing the Agenda
- [The Examples Repo](https://github.com/DissidentTrainings/node-js-training-examples) - Containing some simple steps to follow

Since most of the training was a practical introduction to something technical there was little documentation of contents (besides some ugly flipcharts - I need to patent the style). So how to solve the problem on getting a piece of documentation to the developers attending tsshe workshop? Easy thing: Just commit on a regular basis: We did Pairprogramming with a 5 minute change timer and on each of these changes of driver and navigator saw a commit to git.

This resulted in the einself App and commonJS module:

We created a webservice that uppercases any word and appends [!!!!1einself](http://heise.forenwiki.de/index.php?title=Einself) to it. I did choose the inside out way of building things (I can hear the ATDD community protesting with pitchforks already): Using Mocha Unit Tests for the CommonJS module and then re-using it in our express.js app the we just built and left untested (another pitchfork protest in front of my house).

We created 2 repos there:

- The [CommonJS Module](https://github.com/DissidentTrainings/einselfuppercase) - A little SJ, mocha tests and
- The [express.js App](https://github.com/DissidentTrainings/einselfuppercase-app)

This forced us to really create something productive and since we committed on every driver/navigator change, there is a good documentation about what we did and when in the commit logs of the [module](https://github.com/DissidentTrainings/einselfuppercase/commits/master) and the [app](https://github.com/DissidentTrainings/einselfuppercase-app/commits/master)

## What I learned

There is a lot of lessons learned for me here for me

- Even after some years of node.js - I have still areas that I do not know very well. The new [cluster](http://nodejs.org/api/cluster.html) module and the libraries behind node are 2 of them.
- [Training from back of the room](http://www.amazon.de/Training-Back-Room-Aside-Learn/dp/0787996629) can be done with straight forward technical trainings.
- Pairing works quite well - Especially when participants with less knowhow learn that they get away from the keyboard all 5 minutes.
- Every pair change one commit not only works at work, but creates a good piece of documentation.
- Grunt and Gulp.js are topics that need to be revisited. Too big to really explain them in a workshop.
- Participants value working it out on the keyboard over getting everything presented on a silver plate

## Interested?

> If you are interested in getting me to your place and bringing your team up to speed in all things node.js and express.js basics: contact me. Still places for 2014 available.

If you want to do it for your self: I will be adding the licenses to the repositories soonish so that the material is us able in a commercial context.
