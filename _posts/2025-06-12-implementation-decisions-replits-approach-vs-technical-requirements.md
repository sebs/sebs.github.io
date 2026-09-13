---
layout: post
title: "Implementation Decisions: Replit's Approach vs. Technical Requirements"
date: 2025-06-12 10:46:49 +0000
permalink: "/2025/06/12/implementation-decisions-replits-approach-vs-technical-requirements/"
description: "In a recent blog post titled \"I Was So Angry, I Built My Own\", I articulated the frustrations that..."
tags: [node, ai]
og_type: article
image: "/assets/posts/implementation-decisions-replits-approach-vs-technical-requirements/cover.png"
series: "I was so angry I built my own"
devto_url: "https://dev.to/sebs/implementation-decisions-replits-approach-vs-technical-requirements-b24"
render_with_liquid: false
---
In a recent blog post titled "I Was So Angry, I Built My Own", I articulated the frustrations that often drive developers to build bespoke solutions. The article hints the creation of a project management tool designed to address shortcomings found in existing commercial offerings. While the ingenuity and comprehensive feature set of the described solution are commendable, particularly its embrace of modern development paradigms, it also raises pertinent questions regarding architectural complexity and the optimal distribution of responsibilities within a system. This follow-up looks into the implementation decisions discussed in the original post, contrasting them with an eye towards technical requirements and the overarching goal of complexity reduction. We will specifically examine the implications of certain design choices, such as the handling of versioning and the calculation of weighted backlogs, and foreshadow an alternative approach leveraging the robust capabilities of another way to architect this problem.

## Implementation Decisions

My original blog post points out several aspects of the custom-built project management tool that I believe align with modern development expectations. I noted that "replit did a lot of things right, in terms of what is expected from modern development." This refers to features such as markdown-based content, a nuanced relative weight system for prioritization, first-class documentation (ADRs, Post-Mortems), integrated DORA metrics, and Kanban boards with built-in metrics. These features collectively contribute to what I aimed to be a sophisticated and highly functional system.

However, the codebase I received pointed to a significant concern: the complexity of my requirements, specifically mentioning "db, orm, migrations." This complexity is particularly evident in how versioning is handled. As I stated, "deserializing JSON and comparing it against old versions is hard to write application code." This implies that my system stores historical versions of data, possibly as JSON blobs within the database, and relies on application-level logic to extract, parse, and compare these versions. While flexible, this approach can indeed introduce several challenges:

```typescript
// Version history for content changes
export const versions = pgTable("versions", {
  id: serial("id").primaryKey(),
  entity_type: text("entity_type").notNull(),
  entity_id: integer("entity_id").notNull(),
  content: jsonb("content").notNull(),
  change_description: text("change_description"),
  created_at: timestamp("created_at").defaultNow().notNull(),
});
```

* Performance Overhead: Deserializing large JSON objects and performing deep comparisons can be computationally intensive, especially as the volume of historical data grows. this actually makes the only part of the application slow that should not be. 
* Developer Burden: Developers are tasked with writing and maintaining complex application code for version comparison, diffing, and merging, which can be error-prone and time-consuming.
* Data Integrity: Ensuring the consistency and validity of JSON data across different versions requires careful validation logic within the application.
* Querying Limitations: Querying historical data or performing analytics on past states can be difficult and inefficient when data is stored as opaque JSON blobs, often requiring application-level processing after retrieval.

The whole, modern, Monthy was present: Database Migration Scripts, ORM Code from Drizzle, well defined fields and application code to calculate it. Everything easy to mock as modern frameworks provide all the bells and whistles.

My current schema provides a robust framework for the application, the extensive use of jsonb for core data and versioning, coupled with the ORM, shifts significant data processing and management responsibilities to the application layer. This design, while flexible, introduces the very complexity I aim to mitigate, particularly for operations like version comparison and complex data calculations (e.g., weighted backlog). 

Learnings:

1. Historical data must be a first class citizen (e.g. I need to be able to gather the data for a Cumulative flow diagram with a query only)
2. To many test doubles: database smoke test, orm config, migrations for incremental changes and a quite overblown architecture with rather extensive Rest API
3. The Database can be decomposed better. I went to Story,   Estimates, Status as their own tables with historical data
4. Performance is not my concern. I can freely use triggers etc. I am not designing for an audience, but only my use case. 

