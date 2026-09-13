---
layout: post
title: "I Was So Angry, I Built My Own Workshop Platform"
date: 2025-07-29 21:42:19 +0000
permalink: "/2025/07/29/i-was-so-angry-i-built-my-own-workshop-platform/"
description: "Sometimes the breaking point comes not from a single catastrophic failure, but from the slow..."
tags: [webdev, ai, productivity, javascript]
og_type: article
image: "/assets/posts/i-was-so-angry-i-built-my-own-workshop-platform/cover.png"
devto_url: "https://dev.to/sebs/i-was-so-angry-i-built-my-own-workshop-platform-439c"
render_with_liquid: false
---
Sometimes the breaking point comes not from a single catastrophic failure, but from the slow accumulation of a thousand small frustrations. After months of wrestling with Miro's limitations while trying to create a simple set of online workshop exercises, I finally reached mine. The platform that promises to revolutionize collaboration had become a obstacle to actually collaborating. So I did what any frustrated developer would do – I decided to build my own.

## The Simple Ask That Wasn't So Simple

All I wanted was straightforward: create 12 interactive workshop exercises for brainstorming and mindmapping, integrated with about 200 markdown files of existing content, plus a collection of images and slides from previous workshops. The concept was elegant in its simplicity – share not just the workshop experience, but the entire methodology and content openly on GitHub, making it accessible to anyone who wanted to run similar sessions.

But Miro had other plans.

The platform that markets itself as the ultimate collaborative workspace quickly revealed itself to be a walled garden with expensive tolls at every gate. Want to embed your exercises? That'll be an iframe solution locked into their ecosystem. Prefer to host your own? You'll still need their REST API, which means you're still paying them monthly for the privilege of using your own infrastructure.

The math was simple and depressing: another $20 down the pipe each month, just to create something that should be as accessible as a markdown file on GitHub.

## When the Guardrails Become Prison Bars

Miro's appeal lies partly in its guardrails – the platform guides you toward "best practices" and keeps you from making obvious mistakes. But those same guardrails become prison bars the moment you want to do something slightly outside their predetermined use cases.

Testing became a nightmare confined to Miro's context. Want to debug your workshop flow? Hope you enjoy clicking through their interface repeatedly, because there's no easy way to automate or script your testing process. The Web SDK, which should have been my escape hatch, turned out to be a black box with minimal documentation and source code that felt deliberately obfuscated.

I found myself spending more time fighting Miro's limitations than actually building the [workshop experience](https://pair-programming-workshop.github.io/) I envisioned. The platform that promised to accelerate collaboration was actively slowing down my development process.

## The Documentation Desert

Perhaps nothing encapsulated my frustration more than Miro's documentation – or the lack thereof. For a platform that charges premium prices and positions itself as enterprise-ready, the docs felt like an afterthought. Basic integration patterns were missing, advanced use cases were ignored entirely, and the examples that did exist were so simplified they were useless for real-world applications.

The Web SDK documentation was particularly painful. Critical methods were mentioned in passing without proper examples, error handling was barely covered, and the relationship between different API endpoints was left as an exercise for the reader. For a tool that's supposed to enable developers, it felt actively hostile to development.

## The GitHub Revelation

The turning point came when I stepped back and really examined what I was trying to accomplish. My workshop content was already on GitHub – 200 markdown files, images, slides, and methodologies, all open source and freely available. The entire concept was built around transparency and accessibility.

So why was I trying to bury the interactive exercises somewhere in a  proprietary ecosystem?

The cognitive dissonance was jarring. I was taking content designed to be open and accessible, then locking it behind a paywall in a platform that made it harder for people to access and modify. Making the exercises accessible in that walled garden would require as much work as building them from scratch – so why not build them in a way that actually aligned with my values?

## WebRTC to the Rescue

The solution crystallized around WebRTC – real-time communication technology that runs directly in browsers without requiring proprietary platforms or monthly subscriptions. Instead of paying Miro to facilitate collaboration, I could build peer-to-peer connections that put users in direct control of their data and experience.

WebRTC offered everything and more I needed: real-time collaboration, screen sharing, voice communication, and data channels for synchronizing workshop state. Best of all, it worked entirely in the browser without requiring server infrastructure for the core functionality.

The architecture became beautifully simple: workshop content served as static files from GitHub, interactive exercises running as client-side JavaScript, and real-time collaboration handled through WebRTC connections. No monthly fees, no vendor lock-in, no artificial limitations: Just lick the 'Run exercise now' button. 

The most liberating aspect of building my own solution was the freedom to prioritize accessibility over monetization. Commercial platforms need to balance user needs against revenue optimization, often resulting in artificial scarcity and paywalled features.

My workshop could be different. Since the content was already open source, the exercises should be too. Participants could fork the entire workshop, modify it for their specific needs, and share their improvements back to the community - or just run it with their teams. 

The technical implementation reflected these values. Instead of requiring accounts or subscriptions, participants can join workshops through simple links. Instead of storing data on corporate servers, everything runs locally in browsers with optional peer-to-peer synchronization. Instead of vendor-specific formats, everything used open standards like markdown, JSON, and standard web technologies.

## The Challenges That Made It Worthwhile

Building a real-time collaborative platform isn't trivial, even with modern web technologies. WebRTC connection establishment can be finicky, especially across different network configurations. Synchronizing state across multiple peers without a central server requires careful conflict resolution strategies. And creating an intuitive user experience for complex collaborative workflows demands significant design iteration.

