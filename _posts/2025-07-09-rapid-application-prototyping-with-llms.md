---
layout: post
title: "Rapid Application Prototyping with LLMs"
date: 2025-07-09 11:37:24 +0000
permalink: "/2025/07/09/rapid-application-prototyping-with-llms/"
description: "LLM-driven rapid prototyping regenerates disposable prototypes from evolving specs to validate assumptions in hours, illustrated with a racing simulator."
tags: [ai-assisted-development, game-development]
og_type: article
image: "/assets/posts/rapid-application-prototyping-with-llms/og.jpg"
devto_url: "https://dev.to/sebs/rapid-application-prototyping-with-llms-240e"
render_with_liquid: false
---


![The basic protoyping loop](/assets/posts/rapid-application-prototyping-with-llms/ta8c55q20o8vtlzgno3f.webp)

The traditional software development cycle—requirements, design, implementation, testing—often validates assumptions too late. By the time you discover a fundamental flaw, weeks of work are already invested. Large Language Models enable a different approach: rapid, disposable prototypes that validate assumptions in hours rather than weeks.

The process begins with  analyzing the project scope and generating focused prototype specifications. For a racing simulator, we might identify tire physics, weather systems, and AI behavior as critical subsystems requiring validation. Each becomes a standalone markdown specification, containing just enough detail to generate a working prototype.

These specifications follow a consistent pattern. They describe the desired behavior, not the implementation. They explicitly state what to test and what to ignore. They include success criteria that can be evaluated quickly. A tire degradation spec might focus solely on whether players can intuitively understand wear patterns, ignoring performance optimization or visual polish.

![Systems lead to prototypes](/assets/posts/rapid-application-prototyping-with-llms/fonslbmwt6x88nar100e.webp)

The workflow operates in tight cycles. The LLM generates a prototype from the specification. Testing reveals flaws or validates assumptions. Instead of modifying the generated code, the specification is updated with learnings. A fresh prototype is generated, incorporating these insights cleanly. Each iteration takes hours, not days.

Consider the track rendering prototype. The first iteration used STL files—too memory intensive. The second tried OBJ format—better performance but insufficient detail for a 20.8km track. The third used glTF with level-of-detail optimization. Each iteration answered specific questions about performance and visual fidelity. The final specification captured these learnings without carrying forward any technical debt.

The discipline required is counterintuitive. Generated code is treated as entirely disposable. No refactoring, no bug fixes, no incremental improvements. This prevents the accumulation of assumptions and workarounds that plague traditional prototypes. Each generation starts fresh, incorporating only the validated learnings from previous iterations.

![When generating anything: analyse it](/assets/posts/rapid-application-prototyping-with-llms/ovpl70jnkd9m2kfqolpy.webp)

Architecture decisions emerge naturally from this process. When the weather system prototype revealed performance constraints, it triggered technical decisions. When tire physics showed unacceptable latency in networked play, client-side prediction became a requirement. These aren't theoretical choices—they're empirically validated through rapid experimentation.

The LLM's role extends beyond code generation. It analyzes test results, suggests new prototypes based on discovered constraints, and maintains consistency across specifications. When the tire degradation UI proved effective, the LLM proposed applying similar patterns to fuel management and brake temperature displays.

Specifications evolve through iterations. Early versions often over-specify implementation details. Through repeated generation cycles, they distill down to essential behaviors and constraints. A mature specification reads like a behavioral contract: "Players must understand tire wear through visual feedback alone. No numbers or gauges. Performance must maintain 60fps with 20 cars on track."

The approach scales beyond technical validation. User experience prototypes test interface concepts. Performance prototypes establish computational boundaries. Integration prototypes verify that subsystems can communicate effectively. Each type follows the same cycle: specify, generate, test, learn, regenerate.

Learnings compound across prototypes. The track renderer's success with glTF influenced the car model approach. UI patterns from tire management informed fuel strategy displays. Performance optimizations discovered in one prototype applied to others. The knowledge graph grows with each iteration, captured in specifications rather than code.



The transition from prototyping to production development becomes a conscious decision based on diminishing learning returns. When new prototypes confirm rather than challenge existing understanding, when technical risks are quantified and mitigated, when user interactions are validated—then the experimental phase can end. The generated code and insights serve as good input for clearly defined requirements and  fetures in the next development phase. 

This approach integrates seamlessly with LLM-conservative development teams. While production code remains entirely human-written, the rapid prototyping phase generates concrete insights that transform requirements engineering. User stories evolve from "As a player, I want to see tire wear" to "As a player, I want color-coded tire temperature visualization transitioning from blue to red, with wear shown as tread depth reduction, updated every 100ms to maintain responsiveness during high-speed sections." The specificity comes from validated prototypes, not assumptions.

This methodology is a shift in risk management. Traditional development front-loads planning and back-loads discovery. LLM-driven prototyping front-loads discovery through rapid experimentation. By the time production development begins, major unknowns have been resolved through empirical testing rather than theoretical analysis.

The economic impact is significant. Validating assumptions in hours rather than weeks reduces both development cost and opportunity cost. Failed approaches are discovered quickly and abandoned cheaply. Successful patterns are identified and can be applied consistently across the system.

The implications extend beyond individual projects. As LLMs improve, the fidelity and sophistication of generated prototypes will increase. The cycle time from idea to validated prototype will continue to shrink. Teams that master this approach will maintain a significant competitive advantage in their ability to explore solution spaces rapidly and thoroughly.

The key insight isn't that LLMs write production code—they don't. It's that LLMs enable a new development methodology where learning is cheap, iteration is fast, and assumptions are validated empirically rather than theoretically. In an industry where building the wrong thing is often more expensive than building the thing wrong, that's a game-changing capability.
