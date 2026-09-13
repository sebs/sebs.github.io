---
layout: post
title: "Generator Generator"
date: 2026-03-10 12:39:08 +0000
permalink: "/2026/03/10/generator-generator/"
description: "Ask AI for procedural grammars, not single assets: a 40-piece, 3D-printable Agile Workshop Token set shows how generative systems beat one-off images."
tags: [ai-assisted-development, game-development]
og_type: article
image: "/assets/posts/generator-generator/og.jpg"
devto_url: "https://dev.to/sebs/generator-generator-1m0h"
render_with_liquid: false
---
Suppose you need to produce a physical set of Agile Workshop Tokens for your development team. Forty distinct pieces: planning poker chips embossed with Fibonacci values, sprint coins, retrospective cards, role medallions. You have two ways to ask an AI for help.

The first way: ask a generative model to show you what an Agile Workshop Token looks like. It obliges. You receive a pleasant render of a melted-looking coin bearing the legend "SCRROM MSTR." It has no dimensional accuracy, no awareness of Agile methodologies, and no manufacturing utility whatsoever. This is the Nano Banana approach — prompting a black-box model to spit out a singular, static artifact. It yields a statistically probable object frozen in time: zero parametric control, no hierarchical semantics, and a complete ignorance of physical constraints. It is an artifact stripped of its axioms.

The second way is the subject of this essay.

Instead of asking for a token, you ask the AI to design the classical procedural grammar for manufacturing an entire ecosystem of tokens. The output is not an image. It is a generative engine — a formal system of rules, constraints, and stochastic parameters that, when executed, produces exactly 40 watertight, functionally distinct, 3D-printable models. This is the paradigm shift: moving from the discrete generation of objects to the synthesis of generative systems.

```plaintext
f(Direct_Prompt) → X_static
f(System_Prompt) → Parametric_Engine(Θ)
Σ Parametric_Engine(p, t) = ∞
```

The token set will reappear throughout this essay as our running example, grounding each theoretical claim in the concrete output of a real pipeline.

---

## I. The Nano Banana Fallacy

Direct asset generation treats artificial intelligence as a glorified vending machine. The fundamental problem is not quality — modern diffusion models produce convincing images. The problem is structure. A static output has no memory of how it was made, no handles by which it can be adjusted, and no awareness of the constraints that govern the domain it represents.

In game development, the fallacy is obvious. A neural network hallucinating a 3D mesh of a sword gives you messy topology that cannot be animated, lacks collision volumes, and has no semantic awareness of its own edge flow. The Nano Banana sword is useless the moment you need a second sword that is longer, or rustier, or held by a different character.

A generated system, by contrast, outputs the deterministic procedural grammar to forge a million weapons. It defines the hierarchical L-system of the hilt, the Bézier constraints of the blade curvature, and the algorithmic distribution of surface wear based on a runtime age parameter. It generates the mathematical forge, not the singular sword.

Apply this lens to our token set. A direct prompt gives us one melted coin. The meta-generative approach gives us a shape grammar:

```plaintext
G = (V, Σ, R, S)

Where V is the set of abstract token categories,
      Σ is the terminal geometries (hexagons, discs, shields, rectangles),
      R represents the substitution rules,
      S is the starting axiom.
```

That grammar, when executed, produces not one token but a coherent family of forty — each geometrically distinct, each semantically correct, each printable.

---

## II. The Three Phases of Meta-Generation

The pipeline that produced our token set operates in three distinct phases. These phases are universal — they apply equally to architectural design, material science, and synthetic data generation. Understanding them is the key to applying the meta-generative approach in any domain.

### Phase One: Semantic Partitioning (SPLIT)

The generator's first task is not to draw anything. It is to understand the domain well enough to partition the problem space correctly. For the token set, this means recognising that "Agile Workshop" implies a specific ecosystem of functional object types with specific real-world usage distributions.