The development process also revealed how much overhead commercial platforms add to simple tasks. Creating a basic brainstorming exercise in commercial platforms from ground up required navigating their complex API, understanding their data models, and working within their constraints. Building the same functionality with standard web technologies was more direct and resulted in cleaner, more maintainable code.

My workshop inverted this model entirely. Instead of extracting ongoing value from users, it provided ongoing value to the community. Workshop facilitators can use it freely, participants can access content without barriers, and people could contribute improvements-

This approach aligned perfectly with the educational mission of the workshops themselves. If the goal was to share knowledge and methodologies, why should the delivery platform create barriers to that sharing?

## The Power of Constraint-Free Development

Perhaps the most unexpected benefit of building my own solution was the creative freedom it provided. Commercial platforms impose their own design patterns and interaction models, subtly shaping how you think about problems and solutions.

Working without those constraints revealed possibilities I hadn't considered. Workshop exercises could integrate seamlessly with external content, participants could customize their experience in real-time, and facilitators could adapt the platform to their specific teaching style without fighting against predetermined workflows.

The platform became a true reflection of how I wanted workshops to work, rather than a compromise between my vision and someones business model. This alignment between tool and purpose created a more coherent and effective user experience.

## Personal Tools for Personal Workshops

What makes this project particularly satisfying is that I'm building it primarily for a small audience. I'm not trying to please enterprise customers with an offer or optimize for maximum market appeal – I'm solving my specific problem in exactly the way I want it solved.

## From Concept to Code: The Prototyping Journey

Once I committed to building my own solution, the real work began. The path from frustration to functional platform involved experimenting with different development approaches that each taught me valuable lessons about what I was actually trying to build.

### Google AI Studio: WebRTC in the Wild


My first serious attempt at prototyping started with Google AI Studio. The appeal was obvious – I could leverage AI assistance to quickly explore WebRTC implementations without getting bogged down in the minutiae of connection establishment and signaling protocols.

But WebRTC's greatest strength – its peer-to-peer nature – also presented the biggest prototyping challenge: nearly impossible to test effectively within Google AI Studio's environment.

I found myself implementing split-screen browser sessions, manually copying and pasting signaling data between different tabs, trying to simulate what would happen when real users attempted to connect from different networks. The artificial nature of this testing revealed gaps in my understanding of NAT traversal, STUN server configuration, and the various failure modes that occur when peers can't establish direct connections.

The Google AI Studio phase taught me that while AI could accelerate the initial implementation, the real complexity of WebRTC lay not in the code itself but in the network topology challenges that only emerged during real-world testing. This realization would prove crucial for the next phase of development.

### Lovable: UX Patterns and Feature Creep

Frustrated by the testing limitations of Google AI Studio, I moved my prototyping efforts to Lovable, a platform that promised to handle both the technical implementation and user experience design aspects of web application development.

![I really liked the Prototype](/assets/posts/i-was-so-angry-i-built-my-own-workshop-platform/c9zl7jnx8mc6unf4zg3q.png)


Lovable exceeded my expectations in several key areas. The platform demonstrated an impressive understanding of modern UX patterns, generating interfaces that felt intuitive and professionally designed. The WebRTC integration was handled more elegantly than my previous attempts, with proper error handling and graceful degradation when connections failed.

More importantly, Lovable understood the collaborative nature of what I was building. The generated interfaces included features I hadn't explicitly requested but clearly needed: participant management, session state synchronization, and visual feedback for connection status. The platform seemed to grasp the implicit requirements of real-time collaborative tools in ways that pure code generation couldn't match.

![Just nailed it here](/assets/posts/i-was-so-angry-i-built-my-own-workshop-platform/7yy5v6ynqca8py1hv4ov.png)

But Lovable's strength in feature generation also became its weakness. The platform's enthusiasm for adding functionality resulted in a feature set that grew far beyond my original requirements.

The feature creep wasn't malicious – each addition made logical sense in isolation. But collectively, they transformed my focused workshop tool into a generic collaboration platform that competed directly with the Miro-style solutions I was trying to escape. The simplicity and targeted functionality that motivated the project in the first place had been buried under layers of well-intentioned but unnecessary features.

The Lovable experience taught me an important lesson about AI-assisted development: the tools are incredibly capable at generating sophisticated functionality, but they lack the constraint and focus that comes from deeply understanding a specific problem. Without careful guidance, AI development platforms tend toward feature maximalism rather than elegant minimalism. 

I will come back to lovables limitations in a later posting. There are many - it is a ok prototyping system - not more, but not less either. 

### The Testing Reality Check

Both prototyping approaches revealed the same fundamental challenge: WebRTC applications can't be properly evaluated without real-world network conditions and multiple simultaneous users. The signaling complexity that seemed manageable in controlled environments became a significant obstacle when testing across different browsers, networks, and device configurations.

This testing reality forced me to confront the gap between prototype and production. The code generated by AI platforms worked beautifully in ideal conditions but failed unpredictably.

The split-screen testing sessions that seemed like a minor inconvenience during the Google AI Studio phase revealed themselves to be a symptom of a deeper problem. Real workshop collaboration involves multiple participants joining from different locations, networks, and devices. Any solution that couldn't be easily tested in these conditions was fundamentally incomplete.

This realization shifted my development approach from rapid prototyping to systematic testing infrastructure. Before adding more features, I needed to solve the basic reliability and connectivity challenges that both AI platforms had glossed over in their enthusiasm to generate impressive demos.

## From Prototypes to Production: The Analysis Phase

