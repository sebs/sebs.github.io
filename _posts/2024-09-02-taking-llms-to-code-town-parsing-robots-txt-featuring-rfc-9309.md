---
layout: post
title: "Taking LLMs to (code) town: parsing robots.txt featuring RFC 9309"
date: 2024-09-02 22:03:38 +0000
permalink: "/2024/09/02/taking-llms-to-code-town-parsing-robots-txt-featuring-rfc-9309/"
description: "Recently, large language models (LLMs) have gained significant attention as tools that can..."
tags: [chatgpt, development, rfc]
og_type: article
devto_url: "https://dev.to/sebs/taking-llms-to-code-town-parsing-robotstxt-featuring-rfc-9309-3g64"
render_with_liquid: false
---
Recently, large language models (LLMs) have gained significant attention as tools that can potentially solve complex IT problems and even replace some aspects of an engineer's workflow. From automating code generation to debugging, these models are advertised as the next step in software development. But how well do they actually perform when put to the test? Are they truly capable of tackling intricate problems, or are they simply overhyped?

I decided to explore this by putting an LLM to work on a real-world problem: building a robots.txt parser. Instead of diving into endless discussions on forums about the capabilities and limitations of LLMs, I chose to see for myself how well they could handle this specific task. In this article, I'll walk you through the problem, the challenges faced, and the ultimate effectiveness of using LLMs for such a task.

## The Problem

The robots.txt file is a small part of a website's interaction with search engines. It provides directives to web crawlers, telling them which parts of a site they can and cannot access. While the syntax of robots.txt is relatively simple, implementing a parser that correctly interprets all the rules can be surprisingly complex.

The robots.txt file specification is outlined in RFC 9309, which is based on ten other RFCs, including one from Tim Berners-Lee himself. Although the syntax may seem easy to learn at first glance, it quickly becomes a "hard to master" type of problem. Many implementations attempt to parse all the directives in the robots.txt file and then compare them against a given URL using a series of conditionals. The directives can be grouped by user agent, making the problem even more challenging.

Google has a comprehensive write-up on the subject, which is highly recommended for anyone interested in the details of how a robots.txt file works. However, the intricacies involved in correctly implementing RFC 9309 make this a tough problem for an LLM to solve. It’s not as straightforward as it might appear, and the matcher syntax (using characters like #, *, and $) adds another layer of complexity.

Given these challenges, I wanted to see how well an LLM like ChatGPT could handle this task.

## The 'Solution'

I began by asking ChatGPT to help me build a robots.txt parser. The solution it proposed involved parsing all the directives in the file and comparing them against a given URL to determine whether the URL was allowed to be crawled or not. The model suggested using a map data structure to store URLs and their corresponding directives.

However, this approach quickly ran into issues. The matcher syntax used in robots.txt (such as wildcards) made the map-based solution less effective. The LLM's reliance on stacking conditionals resulted in code that was functional but far from elegant. Moreover, as I tried to complete the implementation, I found that ChatGPT struggled to handle edge cases and required significant back-and-forth discussions to refine the solution.

Despite these challenges, ChatGPT was able to pass an increasing number of unit tests as the dialogue continued. It wasn't a perfect solution, but it was functional to a degree. However, the process highlighted some fundamental limitations of using LLMs for complex coding tasks.

## The Caveats of the LLM-Generated Solution

While the map/list solution proposed by ChatGPT was functional, it was neither efficient nor elegant. This approach is commonly upvoted in forums like Stack Overflow, where similar solutions are often proposed. However, just because something is popular doesn't mean it's the best solution.

In this case, storing the directives in a tree data structure and prioritizing validation time over startup time would likely result in a more computationally sound and elegant solution. Such an approach might be more complex in theory, but it could significantly reduce the number of conditionals required, making the code cleaner and more maintainable.

Another potential solution would involve parsing the robots.txt file using a parser generated with [Peggy](https://peggyjs.org/) (a modern parser generator), based on the RFCs’ Augmented Backus-Naur Form (ABNF) syntax description. This method would ensure that all aspects of the specification are covered. While I have yet to try this approach, it represents another avenue for getting to the solution.

Throughout this process, it became clear that convincing an LLM to diverge from well-established patterns and explore alternative approaches is challenging. The model tends to base its ideas on a small set of prominent answers and well-known implementations, making it difficult to guide it towards more innovative or less common solutions. At some point I got tired of it and went along. Normally not my cup of tea. 

## The Human Problem

One of the most frustrating aspects of working with LLMs in this context is their reliance on widely accepted answers. LLMs are trained on vast amounts of data, much of which comes from sources like Stack Overflow. While these sources are valuable, they also reflect the limitations of the broader programming community.

Many of us are guilty of resorting to quick fixes and stacking conditionals rather than striving for more elegant, complete solutions. This tendency is deeply ingrained in the DNA of LLMs, leading them to produce results that are often just "good enough" rather than elegant and maybe a little exceptional.

In my experience, the learning loop with an LLM is broken. Rather than learning and refining my skills, I found myself spending more time trying to get the LLM to produce a solution that met my standards. The model's tendency to generate code based on popular but mediocre solutions was a significant hurdle. 

The crux of the issue lies in how LLMs are trained and how we, as developers, use them. LLMs are fed vast amounts of data, but that data is only as good as the contributions from the community. When we rely on LLMs to generate code, we're often getting a reflection of the average quality of solutions found in public repositories and forums. This situation leads to a cycle of mediocrity. We write code, others copy it, and it eventually ends up training the next generation of LLMs. If the original code isn't optimal, the LLM won't be either. As a result, we end up with models that struggle to break free from the conventions and limitations of the human programmers who trained them. 

## Conclusion

In conclusion, my experiment with using an LLM to build a robots.txt parser revealed both the potential and the limitations of these models. While they can be helpful in generating functional code, they often fall short when it comes to producing elegant, efficient, and innovative solutions. The reliance on popular answers and well-known patterns limits their ability to tackle more complex problems effectively.

The true value of LLMs in software development may lie not in their ability to replace engineers but in their potential to assist them. They can serve as a starting point, providing suggestions and generating code snippets, but the heavy lifting—especially for more challenging problems—still requires human insight and creativity.

Ultimately, the success of LLMs in the realm of coding depends on how we use them. If we rely on them solely to produce code, we'll likely end up with solutions that are no better than the average quality of code found in the wild. However, if we use them as tools to augment our own capabilities, guiding them to explore new ideas and approaches, we may unlock their true potential.

As developers, it's essential to remain critical of the solutions generated by LLMs and to push beyond the easy answers. By doing so, we can ensure that our code—and the code generated by the models we train—continues to improve and evolve, rather than stagnating in mediocrity.