The system allocates thirteen VotingChips — because planning poker requires a full Fibonacci sequence plus variants — eight SprintCoins, twelve RetroCards, and seven RoleMedallions. These numbers are not arbitrary. They reflect the actual ratio of pieces required for a workshop of eight to twelve people. A Nano Banana generator ignores this entirely; it does not know what a sprint retrospective is.

In architectural morphogenesis, the equivalent phase generates Voronoi tessellation logic for load-bearing steel, partitioning the structural problem into zones parameterized against wind shear and solar radiation. The output is not a building; it is a spatial algorithm.

### Phase Two: Parametric Substitution (SUB)

Once the semantic partitions exist, the generator binds each abstract category to concrete geometry and encodes domain-specific rules as mathematical constraints. This is where the system demonstrates genuine understanding.

For VotingChips, the generator correctly applies the Fibonacci sequence to the value distribution:

```plaintext
f(n) = f(n−1) + f(n−2)  ∀ VotingChip_value
Values: 0, ½, 1, 2, 3, 5, 8, 13, 21, ?
```

This is not a cosmetic choice. Fibonacci values in planning poker reflect a deliberate epistemological decision: the gaps between numbers encode increasing uncertainty. A generator that assigned random integers would produce a set that looks like poker chips but fails as a planning tool. The meta-generative system encodes the mathematical rule directly into the substitution grammar.

SprintCoins become hexagons (stable, grippable, stackable); RetroCards become rectangles with write-on surfaces and lane indicators (+/Δ/−) that map to the three-column retrospective format; RoleMedallions become shields, differentiated by weight and finish from the lighter functional tokens.

The industrial engineering parallel is the generation of topology optimisation algorithms for triply periodic minimal surfaces — gyroids and diamond lattices — where the substitution rules encode physical constraints like energy absorption and mass minimisation rather than Fibonacci sequences and retrospective formats. The structure of the problem is identical.

### Phase Three: Instantiation (TERMINAL)

The grammar resolves. Terminal rules execute Boolean mesh operations, stamp glyphs onto base geometry, apply edge-banding for physical grip, assign material properties, and export watertight models. For the token set:

```plaintext
AXIOM: Token → queued

────────────────────────────────────────────────────────────
[SPLIT]    Token → VotingChip    ×13 instances
[SPLIT]    Token → SprintCoin    ×8  instances
[SPLIT]    Token → RetroCard     ×12 instances
[SPLIT]    Token → RoleMedallion ×7  instances

────────────────────────────────────────────────────────────
[SUB]      VotingChip    → BaseDisc    + ValueBadge(0,½,1,2,3,5,8,13,21,?)
[SUB]      SprintCoin    → BaseHex     + FaceGlyph(⚡×3, ↗×2, ✓×2, 🔥×1)
[SUB]      RetroCard     → BaseRect    + WriteSurface + CategoryBar(+/Δ/−)
[SUB]      RoleMedallion → BaseShield  + RoleGlyph(SM,PO,Dev,QA,UX,STK,Coach)

────────────────────────────────────────────────────────────
[TERMINAL] 40 meshes instantiated, glyphs stamped, edge-bands placed
[TERMINAL] GENERATION COMPLETE: 40 tokens, seed 0xA91ECAFE
```

The same three-phase structure appears in every successful application of meta-generation: partition the domain, bind abstract categories to mathematically constrained geometry, instantiate. The domain changes; the architecture does not.

---

## III. Where the Paradigm Extends

### Parametric Architecture and Urban Morphogenesis

When an architect uses a basic generative AI to create a render of a futuristic building, they receive a beautiful hallucination that fundamentally ignores thermodynamics, zoning laws, and material tensile strength. It is, like the melted coin, a useless image.

A meta-generative system does not output a building. It outputs a spatial algorithm. It generates Voronoi tessellation logic for load-bearing steel, parameterizing geometry against wind shear and solar radiation. Instead of a static blueprint, the system defines a generative grammar where floorplans dynamically restructure themselves based on traffic flow optimisations and HVAC efficiency constraints. Critically, the geometry produced can be mathematically constrained by Cauchy's equilibrium equation:

