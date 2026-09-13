---
layout: post
title: "Projen just put the fun back into releasing OS for me"
date: 2024-07-16 22:24:35 +0000
permalink: "/2024/07/16/projen-just-put-the-fun-back-into-releasing-os-for-me/"
description: "Projen takes the yak shaving out of releasing open source Node.js projects by generating and maintaining TypeScript, linting, testing and CI setup."
tags: [developer-tooling, web-development]
og_type: article
image: "/assets/posts/projen-just-put-the-fun-back-into-releasing-os-for-me/og.jpg"
devto_url: "https://dev.to/sebs/projen-just-put-the-fun-back-into-releasing-os-for-me-cp5"
render_with_liquid: false
---
Releasing open-source software has always been a gratifying experience. The barriers to doing so are incredibly low these days, thanks to platforms like NPM, NuGet, and other package management solutions that make it straightforward to distribute code where it’s needed. The expansive ecosystem of NPM, in particular, despite its size and influence, still has plenty of room for well-crafted code. Modern development tools offer an enjoyable developer experience, enabling the creation and distribution of high-quality code efficiently.

## Setup - Ain't Nobody Got Time for That

However, the setup for modern Node.js projects can be tedious. Configuring TypeScript, setting up linting, implementing testing and CI support, ensuring automated builds of pull requests, managing automated dependency updates, and supporting different Node.js engines and versions—these tasks can lead to a significant amount of "yak shaving," which I'd prefer to avoid.


```json
{
 .....
 "scripts": {
    "test": "mocha -t 20000",
    "posttest": "npm run lint",
    "lint": "jshint lib test",
    "docs": "npx documentation build ./lib/init.js -f html -o out",
    "preversion": "npm run lint && npm run changelog",
    "postversion": "git push && git push --tags",
    "changelog": "rm ./docs/CHANGELOG.md && npx changelog https://github.com/sebs/etherscan-api all > ./docs/CHANGELOG.md && git add ./docs/CHANGELOG.md && git commit ./docs/CHANGELOG.md -m changelog",
    "build": "npm run test && npm run docs"
  }
}
```

> "Yak shaving" is a term often used in software development and other technical fields to describe a series of seemingly unrelated and often tedious tasks that need to be completed before you can work on the task you initially set out to do. The phrase evokes an image of performing an absurdly detailed and indirect task (like shaving a yak) that is only tangentially related to the main goal.

While all these configurations are achievable, they require a considerable investment of time. Moreover, many of these options come with deep rabbit holes, each accompanied by opinionated communities. This makes it challenging to streamline the setup process. If only there was a way to kickstart a project with a set of default assumptions, build what’s necessary, and tweak the setup when opinions drastically differ.

## Projen - A Bunch of Opinionated Helpers with a Scaffolder

Enter Projen. Projen is a tool that has changed how I approach building open-source projects. It is essentially a scaffolding tool that not only sets up your project but also maintains it. Projen provides a set of opinionated defaults that can be customized as needed, allowing you to focus on writing code rather than managing the setup and maintenance of your project.

What makes Projen great is its ability to automate tedious tasks. It can configure your TypeScript setup, ensure linting standards are in place, set up testing frameworks, and integrate CI/CD pipelines effortlessly. Projen also manages automated dependency updates and helps support different Node.js versions This level of automation significantly reduces the time and effort required to maintain a project.

Projen works by defining your project configuration in a single file, typically a .projenrc.js or .projenrc.ts file. This file acts as the blueprint for your project, where you specify all the configurations and dependencies. Projen then generates and maintains all the necessary files and settings based on this blueprint. This approach ensures that your project remains consistent and up-to-date with minimal manual intervention.

```typescript
import { cdk, javascript } from 'projen';
const project = new cdk.JsiiProject({
  author: 'Sebastian Schürmann',
  authorAddress: 'sebs@2xs.org',
  defaultReleaseBranch: 'main',
  jsiiVersion: '~5.4.0',
  name: 'robots-jsii',
  packageManager: javascript.NodePackageManager.NPM,
  projenrcTs: true,
  repositoryUrl: 'https://github.com/ssebs/robots-jsii.git',
  entrypoint: 'lib/robots-txt-parser.js',
  publishToPypi: {
    distName: 'robots-txt-parser',
    module: 'robots_txt_parser',
  },
  // deps: [],                /* Runtime dependencies of this module. */
  // description: undefined,  /* The description is just a string that helps people understand the purpose of the package. */
  devDeps: [
    '@jest/globals',
  ], /* Build dependencies for this module. */
  // packageName: undefined,  /* The "name" in package.json. */
});
project.synth();
```

One of the key benefits of Projen is its extensibility. It supports a wide range of project types, including Node.js libraries, CDK constructs, and even Python projects. You can also create your own Projen components to extend its functionality further. This flexibility makes Projen a valuable tool for any developer looking to streamline their project setup and maintenance processes.

Using Projen has reignited my lust for releasing open-source software. The time saved on setup and maintenance allows me to focus more on writing code and contributing to the community. The built-in best practices and automation features provided by Projen ensure that my projects are well-maintained without requiring constant manual updates.

Projen has put the fun back into releasing for me by automating the tedious aspects of project setup and maintenance. Its opinionated helpers and scaffolding capabilities make it an indispensable tool for modern development workflows. If you’re looking to streamline your open-source project setup and maintenance, I highly recommend giving Projen a try. It might just transform the way you approach your projects, as it did for me. Projen is the base on many cdk components these days and I am starting to make the software 'my own' right now. 


* [Projen on github](https://github.com/projen/projen)
* [Projen and CDK](https://aws.amazon.com/de/blogs/devops/getting-started-with-projen-and-aws-cdk/)
* [Migrating CDK Constructs to Projen and JSII](https://www.sebastianhesse.de/2021/03/01/migrating-a-cdk-construct-to-projen-and-jsii/)
