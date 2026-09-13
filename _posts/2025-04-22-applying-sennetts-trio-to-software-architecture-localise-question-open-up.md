---
layout: post
title: "Applying Sennett's Trio to Software Architecture – Localise, Question, Open Up"
date: 2025-04-22 09:58:09 +0000
permalink: "/2025/04/22/applying-sennetts-trio-to-software-architecture-localise-question-open-up/"
description: "Software development, particularly software architecture, is often discussed in terms of engineering..."
tags: [architecture, programming]
og_type: article
devto_url: "https://dev.to/sebs/applying-sennetts-trio-to-software-architecture-localise-question-open-up-l5n"
render_with_liquid: false
---

Software development, particularly software architecture, is often discussed in terms of engineering – precision, blueprints, predictability. While engineering principles are vital, there's a deeper layer: **craftsmanship**. Like a master woodworker or potter, a great software architect blends technical skill with intuition, adaptability, and a profound understanding of their materials (code, patterns, infrastructure).

> Sociologist Richard Sennett, in his [exploration of craftsmanship](https://en.wikipedia.org/wiki/The_Craftsman_(book)), identified three foundational abilities: **"to localise, to question and to open up."** He elaborates: "The first involves making a matter concrete; the second, reflecting on its qualities; the third, expanding its sense."

This simple yet profound framework offers a powerful lens through which to view the art and practice of software architecture. Let's break down how these abilities manifest in the architect's daily work.

### 1. Localise: Making Architecture Concrete

> *Sennett: "...making a matter concrete..."*

Software architecture often starts with abstract concepts: business needs, user stories, high-level goals ("We need a scalable e-commerce platform," "Improve user engagement," "Reduce operational costs"). The first act of architectural craftsmanship is **localisation** – translating these fuzzy requirements into tangible, specific architectural elements.

This involves:

*   **Defining Boundaries:** Identifying distinct services, modules, or components. Where does one part of the system end and another begin?
*   **Specifying Interfaces:** Designing clear API contracts (REST, gRPC, message schemas) that define how components interact. This makes abstract communication concrete.
*   **Choosing Technologies:** Selecting specific databases, programming languages, frameworks, cloud services, or communication protocols based on concrete needs and constraints.
*   **Modeling Data:** Defining precise data structures and schemas. How is information actually represented and stored?
*   **Diagramming:** Creating sequence diagrams, component diagrams, deployment diagrams – visual representations that make the abstract structure concrete and understandable.

Localisation anchors the architecture. It moves from vague ideas to specific, actionable decisions. Without localisation, architecture remains a hand-wavy concept; with it, we have a blueprint, a tangible plan that engineers can build upon. It's about taking "it should be fast" and defining *how* fast (latency targets) and *how* we achieve it (caching strategy, asynchronous processing, efficient database queries).

### 2. Question: Reflecting on Architectural Qualities

> *Sennett: "...reflecting on its qualities..."*

Once an architectural element or decision is localised (made concrete), the next critical step is to **question** it. This isn't about negativity; it's about deep analysis, critical thinking, and understanding the inherent properties and trade-offs of the choices made.

Architects must constantly ask:

*   **Why this choice?** What are the alternatives we considered and rejected, and why?
*   **What are the trade-offs?** Choosing microservices might improve deployability but increase operational complexity. What are we gaining, and what are we sacrificing?
*   **How does it perform?** What are the expected latency, throughput, and resource consumption characteristics? How will it behave under load?
*   **Is it secure?** Have we considered potential vulnerabilities? How are we addressing authentication, authorization, and data protection?
*   **How maintainable is it?** Is the design understandable? How easy will it be to modify or debug later? Is the code complexity manageable?
*   **Is it scalable? Resilient? Testable? Observable?** Architects evaluate the design against these critical "ilities" or quality attributes.
*   **What are the failure modes?** What happens when a dependency fails? How does the system degrade gracefully?
*   **What assumptions are we making?** Are these assumptions valid? What happens if they change?

Questioning prevents architects from blindly following trends or making decisions based on incomplete information. It forces a rigorous evaluation of the *qualities* of the concrete design, ensuring it truly meets the system's needs (both functional and non-functional). This reflection is the heart of architectural decision-making.

### 3. Open Up: Expanding the Architectural Sense

> *Sennett: "...expanding its sense."*

The final ability, **opening up**, is about broadening the perspective beyond the immediate, localised, and questioned element. It involves seeing the bigger picture, considering future evolution, and challenging the status quo.

In software architecture, opening up means:

*   **Considering Alternatives:** Actively exploring different architectural patterns, technologies, or approaches, even if they seem unconventional at first. Could a different paradigm (e.g., event-driven vs. request-response) offer significant advantages?
*   **Thinking Long-Term:** How might this system need to evolve over the next 1, 3, or 5 years? How can the current architecture facilitate future changes and growth rather than hinder them? This involves designing for extensibility and adaptability.
*   **Seeing Systemic Impact:** Understanding how a decision in one part of the system affects other parts, the team's workflow, operational practices, and even the business strategy.
*   **Challenging Constraints:** Questioning perceived limitations. Are constraints genuinely fixed, or are they assumptions that can be revisited? Can we influence requirements or infrastructure decisions?
*   **Learning and Adapting:** Staying abreast of new technologies, patterns, and ideas from the wider software development community and considering how they might apply or reshape the current understanding.
*   **Fostering Innovation:** Creating space for experimentation and emergent design where appropriate, allowing the architecture to evolve based on learning.

Opening up prevents architectural stagnation and myopia. It ensures the architecture is not just technically sound for today but also strategically positioned for tomorrow. It's about understanding the "sense" or meaning of the architecture within its broader context and potential future.

### The Cycle of Craftsmanship

These three abilities are not strictly linear; they form a continuous cycle. You **localise** an idea into a concrete design. You **question** its properties and trade-offs. This questioning might reveal flaws or limitations, prompting you to **open up** to alternative solutions or broader implications. This leads to new ideas that need to be **localised** again, starting the cycle anew.

> By consciously cultivating the abilities to localise, question, and open up, software architects move beyond mere technical implementation towards true craftsmanship. They build systems that are not only functional but also robust, adaptable, and well-suited to their purpose, embodying the thoughtful integration of skill, analysis, and vision that defines the master craftsman.
