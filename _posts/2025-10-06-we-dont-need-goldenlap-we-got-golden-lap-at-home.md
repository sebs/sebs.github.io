---
layout: post
title: "We don't need GoldenLap, We got Golden Lap at home"
date: 2025-10-06 19:45:48 +0000
permalink: "/2025/10/06/we-dont-need-goldenlap-we-got-golden-lap-at-home/"
description: "A weekend attempt at a Golden Lap-style browser racing game: board game research, real-time simulation, GPU offloading, minimap rendering and physics."
tags: [game-development]
og_type: article
image: "/assets/posts/we-dont-need-goldenlap-we-got-golden-lap-at-home/og.jpg"
devto_url: "https://dev.to/sebs/we-dont-need-goldenlap-we-got-golden-lap-at-home-ndb"
render_with_liquid: false
---
Another weekend, another rabbit hole. This time, it started with a game called Golden Lap. If you haven't seen it, it's a minimalist, 70s-themed motorsport management game that's been getting some well-deserved attention. It's got that sleek, retro vibe, but underneath the hood, there's a surprisingly deep strategic engine. And, of course, being me, my first thought wasn't just "this is cool," but "I could probably build something like this."

This is a recurring theme in my life: a dangerous cocktail of overestimating my own abilities and an unhealthy interest in the intricate mechanics of video games. I saw Golden Lap and its scientific touch, the way it distills the chaos of motorsport into a series of critical decisions, and I was hooked. But I had a different kind of race in mind. I wanted to build something like Golden Lap, but in the browser, and with my own twist on the racing model.

So, I did what any self-respecting developer with a bad idea does: I started trying.


> I tried to research all tabletop games with this theme I could get my hands on.

Before diving into code, I went analog. I have a soft spot for the tangible mechanics of board games. I dug into classics like Formula D, a game that brilliantly captures the feel of F1 racing with a clever dice-based gear system. You're not just rolling and moving; you're managing risk, deciding when to push your luck in a corner, and when to play it safe. It’s a masterclass in translating real-time action into a turn-based format. The goal was to see how others had solved the problem of making a race feel like a race, without the real-time twitch reflexes.


> I tried to get an idea of how to simulate this in 'real time'.

Here's where the hubris really kicked in. How hard could it be to simulate a few cars on a track? Turns out, very. The moment you move from a turn-based system to a real-time simulation, the complexity explodes. Suddenly, you're dealing with physics, with continuous updates, with the need for a system that feels both authentic and, well, fun. My initial, naive implementations felt less like a thrilling race and more like a procession of slightly uncooperative rectangles.


> I ended up starting to use the GPU, because my implementation surely was computationally heavy.

It quickly became apparent that my little browser-based experiment was going to be a lot more computationally heavy than I'd anticipated. The constant calculations for position, velocity, and the interactions between cars were starting to make my laptop sound like it was preparing for takeoff. So, naturally, I thought, "I'll just offload it to the GPU!" As if that's a simple, one-line fix. The elder I get, the more I appreciate that the answer to "how hard can it be?" is almost always "harder than you think."


> Rendering any track and the cars positions for a minimap was far from a simple task.

And then there was the visual side. I just wanted a simple minimap. A few dots on a line. Easy, right? Wrong. Rendering a track, even a stylized one, and accurately plotting the cars' positions in real-time, turned out to be a significant challenge in itself. It's one of those things that seems trivial until you're the one staring at a blank canvas, trying to remember your high school trigonometry.


> Surely the calculation is arcane. The well known 'the Physics of Racing' was good as a basis to simplify from there.

This is when I finally admitted I was in over my head and turned to the experts. I dusted off my digital copy of Brian Beckman's "The Physics of Racing." It's a legendary text for a reason. It breaks down the complex physics of a race car into understandable, mathematical principles. It's dense, it's arcane, but it's also the ground truth. I wasn't trying to build a perfect simulation, but to build a believable one, I needed to understand the rules I was trying to break. Beckman's work was the perfect foundation to simplify from, to find the right abstractions that would give my little browser game the feel of racing, without needing a supercomputer to run it.

So, where does that leave me? With a half-finished, overly ambitious browser game, a newfound respect for the developers of games like Golden Lap, and a much deeper understanding of the physics of a four-wheeled vehicle. And, in all sincerity, that's a pretty good outcome for a weekend project.

As a wise man once said:


> At times, the sole viable course of action is to refrain from participating.

Or, in this case, to know when to stop, take a breath, and appreciate the beautiful complexity of the things we try to build. Even if we don't quite get there. I do think Golden Lap is a good hint we still can get really interesting games and much of the bling bling out there is just 'lipstick on a pig' to make up for missing depth.
