---
layout: post
title: "Junk agile had this coming"
date: 2026-11-19 09:00:00 +0000
permalink: "/2026/11/19/junk-agile-had-this-coming/"
description: "Agile is not dying because of LLMs. It is dying because the junk version of it can't adapt to a backlog where effort stopped being the scarce thing."
tags: [agile-practices, ai-assisted-development]
og_type: article
render_with_liquid: false
---
I've heard a lot of people say that agile is no longer relevant. The agents write the code, a sprint is too slow for a team that delivers a feature before lunch, and the refinement meeting takes longer than the implementation. 

And everyone wants to know what the Scrum Master's responsibilities are now.

I don't believe LLMs eliminated agility. I believe they killed the garbage version of it, which included the majority of what was out there. Dave Thomas [called this in 2014](https://pragdave.me/thoughts/active/2014-03-04-time-to-kill-agile.html), and the LLMs have just finished the job.

## The tale point issue

Take the tale points. One number per item, related to "not time" (time). In actuality, that single number had to convey a lot of things it was never meant to: effort, complexity, ambiguity, and, on occasion, how upset the team was with the ticket. Then it divides some value guess by it, yielding the well-known "best bang for the buck" backlog ordering.

Already, the value side had never worked well. Whose worth is this? A feature can be beneficial to the client but useless to the shareholder, or vise versa (the dark pattern in the cancelation flow is extremely important, but not to the person cancelling). Both were marked as "business value: 8," and no one inquired which business.

Next, there's risk. Teams give an item high marks because it is dangerous. "We have to do this first; it's the dangerous one."That is a good reason to do it early; it is not a good reason to do it later. Risk was smuggled in as value, and the ordering became quite reasonable.

Nothing in this was a secret. It didn't really matter because effort was expensive and around the same magnitude for everything. If everything costs between 3 and 13, a sloppy value number will still yield an acceptable order.

## Rituals without much underneath

Only the most visible story points are highlighted. A lot of what was promoted as agile (and certified and workshopped) is not really based on anything. Some of it is valuable habit, some of it is cargo, and no one really knows which is which because the "why" was never included.

Take the two-week sprint. The [Scrum Guide](https://scrumguides.org/scrum-guide.html) specifies a month or less, not two weeks. The rationale is based on a feedback loop: create something that a consumer can look at, show it, and learn something before spending too much money in the wrong path. Now a feature is being built before lunch. A team that understands the why maintains the loop and reduces it to a day. A team that only knows the routine either keeps the two weeks and fills them with forty tickets, or skips the sprint and the review since "we don't do sprints anymore". Same ceremony, two ways to lose the one thing it was meant for.

That is the real damage. You recognize that you can adjust your practice when the situation changes. A ritual that can be kept or dropped. So, when the circumstance changes dramatically, individuals abandon the entire project and refer to it as the decline of agile.

## LLM backlogs are long-tail

The scenario shifted dramatically. When an agent does the typing, a significant portion of the backlog falls. Not for everything, but for the dull majority, it's close to nothing. Generating backlog items has also become cheaper. When you ask a model, "What else could we build here?" it always returns something, and the backlog rises by whatever is returned.

You receive what appears to be a long tail. A few really valuable items, followed by a huge list of things that are possible, inexpensive, and worthless. Divide a terrible value guess by an effort that is now near zero for most of them, and the "bang for the buck" ordering places the garbage at the top. And the few valued objects at the top of the tail are frequently the most difficult, where the agent does little to aid and effort remains where it was. As a result, they sink rather than simply remaining in place. Everything is inexpensive, therefore everything appears to be a good deal.

When effort is no longer scarce, the number you were dividing by becomes ineffective. The other numbers, which you never adequately measured, are now the whole game.

## Estimate four things instead of one.

There is an ancient and tedious explanation to this. Measure each aspect separately: value, effort, risk, and penalty (the cost of not doing it). In 1999, [Karl Wiegers' prioritization matrix](https://www.processimpact.com/articles/prioritizing.html) accomplished just that. Value is comprised of benefit and penalty, while cost and risk are below the line and are weighted by you. Take note of where the risk ends: below the line. It detracts from an item's appeal rather than adding to it. The polar opposite of "it's the risky one, so it goes first". It also doesn't answer the question "whose value?" However, if that is the issue, you can divide benefit into a customer and a business column, and four numbers will make that conflict evident, which is already more than "business value: 8" did. When effort reaches a plateau, its weight is reduced, and the ordering resumes with values and penalties. Same backlog, different calculation, and it's clear why it changed.

Here's where things become funny. Suggest estimating four things rather than one to a "agile" team, and you will lose the room. One number per item was already offered as overhead; the #noestimates mob desired zero. Four is heresy.

However, "we only estimate one thing" was not an agile principle. It was a convenience that happened to be adequate, whereas effort was the bottleneck. The guiding principle was inspect and adjust. Teams that understand why they estimated can modify the estimate. The rest merely have a poker deck, which does not adapt.

The second funny element is that the overhead argument has never been weaker. The same agent who does the typing can perform the first pass on the estimations, and it excels at the one area where teams struggled: risk. It has already scanned the codebase and can tell you that item 312 interacts with the payment module, as well as three integrations for which no tests exist. Effort can also guess, for the backlog items where effort is still relevant. Allow it to fill both overnight, and the team will only dispute about the outliers. These are drafts, not replies. The poker numbers were drafts, too, but no one considered them as such. What remains for humans is value and penalty. Which was always the actual job, while tale points allowed everyone to skip it.

p.s. If you want to, you can let your agents estimate token cost beforehand and create a feedback loop with IRL token cost + fixes token cost. But what do I know - I am not yet a geriatric with a LinkedIn Account and too much time at hand.