```plaintext
∇ · σ + F = 0
σ = C : ε
```

Every procedural strut is guaranteed to actually support its structural load — something no hallucinated render can promise.

Note the structural echo of the token pipeline. The architect's grammar partitions a building into zones (SPLIT), substitutes each zone with geometrically constrained elements (SUB), and instantiates watertight, structurally valid meshes (TERMINAL). The domain is different. The architecture is the same.

### Synthetic Data and Kinematic Reality

Machine learning models for autonomous driving or robotics cannot be trained on static images. They require rich, physically accurate synthetic environments. A direct-to-image AI cannot generate a functioning physics simulation.

A meta-generative system writes the deterministic rules for a dynamic world. It parameterises the friction coefficients of procedural asphalt, generates the optical scattering algorithms of simulated fog, and orchestrates the localised stochastic behaviours of pedestrian traffic models. The system continuously updates its probability distributions:

```plaintext
P(A | B) = P(B | A) · P(A) / P(B)
```

The generative system iterates its own parameters to generate edge-case scenarios — the long tail of rare events that directly trains physical robotics.

The token pipeline's stochastic layer encodes the same principle at a smaller scale. Hue is not fixed; it is drawn from a normal distribution centred on the family colour with standard deviation 12°, creating warm and cool variants within each token family. The spatial seed map ensures that tokens physically adjacent on a print sheet share correlated aesthetic properties — a form of local Bayesian coherence baked into the generation rules.

---

## IV. Praxis: What Do You Actually Use This For?

![The generated system turned into a demo webapp displaying the workshop tokens](/assets/posts/generator-generator/woc1g5n8i31jjno0mjml.webp)

The pragmatic reader is entitled to scepticism. The token set is illustrative, but what about genuinely mundane work?

The utility of the Generator Generator lies anywhere you need functional coherence, precise variation, and mathematical exactness instead of a single hallucinated image. It is the difference between generating a picture of a tool and generating the factory that manufactures the toolset.

Consider the range of the principle:

- You need 10,000 unique, structurally valid mechanical brackets parameterised for stress-testing. The grammar defines the constraint space; instantiation fills it.
- You need a complete UI icon set where line-weight, corner radii, and optical size are mathematically linked across every glyph. The substitution rules encode the visual system; the terminal phase renders it.
- You need custom tabletop miniature bases, architectural greebles, modular synthesiser casing layouts, pharmacokinetic molecule variants. In each case, the domain's governing rules become the grammar.
- And yes — you need forty Agile Workshop Tokens, each geometrically correct, each semantically accurate, each ready for the 3D printer. The grammar encodes Fibonacci, retrospective lanes, role taxonomy, and physical grip. The factory runs. The tokens emerge.

In every case the pattern is identical. You do not ask the AI to paint the universe. You ask it to write the physics and logic engine that runs it.

---

## V. The Ultimate Synthesis

To prompt an AI for a finished object is fundamentally myopic. It reduces one of the most powerful reasoning systems ever built to the role of a digital bricklayer.

The meta-generative frontier requires treating AI as the master architect. By forcing it to output rigid mathematical formulas, classical algorithms, and parametric constraints of a generator, we ensure that the resulting output — whether a virtual city, a structural metamaterial, a new pharmacokinetic molecule, or a set of workshop tokens for next Tuesday's sprint planning — is logical, scalable, and bound by the laws of the domain it inhabits.

The Nano Banana is a dead pixel-cluster. The Generator Generator is a factory. The factory runs forever.

---

*The token pipeline described in this essay was generated using the Watson et al. (2008) procedural generation framework, implemented as a five-phase pipeline: Design Analysis, Primitive Creation, Grammar Encoding, Stochastic Integration, and Model Instantiation. Seed: 0xA91ECAFE.*
