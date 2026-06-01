---
layout: post
title: "The crux of done"
date: 2019-02-03
permalink: "/2019/02/03/The-crux-of-done/"
description: "There are always big discussions revolving around when some piece of work is “done”: Often the discussion goes as far as defining different states of done…"
tags: [teamwork]
og_type: article
---
There are always big discussions revolving around when some piece of work is “done”: Often the discussion goes as far as defining different states of done and there is even the notion of “done done”. This stands for “it is really done now”.

Some definitions of done revolve around the following ideas:

When Tests Pass: This is basically a fire and forget way of working that expects feedback at the and of a sprint. Then the piece of work is getting deployed and then you might have a good indicator if that works or not. When your app just has compiled and all tests are green: It has not yet been integrated with the system. Not done my friend.

When Integrated: You might be a active reader or just had the experience, that a a piece of software not only must pass its (unit) tests, but needs to be integrated with other systems and live data in order to prove that it works. So integrate it, like your jenkins would do. Download all the dependencies, setup the system, use live data. Profit? Not yet, still the thing is lying around in a repo and no one is using it (apart from a mr Jenkins)

When deployable build exists: If I had a nickel for every time I heard a discussion about “potential shippable”, sprints that end successfully without a deploy and all that yada yada. Simple truth: If you haven’t shipped, you are not done. Just that you integrated the system with a copy of all user data, on a 1 to 1 equal hardware setup, with automated acceptance and performance tests does not mean it will work on the live system. Admit it, there is not a 100% chance for this to work on live.

When deployed: So your sprint ends on a Friday and you just When measurably delivering value want to deploy, you deploy, all is fine. Just until something goes wrong. Especially deploys for multiple teams with different areas of expertise (mobile apps, backend, web) can get hairy. Its just that notion of “all at once, now” that makes it problematic. Deployed software always needs a little time to prove that it works. A green lit deploy is by no means a good indicator if your rollout was successful from the customer side. Customer does not care if the feature was rolled out, customer wants to use it!!! Big difference. ;) Not done when deployed.

When measurably delivering value: It might be surprising, but this is the only thing I go by since I came by that definition for the first time. Its delivered and I have access to the tool that shows me the value in your business (e.g. Sales made) in any tracking tool (e.g. google analytics, salesforce, e-commerce backend) and I can see for myself. When the thing is deployed, I have observed it working and seen the tracking systems . I might have gone the extra mile to set up a piece of hardware or do a order on a online retail system for about 20.000 Euro (only to find out that the rollback did not rollback the expenses on my customer card account — free credits, not even part of the development I had done). After another change and deploy, the product manager got informed and we reviewed the change on the live systems and all was fine then.

## Fail Forward

This is a thing to go by. Not every condition can be foreseen, not every plan can be made up. I do sport a extra round of automation tools and logging foo and I spend a extra amount of time on live systems. Just to be there and inform myself of the mishap that is going on. Isn’t it that always just the one test or test category was missing, just to find out 2 weeks later that another type of test would have avoided the problem. A failed (forward) deploy is just another fail, that leads to just another improvement of process and there are ways to make sure that this type of error will likely not happen again.

That is normal operating procedure already in one or the other form. It just removes the need for a discussion about when done is done. The answer is: Not as long as the software runs on a live system.

Its not that I am ignoring the learnings out of old DOD documents, but in the end, it boils down to one thing and other things got so internalized and do not need a entry on such a list (e.g. doing all the translation work before release, writing tests). The more I put on such a list, the more exemptions need to be done (e.g. no unit tests for UI features, just cucumber, no translations for CLI tools). There is a deep rabbit hole of arcane processes and deploy/build chains down this way.

This is why I can live with a “Definition of done” with only one rule:

```plain
When measurably delivering value
```
