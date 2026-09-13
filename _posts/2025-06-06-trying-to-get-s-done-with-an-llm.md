---
layout: post
title: "Trying to get s*** done with an LLM"
date: 2025-06-06 16:25:28 +0000
permalink: "/2025/06/06/trying-to-get-s-done-with-an-llm/"
description: "Building a Python CLI for an OpenAPI-based API with an LLM: a dynamic client, a clean Bandit scan, one powerful review prompt and why AI code rarely ships."
tags: [ai-assisted-development, developer-tooling]
og_type: article
image: "/assets/posts/trying-to-get-s-done-with-an-llm/og.jpg"
devto_url: "https://dev.to/sebs/trying-to-get-s-done-with-an-llm-k05"
render_with_liquid: false
---
I had a goal: to create a command-line interface (CLI) for a well-known API I was using at work. There wasn’t one available, and I saw an opportunity. The twist? I decided to write it with the help of a Large Language Model (LLM), using Python—a language that isn't exactly my mother tongue. The ultimate aim was to release it to the public on PyPI.

This is the story of my journey and the lessons I learned along the way.

## The Perils of Over-Engineering & The Unsettling Silence of the Linter

My first major hurdle was finding a valid client generator for the OpenAPI spec provided by the API. I went down a rabbit hole trying to find a tool that could generate a set of reusable API client classes that would play nicely with my chosen Python dependency management flavoor. It was a frustrating and time-consuming process.
Then, a thought struck me: what if I just read the JSON file dynamically and used that information to craft a client? It turned out to be not only possible but also significantly simpler. This was a crucial lesson: sometimes, the available software is so complex and hard to use that it’s more straightforward to just implement the spec using an agent.

As the LLM and I churned out code, I decided to run it through Bandit, a static linter that sniffs out security vulnerabilities in Python code. I braced myself for a deluge of warnings and errors. To my astonishment, Bandit came back with nothing. This was genuinely surprising, as my own, human-written code is usually a magnet for Bandit's critiques. 

After successfully implementing about 30% of the API endpoints, I had something that worked. But it was a mess. It became glaringly obvious that the project desperately needed more structure and a solid testing framework. I can’t entirely blame the LLM for this, though. The state of the code was a direct reflection of my own limited ability to articulate precisely what I wanted and what I was asking for.

## One powerful prompt

Just as I was starting to feel a bit lost in the weeds, I remembered what might be one of the most effective prompts I’ve used so far: "Propose improvements for the code in file X.py." The LLM responded with a list of about 20 things to improve, ranging from small tweaks to significant refactoring suggestions. This gave me a clear path forward and the confidence that I could actually get this project into a releasable state. All bit one of the proposals made sense and maybe this was a bit more work than I had anticipated, there is nothing in the remaining list that turned out to be unreasonable or leads multiple layers down a rabbit hole. 

## Why There's So Little "AI-Engineered" Code Out There?

This experience has given me a new perspective on why we aren't seeing more "AI-engineered" code in the wild.
First, there’s a stark difference between "getting it to work" and "I can release this to the public." The journey from a functional prototype to a polished, well-documented, and robust application is a long one, and it’s a journey that still requires a significant amount of human intervention.
Second, you need to know what to ask and be willing to learn. I can't help but notice that this is often missing from the "I cloned a $50 billion startup in one night using AI" crowd. You need to have a deep understanding of the problem you're trying to solve and the ability to ask the right questions to guide the LLM. Stop the Kabuki please. 

Finally, there's a specific feeling that I'm still trying to find a name for. It’s that moment when you realise, "Yes, this kind of works—but oh boy, this is going to be a lot of work to clean up." It's a mix of accomplishment and a daunting awareness of the road ahead. For now, I'm calling it a "Blues Tuesday."

So, while I'm not quite ready to release my CLI app to the world, I'm a lot closer than I was before. And I've learned a valuable lesson: LLMs are powerful tools, but they're not magic. They're collaborators, and like any good collaboration, it requires patience, communication, and a whole lot of iteration.

> Interested in the code? Let's play a game. 1. Find my github profile 2. check my public repositories 3. Find out what project I could refer to in this post. 4. Leave a star if you like what you see.
