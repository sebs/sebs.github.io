---
layout: post
title: "Less Dependencies, Less Problems: How to keep node.js Package Footprint Minimal"
date: 2025-09-29 11:08:41 +0000
permalink: "/2025/09/29/less-dependencies-less-problems-how-to-keep-node-js-package-footprint-minimal/"
description: "Why the Bus Factor Analyzer CLI uses only five npm dependencies, such as commander, ajv and simple-git, to cut supply chain risk and ownership costs."
tags: [supply-chain-security, developer-tooling, web-development]
og_type: article
image: "/assets/posts/less-dependencies-less-problems-how-to-keep-node-js-package-footprint-minimal/og.jpg"
devto_url: "https://dev.to/sebs/less-dependencies-less-problems-how-to-keep-nodejs-package-footprint-minimal-50o"
render_with_liquid: false
---

The [Bus Factor Analyzer](https://github.com/sebs/bussybussy) takes a deliberately minimalist approach to dependencies. With only five carefully selected packages, this tool tries to build build robust software without dragging in half the NPM ecosystem. Not wanting to get regular pings about broken dependencies is a desire I picked up when releasing way more to NPM than I do today. 

> Keep in mind: The tool is experimental, not meant for production use has no educational purpose beyond the dependencies here. It is something I needed, so I created it.

## The Reality of Modern Dependency Management

The Shai-Hulud worm (that [supply chain attack I wrote about](https://dev.to/sebs/facing-the-shai-hulud-worm-where-the-hell-is-easystreet-4b60)) showed us how vulnerabilities propagate through interconnected dependencies. Each package you add isn't just code—it's trust. Trust in maintainers you've never met, in their security practices, and in their own dependency choices. One package might bring 50 transitive dependencies, each a potential entry point for compromise.

Bus Factor Analyzer's dependency strategy is minimalism:

```json
"dependencies": {
  "commander": "14.0.1",
  "ajv": "8.17.1",
  "chalk": "5.6.2",
  "simple-git": "3.28.0",
  "fs-extra": "11.3.2"
}
```

**Commander (14.0.1)** - A battle-tested CLI framework that's been around since 2011. Instead of rolling our own argument parser or using heavier alternatives, Commander provides just enough structure without the bloat. Its maturity means fewer surprises lurking beneath.

**AJV (8.17.1)** - JSON schema validation done right. Rather than manually validating data structures (error-prone) or importing a heavyweight validation framework, AJV compiles schemas into performant JavaScript. It's focused, fast, and does one thing well.

**Chalk (5.6.2)** - Terminal styling that respects the principle of progressive enhancement. The tool works without colors, but Chalk makes output more readable when available. No complex terminal manipulation libraries, no curses dependencies—just colors when you need them.

**Simple-git (3.28.0)** - The key word is "simple." Instead of shelling out to git directly (security risks, platform differences) or using the massive nodegit native bindings, simple-git provides a clean abstraction over the git CLI. It's the Goldilocks choice: not too raw, not too heavy.

**fs-extra (11.3.2)** - Node's fs module with promises and convenience methods. Rather than pulling in multiple utility libraries for file operations, fs-extra consolidates common patterns. One dependency instead of five.

## The TCO Mathematics

Total Cost of Ownership isn't just about the initial `npm install`:

1. **Security Audits**: 17 dependencies vs 500 means a multitude fewer security advisories to evaluate
2. **Update Fatigue**: Each dependency update requires testing. Fewer dependencies = fewer breaking changes
3. **Attack Surface**: With minimal dependencies, `npm audit` stays green longer
4. **Debugging Time**: When something breaks, the suspect list is short
5. **Build Times**: Fewer packages = faster CI/CD pipelines
6. **Disk Footprint**: The entire node_modules is under 50MB, not 500MB

Sometimes the best decision is not to participate. Every dependency we *didn't* add is:

- A supply chain attack that can't reach us
- A breaking change that won't affect us
- A maintenance burden we'll never carry
- A security audit we'll never need to run

This tool could have been "fancier" with more dependencies:

- A CLI framework with animated spinners and progress bars
- A full ORM for data management
- A templating engine for output formatting
- A logging framework with multiple transports


But experience with supply chain attacks like Shai-Hulud has taught us that lean and secure beats feature-rich and vulnerable. The Bus Factor Analyzer does exactly what it promises—analyzes repository bus factors—without unnecessary complexity. In a world where a simple "hello world" app can transitively pull in hundreds of dependencies, creating the Bus Factor Analyzer was a reminder that thoughtful, minimal dependency selection isn't just possible—it's pragmatic. By choosing mature, focused libraries and resisting the temptation to add "just one more package," we maintain security and reduce complexity.
