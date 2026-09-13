---
layout: post
title: "Taking LLMs to (code) town - part II. Creating a vanilla.js web component toolchain from ground up"
date: 2025-01-02 21:49:19 +0000
permalink: "/2025/01/02/taking-llms-to-code-town-part-ii-creating-a-vanilla-js-web-component-toolchain/"
description: "A lean toolchain for vanilla web components built on TypeScript, JSDOM, memfs and the Node test runner, developed in 40 hours with the Windsurf AI editor."
tags: [web-development, ai-assisted-development, developer-tooling]
og_type: article
image: "/assets/posts/taking-llms-to-code-town-part-ii-creating-a-vanilla-js-web-component-toolchain/og.jpg"
devto_url: "https://dev.to/sebs/taking-llms-to-code-town-part-ii-creating-a-vanillajs-web-component-toolchain-from-ground-up-mi9"
render_with_liquid: false
---
I have been developing vanilla web components using a very minimal toolchain, primarily consisting of TypeScript and jsdom, for a number of years as a on-going experiment now. **Goal**: At runtime, do not depend on anything and exploit web component properties where the concept shines: small, as stateless as possible, elements.

In a gist, it seems simple: write TypeScript code, make JavaScript out of it, and 'profit.' In theory. Additionally, bundlers, compilers, and tree shaking are involved. Vendor lock-in can easily ensnare you. Just look back at what <insert your frontend framework> just released in updates in the last 2 years and apply this information as a projection of updates to come in the future. This approach may not always yield positive outcomes. Many software system components, including very basic UI elements, should have separate and more boring update lifecycles, in my opinion. Not all web frontends, such as configuration UIs on edge devices, are easily updatable.

The aim of the web component spec is not to supplant frameworks but to offer a variety of ready-to-use elements that lessen dependency on them. Web Components merely tackle a specific set of issues that React, Angular, and other frameworks also attempt to tackle, albeit at the expense of being confined within the development processes, general idioms, and career paths of these frameworks. Put in simple terms: When your UX team publishes a web component catalogue based on Tailwind and React, it will be much harder to use other frameworks or even plain HTML. 

## Why re-invent the wheel?

Whenever I adopt a new and modern framework, it seems to be a different combination of already existing things with various layers of packages building on packages and adding other layers of abstraction. I don't mind abstraction in software; up to a certain point, it makes life easy. However, when my understanding of the current standards stagnates due to the abstraction of information, I find it difficult to make informed decisions about information architecture. Interfaces are the foundation of everything, which is why they are so crucial.

Today's toolchains come with a dependency tree that is a bit too huge for my taste. This presents a significant maintenance challenge: frameworks evolve quickly, frequently release updates, and the constant need for more dependencies and updates can be burdensome when operating in production environments. I would like to understand why these frameworks are so "heavy."

Then there's my allergy to bundlers: TypeScript already exists for simple, stateless components like 'bundling,' 'tree-shaking,' and methods, and it primarily addresses the issues associated with relying on the SPA pattern. I am aware that this will significantly reduce the features at my disposal, but I am prepared to bear the consequences and restore my sanity.

I'd like to shy away from runtime components as well. Runtime components create a dependency on the end-user side, which I would prefer to avoid. In the end, it would be the project's responsibility to maintain it. Let's see how far I can get without it. 

## Ground rules. 

This is not a drill: UHU (under 100) rules apply: We stay under the dependency limit for the tools required to run the TDD loop. This limit forces us to either build certain features or exclude others. This limit will prevent me from developing an excessively extensive feature set solely for the purpose of navigating through third-party interfaces.

I want to focus on TypeScript and research its features a bit more. Often, we use TypeScript without giving it much thought, just throwing configuration at it until it works. Turns out it is feature-rich and very, very, very well documented. 

JSODM is my choice of test environment for the components. The implementation of the web components standard is an ongoing discussion, and I guess it is still progressing. The method has theoretical limits, but I want to see how far I can push it.

Node has delivered tooling for testing, and I want to explore this a bit more as well. Performance is where it needs to be, and I am very productive with it so far. In the end, I want to build a bunch of vanilla.js web components with no runtime dependency and the tooling to do so while I am on it. Being able to change the source code of a component and have a clear TDD loop against a simulated DOM in one go should be feasible. 

