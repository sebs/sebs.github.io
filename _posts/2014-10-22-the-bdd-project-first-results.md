---
layout: post
title: "The BDD project - My first results"
date: 2014-10-22
permalink: "/2014/10/22/the-bdd-project-first-results/"
description: "First results of a BDD side project: an impact map for an XP practices workshop site, its user groups, and the first two user stories for cucumber.js."
tags: [testing-and-quality, agile-practices]
og_type: article
original_source: "Dissident Trainings"
original_url: "http://dissident-trainings.de/2014/10/22/the-bdd-project-first-results.html"
canonical_url: "http://dissident-trainings.de/2014/10/22/the-bdd-project-first-results.html"
render_with_liquid: false
---
Starting of on [sunday](https://github.com/DissidentTrainings/xp-practices-site/commits/master/impact.txt) with a little **impact mapping** I tried to outline the first basic ideas using this technique. It turns it takes some rewrites and a little back and forth untilyou hit the spot.

Here is my first Impact Map for the project.

    Simplyfy workshop preparation
        Sebs
            Avoid having to use single google spreadsheeds to calculate which are the most important practices for participants
            Avoid having to explain "what do I need to do in order to  prepare"
        Participants
            Read about practices
            Get the links to the "original" Contents
                Website listing the basic descritption
            Get information about related Practices
                Links to "allies"
        Boss of Participants
            Get a list of practices selected by teams
                Mail or Website to look at 
    Convince potential customers that the workshop is awesome
        Sebs
        Participants
        Potential participants
    Provide a general information hub for XP practices

What did I take away from that little session of 2 hours in a starbucks?

I have identified 4 groups of users

- Me as the creator of the site
- Participants of the workshops
- Bosses and “deciders” who will pay for workshops and send participants there

What can people do on the site?

- Look at practices
- get references to the “original” content
- get info to related practices
- select practices to “build” a workshop

## The first Userstories

I created 2 Userstories out of that which will provide my first features

[List of Practices \#1](https://github.com/DissidentTrainings/xp-practices-site/issues/1)

    As a workshop participant and website user 
    I want to see a list of available practices 
    so that I can get an overview about all the practices offered for the workshop

[Show practice \#2](https://github.com/DissidentTrainings/xp-practices-site/issues/2)

    As a workshop participant and webiste user 
    I want to read about specific practices 
    so that I know what it is about 
    and I can decide if I want to have it in the workshop

## It is all rough

The main idea on interative and incremental development is to actually do stuff before you get into more planning. I have absolutely no incentive to do way more upfront planning. The basic idea remains to have **a tool help participants fo workshops select the practices they want to hear about** and thus I am gonna to add some feature files that I can feed into cucumber.js and start developing right away.

It is getting interesting. ;) So lets code a bit.
