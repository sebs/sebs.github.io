---
layout: post
title: "The software factory is 58 years old"
date: 2026-10-25 19:43:58 +0000
permalink: "/2026/10/25/the-software-factory-is-58-years-old/"
description: "Bemer proposed the software factory in 1968, Hitachi built one in 1969. Five things to read from the last people who tried, before building another one."
tags: [ai-assisted-development, software-architecture, tech-strategy]
og_type: article
render_with_liquid: false
---
Everybody is building a "software factory" right now. Agents write the code, agents review the code, nobody reads it, lights off. Dan Shapiro gave it a name in January, StrongDM shipped one, and the term has been everywhere since.

The term is from 1968. Bob Bemer (the ASCII guy) proposed a software factory at the IFIP Congress in Edinburgh, then handed in a design document for one at the NATO conference in Garmisch, the same meeting that coined "software engineering". Hitachi opened the first one in 1969. SDC in Santa Monica built one in 1975 and let it lapse in 1978. Toshiba, NEC and Fujitsu ran theirs for decades. Then Europe tried again with Eureka, HP tried a reuse factory, Microsoft reused the name in 2004 for something else, and it went quiet.

So before I build another one [I am running a small one myself, 31 CLIs for German public APIs, more on that another time], I went and read what the last people who tried had to say. Most of it is free, most of it is short, and the failure modes are exactly the ones people are tweeting about as if they were new: components that nobody reuses, a process that managers quietly route around, and design and production split apart until the work flow breaks.

If you read five things, read these:

1. [Factory concepts and practices in software development](https://dspace.mit.edu/handle/1721.1/47992), Michael Cusumano, 1989. The whole story in 40 pages, IBM and SDC and then Japan. Free on MIT DSpace. Start here.
2. [The Software Factory: Contributions and Illusions](https://cin.ufpe.br/~if722/2006.2/readings/03/Software_Factories_17.pdf), Aaen, Bøttcher and Mathiassen, 1997. Four factory approaches compared on the same five questions, then a plain list of what the metaphor delivers and what it only promises. Best critique I found.
3. [System Development Corporation: defining the factory challenge](https://dspace.mit.edu/handle/1721.1/49002), Cusumano, 1988. The post mortem of the one factory that got shut down. Five problems it was built to solve, three it created.
4. [Mass produced software components](https://www.cs.dartmouth.edu/~doug/components.txt), Doug McIlroy, 1968. The original promise, in the words of the guy who later gave us Unix pipes. Ten pages.
5. [Japan's Software Factories](https://academic.oup.com/book/52424), Cusumano, 1991. The book, one chapter per company. Not free, but the library will have it. Read it when you want the detail, not before.

What held, by the way: the Japanese factories that lasted all made one narrow kind of software, for customers who did not change much, with a team paid to keep the parts library alive. Nobody had a general purpose factory. That is worth remembering before promising one.
