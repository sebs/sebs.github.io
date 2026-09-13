---
layout: post
title: "The seven Lamps of (Software)Architecture"
date: 2012-03-14
permalink: "/2012/03/14/the-seven-lamps-of-softwarearchitecture/"
description: "I am still reading “The Craftsman” by Richard Sennet, a book that was given to me by a very smart Product-Designer/UX-Guy/Carpenter because we talked a lot…"
tags: []
og_type: article
original_source: "Dissident Trainings"
original_url: "http://dissident-trainings.de/2012/03/14/the-seven-lamps-of-softwarearchitecture.html"
canonical_url: "http://dissident-trainings.de/2012/03/14/the-seven-lamps-of-softwarearchitecture.html"
render_with_liquid: false
---
I am still reading “[The Craftsman](http://www.amazon.com/The-Craftsman-Richard-Sennett/dp/0300151195/ref=sr_1_1?ie=UTF8&qid=1331713637&sr=8-1)” by Richard Sennet, a book that was given to me by a very smart Product-Designer/UX-Guy/Carpenter because we talked a lot about the merits on the crafty part of software-development and web-architecture. Amazon describes it as:

> *Why do people work hard, and take pride in what they do? This book, a philosophically-minded enquiry into practical activity of many different kinds past and present, is about what happens when people try to do a good job. It asks us to think about the true meaning of skill in the ‘skills society’ and argues that pure competition is a poor way to achieve quality work. Sennett suggests, instead, that there is a craftsman in every human being, which can sometimes be enormously motivating and inspiring - and can also in other circumstances make individuals obsessive and frustrated.“The Craftsman” shows how history has drawn fault-lines between craftsman and artist, maker and user, technique and expression, practice and theory, and that individuals’ pride in their work, as well as modern society in general, suffers from these historical divisions. But the past lives of crafts and craftsmen show us ways of working (using tools, acquiring skills, thinking about materials) which provide rewarding alternative ways for people to utilize their talents. We need to recognize this if motivations are to be understood and lives made as fulfilling as possible.*

In the Book is a whole chapter about [John Ruskin](http://en.wikipedia.org/wiki/John_Ruskin), a art critic in the Victorian era who had interest environmentalism, sustainability, craft and his “7 Lamps of Architecture”. These are a part of an essay that was a (slightly polemic) critic on the architectural style of that time. The [“7 Lamps of Architecture”](http://www.archive.org/details/lampsofarchseven00ruskrich) represent a take on the “good deeds” of construction things, in this case architecture for buildings. Long story short, I find these 7 principles apply to the construction of software architectures as well and I want to outline the connection here.

## **7 Lamps of (Software)Architecture**

***Sacrifice** – dedication of man’s craft to God, as visible proofs of man’s love and obedience*

There are physical facts you have to obey and you better do not try to get around them. For example: Network has latency, bandwidth limits and might not be available all the time. Better design for it and be dedicated to it, don’t be sloppy and build tech debt.

***Truth** – handcrafted and honest display of materials and structure.*

Do not cover up the real architecture of a software design behind thick layers. It is what it is and is has to work this way. The Single responsibility principle might be a way to interpret this.

***Power** – buildings should be thought of in terms of their massing and reach towards the sublimity of nature by the action of the human mind upon them and the organization of physical effort in constructing buildings.*

Take into consideration that humans are after all the Users of your software. Design it that way. Think about who is the End-User and how many of them will be there.

***Beauty** – aspiration towards God expressed in ornamentation drawn from nature, his creation*

Yes there is the saying “Form follows function”, but there is a little more if you walk the world with open eyes. A User interface might need some Beauty to be used with Joy. Take Joy of the End-User and Administrator into consideration when building things.

***Life** – buildings should be made by human hands, so that the joy of masons and stone-carvers is associated with the expressive freedom given them*

Even if you the architect decided on principles for the design of a system, the thing is built by Programmers and UX-Designers. They need not only some freedom to do so. Work closely with them to avoid a technical perfect but boring product just created by design principles and build by numb coders just following them.

***Memory** – buildings should respect the culture from which they have developed*

You are developing the Software in a specific environment. One example might be the customers lingo that you find in the design of classes and database layouts as well as in the name of the fields of your web forms.

***Obedience** – no originality for its own sake, but conforming to the finest among existing English values, in particular expressed through the “English Early Decorated” Gothic as the safest choice of style.*

I guess we are back at “Form follows Function”, there should be a  reasoning behind a design. You can measure a lot do things and should not build just what you want. [Lean Startup](http://en.wikipedia.org/wiki/Lean_Startup) being here the latest example coming to my mind.

These are just small examples of how you could interpret Ruskin’s take on Architecture. I found that very enlightening in the angle of the “Software Craftsmanship”-Thinking.

## **Seriously?**

You have to take into consideration that this essay was heavily influenced by the industrialization and the dehumanization coming with it. The seven Lamps are an Idea and not a set of rules carved into the stones of Software Architecture/Development. I hope it makes you think and I want to close with a citing attributed to Ruskin

> *THERE IS NO WEALTH BUT LIFE. Life, including all its powers of love, of joy, and of admiration. That country is the richest which nourishes the greatest number of noble and happy human beings; that man is richest who, having perfected the function of his own life to the utmost, has always the widest helpful influence, both personal, and by means of his possessions, over the lives of others.*
