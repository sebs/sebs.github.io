---
layout: post
title: "Yo dawg, I heard you like XP Practices and BDD"
date: 2014-10-17
permalink: "/2014/10/17/yo-dawg-i-heard-you-like-xp-practices/"
description: "I need to get a website for the upcoming XP Practices training together that shows basic practices and allows participants to prepare for the workshop.…"
tags: []
og_type: article
original_source: "Dissident Trainings"
original_url: "http://dissident-trainings.de/2014/10/17/yo-dawg-i-heard-you-like-xp-practices.html"
canonical_url: "http://dissident-trainings.de/2014/10/17/yo-dawg-i-heard-you-like-xp-practices.html"
render_with_liquid: false
---
I need to get a website for the upcoming XP Practices training together that shows basic practices and allows participants to prepare for the workshop. There is a little prototype already, but the final product needs to be included in this site.

## Eat your own dogfood

On the other hand I am preparing more contents for the BDD workshop that needs a lot more examples and a lot of them need to be fail, fix, win in order to show how it can be done and how it can be done better. So I decided to develop the whole site with BDD and some tools related to it.

**The creation of the XP Practices site will generate the examples for the BDD workshop**

## Failing is not an option it is a goal

I do not want to make failures up and I don’t think there is need for it. I will fail hard enough without any simulated attempts to do something wrong. On the other hand I will start very simple with a basic application and a basic deploy script. It will be just like a real life software project.

**Everyone puts his pants on one leg at a time**

I guess it is a little risky to go out there **pants down** and show how I do this BDD thingie. I am seeing trainers rarely doing this. Most time you come up with cooked up examples and those are kind of gated simulations like gated communities. With limiting the feature set or the variables there is a more narrowly defined outcome. This is not the case here.

## Continuous Delivery

The whole website will be set up with continuous delivery and we will start with a hello world as the beginning. I will use the hints and experiences I grabbed at a talk from the developers at @unruly about CD and their practices. Some of them are

- deployment gateways instead of pipelines (done make a big fuzz of deployment)
- sync deployments - deploy and check if you can measure that it is working
- start with a deploy (this is part of my upcoming talk anyways)
- make it possible to run tests against production to validate the site

## The repo

The [repo](https://github.com/DissidentTrainings/xp-practices-site) is still empty