## Another Approach: Do it in the Database!

Using "Postgres with triggers and stored procedures for common usecases" is alternative to my current architecture, particularly for addressing the complexities of versioning and data calculations. This approach advocates for pushing more business logic and data manipulation into the database layer, leveraging PostgreSQL's powerful native capabilities. My core idea is to reduce the "many different elements that have to work together to do simple things as calculating a number," thereby simplifying the overall system and reducing the learning curve for additional tools.

Instead of storing entire JSON blobs in a versions table and relying on application-level deserialization and comparison, a pure PostgreSQL approach could manage versioning more natively. PostgreSQL offers several features that can be leveraged:

* Triggers: Triggers can automatically capture changes to specific tables (e.g., stories, adrs). When a row is updated, a BEFORE UPDATE or AFTER UPDATE trigger can record the old and new values of relevant columns into a dedicated history table. This eliminates the need for the application to explicitly manage version creation.
* Row-level Change Tracking: Instead of storing full JSON documents, history tables can store only the changed fields, along with metadata like the timestamp of the change and the user who made it. This reduces storage overhead and makes querying specific changes much more efficient.
* Temporal Tables (via Extensions or Manual Implementation): While not native in the same way as some other databases, PostgreSQL can implement temporal table-like functionality using triggers and history tables. This allows querying data as it existed at a specific point in time, without complex application-level logic

I also found complexity of calculating a "weighted backlog" and searched for a way that such calculations could be done "much earlier." By leveraging PostgreSQL's capabilities, these calculations can be performed directly within the database, in one query, reducing the need for complex application-level logic

```sql
WITH weights AS (
  SELECT 1.5 AS w_benefit, 1.5 AS w_penalty, 1.5 AS w_effort, 1.5 AS w_risk
)
SELECT
  slug,
  benefit,
  penalty,
  effort,
  risk,
  (benefit + penalty) AS value,
  (effort + risk) AS cost,
  ((w.w_benefit * benefit + w.w_penalty * penalty) / NULLIF((w.w_effort * effort + w.w_risk * risk), 0)) AS weighted_priority,
  ROUND(benefit::numeric / SUM(benefit) OVER (), 5) AS relative_benefit,
  ROUND(penalty::numeric / SUM(penalty) OVER (), 5) AS relative_penalty,
  ROUND(effort::numeric / SUM(effort) OVER (), 5) AS relative_effort,
  ROUND(risk::numeric / SUM(risk) OVER (), 5) AS relative_risk,
  ROUND((benefit + penalty)::numeric / SUM(benefit + penalty) OVER (), 5) AS relative_value,
  ROUND((effort + risk)::numeric / SUM(effort + risk) OVER (), 5) AS relative_cost
FROM stories, weights w
ORDER BY weighted_priority DESC;
```

## Conclusion 

Given what modern development suggests: Replit gave a valid solution, that if it had came with a lot let 'wrestling with the AI', would have far exceeded what I'd expect a Developer to deliver. And this is exactly the problem. The approach creates and avalanche of dependencies and maintenance tasks. I would think, the code even follows clean code principles to a certain standard and dependencies can be easily mocked. But I ask myself: Why should I even. The avalanche effect can go both ways: finding something that expresses the complexity of the task at hand in a much more elegant way, with much less elements that I need to know about, has clear implications for the design of the application down the line.

Next Step: Build a well done Postgres Database test it and then feed it back to replit. A cumbersome, manual and exact process - Reality nuked expectations I guess - but nevertheless, 

I don't wonder the LLM/Agent created this code. It is trained on the things that are upvoted in Stack Overflow and other places. However: Last years have been preachy and full of gatekeepers. So we see certain viewpoints drastically over amplified and taken at face value. My wish to future Agentic Development tools as well as to developers: Maybe think a little more and do less of that 'copy paste from upvoted stack overflow' or hype driven development but come up with more 'novel solutions' in the process. Our Brains will thank us along the way
