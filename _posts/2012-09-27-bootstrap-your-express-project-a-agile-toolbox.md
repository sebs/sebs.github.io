---
layout: post
title: "Bootstrap your Express Project - A agile toolbox"
date: 2012-09-27
permalink: "/2012/09/27/bootstrap-your-express-project-a-agile-toolbox/"
description: "When starting with a new node/express project there is a variety of tools available that help your development effort. I have started a new project and want…"
tags: []
og_type: article
original_source: "Dissident Trainings"
original_url: "http://dissident-trainings.de/2012/09/27/bootstrap-your-express-project-a-agile-toolbox.html"
canonical_url: "http://dissident-trainings.de/2012/09/27/bootstrap-your-express-project-a-agile-toolbox.html"
render_with_liquid: false
---
When starting with a new node/express project there is a variety of tools available that help your development effort. I have started a new project and want to write down my recommendations for the tools to use.

**TL;TR; You can clone a github repo [here](https://github.com/sebs/express-tdd-ci-template) and start right away.And see the build status on [travis](http://travis-ci.org/#!/sebs/express-tdd-ci-template)**

##  NPM and package.json

Since you will have to manage dependencies in your node project, i advise you to start up with a package.json. This file contains the node modules you are using in your application. You might wanna exclude node_modules via the .gitignore file to avoid external node modules beeing checkied into git. You should now have a basic package.json file and a .gitignore file. Both need to be pushed to master right now.

A [Blog Post](http://blog.nodejitsu.com/package-dependencies-done-right)about NPM and package.json

## Express.js

After you installed express.js via npm and your package JSON  you simply generate a Application Skeleton via the express command line tool. Now you have the skeleton application and push this to git. You might wanna add jade to your dependencies.

Express.js starter [tutorial](http://expressjs.com/guide.html)

## Grunt.js

Grunt helps you with linting your javascript files and orchestrate your general build. A grunt.js file in your projects root contains all the information that it needs to validate your project. To integrate it with npm aka npm test you can add a scripts.test property to your package json. Note that the npm grunt package is listed under the devDependencies property.

grunt.js [docs](https://github.com/cowboy/grunt)

## Mocha

Mocha is a nice Unit Test framework. You want to use it for your TDD efforts. You can integrate this nicely into your grunt.js file to combine linting of js files and unit tests. Mocha and its commandos need a little tuning in the grunt.js template in order to make it stop complaining about unknown globals

Mocha [docs](http://visionmedia.github.com/mocha/)

## Supertest

You mioght wanna test HTTP calls to your apps in a isolated way to check if not only your library code is working but your Webserver anwers with the right HTTP status codes etc.

Supertest [Github](https://github.com/visionmedia/supertest) repo

## Travis CI

In order to let all your tests run as soon as you have pushed to your git you might wanna setup a travis ci build. Just connect travis to your repo and add .travis.yml file.

This is a superfast development chain that will help you to get superfast at implementing features into your app. The Setup time of ca. 20 Minutes will help a lot of time.

Travis setup [docs](http://about.travis-ci.org/docs/user/languages/javascript-with-nodejs/) for node.

You can clone a github repo [here](https://github.com/sebs/express-tdd-ci-template) and start right away.
