---
layout: post
title: "Agentic \"Agile\""
date: 2025-06-19 09:52:32 +0000
permalink: "/2025/06/19/agentic-agile/"
description: "Experiments with AI agents in agile work: generating backlogs, relative estimation, Definition of Ready checks, Gherkin, backlog paths and post-mortems."
tags: [agile-practices, ai-assisted-development]
og_type: article
devto_url: "https://dev.to/sebs/agentic-agile-4386"
render_with_liquid: false
---
Let's be honest: the "ceremonies" and processes of Agile can often feel like a drag. The endless backlog grooming, the contentious estimation sessions, the meticulous documentation—it's necessary work, but it's work that drains energy from what we love most: building great software.

What if we could automate the toil while amplifying the strategy?

Enter **Agentic Agile**. This isn't just about using a ChatGPT window to rephrase a user story. This is about employing sophisticated AI agents as active and persistent helpers of your development team. These agents understand context, learn from your project's history, and execute complex tasks that are traditionally manual, time-consuming, and prone to human error.

Let's explore how I experimented with "Agentic AI" in my dev lifecycle,

### 1. The Spark: Turning a Vague Idea into a 100-Item Backlog

Every great product starts as a simple idea. But turning "an app for local gardeners to trade plants" into a workable backlog is a mountain of work. An AI Agent can act as a tireless Business Analyst.

Using a technique called **Metaprompting**, you don't just give the AI a command; you give it a role, a process, and a goal.

### 2. The Art of Estimation: Reasoned, Relative, and Real-Time

Estimation is often the most dreaded part of sprint planning. It's subjective, full of debate, and often wrong. An Agentic approach brings data-driven sanity to the process.

*   **Contextual Comparison:** Instead of estimating in a vacuum, the agent analyzes the *entire 100-item backlog*. It can reason: "Story A (Create Login Button) is less complex than Story B (Implement OAuth 2.0 Flow), but more complex than Story C (Change Button Color). Therefore, if B is an 8, A is likely a 3, and C is a 1." It provides its reasoning, making the process transparent. The decision to use these new estimates is up to me. 

*   **Re-estimation on Change:** When a user story is modified, the agent automatically detects the change and its potential ripple effects. If the requirements for Story B (OAuth) are simplified, it will flag the story for re-estimation and even suggest a new, lower value based on the reduced scope.

*   **Learning from Reality:** This is the game-changer. When your team completes a 5-point story about a "simple API integration" in twice the expected time, the agent *learns*. It logs this. The next time a similar API integration story appears, the agent will reason: "Historically, stories of this type have been underestimated. Based on the performance on Story X, I recommend increasing this estimate from 5 to 8." It closes the feedback loop between estimation and rqeality. Adding information from Bugtrackers and Changelogs helps as well. 

### 3. Enforcing Quality: The Definition of Ready and Gherkin Syntax

A poorly defined story is a recipe for disaster. An agent can serve as a vigilant gatekeeper.

*   **Checking the "Definition of Ready" (DoR):** You provide the agent with your team's DoR checklist (e.g., "Must have clear acceptance criteria," "Must have a business value statement"). The agent scans every story before sprint planning. If a story is missing acceptance criteria, it won't just flag it—it will attempt to *draft* the criteria based on the story's description and ask the Product Owner for confirmation. Make Sure to have a good git history on the DoR, so the agent knows why things were changed. So it does not only know the State of this file, but it past as well. 

*   **Converting Requirements to Gherkin:** Clear requirements prevent bugs. An agent can instantly translate a story's acceptance criteria into well structured Gherkin syntax. This creates an unambiguous, testable specification that bridges the communication gap between product, development, and QA.

### 4. Strategic Navigation: Charting the Course to Completion

A 100-item backlog is a sea of possibilities. Which path do you take?

*   **Calculating Optimal Paths:** An agent can analyze dependencies, priorities, and story estimates to propose multiple strategic paths through the backlog (using genetic algos - llm proposed the code to export the  backlog with all informations and then make it available for the genetic algo. 
    *   **Path A: Time-to-Market Focus:** The absolute minimum set of stories needed for a functional MVP.
    *   **Path B: High-Value First:** Prioritizes stories that deliver the most significant business value early on.
    *   **Path C: Risk Mitigation:** Tackles the most technically challenging or uncertain stories first to de-risk the project.

*   **Adapting to Architectural Changes:** When an architect adds an **Architecture Decision Record (ADR)**—like "We will use a serverless architecture for all new APIs"—the agent immediately scans the backlog. It identifies every story impacted by this decision, flags them for review, and suggests modifications to align with the new architectural standard.

### 5. The Full Cycle: Story Management and Post-Mortems

The agent's work doesn't stop once development begins.

*   **Intelligent Story Splitting:** When the team decides a 13-point story is too large for a single sprint, the agent can propose logical ways to split it. It can break "Build User Profile" into "Backend: Create Profile API Endpoints," "Frontend: Build Profile View," and "Frontend: Build Profile Edit Form," providing initial estimates for each new, smaller story.

*   **Kick-ass Post-Mortems:** When a critical bug occurs, the agent can be a world-class detective. It can be tasked to pull data from Git commits, Jira tickets, monitoring logs, and even Slack channel discussions related to the incident - if it is not connected, it can give you the queries for your O11y systems and logs to collect data. It then assembles a structured, blameless post-mortem document including a timeline of events, contributing factors, root cause analysis, and suggested action items to prevent recurrence.

*   **Creating a Clear Product Vision:** A strong vision aligns the team. By feeding an agent market research, user personas, and business goals, it can generate multiple compelling, inspiring product vision statements. This gives leadership a powerful starting point to refine and rally the team around a shared North Star.

### The Path forward

I am not sure where all this leads us, but I am deeply aware for the fact that there is no real market  - yet - for this kind of software.  People want to generate Code, Music and Images - but maybe there is a bunch of grunt work to be found, that can be automated away.  
I understood so far, that documentation and software should live in one repos if that is feasible. Having all that in one context is a great enabler for methods like this.
