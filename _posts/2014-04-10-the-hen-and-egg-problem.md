---
layout: post
title: "The hen and egg problem"
date: 2014-04-10
permalink: "/2014/04/10/the-hen-and-egg-problem/"
description: "Building UI and API in parallel causes interface ping-pong that slows delivery; a quickly changeable mock API built with Interfake saves that time."
tags: [web-development, developer-tooling]
og_type: article
original_source: "Dissident Trainings"
original_url: "http://dissident-trainings.de/2014/04/10/the-hen-and-egg-problem.html"
canonical_url: "http://dissident-trainings.de/2014/04/10/the-hen-and-egg-problem.html"
render_with_liquid: false
---
Imagine, you do a project with a UX guy. He is building the UI and expects an api while doing so.

**The Problem**

The API will change and new methods will be required as well as changes to “old” parts of the API. You are creative, right? Not everything is laid out in a User-Story, right? New features lead to new Ideas, right?

This leads to a slow down in the cycle. A Server is a different thing. If you want to release, you need a working server component and the client. In order to build a stable one, a defined interface in terms of a restful API would be a good start.

However, this Ping-Pong has a price: time.

**Fake it, until you make it**

A good Idea would be a API prototype, kinda easy to create and change. In a very short amount of time. Save the time for the concrete implementation of the API by using a mock System.

> *Interfake is a tool which allows developers of client-side applications of any platform to easily create dummy HTTP APIs to develop against. Let’s get started with a simple example.*