Three prototyping attempts had taught me valuable lessons about what I wanted to build, but they had also revealed the limitations of rapid AI-assisted development for complex distributed systems. Before writing another line of code, I needed to step back and systematically analyze what I had learned.

This led to what I now think of as the analysis phase – a deliberate pause in development to apply more rigorous engineering practices to the problem. Instead of continuing to iterate on prototypes, I decided to treat the existing code as research artifacts that needed proper evaluation and requirements extraction.

The first step was subjecting my prototypes to systematic code review. I developed a specialized AI agent focused entirely on code analysis, feeding it the complete codebases from Google AI Studio, Lovable, and Gemini AI implementations.

The code review agent's analysis was brutally honest and incredibly valuable. It identified patterns I had missed across the three implementations: inconsistent error handling in WebRTC connection logic, naive approaches to state synchronization that would break under network partitions, and architectural decisions that worked for demos but would fail under real-world load.

More importantly, the agent highlighted the evolution in my thinking across the three prototypes. The Google AI Studio version was technically ambitious but architecturally naive. The Lovable version had better UX patterns but suffered from scope creep. The Gemini AI version achieved focus but sacrificed robustness for simplicity.

The review revealed that each prototype had solved different aspects of the problem well, but none had achieved the holistic solution I actually needed. The Google AI Studio version's WebRTC implementation was the most technically sound. Lovable's user interface patterns were the most intuitive. Gemini AI's focused scope was the most aligned with my actual requirements.

Armed with the code review insights, I deployed a requirements engineering sub-agent to systematically analyze what I was actually trying to build. Instead of starting with technical solutions, this agent focused on understanding the problem space: what makes collaborative mindmapping different from other real-time collaboration scenarios?

The requirements engineering process was revelatory. By analyzing the workshop context, participant behaviors, and facilitation needs, the agent identified requirements I had never explicitly considered. The need for offline-first functionality wasn't just a nice-to-have – it was essential for workshop environments with unreliable connectivity. The importance of conflict resolution wasn't just a technical challenge – it was a user experience requirement that could make or break collaborative sessions.

The agent produced a comprehensive requirements document that transformed my understanding of the project. What I had initially conceived as a simple "collaborative mindmap" was actually a complex system with specific needs around session management, participant coordination, data persistence, and real-time synchronization.

The requirements analysis revealed why my prototypes had felt incomplete despite working demonstrations. I had been solving the technical challenges of real-time collaboration without addressing the human challenges of workshop facilitation. The missing pieces weren't just features – they were fundamental architectural decisions about how people would actually use the tool.

### The Architecture Decision Records

The analysis phase culminated in a series of Architecture Decision Records (ADRs) that codified the lessons learned from prototyping and requirements analysis. These weren't just technical decisions – they were philosophical statements about what kind of tool I wanted to build.

ADR-001 established the commitment to vanilla JavaScript without frameworks or build tools. This wasn't just a technical preference – it was a statement about longevity and maintainability. The prototyping phase had shown how quickly AI-generated code could become obsolete when tied to specific frameworks or toolchains.

ADR-002 defined the offline-first architecture with IndexedDB as the primary data store. This decision emerged directly from the requirements analysis, which had identified network reliability as a critical concern for workshop environments.

ADR-003 and ADR-004 addressed the collaboration model, establishing support for both host-controlled approval workflows and distributed CRDT-based synchronization. This dual approach reflected the tension between structured workshop facilitation and free-form collaborative brainstorming.

![ADRs were created while writing this software](/assets/posts/i-was-so-angry-i-built-my-own-workshop-platform/u9vyr44kw27w7ts319f6.png)

The ADRs transformed the project from a collection of prototypes into a coherent architectural vision. They provided the constraints and principles needed to guide implementation decisions, preventing the feature creep that had plagued the Lovable prototype while ensuring the robustness that the earlier prototypes had lacked.

## Getting WebRTC Right: Down the Protocol Rabbit Hole

With the architectural foundation established, I faced the most technically challenging aspect of the project: implementing reliable WebRTC connections for real-time collaboration. The prototyping phase had revealed that WebRTC was more complex than any AI platform had suggested, but the analysis phase had shown me that understanding this complexity was essential for building a robust solution.

This led me to make a decision that would define the next phase of development: instead of reaching for an existing WebRTC library or framework, I would implement the protocol myself from first principles. Not because I intended to reinvent the wheel permanently, but because I needed to understand exactly how deep the rabbit hole went before making informed decisions about abstractions and trade-offs.

The journey began with the WebRTC specifications themselves – not blog posts or tutorials, but the actual RFC documents that define how the protocol works. RFC 8825 for the JavaScript API, RFC 8826 for the security architecture, RFC 8829 for the JavaScript Session Establishment Protocol (JSEP), and dozens of related specifications that form the complete WebRTC ecosystem.

Reading RFCs is a particular kind of technical discipline. These documents are written for implementers, not users, and they assume knowledge of networking protocols, cryptography, and distributed systems. But they also provide the authoritative source of truth about how things are supposed to work, unfiltered by the interpretations and simplifications that inevitably creep into secondary sources.

The RFC deep dive revealed the staggering complexity hidden beneath WebRTC's seemingly simple JavaScript API. More importantly, the RFCs revealed why my prototyping attempts had failed in subtle ways. The AI-generated code had implemented the happy path scenarios described in tutorials, but real-world WebRTC connections involve dozens of potential failure modes, fallback strategies, and edge cases that only become apparent when you understand the full protocol stack.

