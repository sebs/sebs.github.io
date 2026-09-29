---
layout: post
title: "Your website relaunch is not a moat anymore"
date: 2026-09-29 13:18:28 +0000
permalink: "/2026/09/29/your-website-relaunch-is-not-a-moat-anymore/"
description: "Why Landtag relaunches killed kleineAnfragen.de, how coding agents flip the scraping cost onto the publisher, and why suing readers is the last trick left."
tags: [open-data, ai-assisted-development, tech-strategy]
og_type: article
render_with_liquid: false
---
In January 2021 netzpolitik.org [interviewed Maximilian Richt](https://netzpolitik.org/2021/zum-ende-von-kleineanfragen-de-die-loesung-zu-all-unseren-problemen-koennte-in-pdfs-schlummern-die-niemand-liest/) about why he switched off [kleineAnfragen.de](https://kleineanfragen.de/). [Kleine Anfragen](https://de.wikipedia.org/wiki/Kleine_Anfrage) are how MPs make the government answer in writing, and the answers are public. Technically. In practice they sit as PDFs in 17 different parliament documentation systems, behind search forms nobody enjoys. Max scraped all of them, put everything in a full text search and gave everyone feeds and mail subscriptions. For years, mostly alone.

Why he stopped is the interesting part. The Landtage kept "relaunching". New HTML templates, same infrastructure underneath, never open data. Every relaunch meant writing the scraper for that Landtag again from zero. In Sachsen the link to a found document just expires after 15 minutes. A mail to the Landtag NRW, who runs the [Parlamentsspiegel](https://www.parlamentsspiegel.de) for all Länder, got answered weeks later by paper mail: "nicht zuständig". An [IFG request](https://fragdenstaat.de/anfrage/dokumente-zum-parlamentsspiegel/) went nowhere. You can not do this as a hobby forever, and he said so.

The OKFN [said it more bluntly](https://okfn.de/blog/2021/01/zur-abschaltung-von-kleine-anfragen/): volunteers running infrastructure that is the job of the public hand changes nothing structurally. They are right. Keep that in mind for later.

## Fragmentation does the work by itself

I spent a lot of my career extending other peoples code bases, so I know what a "relaunch" usually is: a new theme on the old thing. I don't think anybody in a Landtag sat down and planned to break Max's scrapers. Nobody had to. 17 parliaments, a handful of vendors, every installation configured different and every one a bit worse. The cost of reading it all lands on whoever wants to read it all, and that was one volunteer. Paid political monitoring exists, as Max points out, so the lobby groups that can afford it were fine anyway.

That is the balkanisation I mean. It does not need a conspiracy, it needs an asymmetry: making the mess is cheap for the publisher, cleaning it up is expensive for the reader. As long as that holds the mess wins, and "Open Data" can go into every strategy paper without anything happening.

## The asymmetry is gone

So I built [openka-cli](https://github.com/maschinenlesbar-org/openka-cli). 17 parliaments, one record format, `ka sync --source berlin` and `ka search "Brücken Zustand"`.

The part that burned Max out, rebuilding a scraper per Land per relaunch, is now the cheap part. Thüringen answers Drucksache 8/979 with 8/1715 and nothing numeric connects the two, so the connector asks the Vorgang API. Saarland's "PDF" link is an HTML page with an iframe, so the URL gets rewritten to the download endpoint the iframe names. Sachsen hides the real file in the navigation frame of a frameset viewer. Niedersachsen has nothing reachable that links question to answer at all, so a factory tool sweeps the Drucksachen range once and freezes the map. Each of these would have been a weekend of swearing in 2016. Now it's a prompt, a fixture and a review. When the next relaunch comes a golden fixture goes red and the fix is an hour.

One thing I care about, because "AI" and "government data" in one sentence makes people nervous for good reason: the agent writes the code, it does not run in it. The runtime is deterministic, no model on the line. When an extractor can't read a document it abstains and the document lands in `ka review`. `ka verify` re-runs the extraction from the archived bytes and the record has to come out byte identical. A missing fact you can fix later. A made-up one in a corpus about what a government told its parliament is poison. Agents in the factory, boring code in the product.

Coverage is honest, not complete ([96 test records from eight parliaments, 68 extract completely]). The rest say what they could not read, instead of pretending.

## What is left are lawyers

Look at the sources table and you see the tricks that remain once the technical drag stops dragging. Brandenburg and Sachsen-Anhalt put `Disallow: /` in the robots.txt of their document servers. NRW disallows its own search, while running the aggregator for everyone (go figure). openka respects that by default and tells you, rather than quietly returning nothing.

And then there is the trick data activists know too well: getting sued. In 2021 Markus Drenger mirrored the official Hauskoordinaten from the Bavarian Landesamt on GitHub. Bayern answered with a takedown, a criminal complaint and a civil suit over database rights, with damages that [according to Drenger](https://blog.wikimedia.de/2026/09/03/wem-gehoeren-oeffentliche-geodaten/) could have gone into the millions. Five years later the [OLG München threw it out](https://netzpolitik.org/2026/mit-urheberrecht-gegen-offene-daten-bayern-verliert-gegen-open-data-aktivisten/) as inadmissible, because the Freistaat changed its story mid-trial about who actually built the database. No appeal. The real question, if a state can lock up data it already publishes, the court never got to. Five years of that hanging over a volunteer is the actual message, win or not.

The funny part is that the law is half way there. The [Datennutzungsgesetz](https://www.gesetze-im-internet.de/dng/BJNR294200021.html) says public data should be "open by design and by default" where possible, and for high value datasets like geodata reuse has to be free. One paragraph earlier the same law says nobody gets a right to have anything published. So the principle is in the Bundesgesetzblatt and the obligation is not. "Follow your own rules" is less a legal argument than an embarrassing one.

For Kleine Anfragen it is even simpler. Drucksachen are published so the public can take notice, which makes them [amtliche Werke](https://www.gesetze-im-internet.de/urhg/__5.html): no copyright, just don't alter them and name the source. openka does both, the archived PDF is the source. Nobody needs to sue anybody here.

The OKFN point still stands. I should not run the infrastructure for 17 parliaments any more than Max should have. But the math changed: when the cost of the mess no longer lands on the reader, the only one still paying for it is the publisher. Suing the people who read your public documents is the most expensive way to stay unreadable. Living up to the principle you already wrote into law, and shipping an API, is cheaper, and it's not a moonshot. Berlin already exports PARDOK XML per Wahlperiode, the Bundestag has [DIP](https://dip.bundestag.de/%C3%BCber-dip/hilfe/api) with a public API key. So it can be done.

p.s. Hamburg, my home town, runs ParlDok, the same software as Mecklenburg-Vorpommern and Thüringen, which both have a working JSON API. Hamburg's service was unreachable when I built this. WTF Hamburtg, WTF. 