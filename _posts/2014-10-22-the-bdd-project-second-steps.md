---
layout: post
title: "The BDD project - Second steps"
date: 2014-10-22
permalink: "/2014/10/22/the-bdd-project-second-steps/"
description: "Progress on a BDD side project: picking Silex, Cucumber.js with webdriver and gulp, writing the first feature scenario and planning steps toward a deploy."
tags: [testing-and-quality, web-development]
og_type: article
original_source: "Dissident Trainings"
original_url: "http://dissident-trainings.de/2014/10/22/the-bdd-project-second-steps.html"
canonical_url: "http://dissident-trainings.de/2014/10/22/the-bdd-project-second-steps.html"
render_with_liquid: false
---
More progress (Version 0.0.1) is made and we are a little further down the road towards a first deploy.

## Frameworks & Tools

I sided with the [Silex](http://silex.sensiolabs.org/) framework that allows for easy development with PHP and Symfony2 components. I spent the last 3 years with [Express.js](http://expressjs.com/) which follows the same doctrine as its Ruby variant [Sinatra](http://www.sinatrarb.com/). If stuff will become a little chaotic and the project gets bigger the switch to [Symfony 2](http://symfony.com/) will not hurt to much since a lot of the infrastructure is the same.

The built in [PHP webserver](http://www.lornajane.net/posts/2012/php-5-4-built-in-webserver) will do nicely for development purposes. It is an awesome tool.

For the Scenario and BDD side of things I went with [Cucumber.js](https://github.com/cucumber/cucumber-js) and [webdriver](https://github.com/admc/wd). It seems the thing that works right now.

Another decision I had to make was the one of the build tool, which is in this case [gulp.js](http://gulpjs.com/). I started to like the non-verbosity of the tool.

## A first scenario

In order to keep scanarios and stories separated the decisionw as to keep stories in the [github bugtracker](https://github.com/DissidentTrainings/xp-practices-site/issues) and the scenarios go as [feature files](https://github.com/DissidentTrainings/xp-practices-site/tree/master/features).

However, there is a point where I have to start and stuff needs to be shipped. In order to wire up everything I decided to add a scenario, [setup cucumber with webdriver](https://github.com/DissidentTrainings/xp-practices-site/blob/master/features/support/world.js) (not only installing it, but writing the code that actually uses the webdriver api).

**The Scenario**

This should force me to implement a lot of basic stuff right away. and relates to [Story \#2](https://github.com/DissidentTrainings/xp-practices-site/issues/2)

    Feature: View Practice
      As a workshop participant and website user
      I want to read about specific practices
      so that I know what it is about
      and I can decide if I want to have it in the workshop

      Scenario: View Pairprogrammig
        Given I surf to '/practices/pairprogramming.html'
        Then I should see a level 1 heading 'Pairprogramming'
        And a paragraph of text
        And a unordered list of links to external websites

      Scenario: Link to allies
        Given I surf to '/practices/pairprogramming.html'
        When I should see a list of allies
        Then the list of allies should contain 'Test Driven Development'

I will see how this works out in the next steps. ;)

## Next steps

Some things come into mind

- Automating the inclusion of the original markdown files about the practices
- Deploy it
- Implement Story \#1 and \#2
- Find a way to test and validate that it works

Things I wont do (yet)

- Heavy TDDing - I am not yet writing an big chun of APIs right now
- CI - Given the “advice” I took away from the guys of Unruly I will delay that for a later time and dont focus so much on it.