Armed with RFC-level understanding, I turned to analyzing existing WebRTC implementations to see how theory translated into practice. This wasn't about copying code, but about understanding the design decisions that experienced developers had made when facing the same complexity I was encountering.

I examined popular WebRTC libraries like SimpleWebRTC, PeerJS, and Socket.IO's WebRTC implementation. These libraries take a different approach from browser implementations – they prioritize developer experience and ease of use. The library analysis revealed a fundamental tension in WebRTC development: comprehensive protocol support requires significant complexity, but most applications only need a subset of WebRTC's capabilities. The libraries that tried to hide this complexity often broke down when faced with real-world network conditions, while the libraries that exposed the complexity required developers to understand much of what I was learning from the RFCs anyway.

## The Decision to Roll My Own

This analysis led to a crucial realization: for my specific use case – small-group collaborative editing with known network requirements – I could implement a focused subset of WebRTC that would be both simpler and more reliable than trying to use a general-purpose library designed for unknown use cases.

The decision to implement WebRTC myself wasn't driven by arrogance or a desire to reinvent the wheel. It was a strategic choice to understand the problem space deeply enough to make informed trade-offs. By implementing only the features I needed and optimizing for my specific constraints, I could try create maintainable and debuggable solution rather than adapting a general-purpose library - with the option to reverse my decision later, when reality kicks in. 

The workshop collaboration scenario had specific characteristics that simplified the WebRTC implementation significantly. Participants would typically be on the same corporate network or similar network environments, reducing the complexity of NAT traversal. Session sizes would be small (2-10 participants), eliminating the need for complex mesh networking optimizations. The data being transmitted was primarily text and simple graphics operations, not high-bandwidth media streams.

These constraints meant I could focus on the core peer-to-peer data channel functionality while deferring or eliminating many of the complex features that make general-purpose WebRTC implementations so challenging. No media streams, no complex codec negotiations, no adaptive bitrate algorithms – just reliable data channels for synchronizing mindmap operations between peers.

### Understanding the Depth of the Rabbit Hole

The process of implementing WebRTC from scratch revealed layers of complexity that no tutorial or AI-generated code had prepared me for. The signaling process alone involves intricate state machines, careful timing considerations, and robust error handling for dozens of potential failure modes. ICE candidate gathering requires understanding network topology, STUN server interactions, and fallback strategies for different types of NAT configurations.

But the deep dive also revealed opportunities for simplification that weren't apparent from the surface. By understanding exactly what each part of the protocol was designed to solve, I could make informed decisions about which parts were essential for my use case and which could be simplified or eliminated entirely.

For example, the standard WebRTC negotiation process involves multiple rounds of offer/answer exchanges to handle complex scenarios like renegotiation and media stream changes. For my collaborative editing use case, I could implement a simplified negotiation process that established data channels once and maintained them for the duration of the session, eliminating much of the state management complexity that makes WebRTC implementations fragile.

The security model was another area where deep understanding enabled simplification. WebRTC's security architecture is designed to handle untrusted peers and protect against sophisticated attacks. For workshop collaboration between known participants, I could implement a simpler trust model while still maintaining the cryptographic protections that make WebRTC secure.

### The Option to Replace Later

Perhaps the most important aspect of the "roll my own" decision was maintaining the option to replace the custom implementation with a library later, once I understood the trade-offs involved. By implementing the protocol myself first, I gained the knowledge needed to evaluate existing libraries effectively and integrate them without breaking the architectural principles established in the ADRs.

This approach inverted the typical development process, where developers choose libraries first and then discover their limitations during implementation. By understanding the problem space thoroughly before selecting abstractions, I could make informed decisions about which libraries would actually simplify the codebase versus which would add complexity without corresponding benefits.

The custom WebRTC implementation also served as a specification for what any future library would need to provide. Instead of adapting my application architecture to fit a library's assumptions, I could evaluate libraries based on how well they supported the patterns and constraints that had proven effective in my implementation.

**WebRTC Library Option**: For future replacement, `simple-peer` from npm provides a clean abstraction over WebRTC data channels with minimal overhead. It handles the signaling complexity while exposing the peer-to-peer data streams in a straightforward API that would integrate well with the existing architecture.

**CRDT Library Option**: For CRDT implementation, `yjs` offers a mature, well-tested library with excellent performance characteristics and support for multiple data types. It provides the Tree CRDT functionality needed for hierarchical mindmap structures while maintaining the offline-first principles established in the ADRs.

### Engineering Depth vs Surface-Level Development

The WebRTC deep dive exemplified a broader philosophy that had emerged from the systematic analysis phase: the importance of understanding foundational technologies before building abstractions on top of them. This approach stands in stark contrast to the surface-level development that characterizes much of modern web development, where developers compose libraries without understanding the underlying systems.

Surface-level development works well for simple applications and well-understood problem domains. But for complex distributed systems like real-time collaboration tools, shallow understanding leads to brittle implementations that fail in unpredictable ways when faced with real-world conditions.

The RFC-reading and implementation exercise represented a significant time investment – weeks that could have been spent building features or polishing the user interface. But this investment paid dividends in system reliability, debuggability, and architectural coherence that would have been impossible to achieve with a library-first approach.

More importantly, the deep understanding enabled confident decision-making throughout the rest of the development process. When faced with trade-offs between different collaboration strategies or debugging connection issues in production, I had the foundational knowledge needed to make informed decisions rather than relying on trial-and-error or community forums.

### The Systematic Approach Extended

