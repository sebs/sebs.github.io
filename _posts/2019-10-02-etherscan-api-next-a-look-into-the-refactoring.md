---
layout: post
title: "etherscan-api@next - a look into the refactoring"
date: 2019-10-02
permalink: "/2019/10/02/etherscan-api-next-a-look-into-the-refactoring/"
description: "I used typescript now for the second time in a commercial project, yet I had not learned it ‘by the book’ and was not getting to the bottom of it. On the…"
tags: [refactoring, typescript, monorepo, lerna, etherscan]
og_type: article
---
I used [typescript](https://www.typescriptlang.org/) now for the second time in a commercial project, yet I had not learned it ‘by the book’ and was not getting to the bottom of it. On the other hand there was serious work to do on the [etherscan-api](https://github.com/sebs/etherscan-api) project and I was able to put the 100 plus hours into the next version of etherscan api to be rewritten in typescript and overcome old problems, mainly in documentation and design.

## Why do a refactoring at all

The etherscan-api client has seen about 43K Downloads in 63 versions so far and there have not been many changes. Earlier this year I killed a lot of other open source projects (about 300+ repositories) and moved them to cold storage in order to allow more focus on those left.

For sure, there was a lack of documentation. I wanted to match the docs at [etherscan.io/apis](https://etherscan.io/apis) as much as possible. What was missing there was a set of examples and not really api docs. These have been added now in form of a vue.js example application that will be filled with examples one by one.

In general a goal of the refactoring (while keeping the outside api stable), was to provide a npm module usable in typescript, node.js and as a browser package. The later 2 should be provided by the already version, but browser packages are not reliably generated and there is no use in typescript yet.

I think learning by doing is a good thing and my practical experience with typescript made me confident to be able to provide working code and a improvement to the already shipped code base. As I stated before: Api should be stable after release but the rest is up to learning and refactoring.

One shortcoming of the old release was the missing set of fixtures and mocked api calls. Every test hit the API and that made releases unstable at best. The used mocha test framework can be configured to do test repeats on failing tests and has configurable timeouts, but that is not fixing the main issue of depending on external servers for development.

The project now has a certain age, and I’d rather do things right than much longer half way. Tests, API docs and Examples must all be there. Developers new to the project should be able to grasp everything easily and not be required to read the (pretty readable) source code to find out how things work.

So there was need for a bit of refactoring

## Assumptions and expectations

I had some assumptions when I started out.

One thing I was expecting is a decent speedup in development when using typescript. Typings make for good auto complete and refactoring should be easier to do and be less error prone to execute.

Using the ava test framework, I was expecting a decent speed up for unit test suite run times (more on that in learnings) and a decent integration into typescript and the resulting compiled Javascript code.

Using a monorepo provided a way to put everything into smaller and simpler components in order to keep the dependencies of the original client codebase small and its lifecycle scripts small.

I wanted 3 ways to use the codebase: Directly in typescript, as a module for node.js using commonJs and as a bundled version in es6.

## Learnings

The typescript development speedup is there, as soon as everything is in place and everything is set up. I tried to use self thought out ‘value objects’ in order to get parameters of classes away from the old strings and numbers patterns and allow for deeper better validation. This turned out to be kind of successful and helps greatly when you want to be sure a parameter is an address on the ethereum network instead of a random string. I quite like this and I am sure the codebase can get a bit more ‘typescripty’.

The toolbox got a bit out of hand I guess. There are at least 3 different test frameworks involved, taking the demo app and the integration tests for the browser into consideration. All that infrastructure work was a bigger upfront investment and took some toll on the performance. However, now it is easy to add a feature and a little more work to add integration tests and a piece of documentation. This allows for a new feature with all documentation in one push.

Ava is pretty slow when it comes to big tests suites, regardless if you track changes on the file system (which would be a good reason for things getting slow) or not. I wrote about 200 tests in small files and I can not see any reason why all this is getting slower and slower to a state where everything feels like a fast integration test suite. Surely there are improvements to find in configuration and setup of the test suite, but this is new to me as a avid user of the mocha framework and I am kind of sure that ava gets kicked in the butt by it’s architecture a bit.

All in all this was a pretty interesting experience: It added some long thought after pieces of testing and documentation additionally to the typescript setup that helps with development. As always, not all tools are as good as the reviews by the respective communities would make you expect.

Bundling was another issue, where not even the authors of the respective bundlers could answer simple questions like how do I transpile a typescript codebase with feature x (x being using global fetch) to a es codebase that just works. I ended up with using es6ify, which is surely a tool that works, but nothing that is really ‘hip’ these days. Maybe this is the best takeaway to close this blogpost with: Even on the ‘hipsterstack’ with latest ‘tech’, sometimes things just need to work. Sometimes I would wish, people would just patch existing tools and not rewrite tools for must being better tools. Get back into your bikesheds and keep the Llamas there.