## The experience 

Shoutout to Windsurf.Idea: It took approximately 40 hours to bring the project to its current state. Windsurf really helps with refactoring and making 'opinionated changes' to codebases. I began with the concept of mounting a web component to a JSDOM object, which would allow for the installation of components in RAM. Another aspect of the process involves utilizing TypeScript. Before I can mount my TypeScript source file to JSDOM, I still need to turn it into proper JavaScript. I began experimenting with the TS compiler, discovering that it was possible to compile while mounting a component. But it was slow. All the practicalities hit now: What about many tests for more than just one component? Well, there are caches (which I have not yet dabbled with) or in-memory filesystems to speed up build time.

[![Toolchain diagram: my-component.ts is compiled to JS and a JSDOM test helper, and passed to doc-gen to produce component docs](/assets/posts/taking-llms-to-code-town-part-ii-creating-a-vanilla-js-web-component-toolchain/image-1.png)](https://mermaid.live/edit#pako:eNplUb1uwyAQfhXrJkey-wAeOnmqFHVIp4oFwdnGMpwFh6ooyrsXGzuNUxb4fu67A26gSCM00E30owbpufhqhSvSCl6V9lorsjM5dPzG4ZSVMRyFcRcWykzoM9Kk6h5dBoyB6wGneVc_Lu3nuSzX7bTVaxVtCpRsyJWP_CUoGR5TFXX9_tJqR6s0hlfzYZINZOGpoXB72SHt3-BPxGpYb5AlqMCit9Lo9KK3hRPAA1oU0KSjxk7GiQUId09WGZkuV6egYR-xgjhrydga2XtpoenkFBI7S_dN9IdRGyZ_zr-2fl4FnmI_bI77L_WbmAc)

There is a documentation angle to the whole effort as well. It should be simple to turn the component into a working demo—preferably by just using doc tags in the component's source code. TSDOC is a useful tool to hook up to TypeScript documentation parsing and add your own tags, for example. In the end, this is where the real rabbit hole starts to open: creating a small working toolchain supporting me building a bunch of vanilla web components that are not trivial and still make sense. 

After conducting some research, I discovered that the topic of audio web components is intriguing: it involves a significant amount of mathematics, and there are numerous examples that illustrate various aspects of technology, age, and other technological factors. Web MIDI has really taken off in terms of providing a viable platform to configure all types of audio devices, and the use cases warrant it. I will now assess the extent to which I can establish a component foundation using the developed tooling.

## Results

I am super confident that Windsurf.ai or other tools built the same way can help me with my efforts in the future. Early CodePilot with ChatGPT primarily motivated my last attempt, and Windsurf feels like a true upgrade. I've used 40% of my credits this month, and the results are worth it. I am not one to hand out compliments to GenML tools easily, but in the case of Windsurf, I really learned a lot using this tool. The interaction with the LLM chat and codebase was satisfactory, providing me with ample time to review the specifications, make informed decisions, and store a wealth of new information in my wetware while working on a project.

The codebase is intriguing in its minimalism. In fact, the tooling for the main TDD loop has fewer than 100 dependencies, which also appears to encompass doc generation. This essentially involves the use of commander.js, TypeScript, TypeDoc, and memfs.

Using an in-memory filesystem for TypeScript compilation and speeding up all procedures was a significant challenge. I anticipate further improvements in build time through the caching of results during test execution.

The CLI application can ship the underlying framework. Unit tests cover the majority (c) of the classes, making changes feel effortless despite their complexities. I get the irony that I am building another layer over existing tooling to simplify development.

## Links

* [The codebase described in this post](https://github.com/sebs/banira)
* [Typescript Virtual Filesystem](https://www.typescriptlang.org/dev/typescript-vfs/)
* [Node Test](https://nodejs.org/api/test.html)
* [Typescript Transformer Handbook](https://github.com/itsdouges/typescript-transformer-handbook)
* [TSDoc Parser](https://github.com/microsoft/tsdoc/blob/main/tsdoc/src/parser/TSDocParser.ts)
* [MemFS](https://github.com/streamich/memfs)
* [Codeium Windsurf](https://codeium.com/windsurf)
