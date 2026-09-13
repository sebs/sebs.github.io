---
layout: post
title: "8 tips for the use of coding conventions"
date: 2014-09-11
permalink: "/2014/09/11/8-tipps-for-the-use-of-coding-conventions/"
description: "Coding conventions sound so easy, but get hard over the course of a longer project and with bigger team size. With a little feedback and forth with Johann…"
tags: []
og_type: article
original_source: "Dissident Trainings"
original_url: "http://dissident-trainings.de/2014/09/11/8-tipps-for-the-use-of-coding-conventions.html"
canonical_url: "http://dissident-trainings.de/2014/09/11/8-tipps-for-the-use-of-coding-conventions.html"
render_with_liquid: false
---
Coding conventions sound so easy, but get hard over the course of a longer project and with bigger team size. With a little feedback and forth with Johann Peter Hartmann, the following principles for a coding standard were up for discussion.

- understandability - The conventions should help the programmer to understand the code and should be easy to understand themselves
- learnability - It should be easy to adopt and learn a coding convention and the convention should help the developer to easily find a way into a codebase
- attractiveness - It should be attractive to adhere to a certain standard
- analyzability - The standard set itself should be machine analyzable. It’s either THIS or THAT, not MAYBE, SOMETIMES or OFTEN. ;)
- changeability - The standard should be easy to change and changes to the code, by a new standard, should be easy to do as well.

My list of tipps should help you find a standard and keep it up.

**1. They apply for everyone in the team.**

No developer, in no situation should be exempt of the conventions. It might sound dogmatic, but this is a rule that applies for everyone. Even for \$pointyhairyboss, if he is still pushing to the codebase.

**2. There is no perfect convention for every given project.**

I see this discussion revolve again and again: Developers looking for “the standard”. Where do I set my braces, which kind of whitespace do I use? Please tell me. I am to smart to look for THE standard, give me any standard and I will adhere to it.

**3. Automate checking**

No one wants to check, what could be millions line of code, by hand ot just looking at the code. Tools can help you with that. What ever you decide, try to create an automated check for violations and make this one available to all the developers working on the software.

**4. Have examples and explanations**

Coding conventions may seem to be a very subjective thing. But when explained properly, in a markdown, text file or wiki page it gets easier to accept to code by standards that are not your own (yet).

**5.  Your codebase must have 0 violations at all time **

With command line tools and checking before you push stuff to a repository, this should be easy. There might me exceptions, but make sure you group them into modules exempt from the checking process or make other wise sure the initial thought of a same structured codebase does not get undermined.  See 6.

**6. Change if required**

If the rules don’t fit, change them to better ones. Migrate the module to the new rules. Do not only change the rules. Change the code as well.

**7. Everyone is responsible not only for his own conventions **

Where ever you are in a pice of code, you are encouraged to fix any violations or add a example here and there. Didn’t you find enough comments? Cool, add some.  Something is formatted wonky? Fix it! Somebody used spaces? Change it to tabs if the spec says so.  Where ever you are in the code, a OneButtonTest will be a good practice to look at.

**8. Make conventions per module, not per team**

Different modules might be written in different times and adhere to different standards. So splitting up parts of your software that follows a very different style might be reasonable. In Javascript and a browser environment you would use tools like component and bower to get things back together.  Small modules help you maintain different styles. Think about it: If you have a long running project, it’s very likely you will have more than one standard. And small modules allow for different ones in different occasions and situations. One argumentative nail in the coffin of Big ball of mud designs

This was my list of hints. What are yours?

## User contrinbutions

**8. Use existing conventions and starndards**

Tobias Schlitt argued, that the use of already existing standards has a lot of advantages over creating your own ones. In PHP there is the PSR- Series of standards. These are pretty good and you will find ready made tools and documentation out there.
