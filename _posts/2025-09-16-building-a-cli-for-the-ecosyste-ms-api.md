---
layout: post
title: "Building a CLI for the Ecosyste.ms API"
date: 2025-09-16 13:12:50 +0000
permalink: "/2025/09/16/building-a-cli-for-the-ecosyste-ms-api/"
description: "Recently, I have been working on a small side project that involves creating a command-line interface..."
tags: [opensource, security, supplychain]
og_type: article
devto_url: "https://dev.to/sebs/building-a-cli-for-the-ecosystems-api-1d4a"
render_with_liquid: false
---
Recently, I have been working on a small side project that involves creating a command-line interface for the [ecosyste.ms](https://ecosyste.ms) platform.  We had started to investigate different sources of metadata for [purl-patrol](https://github.com/MaibornWolff/purl-patrol) and stumbled over ecosyste.ms.

If you've never heard of ecosyste.ms, it's essentially a huge dataset about open source software that keeps track of repositories, packages, dependencies, and other fascinating metadata throughout the whole open source ecosystem.

 The problem is that even though ecosyste.ms has some fantastic web APIs, I was always wanting to use the terminal to query them—for example, in a pipeline or build script.  You understand that there are instances when you simply want to verify something quickly without launching a browser or creating a custom script.

 ## Why Create Another CLI?

 Packages, repositories, academic papers mentioning open source projects, and even tracking "awesome lists" on GitHub are among the various APIs exposed by the ecosyste.ms platform.  While it makes sense from their point of view, each API has its own peculiarities and data structures, which can be a little overwhelming when all you want to do is retrieve some data.

 I was looking for a command-line tool that would combine all of these distinct APIs.  Something where I could type `ecosystems packages package npmjs.org react` to learn more about the React package, or `ecosystems repos topics` to see what subjects are popular.  All of that in a "terminal friendly" manner.

 ## Maintaining Simplicity

 The CLI is designed to be simple to use and is built in Python.  The CLI commands should feel fairly natural to anyone who is familiar with the ecosyste.ms website because I structured them to match the structure of the APIs.

 Making the output useful in various contexts was one of the things I worked on.  A nice, readable table is provided by default, but if you want to pipe the data into other tools, you can also obtain it as JSON, TSV, or JSONL.  Being able to do `ecosystems packages package npmjs.org react --format json | jq '.name'` and get precisely what you need is gratifying.

 ## MCP Integration: Revolutionary

 I recently added experimental support for Model Context Protocol (MCP), which is one of the coolest features.  Now that every command in the CLI is an MCP tool, any ecosyste.ms functionality can be directly invoked by AI assistants and other tools.  Do you want to ask an AI about the dependencies in React?  It can now directly call the ecosystem's CLI and retrieve structured data.

 This feature is more than just a nice-to-have; it completely alters the tool's functionality.  The complete ecosyste.ms dataset is made available to AI workflows, automated scripts, and other programmatic consumers rather than being restricted to manual command-line usage.  The MCP interface now offers all commands, from `repos topics` to `papers mentions`.

 ## Next Steps

 For my purposes, the tool is functioning fairly well, but there is always room for improvement and testing.  We will soon begin releasing it via PyPI after hardening what is currently there. 

 This little project has been enjoyable; it's the kind of thing that fulfills your own desires and, ideally, benefits others.  Additionally, I now have a much better understanding of the volume of data that passes through the open source ecosystem on a daily basis as a result of working with the ecosyste.ms APIs.

 ## A New Phase

 This CLI tool has been officially adopted by the ecosyste.ms project, which is incredibly exciting news!  In addition to adopting the codebase, they are also offering assistance with continuing development and maintenance.  This means that my "moonshining" will finally turn into something useful, and the tool will receive the resources and attention it needs to join the ecosystem of ecosyste.ms.

 It's amazing to have the support of the ecosyste.ms team.  They see the CLI (and particularly the MCP integration) as an essential component of their mission to make open source intelligence more accessible to developers, researchers, and AI systems alike. They also recognize the importance of making their data accessible through a variety of interfaces, and they received a toy they wanted without really asking. 

 The code is available on [GitHub](https://github.com/ecosyste-ms/ecosyste_ms_cli) for those who are interested.  Please feel free to look it over or even contribute; with official backing, this small side project could grow into something much more!