The WebRTC implementation process demonstrated how the systematic approach established during the analysis phase extended naturally to every aspect of the development process. Just as I had used specialized AI agents for requirements analysis and code review, I applied the same methodical approach to understanding and implementing complex protocols.

This consistency of approach created a development process that was both rigorous and efficient. Instead of switching between different methodologies for different aspects of the project, I could apply the same systematic thinking to everything from high-level architecture decisions to low-level protocol implementation details.

The WebRTC deep dive also validated the architectural decisions made during the analysis phase. The offline-first approach meant that WebRTC failures didn't break the core application functionality. The vanilla JavaScript architecture meant that debugging protocol issues didn't require navigating through framework abstractions. The modular design meant that the WebRTC implementation could be developed and tested in isolation from the rest of the application.

Perhaps most importantly, the protocol-level understanding reinforced the value of building rather than buying for complex technical requirements. The depth of knowledge required to implement WebRTC effectively was the same depth needed to evaluate and integrate WebRTC libraries successfully. By doing the implementation work first, I gained capabilities that would benefit every future technical decision, not just the immediate WebRTC requirements.

The rabbit hole of WebRTC implementation turned out to be exactly as deep as I had suspected from the prototyping failures, but also more navigable than I had feared. With systematic analysis, comprehensive understanding, and focused implementation, even complex protocols could be tamed and made to serve the specific needs of the application rather than dictating its architecture.

## Mastering Distributed Data: The CRDT Deep Dive

With WebRTC connections established and real-time communication flowing between peers, I faced the next fundamental challenge of distributed collaboration: how to handle concurrent edits to shared data without conflicts. This led me into the world of Conflict-free Replicated Data Types (CRDTs), a family of data structures designed specifically for distributed systems where network partitions and concurrent modifications are inevitable.

The CRDT challenge represented a different kind of complexity than WebRTC. While WebRTC was primarily about network protocols and connection management, CRDTs were about mathematical properties of data structures and the theoretical foundations of distributed computing. This wasn't just an implementation challenge – it was a computer science research problem that required understanding decades of academic work on distributed consensus and eventual consistency.

### The Distributed Data Problem

The core problem that CRDTs solve is deceptively simple to state but fiendishly difficult to implement correctly. When multiple users edit the same data simultaneously across an unreliable network, how do you ensure that all users eventually see the same consistent state without requiring coordination between them?

Traditional approaches to this problem rely on centralized coordination – a single source of truth that serializes all operations and resolves conflicts. But centralized coordination introduces single points of failure, requires constant network connectivity, and creates bottlenecks that limit scalability. For a workshop collaboration tool designed to work offline and handle network partitions gracefully, centralized coordination was fundamentally incompatible with the architectural principles established in the ADRs.

CRDTs offer a mathematically elegant solution: data structures that are designed so that concurrent operations can be applied in any order and will always converge to the same final state. This property, called strong eventual consistency, enables truly distributed collaboration without requiring any centralized coordination or conflict resolution.

But the elegance of the theoretical solution masked significant implementation complexity. CRDTs come in many varieties, each optimized for different use cases and with different trade-offs in terms of memory usage, computational complexity, and network overhead. Understanding which CRDT types were appropriate for mindmap collaboration required a systematic exploration of the entire CRDT design space.

### Prototyping the CRDT Landscape

Following the same pattern that had proven effective for WebRTC exploration, I decided to implement a comprehensive prototype that demonstrated all the major CRDT types and their behavior in various conflict scenarios. This wasn't about building production code – it was about developing intuition for how different CRDT approaches would behave in the specific context of collaborative mindmapping.

![This was a very interesting way to prototype data structures by designing a UI on top of them](/assets/posts/i-was-so-angry-i-built-my-own-workshop-platform/jnxs3rm0zve34h4rgtsd.png)

I returned to 'Google AI Studio' for this exploration, but with a much more structured approach than my initial WebRTC prototyping attempts. Instead of asking for a complete collaboration system, I requested focused implementations of individual CRDT types with comprehensive test scenarios that demonstrated their convergence properties under various conflict conditions.

The AI proved remarkably capable at generating clean implementations of the fundamental CRDT types. G-Counters for increment-only values, PN-Counters for values that could be both incremented and decremented, LWW-Registers for last-writer-wins semantics on individual properties, and OR-Sets for collections that supported both additions and removals. Each implementation came with test cases that demonstrated the mathematical properties that made them conflict-free.

More importantly, the LLM could generate scenarios that stressed the edge cases of each CRDT type. What happens when two users simultaneously add the same element to an OR-Set? How does an LWW-Register behave when operations have identical timestamps? How do PN-Counters handle the case where decrements arrive before their corresponding increments due to network reordering?

These stress test scenarios revealed the subtle complexities that make CRDT implementation challenging in practice. While the mathematical properties guarantee eventual consistency, the path to convergence can involve intermediate states that appear inconsistent or confusing to users. Understanding these transient inconsistencies was crucial for designing user interfaces that would remain comprehensible during the convergence process.

### The Key Insight: Matching CRDTs to Collaboration Patterns

The most important learning from the CRDT exploration wasn't about any specific data structure or algorithm, but about the fundamental principle that different types of collaboration require different types of CRDTs.

A simple voting scenario, for example, needs nothing more than a G-Counter - users can only increment their vote count, conflicts are impossible, and the final result is just the sum of all increments. The CRDT implementation is trivial, the convergence behavior is predictable, and the user interface implications are minimal.

