---
layout: post
title: "I Was So Angry, I Built My Own"
date: 2025-05-28 15:24:53 +0000
permalink: "/2025/05/28/i-was-so-angry-i-built-my-own/"
description: "A self-built project management tool born of frustration: markdown stories, relative weight estimates, ADRs, post-mortems, DORA and Kanban metrics."
tags: [developer-tooling, agile-practices]
og_type: article
series: "I was so angry I built my own"
devto_url: "https://dev.to/sebs/i-was-so-angry-i-built-my-own-4mj1"
render_with_liquid: false
---
Frustration often breeds innovation. After years of wrestling with project management tools that never quite fit my needs, I reached my breaking point. The tools were either too complex, too rigid, or missing critical features that my teams needed. So I did what any frustrated developer would do – I built my own.

## Markdown Simplicity in a WYSIWYG World

Most project management tools force you into their proprietary editors with fancy formatting options that ultimately create more problems than they solve. All I wanted was to edit markdown files – simple, portable, version-control friendly text that everyone already understands. Why should documenting a story be more complicated than writing code?


![Markdown editor with YAML front matter for a user story beside a metadata panel showing benefit, penalty, estimate and risk](/assets/posts/i-was-so-angry-i-built-my-own/qvrobwm9r7bes3vwt9o2.webp)



My solution: a project management system where everything is markdown at its core. Stories, documentation, comments – all just markdown files that can be edited with any text editor or through a clean interface that doesn't get in your way.

## Beyond the Tyranny of Story Points

The industry's obsession with story points as the one true estimation metric has always felt limiting. Development work is multidimensional, so why shouldn't our estimates reflect that?

I implemented a relative weight system with four key metrics:
- **Value**: What benefit does this bring to users/business?
- **Penalty**: What's the cost of not doing this work?
- **Effort**: How much work is required?
- **Risk**: How uncertain or complex is the implementation?



This approach gives teams a more nuanced way to prioritize work and makes trade-offs explicit rather than hidden.

## Documentation as First-Class Citizens

In most tools, Architecture Decision Records (ADRs) and Post-Mortems are afterthoughts – if they exist at all. They're typically buried in wikis or shared drives, disconnected from the work they relate to.

![Kanban board of the self-built tool with Backlog, Ready and In Progress columns holding user story cards](/assets/posts/i-was-so-angry-i-built-my-own/9d824xpo3f5vp3no9n58.webp)

I built a system where ADRs and Post-Mortems are just as important as stories. They're versioned, linked to related work items, and follow the same workflow processes. This creates a connected knowledge base that evolves with your project, not separate from it.

## Closing the Feedback Loop

One of my biggest frustrations was the lack of feedback from production systems. We'd deploy features and then... silence. The project management tool had no idea what happened next.

My solution aims to integrate deployment data and production metrics directly into the workflow. When a story is deployed, we automatically track:
- Deployment frequency
- Lead time for changes
- Mean time to restore service
- Change failure rate

These DORA metrics provide immediate feedback on how our development practices are working, creating a cycle of feedback.

## Kanban That Actually Measures

Most Kanban implementations are just pretty boards with columns. They lack the metrics that make Kanban powerful: cycle time, throughput, and work in progress limits.

I built Kanban metrics into the core of the system, automatically tracking how work flows through the process and highlighting bottlenecks. The board isn't just a visualization – it's a data collection tool that helps teams continuously improve.

## The Power of Large Context Windows

Building this system became much more feasible with the advent of large context window AI models. I could feed in CSV files, Excel spreadsheets, and entire codebases to generate comprehensive documentation, user stories, and even implementation plans.

This dramatically accelerated development and ensured consistency across the entire system. The AI could understand the relationships between different components and help generate coherent documentation that reflected those connections. 

Having everything structured and a application that lends it self well to 'tool usage' - this could be a starting point for a lot of help. However - I don't want to cheap out and get a bunch of things ironed out before integrating some 3rd party agentic api.  

## Personal Tools for Personal Workflows

What makes this project special is that I'm building it primarily for myself. I'm not trying to please every user or cater to enterprise requirements – I'm solving my own problems in exactly the way I want them solved. This freedom has allowed me to experiment with approaches that commercial tools would never consider.


What started as a frustration-fueled side project has the potential to become my personal competitive advantage. I move faster, make better decisions, and have a complete history of why I built what I built – all while creating an environment where AI agents can provide increasingly valuable assistance.

Sometimes the best solution isn't finding the perfect tool – it's building exactly what you need. And sometimes, a little anger is all the motivation required.
