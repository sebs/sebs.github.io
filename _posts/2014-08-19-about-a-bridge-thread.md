---
layout: post
title: "About a Bridge Thread"
date: 2014-08-19
permalink: "/2014/08/19/about-a-bridge-thread/"
description: "Tips for the XP bridge thread as first iteration: pick an independent, end-to-end core story that touches all layers, sets up CI and informs estimates."
tags: [agile-practices, software-architecture]
og_type: article
original_source: "Dissident Trainings"
original_url: "http://dissident-trainings.de/2014/08/19/about-a-bridge-thread.html"
canonical_url: "http://dissident-trainings.de/2014/08/19/about-a-bridge-thread.html"
render_with_liquid: false
---
Reading the C2 wiki, in the context of extreme programming, a bridge thread is

*The first iteration of an XP project should aim to be a [BridgeThread](https://c2.com/cgi/wiki?BridgeThread) : an end-to-end application, which does not have to contain much significant functionality, but from which the rest of the system can be hung. The [BridgeThread](https://c2.com/cgi/wiki?BridgeThread) determines the system architecture. In this XP works much like a weaving spider*

\[caption id= align=alignright width=105\] Bridge Thread\[/caption\]

The bridge thread tries to answer a question that is posed very often and I do hesitate to give an more specific answer than: “Just pick ANY, it will be a long effort to build this product and in X months, what does it matter with what we started”.

The idea of the bridge thread tries to answer the same question. Some ideas (far from complete) regarding the **Bridge Thread**

- Make sure it is as independent as you can from other stories. It is the beginning, so one of the primary concerns, even more than in later sprints is: Deliver something.
- Make it a core functionality for your product. If you write a app that helps you getting a cab in a city: Do not make it the login. Try to be as close to the part that delivers the value to the customer as possible. Most likely login is not your main business case. (I have advised otherwise in the past … I changed my mind)
- Don’t take any shortcuts. Use a small story, but implement it completely
- Don’t sweat it . It is sprint 1. Getting shit done is more important than getting a lot of shit one. Not producing any bullshit is even more important
- You will have to set up a lot of stuff: CI, automated tests etc. Did I vote for a small Story already?
- All layers included. use a story that needs all layers of your architecture.
- Your estimates are most likely not really good in the beginning. You could pull a story, implement it and pull the next one. Story by story. This is how a Kanban team could approach such a problem.
- Don’t commit to a sprint goal .. just try. There is no real way to commit to something you don’t know.
- Have everything extra-ready. All assets. Maybe a DB design. Architecture? You should have a good Idea of this. As much as I love emergent Architecture and Design, just don’t try always when the last responsible moment for that is. One or two extra hours invested wont hurt. Beforehand the sprint. Not 20 minutes before you start the story.
- Try to hammer a estimate in SP on the Bridge Thread anyways. And Re-Estimate in later sprints. This way you can make sure, that the learning, that took place in the first sprint lands in later sprints.

Do you have more hints what to choose for starters in bigger “Projects” or at the beginning of a new Product or Codebase? Please share them below.
