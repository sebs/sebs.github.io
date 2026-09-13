---
layout: post
title: "Ideas for modern coding"
date: 2014-08-20
permalink: "/2014/08/20/ideas-for-modern-coding/"
description: "If starting a new web project follow some basic principles"
tags: []
og_type: article
original_source: "Dissident Trainings"
original_url: "http://dissident-trainings.de/2014/08/20/ideas-for-modern-coding.html"
canonical_url: "http://dissident-trainings.de/2014/08/20/ideas-for-modern-coding.html"
render_with_liquid: false
---
If starting a new web project follow some basic principles

- Start with deploy code - It must be deployable from moment 0
- Use Unit- and Functionaltests
- The deployed code is testable and thereby you can verify it
- Use Virtual machines to recreate the live environment
- All is in GIT - dev and ops code
- Use cont. integration and cont. deployment from moment 0
- Static analyze the code - it’s cheap
- Build in monitoring and logging
- Whatever you do, write some docs, build them automatically

I think I will try this. Using this one would end up with a recreatable environment, that 5 years later, everyone who wants to use the software, can recreate. It’s not ma a magic bullet, but I think it could speed up a lot of things heavily.

A day setup can save you a lot of worries. The less you depend on things made “by hand” and if you put something aside for a while, you will be able to return easily.
