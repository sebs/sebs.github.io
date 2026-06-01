---
layout: post
title: "Monorepos with Lerna"
date: 2019-01-04
permalink: "/2019/01/04/Monorepos-with-Lerna/"
description: "When approaching a web components project you will end up will a lot of repositories: In our case these are at least 2 apps, the components used in these…"
tags: [monorepos, javascript, frontend]
og_type: article
---
## One repo to rule them all

When approaching a web components project you will end up will a lot of repositories: In our case these are at least 2 apps, the components used in these apps and a bunch of self developed es6 modules. All these are related to each other and can depend on each other. Normally there would be one repository per component and all these could be put under a git user/project. In practice there is repo management getting in your way and becoming a bit of a behemoth, when you try to give many users access to these lots of small repos. Plus bug tracking is all over the place.

## Hello lerna.js

This is where lerna.js comes into play. The nimble helper for node js projects basically allows you to manage multiple dependencies and NPM releasable modules in ONE repositories /packages directory. It provides the nuts and bolts that allows you to use dependencies directly from the /packages directory instead of installing the from npm as long as the package local version numbers matches your needs. Lerna can run npm lifecycle scripts and thus trigger tests and other processes in your modules giving you a rather powerful ‘test and build it all’ button. The fact that multiple modules share build and test infrastructure can be used to your advantage by sharing this infrastructure via the repository and npm infrastructure to all contents of /packages.

## Features

One thing I rely heavily on is a ‘one button install’ - A way to install all child packages dependencies in one go. As soon as the basic dependencies are installed for the main repository a ‘postinstall’ hook gets used that simply triggers lernas ‘bootstrap’ commando. ‘lerna bootstrap’ triggers npm install for all subsequent packages with one twist: Whatever is installed locally and matches versioning gets installed from this source.

The child packages are a bit differently structured though, they rarely contain development dependencies, as those are installed in the main package that allows for sharing. Here is an example of a package.json triggering the bootstrap and containing everything to test polymer.js code.

```javascript
{
  "name": "component-zoo",
  "private": true,
  "devDependencies": {
    "lerna": "^3.4.3",
    "polymer-cli": "^1.9.4",
    "wct-headless": "^2.2.2",
    "web-component-tester": "^6.9.2"
  },
  "scripts": {
    "test": "lerna run test",
    "postinstall": "lerna bootstrap"
  },
  "dependencies": {}
}
```

Another feature is triggering the ‘test’ script of each installed child package aka a ‘one button test’. This is as easy as calling ‘lerna run test’. You can make work concurrent, but you better bring a computer that allows for that. Your goto notebook processor and IO might not be the right architecture to bank on when building and testing 2 applications, some ja modules and a bunch of web components. A full blown desktop, with enough ram and CPU cores (12 cores/24 threads) is less “glitchy”. We will have a look into speed improvements later and will try to sort out some of the problems by design.

## Challenges

One thing is not to overestimate the concurrency flag and the capabilities of your frameworks. Alone polymer takes a toll of 20 seconds to delete its build directory when re-building. Even when that said directory is empty its blocking a thread just to wait exactly for this. Starting a headless chrome browser for a test uses a thread as well and building all those little packages with babel is not free of cost either. I just wanted to issue this statement of fair warning and avoid later optimizing a setup that was never created to do that. The default framework setups mostly need some tuning and building this is neither easy, nor has someone write many manuals for it. These setups are very individual. My message here is: The build tools and code to build must be fine in the first place, errors and problems will stack up and what was a little wait for one package is a very long wait for about 20 …. or even 100 single elements in /packages.

So if your calculation is to get max(t) instead of sum(t), while t being the time used for tests, when using concurrency in lerna, you are very wrong. Keep this in mind. You will have to provide CPU cores, RAM in order to make this stack of tests fast. Running all tests all time is not the right strategy as well.

When integrating everything with everything it will take time … you better find way to do this in stages. Splitting unit and functional tests is one thing, anotherone is to split the types of modules you test: some being es6 code, others complete framework based webcomponents. But in general: Buy the cores you need and stop optimizing here. The services are many and all of them are happy to sell (!) you the service.

Another challenge is in managed Windows setups: On one hand Windows often indexes the many sub directories, created by npm install, and all subsequent test and even json files for faster text search. Then there is Anti Virus, which is basically taking a hash of each new file and compare it with a list of other hashes to be known a virus. Both can be forced on you by the “IT department” managing your box. Another special Windows challenge is the ‘Linux Subsystem’, a set of extensions for your terminal that makes it basically linux compatible in syntax and functionality to a point where everything works without a patch for windows.

It might be a special quirk of me, trying to use terminal commands (e.g. rm) where pm modules exist that can use both platforms (rimraf replacing rm for example) but the effort is just to much. If you have developers insisting on using windows, just manage the Anti Virus for your node modules, the full text indexer and get the linux subsystem. Otherwise you are in for a long and boring development project with a lot of ‘wait time’. I am not saying Windows is slow per se, but I am saying you need to set it up in a way that works.

## Takeaways

- Lerna can save install time with shared infrastructure
- Lerna can use local modules over external npm
- Lerna can manage test and bootstrapping dependencies
- Lerna is heavy lifting, make sure you bring the tools

## Links

- [Blog Post Overview](https://sebs.github.io/blog/managing-a-webcomponent-zoo/)
- [Example Git Repo](https://github.com/sebs/component-zoo)
- [Lerna js](https://lernajs.io/)
