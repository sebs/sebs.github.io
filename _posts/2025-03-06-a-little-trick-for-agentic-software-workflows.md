---
layout: post
title: "A little trick for 'Agentic Software Workflows'"
date: 2025-03-06 12:29:09 +0000
permalink: "/2025/03/06/a-little-trick-for-agentic-software-workflows/"
description: "While working on the next version of the Pair-Programming Workshop, I recently tackled the task of..."
tags: []
og_type: article
devto_url: "https://dev.to/sebs/a-little-trick-for-agentic-software-dev-2clc"
render_with_liquid: false
---
While working on the next version of the Pair-Programming Workshop, I recently tackled the task of updating 120 markdown files in a software documentation repo, which involved adding a category, grouping documents with tags, and setting slugs for URLs on the actual website. Initially, I relied on the agentic features of my IDE, but I quickly found that this method was slow, despite being consistent enough.

To speed things up, I decided to utilize a coding agent to generate a script to handle the updates. I'm pleased to say the script worked perfectly on the first try. Here’s how I structured the solution:

1. Adding a Category: The script changed a specific string in each file to reflect the new category effortlessly. I set the category to identify glossary items.

2. Using NLTK for Feature Extraction: I employed the Natural Language Toolkit (NLTK) for feature extraction on the markdown documents. This process analyzed the content, reducing it to the top ten features. We saved the results into a CSV or markdown table. Then, I had the coding agent read this table, adding an extra column with three proposed tags for each document. This consolidated what would have been 120 separate calls into one longer-running operation. The agent also created a script to apply those tags, making the initial code closely aligned with the final requirements.

3. Setting Up the Slug: I included the slug setup in the initial script, generating it based on the selected category and the first letter of each document's title. This integration allowed for clean, SEO-friendly URLs and simplified the overall workflow.

By using the coding agent to create code that completed the task, I achieved better results with faster execution compared to just letting the agent handle everything on its own. As a bonus, this approach consumed much less compute for inference, as future executions of the scripts are relatively cheap.

## What I Learned

A few key takeaways 

Getting too comfortable with just saying “make it so” to the agent can lead to passivity—you end up watching the computer do its thing without engaging. Being hands-on in the process adds real value and gets you from A to B faster.

Switching between intermediary formats like lists and CSVs is invaluable. By selecting and structuring data yourself, you can pass it to the system in a much more efficient way.

This method also supports the creation of reusable tooling. For instance, the tag functionality is easy to apply to new content, allowing you to scale operations without reinventing the wheel.

If similar tasks arise in the future, consider turning your script into a CLI application. This will streamline the application process for future updates without the need for complete rework.
