---
layout: post
title: "Ideas on Pairprogramming"
date: 2017-07-23
permalink: "/2017/07/23/Ideas-on-Pairprogramming/"
description: "Over the last years, I got many good Ideas from teams on how to use pairing in their daily work. It is very interesting how the initial idea is “hacked”,…"
tags: [extremeprogramming, practices, pairprogramming]
og_type: article
---
Over the last years, I got many good Ideas from teams on how to use pairing in their daily work. It is very interesting how the initial idea is “hacked”, changed and adapted. Some traditional and not so traditional approaches here in a blog post.

## PAIR “PROMISCUOUSLY”

Everyone pairs with everybody else is a nice way to get knowhow shared in your team. Sometimes it is a hard start, but when you have completed this for the first time, there will be foundations of teamwork that are hard to achieve otherwise. Some of the advantages of doing so.

- Learn to know development setups of your colleagues
- Understand the reasoning behind that ‘quirky’ behavior everyone shows once in a while
- This is a good team building exercise
- You will probably lift the level of the person who is ‘the weakest link’ in your teams ‘chain’
- This is the number one way to reduce the bus factor

## PAIR AND CHANGE ON RED-GREEN-REFACTOR

You can pair in a environment with Unit-Tests and make a change not based on time (although it is good to set a maximum time limit) but when you go forward in the re-green-refactor loop. Use the following Cycle when starting with a green lit unit test suite:

1.  Person A: Add a test that makes the suite go: red
2.  Person B: Implement code so that it goes to: green
3.  Person A: Refactor (all still green)
4.  Person B: Add a test that makes the suite go red:
5.  Remark Always on green tests and rector make a commit. Push to master if you are done

This is very good to learn and internalize the way TDD in its purest form as in test first works. It will give you very good insight in the method and produce code. You can have a very fast cycle here as soon as the basics between the two persons pairing are sorted out.

## PAIR RED-(GREEN-REFACTOR)

This is a variant of the above, but James Shore describes “Sit together” in his book as

Sitting together fuels team communication. This has impressive results, cutting time-to-market by two thirds in one field study. It enables simultaneous phases, eliminates waste, and allows team members to contribute insights to others’ conversations.

To sit together, create an open workspace. This takes longer than you expect. Organize your workspace around pairing stations, locating people according to conversations they should overhear. Provide plenty of whiteboard space. Make sure there’s room for personal effects and a place for private conversations.

Open workspaces are hard for some to accept. Get team members’ permission before switching, or they may rebel.“

1.  Sit all the disciplines together.

I often see designers skipping this one and staying with their designer teams. Not so good. Everyone should be on the product they are working on.

2.  Agree to common rules explicitly

Different people have different needs and desires. Talk about them and write them down. After a few weeks: rinse and repeat. make this explicit

3.  Must not be in a room, but can be close

A glass wall often does as well. If I can see my Product owner (a role that requests own rooms very often in my experience), I can approach him.

4.  Adapt your visual management

If you are doing hardcore Scrum you might dive into Kanban now. There are different disciplines and roles in the room, working on on one thing. So the normal Scrum Board most likely will not cut it. A good place to start is Kanaban.

5.  Rituals! Rituals! Rituals!

I have heard of a “Disco Friday” where teams would play nice music all day long aloud on friday or seen hourly Nerf gun matches. These rituals help to firm groups and keep them in high cohesion.

6.  Style it

Invest some work in styling the place. Some lights, LED ambient illumination, posters on the wall etc. will really help teams to form and stick. Make sure to provide a budget.

7.  Clean it

Once a week/sprint: Clean the workplace and bring everything in order. Its a very short procedure for most places and it helps providing general order and cleanliness.

8.  Have the Meetings together

Do not let the “Backend Guy” bail the Grooming when you are working on Frontend Stories. Do not let the designer bail as well. Everyone has to learn what the other disciplines do. When someone sits there and does not get it: Help him understand. Re-Arrange Groomings so that there are Stories of any Kind. You know the vertical slicing thingie? You should do it. And no .. neither the designer nor the tester will bail the Retrospective. It takes disciplined and willing teams to practice it this way. But in my experience: The seasoned crafts(wo)men will happily participate.

