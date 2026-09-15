---
layout: post
title: "200 million URLs, please"
date: 2026-09-15 14:39:11 +0000
permalink: "/2026/09/15/200-million-urls-please/"
description: "A challenge repo on storing 200 million URLs from 20.000 sources: dedup, daily additions, domain counts, query parameters and a storage estimate."
tags: [software-architecture]
og_type: article
render_with_liquid: false
---
I have a little side project that keeps growing and at some point the question came up: where do I put 200 million URLs? Not in theory, in a box I pay for. So I turned it into a challenge and put it in a [repo](https://github.com/sebs/200-mio-urls-challenge), because the problem is a nice size. Big enough that the naive approach falls over, small enough that one person can tinker with it on a weekend.

The setup: 200 million URLs, coming from 20.000 sources, collected over four years. That is roughly 160.000 URLs per day, every day, steadily. Nothing bursts, nothing stops.

## What it has to do

- Store 200 million unique URLs and find them again.
- Tell me quickly if a given URL is already in there.
- Give me everything that was added today, without duplicates.
- Count URLs by top level domain.
- Count URLs by domain and subdomain.
- Query URLs by specific GET parameters.

Optional, if you feel fancy: store the link structure. Which URLs link from here, which ones link to here. That is the point where the thing quietly turns into a graph and the storage estimate doubles, so its optional for a reason.

## Why this is not just "put it in Postgres"

You can put it in Postgres. I probably will, at least at first. But a URL is not a string, it just looks like one. Protocol, host, path, query, fragment, and every part wants a different kind of index. The query part is the ugly one: `?a=1&b=2` and `?b=2&a=1` are the same page for most sites and different pages for some, and nobody on the web follows a standard for this. So normalization and dedup is where the real work hides, not in the INSERT.

Then there is the index itself. A btree over 200 million strings of maybe 80 bytes is not nothing and the "is this URL already known" check runs 160.000 times a day before anything gets written. This is the textbook case for a [Bloom filter](https://en.wikipedia.org/wiki/Bloom_filter) in front of the real store, or for partitioning by host, or by day, or both (day partitions also make "give me todays URLs" a table scan of one small table instead of an index lookup on a huge one).

And the estimate. Raw data is easy, 200 million times 80 bytes, call it 16 GB. Now add the indexes, the parsed components if you store them separately, the metadata, four years of write amplification. I do not have a number I trust yet and thats half the point of the exercise. I am guessing a factor of 4 to 5 over the raw data, would love to be wrong.

## How to play

Fork it. Do not start with the architecture diagram. Generate some synthetic URLs first, because nobody has 200 million real ones lying around, and make the generator ugly on purpose: weird parameter orders, trailing slashes, the same host in three spellings. Then build one part, measure it, throw half of it away, build the next part. Batch inserts, async writes, maybe more than one machine, whatever survives contact with the data.

I want to see what people come up with. The interesting solutions are not the ones with the biggest cluster, they are the ones where someone noticed which requirement is cheap and which one is a trap.

p.s. This is a wicked problem in the small. You will not finish it, you will just stop at some point and know a lot more about URLs than you wanted to.
