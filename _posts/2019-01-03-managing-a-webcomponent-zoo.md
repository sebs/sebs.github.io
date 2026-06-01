---
layout: post
title: "Managing a (webcomponent) Zoo"
date: 2019-01-03
permalink: "/2019/01/03/Managing-a-(webcomponent)-Zoo/"
description: "Developing and shipping webcomponents seems simple at first, but modern frontend stacks come with their own set of challenges: A wide set of browsers…"
tags: [monorepos, javascript, frontend]
og_type: article
---
- [Part 1: Monorepos with learna.js](https://sebs.github.io/blog/managing-a-webcomponent-zoo-monorepo/)
- Part 2: Anatomy of an improved polymer3 component
- Part 3: Scaffolding
- Part 4: TBD

Developing and shipping webcomponents seems simple at first, but modern frontend stacks come with their own set of challenges: A wide set of browsers implements relatively new specs and not everything is set in stone yet and the framework codebases seem to drift, one faster than the other, towards a set of es-x features that allow easy creation and deployment of custom web components with the same architecture. If you set out to create and ship your own set of custom elements this eventually needs organization and strategies to deploy the code with documentation as easy as possible and continuously while adapting to changes in the underlying frameworks and your own set of features.

In this blog post series I will provide you with all the examples and docs to do so yourself.

We will make use of NPM to manage dependencies and publish our own elements while we automatically deploy documentation. API resources will be accessed with OpenAPI clients and can be updated via npm as well if the underlying API changes. Lerna.js will help us to keep the repository count small, speed up development and servers as a general access point for a “one button install” and “one button build”. A component catalogue provides “End-User” documentation to show the components in different contexts. Test Automation helps to keep these old and new browsers at check and keep an eye on a11y issues. Look at a set of self created templates that helps the components to be uniformly structured and dependencies fit your environment.

We will develop a set of web components which will be extracted from 2 demo applications that I provided over the last weeks. One is a simple Crypto Coin Price viewer and the other one a web app that supports writing user stories and bdd examples. API dependencies will be managed with OpenAPI and we will look into the nuts and bolts of these abstractions.

Lerna.js will help with the managing part and we will use a small amount of git repositories to build a great number of components and elements. Thus we make sure to use resources scaled over multiple CPU cores which will speed up the build and test times drastically.

A special issue of the series will be looking into documentation and deployment of it. Multiple versions of documentation and examples can and should be easily accessible to multiple groups of recepients with different needs. There are several tools helping the documentation process of web component catalogues and we will pick one to document the usage of our components in different environments while cutting short the development dependency tree.

NPM is the main goal for releases of this project and all packages will end up there. A look into good practices of these processes and which to automate is a integral part of a single issue of this series.

Lets see where this is going.

In the mean time you might want to have a look on the source material

- The [Gherkin Editor](https://hiherto-elements.github.io/gherkin-editor/) [(Polymer Application Source)](https://github.com/hiherto-elements/gherkin-editor)
- The [Crypto Coin Test App](https://hiherto-elements.github.io/test-app/)
- Some of the underlying, [pure es6 modules](https://github.com/hiherto-elements/es-next-modules) that are used

It will be interesting to see where this ends up.