A collaborative mindmap, by contrast, requires a complex combination of CRDT types working together. Node text needs LWW-Registers, node positions need specialized conflict resolution for simultaneous moves, and the hierarchical structure needs Tree CRDTs that can handle cycles and maintain tree invariants. The implementation is complex, convergence can involve confusing intermediate states, and the user interface must handle transient inconsistencies gracefully.

This insight fundamentally changed how I approached the CRDT implementation. Instead of trying to find a single "best" CRDT approach, I needed to design a system that could use different CRDT strategies for different collaboration patterns and switch between them based on the current workshop activity.

### Mapping CRDTs to Mindmap Operations

The prototype exploration revealed that collaborative workshop content required a sophisticated combination of different CRDT types, each handling different aspects of the shared state. Node text content could be handled with LWW-Registers, assuming that simultaneous edits to the same text field were rare enough that last-writer-wins semantics were acceptable. Node positions required more complex handling, since simultaneous position updates were common during collaborative layout activities.

The hierarchical structure of mindmaps presented the most complex CRDT challenge. Parent-child relationships between nodes form a tree structure, but collaborative editing can temporarily create cycles or disconnected components that need to be resolved automatically. This required implementing a specialized Tree CRDT that could handle structural operations like node creation, deletion, and reparenting while maintaining the tree invariant that every node has exactly one parent.

The prototype phase revealed that different collaboration scenarios required different CRDT strategies. For structured workshop activities where a facilitator guided the process, simpler CRDT types with predictable convergence behavior were preferable even if they occasionally required manual conflict resolution. For free-form brainstorming sessions where multiple users were simultaneously creating and connecting ideas, more sophisticated CRDTs that could handle complex structural conflicts automatically were essential.

This analysis led to a crucial architectural insight: the collaboration system needed to support multiple CRDT strategies and allow switching between them based on the current workshop activity. This flexibility requirement would significantly influence the final implementation design, ensuring that the CRDT layer could adapt to different collaboration patterns without requiring application-level changes.

### Understanding CRDT Performance Characteristics

The prototype exploration provided initial insights into the performance implications of different CRDT approaches. While CRDTs guarantee eventual consistency, they achieve this property by maintaining additional metadata that can grow substantially over time. Vector clocks for operation ordering, tombstones for tracking deleted elements, and operation logs for state reconstruction all consume memory and network bandwidth.

Research into CRDT implementations and documentation revealed that for mindmaps with hundreds of nodes and thousands of operations, these metadata overheads could become substantial. 

Understanding the performance characteristics was essential for making informed design decisions about which CRDT types to use for different aspects of the workshop activities state. High-frequency operations like cursor position updates required lightweight CRDTs with minimal metadata overhead. Structural operations like node creation and deletion could tolerate more complex CRDTs with richer conflict resolution capabilities - i would mostly only need the latter. 

The academic literature revealed that CRDT research was an active  field. New CRDT types were being developed for specialized use cases, and existing types were being optimized for better performance characteristics. It also revealed the importance of verification for CRDT implementations.

### Synthesis: From Theory to Practice

The CRDT exploration phase culminated in a synthesis document that mapped the theoretical CRDT concepts to the practical requirements of collaborative mindmapping. This document served as a bridge between the academic literature and the implementation work that would follow, translating abstract mathematical properties into concrete design decisions.

The synthesis revealed that successful CRDT implementation required careful attention to three distinct layers: the mathematical properties that ensured convergence, the data structure implementations that realized those properties efficiently, and the user interface design that made the convergence process comprehensible to users.

Each layer had its own complexity and constraints. The mathematical layer required rigorous reasoning about commutativity, associativity, and idempotence properties. The implementation layer required balancing memory usage, computational complexity, and network overhead. The user interface layer required designing interactions that remained intuitive even when the underlying data was in temporary inconsistent states during convergence.

The systematic exploration of CRDTs through prototyping and literature review provided the foundation for making informed decisions at each of these layers. Instead of choosing CRDT types based on superficial characteristics or tutorial recommendations, I could select approaches based on deep understanding of their theoretical properties and practical implications for the specific use case of collaborative mindmapping.

### The Pattern of Systematic Understanding

The CRDT deep dive followed the same pattern that had proven effective for WebRTC exploration: systematic prototyping to develop intuition, comprehensive analysis of existing approaches, and synthesis of theoretical understanding with practical requirements. This consistent methodology created a development process that was both rigorous and efficient, ensuring that complex technical decisions were based on solid understanding rather than guesswork or cargo-cult programming.

The pattern also revealed the value of using AI tools for systematic exploration rather than direct implementation. By focusing the AI on generating comprehensive examples and stress test scenarios rather than production code, I could leverage its capabilities for rapid prototyping while maintaining the analytical rigor needed for complex distributed systems design.

Perhaps most importantly, the CRDT exploration demonstrated that the systematic approach scaled to handle multiple layers of complexity simultaneously. Understanding CRDTs required integrating knowledge from theoretical computer science, practical distributed systems engineering, and user experience design. The methodical approach provided a framework for managing this complexity without becoming overwhelmed by any single aspect.

The CRDT deep dive also validated the architectural decisions made during the earlier analysis phase. The offline-first design meant that CRDT convergence could happen asynchronously without blocking user interactions. The vanilla JavaScript architecture meant that CRDT implementations could be debugged and optimized without framework abstractions getting in the way. The modular design meant that different CRDT types could be implemented and tested independently before integration into the larger system.