9.  Have a extra room for “Discussions”

When different trades of craft work together, there is a lot of need to discuss things and talk about it. You will need a room for this since every discussion will be a interruption for everyone else in the room. Buy a set of high quality noise dampening head phones. I am working at a client here in Hamburg where you have small chambers for working 1on1 as well as meeting rooms that are general available for phone conferences etc.

10. Have more than enough Space

Even People with Computers need Space to work and think. Provide this. Don’t make cross-functional teams and cram them in a small room and be surprised you get a lot of complaints from the inhabitants of that room . If you cant afford space, maybe do not hire developers at all. There are regulations for how many office workers can be in a certain set of size here in Germany and I have seen several occasions where these laws where used as a common denominator of how many people fit in a room. This is not the way it works.

So this is what I came up with. What are your Ideas?with the exception that one person makes the tests green and refactors them. This is a little more training oriented and can be used to teach a newbie essential skills in software development and TDD.

Hint Even if it is hard for you as the expert: The newbie should write the code. Doing creates a way better understanding.

## PAIR WITH THE NEW PERSON ON THE TEAM

Speaking of newbies how about this: The next time you onboard a new team member you do not make his setup for the development environment for a week. Instead you let him pair with every member of your team for a longer time.

New colleagues in a company are still free from most of the organizational duty and are often stuck in a situation where they have to ask a lot of questions in order to be productive. Codebases are big and the details of implementations are specific: The new person will have a hard time to contribute to productive code and learn at once. By pairing with a experienced team member this problem can be solved. You do not even need a computer and this can be done from the moment a new person enters the office.

```plain
Remark This leads to a extremely lowered on boarding time. Additionally the person can actively bring his skills to the table.
```

## PAIR A RELEASE

Releases kinda suck. Always a bit. A little more when you do not have a complete Integration and Continuous Delivery pipeline set up and there is stuff to be made by “hand”. Often this “duty” will be on one person and thereby you create a single point of failure in many ways. It is hard to review a release. You just know if it worked or not. So working as a pair might be a good thing. Shitty duty gets more fun this way and the peer-pressure will keep the pair in line not to cross the many lines in a release process that can be harmful just for sloppiness. Releases suck. Been there done that.

## PAIR A BUGFIX

Bug fixing kinda sucks too. At first something is not working. After it you will be looking for the source of the bug and then you will find out that you have made a very specific mistake (you as in team). This burden can be shared. It’s not that your colleagues have not made the same kind of errors (or worse) in the past. We are humans. So lets get this painful duty over with as a pair. The bugfixes will be more complete (because they are challenged by your navigator) and there will be less problem with regressions. Additionally: Two people learn at once what mistake not to make next time and two people can bring their knowhow to the table regarding this specific problem. It’s making a fail a win-win (as far as possible).

## PAIR WRITING A USER-STORY

Writinglearning a User-story is often done by the product owner. And when the teams first re-views the story, a lot of technical remarks and constraints are added etc. In this situation, the product owner often resembles just to “write these informations down” and is not learning too much. Why? The amount of information that a team of developers generate in a grooming or estimation meeting is just to high in that moment very often. Change this a bit: Stay with the grooming meeting but let the product owner write down the User story together with one of the developers. Just use driver and navigator as in normal pairing and a blank text file. The story will be more dense of information and the additions that have to be made by the whole team a little less.

## PAIR A SPIKE

Coding experimental features to prove that something works is called a spike in XP. Another name for that is a “Research Task”. This is one of the cooler thing and might be very good to do it as a pair. Why?

It’s mainly a learning opportunity. Learning is important. I see that a wide range of knowledge is required for most of these. So two persons knowledge might help to make a successful spike happen (or just successfully find out it is not working how you anticipated). more than one person will have the freedom to work on a new thing. It is just motivating to “move fast and break stuff”. It would be nice to get some other ideas from you here in the comments section. What is your special way of Pairprogramming?
