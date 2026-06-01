---
layout: post
title: "Surive your Frontend"
date: 2014-04-10
permalink: "/2014/04/10/Surive-your-Frontend/"
description: "I am building a talk on how to approach big/long running front end projects that was initially presented at the Berlin PHP User-group July 2014. I started…"
tags: [javascript, talk]
og_type: article
---
I am building a talk on how to approach big/long running front end projects that was initially presented at the Berlin PHP User-group July 2014. I started to prepare it and want to nail down my thoughts.

## WHERE I AM COMING FROM

I have had the chance to get my hands on a lot of Javascript projects and most of the were not small projects per se. It is not only the raw lines of code that let me speak of “big” projects but longevity and complexity that you find in a modern front-end to a web applicationmaking it “big”.

A regular observation is that front-ends do not get the same level of love that a backend gets. Some examples I came across this year alone:

Specifications are very roughly prepared for front-ends The crafty side of development, modularization and testing is neglected Standards are not set and/or followed The fact that a javascript front-end is the client to a server application is often overlooked Front-end code is often thought as throw away. Seriously guys. It would be good business to go on and on and on like this for years. It is already going on. You think your back-end code rots from greenfield to brownfield fast? Look at your front-end code. It always rots faster.

“Code this fast. We can rewrite this next year.” and next year we are sitting on the same type of code for the same website, thinking about other things we could do, but re-write a bunch of front-end legacy crap. Yeah, just implement another slider. You like to work in one checkout with 20k lines of code? You want to implement just another self made inline validation for address data? Go for it, but just do not expect me to like this and help you failing.

Sorry, I am too old for this. Been there, done that - 10 Years ago.

## WHERE TO START?

When working out all the specific little hints and tipps for the talk I had to group them in order to create a flow for the presentation. All the little things and tricks go into 3 groups.

- Tools - Its 2014 and there are a lot of new toys. Lets use them.
- Craft - We must use the tools. This means pure development
- Process - Development is just a part of a larger process.
- It is just the first order I brought into the first set of ideas. It all might be subject to change.

## TOOLS

There is a bunch of new tools to help with front-end development. A little sneak peak of the things I have used in the last weeks and months.

Bower, Component.js or NPM - for modularization and re-use Gulp and Grunt for Builds Docker, Chef or Puppet to build a machine where it runs on Mock and Stub Servers GIT(hub), do you speak it? …..(more in the talk) You can still right click and download Jquery if you want to, but there is no need for it and if you’ve checked it into your version control I do think of this as a anti-pattern. We moved way beyond this.

I do not mind using Jquery plugins as a basis for a project or React components, but please, can have consistency? I do not mind doing coffeescript for you (and learning another language while you pay me doing this) but please, can we have all the code consistent in like one langugae then?

## CRAFT

The pure coding is the thing that I call craft. This has not changed much. But using tools alone will not help you.

I mean we can go on for the next ten years like this in our code ….

```javascript
function validForm(formName) {
    switch (formName) {

        case "request_showing":
            // Validate the first name
            if (request_showing.first_name.value == "") {
                alert("Please enter your first name.");
                request_showing.first_name.value = "*** FIRST NAME";
                request_showing.first_name.focus();
                problem = true;
            };
            break;

        case "email_friend":
        // ....... 

    }
}
```

or we can grow up and use patterns and a little thinking to find some slick implementations that follow old concepts like coupling) and cohesion). It is not new and just because you have visited jsconf last week and took away the concepts from es5, rxJS or any other reactive variant these “rules” are not bollocks.

Really, I have seen this pattern over and over. The Jquery guys told us all the stuff we did before was crap in 2004 with all the same arguments used today by the rxJS community. And seriously the language that we actually use has not really changed. It is still javascript and the browsers we target still ask for a pretty old ECMA Standard. IE8 anyone? ;)

It is not that I do not care for the niceties of es5, but some old patterns do not get out of fashion and a DOM tree, the main target of any JS front-end project, is still a evented thing so event driven programming will get you very far.

## PROCESS

The “best” thing I have seen in the last year was a code review tool giving a automated +1 for any checkin based on executing the tests of the codebase I was assigned to. So far so good. But the tests executed in this case were the ones for the backend codebase. Front-end tests did not get executed at all (they were broken at the time). This is how you subvert the basically pretty cool code review process (no I wont argue pairing vs. code reviews here - although I am a big proponent of paired code as you all know). A lot of the investments done (tests for the frontend code), but all the money invested thrown out of the window.

With a non-modularized codebase, in the same repository like your backend you are pretty much set up to fail. It starts with the big codebase, goes on with a one size fits all test and release process where you are pretty much forced to check all the functionality all the time. Besides TDD and some integration testing you are pretty much bound to do most of your real testing in a explorative way. It is a very important way of testing but should be used as a an extra to show your blind spots, discover new areas to test and not be the most important source for bugs.

This is what you do when you specify requirements. The checkouts address form does need a inline validation is not a requirement in my world. I am sorry. But starting coding will just get you into a long loop of trial and error that is inherently costly and as I started out: you will repeat this next year. To be constructive here, why not go down the road of [specification by example](http://www.wikiwand.com/en/Specification_by_example#/overview). Yeah I know, that sounds like a big hassle. If you calculate the cost of bugs in specific steps of the development process, you might change your thinking here.

## MY POINT!

I think we now can stop repeating the fails of the last ten years (and more) over and over. We have evolved the tools, craft and process over the last 10 years in a way that really helps with this.

- Tools - Use the tools at hand. They are not toys and they are a pretty good investment. Use them with care, but use them.
- Craft - Front-end is hardcore software development. Accept it and learn it.
- Process - Process wise we learned a lot on how we can improve development and find errors and bugs early in development. CI, CD, Feedback and all this is not a joke. This is the new imperative. I am looking forward to the talk and as always I am looking for feedback in the comments section here.

[The crux of done →](https://sebs.github.io/blog/the-crux-of-done)
