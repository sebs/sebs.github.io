---
layout: post
title: "20 Questions to Ask an LLM About Your Codebase (That You Probably Won't Like the Answers To)"
date: 2025-08-04 18:50:43 +0000
permalink: "/2025/08/04/20-questions-to-ask-an-llm-about-your-codebase-that-you-probably-wont-like-the/"
description: "Twenty uncomfortable questions to ask an LLM about your codebase, from coupling and complexity to technical debt, weak tests, security and bus factor."
tags: [testing-and-quality, ai-assisted-development]
og_type: article
devto_url: "https://dev.to/sebs/20-questions-to-ask-an-llm-about-your-codebase-that-you-probably-wont-like-the-answers-to-2h9k"
render_with_liquid: false
---

**LLM generated or not. Stop letting a machine generate only the words that you want to hear and start with some words, that most of us should hear!**

1. **"What percentage of my functions are doing more than one thing, violating the Single Responsibility Principle?"**
   - Prepare to discover that most of your "simple" functions are actually doing 3-5 different things.

2. **"How many of my classes have more than 10 dependencies, and what does this say about coupling?"**
   - You'll likely find out your "modular" architecture is actually a tangled web of dependencies.

3. **"What's the actual cyclomatic complexity of my most important functions, and how many are unmaintainable?"**
   - That function you're proud of? It probably has a complexity score that would make computer science professors weep.

4. **"How much of my codebase consists of duplicated logic that should be abstracted?"**
   - Spoiler alert: You've probably copy-pasted the same logic in 15 different places with slight variations.

5. **"What percentage of my variable and function names would be considered unclear or misleading?"**
   - Turns out `data`, `temp`, `thing`, and `doStuff()` aren't as self-documenting as you thought.

## Technical Debt & Maintenance

6. **"How many TODO comments do I have, and what's the oldest one?"**
   - That TODO from 2019 about "refactoring this later" is still there, isn't it?

7. **"What's the real cost of my technical debt in terms of development velocity?"**
   - You'll discover that "quick fix" from last year is now costing you 3x the development time.

8. **"How many of my dependencies are outdated, deprecated, or have known security vulnerabilities?"**
   - Your package.json probably looks like an archaeological dig site.

9. **"What percentage of my codebase would need to be rewritten to follow current best practices?"**
   - The answer is probably "most of it," and that hurts.

10. **"How many magic numbers and hardcoded values are scattered throughout my code?"**
    - You'll find constants that should have been configurable buried in the depths of your business logic.

11. **"What's my actual test coverage, and how much of it is just testing trivial getters/setters?"**
    - That 80% coverage number drops to 30% when you exclude meaningless tests.

12. **"How many of my tests would fail if I changed the implementation without changing the behavior?"**
    - Your tests are probably testing implementation details rather than actual behavior.

13. **"What happens to my application when external services are down or slow?"**
    - You'll discover your app becomes a house of cards when the third-party API hiccups.

14. **"How many potential race conditions and concurrency issues exist in my code?"**
    - That multithreaded code you wrote? It's probably a ticking time bomb.

15. **"What are ways my application could be exploited by malicious input?"**
    - SQL injection, XSS, and other vulnerabilities are probably hiding in plain sight.

16. **"How many performance bottlenecks exist that I'm not aware of?"**
    - That innocent-looking loop is probably doing O(n²) database queries.

17. **"What sensitive data am I accidentally logging or exposing?"**
    - Your logs probably contain more passwords and API keys than you'd like to admit.

18. **"How would my application perform under 10x the current load?"**
    - Spoiler: It wouldn't. At all.

19. **"If I left the company tomorrow, how long would it take someone to understand and maintain my code?"**
    - The answer is measured in months, not days, and that's terrifying.

20. **"What critical business logic exists only in my head and nowhere in the documentation?"**
    - That "obvious" workflow that everyone just "knows"? Nobody actually knows it except you.
