---
layout: post
title: "Weekly recap - Week #40"
date: 2014-10-04
permalink: "/2014/10/04/weekly-recap-week-40/"
description: "This week was a wild mix of code and topics from the “agile world”"
tags: []
og_type: article
original_source: "Dissident Trainings"
original_url: "http://dissident-trainings.de/2014/10/04/weekly-recap-week-40.html"
canonical_url: "http://dissident-trainings.de/2014/10/04/weekly-recap-week-40.html"
render_with_liquid: false
---
This week was a wild mix of code and topics from the “agile world”

## Development

I started to experiment with Node.js based systems that allow for rapid prototyping. I took a look into hoodie (again) and liked it (again). So if your thing is rapid development, based purely on javascript and offline first: [Hoo.die](http://hood.ie/#installation) is your friend. The development pipeline gets better and better version by version.

Microsoft is open sourcing WinJS, a nice tool to build windows styled apps. One of the better framework approaches although it feels kinda full stack. If you are doing stuff for Windows: [try this](http://try.buildwinjs.com/). Windows Phone support? Oh yeah ;)

Apache [Cordova](http://plugins.cordova.io/#/) seems to be a nice toy for HTML5/CSS Desktop Apps. I took it out for a ride and kinda liked it. We will see more of this and I feel its good.

Again, it was time to [remove all globally installed node.js modules](http://stackoverflow.com/questions/9283472/command-to-remove-all-npm-modules-globally) from one of my machines. Lucky me someone did it before. Actually I end up re-installing stuff on a quite regular base and I don’t like it. Basically you will have to do a node re-install after it. I need to completely switch t NVM.

## Agile

For a upcoming talk about **Pair-Programing** I did some research on arguments against it. Here is a extra nice example of [FUD](https://news.ycombinator.com/item?id=1974503).

> In fact, the cowboy programmers still rule the programming session when you pair up with them and they can easily take up most part of the day arguing small uninteresting details until they get it their way making the software theirs - not the team.

A evening out with [Endgegner Soenke](https://twitter.com/s0enke) brought the topic of the advanced problems of TDD. He is a Devops guy and so his view on all this is tainted with things like feature flags, A/B testing etc. There are others thinking in the [same direction](http://joblivious.wordpress.com/2009/02/24/advanced-tdd-two-birds-with-one-stone/). I will do more research and promised to come up with a workshop format for the more advanced TDD things beyond red-green-refactor

To understand [CI](http://www.wikiwand.com/en/Continuous_integration) and [CD](http://www.wikiwand.com/en/Continuous_delivery) there is a very [nice tutorial for a setup using Github/TravisCI and Heroku](http://shapeshed.com/continuously-deploy-node-apps-with-github-travis-and-heroku/). These 3 go together very well and are a nice playground if you want to start experimenting. I am using this pipeline for a while and when you come from a more classic development pipeline this will blow your mind.

A little late, but this is how I feel when consultants talk about [scaling “agile”](http://scrummasterreactions.tumblr.com/post/98478026061/scaling-agile)