By the end of the CRDT exploration phase, I had developed not just technical knowledge about distributed data structures, but a systematic methodology for understanding and implementing complex distributed systems concepts. This methodology would prove invaluable for all the subsequent technical challenges in the project, from performance optimization to security implementation to user experience design.

## From Prototype to Production: The Complete Engineering Cycle

The CRDT exploration represented the final piece of the theoretical foundation, but transforming that understanding into production-ready code required a systematic transition from prototype to implementation. This phase demonstrated the full power of the methodical approach I had developed, showing how specialized analysis could guide confident implementation decisions.

### The Multi-Agent Analysis Pipeline

Rather than jumping directly from CRDT prototypes to implementation, I applied the same systematic approach that had proven effective for requirements analysis and architectural planning. This involved deploying specialized AI agents for different aspects of the transition from research to production code.

The first step was a comprehensive code review of the CRDT prototypes using a specialized code review agent. This wasn't a superficial style check, but a deep analysis of the algorithmic correctness, performance characteristics, and integration implications of the prototype implementations. The code review agent examined each CRDT type for mathematical correctness, identifying subtle bugs in the convergence logic that could have caused data inconsistencies in production.

The code review revealed several critical insights that wouldn't have been apparent from casual inspection. The vector clock implementation had edge cases around timestamp handling that could cause incorrect ordering decisions. The LWW-Register deterministic tie-breaking logic had potential performance issues when dealing with large numbers of concurrent operations. The Tree CRDT cycle detection algorithm had exponential worst-case complexity that could freeze the application with pathological input.

More importantly, the code review identified architectural integration challenges that the isolated prototypes hadn't addressed. How would CRDT operations integrate with the existing IndexedDB storage layer? How would the vector clock metadata be synchronized across WebRTC connections? How would the user interface handle the transient inconsistencies that occur during CRDT convergence?

The code review findings triggered a second round of requirements analysis using a specialized requirements engineering agent. This agent took the prototype learnings and the architectural constraints established in the earlier ADRs and produced a comprehensive specification for the production CRDT implementation.

![Image description](/assets/posts/i-was-so-angry-i-built-my-own-workshop-platform/4iwny1sb409cxxk7rlao.png)

The requirements engineering process revealed that the production system needed capabilities that hadn't been apparent during the prototype phase. The CRDT implementation needed to support multiple collaboration modes, allowing users to choose between automatic conflict resolution and host-controlled approval workflows depending on the workshop context. The storage layer needed to handle CRDT metadata efficiently while maintaining the offline-first guarantees established in earlier architectural decisions.

The requirements analysis also identified performance and scalability constraints that would significantly influence the implementation approach. The system needed to handle mindmaps with hundreds of nodes while maintaining sub-100ms response times for user interactions. The CRDT metadata overhead needed to be minimized to avoid overwhelming the WebRTC data channels with synchronization traffic.


![Image description](/assets/posts/i-was-so-angry-i-built-my-own-workshop-platform/6ccj6154wt0zdcrwav0a.png)

Perhaps most importantly, the requirements engineering process produced a clear specification for how the CRDT implementation would integrate with the existing application architecture. Instead of retrofitting CRDTs onto the existing codebase, the specification defined clean interfaces and abstraction layers that would allow the CRDT functionality to be developed and tested independently before integration.

With comprehensive requirements and architectural guidance in place, the actual implementation work was delegated to Opus, an AI agent specialized in production code generation. This division of labor proved remarkably effective – the analysis agents had provided the deep understanding and architectural constraints needed for confident implementation, while the implementation agent could focus on translating those specifications into clean, well-tested code.

The implementation process followed the test-driven development practices established in the earlier phases, but with the added confidence that came from thorough upfront analysis. Each CRDT operation was implemented with comprehensive test coverage that verified not just the happy path scenarios, but the edge cases and error conditions identified during the code review phase.

The systematic approach enabled rapid implementation without sacrificing quality. The implementation agent could generate production-ready code quickly because many of the difficult design decisions had been resolved during the analysis phase. The code review findings had identified potential pitfalls in advance, allowing the implementation to avoid common CRDT implementation mistakes that often require expensive refactoring to fix.

### Architectural Decision Records: Codifying the Learning

The transition from prototype to project culminated in a series of Architecture Decision Records that codified the lessons learned during the systematic analysis process. These ADRs represented the distillation of weeks of research, prototyping, and analysis into concrete architectural principles that would guide ongoing development.

ADR-004 established the conflict-free collaboration architecture, defining how CRDTs would be integrated with the existing WebRTC and storage layers. The ADR included detailed specifications for vector clock implementation, operation serialization protocols, and conflict resolution strategies. More importantly, it established the hybrid approach that would allow the system to support both automatic CRDT-based collaboration and host-controlled approval workflows depending on the workshop context.

ADR-005 defined the domain model architecture, establishing patterns for representing business entities in vanilla JavaScript without the type safety provided by TypeScript or similar systems. The ADR codified the constructor-based initialization patterns, serialization approaches, and validation strategies that would ensure consistency across all domain objects in the system.

ADR-006 addressed the database abstraction layer, defining how the Promise-based IndexedDB wrapper would be extended to handle CRDT metadata and operation logs. The ADR established patterns for transaction management, error handling, and performance optimization that would ensure the storage layer could handle the additional complexity introduced by distributed collaboration.

ADR-007 formalized the test-driven development practices that had proven essential for managing the complexity of distributed systems implementation. The ADR established guidelines for test structure, coverage requirements, and the red-green-refactor cycle that would ensure continued code quality as the system grew in complexity.

