---
layout: post
title: "No more servers already!"
date: 2018-07-06
permalink: "/2018/07/06/No-more-servers-already!/"
description: "I am working a lot with clients who pay me to extend software they have created themselves or let others write it for them. A web shop here, a custom CRM…"
tags: [serverless]
og_type: article
---
I am working a lot with clients who pay me to extend software they have created themselves or let others write it for them. A web shop here, a custom CRM there. Nothing crazy. I fix broken dependencies often and add features where ever my work is required. Me and the previous Hackers on these code bases seem too have the same approach to code/style and documentation (fancy/questionable and documentation minimal). Its ok to build things like this, but over the years, it is hard to keep all the elements up and running as if it were “day 1” (or better said bug fix release 1.14)

However, such software is in use for a while updates and security fixes come around the corner, hearts bleed and processors melt down. And while these projects do what every they are supposed to do, the maintenance of old code and updates create a drag on goals my customers try to reach. In the end, I am paid to fix mistakes, that other developers already made and fixed in their own (often open source) code bases. Reinventing the Wheel for a living. Why is that?

## Times are changing

When these projects were created, there was neither a server less, nor a movement for micro services. In one case, the main Framework was to be updated 3 major versions, just to hint at the day of the creation. Plus there is the cost of being a first mover: Given todays standards, INSERTFRAMEWORKHERE, back then had totally different ideas of clean code etc.

Other things got just way simpler: Where a version of Elasticsearch was used, nowadays a simple Postgres extension will do. Where contact attempts got stored in a JSON Database again Postgres can handle this now.

But if I look beyond the horizon of this specific vendor locked box I have my self shut in: With CDN, DNS, Email, Monitoring: There are already a lot of different external services used. Just not the main job at hand: In this case selling things and receiving contact attempts about products.

The customers site has a login, but he has no desire to use any data beyond order data at any time in future. So even this could be put to a external service. There are a bunch of content elements like Videos/Blog posts etc.

All these services are out there as a service these days.

Most of them are easy scalable beyond what one can achieve with small server setups or small teams

Shop: Snipcart provides a shopping back-end charging 2% by purchase plus handling for payment. Search: Multiple providers Allow for simple indexing and add the metadata that Snipcart can not provide CMS: Aerobatic provides everything to deploy and static stack of sites. Or use Amazons infra to get cheaper rates. however. Contact: In 2018, there are several simple Services to do this. Contact management and CMS in SAAS is already a commodity, available widely and provide several products to pick from. In the case of shopping and search, the amount of companies coming into closer consideration is not so big anymore.

## Wardley

All this code is custom controllers on top of a framework. This is how things got done, when there was no big collection of gems, ready to do anything for you. If I would replace the DIY shop codebase with a predefined gem or framework, a mode towards the “Product” is in order. Search is a good example.

Lets assume 2 user groups for a eShop: Owner and Customer . And now lets think of some some Basic needs.

Customer Needs: Search, Order and being informed about products

Owner Needs: Process orders; Provide Information and Products

Another thing is to think about how visible these features are to the customer.

Shop: 50% lots of things “under the hood” Contact: Code handles a message, delivers it. There is not even an admin part 90% CMS 40%: With image handling etc. Not so visible to the user. Search: Very invisible. Apart from a well filled index, you just dont care — as long as it works.

Mapping alls this we get

So what happens, when we start refactoring as proposed before? Host only static content from a base website service, fully CDN backed! Search is a configurable service that needs monitoring of requests/day and success of imports. CMS is as simple as “github” pages and the shop integration done on “deploy” time! Contacts are done with any of the services out there.

Nowadays one can rent most of these services and it seems, this is a very good visual representation if where I want to go.

There are many nice things about commodity services and one of them being widely available, normally high quality and a good bang for the buck. Why? Markets make sure of that in most cases. When a service sucks: Users Change it. In markets like this: Money buys you features and I heavily doubt, I can beat my providers on their own game (aka build a better shop than Snipcart e.g.)

Conclusion

I can not wait to see more commodity services available for general tasks and I enjoy every announcement about it. And the great thing about it is: Scaling and Distribution of load is not a secret to these companies anymore and their core business (e.g. providing a eCart) is completely different to mine (adding functionality) and my customers (selling things). So we are all winning so far.

For me it looks like I will be a bit more wary, with spinning up a container here, installing a database there and try to explore the “No more servers already” idea a bit more. I am starting to enjoy it being “serverless”