ADR-008 defined the module organization strategy, establishing how the growing codebase would be structured to maintain clarity and prevent the architectural decay that often accompanies rapid feature development. The ADR established patterns for feature-based organization, dependency management, and interface design that would support continued development without compromising the vanilla JavaScript architectural principles.

### The Eight-Hour Engineering Cycle

The complete cycle from initial Miro frustration to production-ready distributed collaboration system represented approximately eight hours of focused engineering work. This remarkable efficiency wasn't the result of cutting corners or accepting technical debt, but rather the compound benefits of systematic analysis and methodical implementation practices.

The first three hours involved problem analysis and initial prototyping. This phase established the basic requirements, explored the solution space through rapid AI-assisted prototyping, and identified the key technical challenges that would need to be addressed. The prototyping work revealed the complexity of WebRTC and CRDT implementation while providing enough understanding to guide the deeper analysis that would follow.

The middle two hours focused on deep technical understanding. This phase involved reading RFCs, analyzing existing implementations, and developing comprehensive prototypes that demonstrated the behavior of complex distributed systems concepts under various conditions. This investment in foundational understanding proved crucial for making informed architectural decisions and avoiding the common pitfalls that plague distributed systems development.

The final two three involved the transition from understanding to production implementation. This phase leveraged specialized AI agents for code review, requirements engineering, and implementation, demonstrating how systematic analysis could enable rapid but high-quality development. The comprehensive ADRs produced during this phase codified the architectural decisions and established principles that would guide ongoing development.

### Measuring Success: From 166 to 300 Tests

The effectiveness of the systematic approach was measurable in concrete terms in the next eight hours. Phase 1 of the project, which established the basic offline mindmap functionality, concluded with 166 passing tests providing comprehensive coverage of the core features. Phase 2, which added the distributed collaboration capabilities, concluded with 300 passing tests, nearly doubling the test suite while maintaining the same high standards for coverage and quality.

This growth in test coverage reflected the increasing complexity of the system, but also demonstrated that the test-driven development practices established during Phase 1 scaled effectively to handle distributed systems challenges. The systematic approach to testing meant that the complex CRDT algorithms, WebRTC connection management, and real-time synchronization features were all developed with the same confidence and reliability as the simpler offline functionality.


![Image description](/assets/posts/i-was-so-angry-i-built-my-own-workshop-platform/kdsklazve677hk4pixro.png)



The test suite growth also validated the architectural decisions made during the analysis phase. The modular design meant that CRDT functionality could be tested in isolation from WebRTC concerns. The clean abstraction layers meant that complex distributed systems logic could be tested without requiring actual network connections or browser environments. The domain model patterns meant that business logic could be tested independently of storage and synchronization concerns.

### Usable Distributed Collaboration

By the end of Phase 2, the systematic engineering approach had produced a collaborative mindmapping system with real-time collaboration between multiple users, automatic conflict resolution through CRDT algorithms, and graceful handling of network partitions and offline scenarios.

The comprehensive ADRs provided clear guidance for future feature development. The extensive test suite provides confidence for refactoring and optimization work. The modular design supports adding new collaboration modes or storage backends without disrupting existing functionality.

### Lessons for Systematic Engineering

The complete engineering cycle from frustration to production system demonstrated several key principles that distinguish systematic engineering from ad-hoc development approaches. The investment in deep understanding, while requiring more upfront time, enabled confident decision-making and rapid implementation that more than compensated for the initial time investment.

The use of specialized AI agents for different aspects of the development process proved remarkably effective, but only when guided by systematic analysis and clear architectural principles. The AI agents were most valuable when focused on specific, well-defined tasks rather than attempting to solve the entire problem space simultaneously.

The Architecture Decision Records proved essential for maintaining architectural coherence across multiple development phases and different implementation approaches. The ADRs served not just as documentation, but as active guidance that prevented architectural drift and ensured that new features integrated cleanly with existing capabilities.

Perhaps most importantly, the systematic approach demonstrated that complex distributed systems could be developed with the same confidence and reliability as simpler applications, provided that the foundational understanding and architectural principles were established through rigorous analysis. The test-driven development practices that worked for basic CRUD operations scaled effectively to handle CRDT algorithms and WebRTC protocols, proving that systematic engineering practices were universally applicable rather than limited to specific problem domains.

## Technical Outcomes


![A good Starter for 2 days of work](/assets/posts/i-was-so-angry-i-built-my-own-workshop-platform/au1xd0wvedinsk3qefsr.png)

**Phase**: 166 passing tests, complete offline mindmap editor with IndexedDB storage, auto-save, undo/redo, and SVG rendering.

**Phase 2**: 300 passing tests, WebRTC peer-to-peer collaboration, CRDT conflict resolution, real-time synchronization, and multi-peer mesh networking.

**Architecture**: comprehensive ADRs covering vanilla JavaScript patterns, offline-first design, CRDT implementation, test-driven development, and module organization.

**Technology Stack**: Pure vanilla JavaScript, IndexedDB for storage, WebRTC data channels for communication, Node.js test runner for TDD, no external frameworks or build tools.

The project demonstrated that systematic analysis and deep technical understanding can accelerate development while maintaining code quality. Reading RFCs, implementing prototypes, and using specialized AI agents for code review and requirements engineering proved effective.

The 8-hour cycle from initial frustration to to initial system showed how methodical engineering practices compound to enable rapid but reliable development of complex distributed systems.

Is it smart to do this? Maybe not! Did I learn something? A lot!
