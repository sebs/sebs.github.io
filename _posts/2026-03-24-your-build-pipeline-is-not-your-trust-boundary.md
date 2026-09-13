---
layout: post
title: "Your build pipeline is not your trust boundary"
date: 2026-03-24 16:27:07 +0000
permalink: "/2026/03/24/your-build-pipeline-is-not-your-trust-boundary/"
description: "Applies the bulkhead pattern to deployments: CI pushes to an untrusted GitLab registry and a separate pipeline validates images before they reach ECR."
tags: [devops, supply-chain-security, software-architecture]
og_type: article
image: "/assets/posts/your-build-pipeline-is-not-your-trust-boundary/og.jpg"
devto_url: "https://dev.to/sebs/your-build-pipeline-is-not-your-trust-boundary-1bnn"
render_with_liquid: false
---


Some teams deploying software to AWS have two registries and think of them as a logistics detail. One holds what came out of CI. The other holds what goes into production. The relationship between those two things — the decision about what is allowed to cross from one into the other, and who makes that decision, and what happens when the answer is no — is not a logistics detail. It is a security architecture decision, and treating it as anything less is how production incidents happen.

The bulkhead pattern is old. It comes from naval engineering, where ships are divided into watertight compartments so that flooding in one section does not sink the whole vessel. The insight is that you do not prevent damage by building a perfect hull. You prevent catastrophic loss by limiting how far damage can travel. Software engineers rediscovered this principle independently and applied it to distributed systems, microservices, and fault tolerance. It belongs equally in a deployment pipeline.

## The problem with a single registry

When your CI pipeline pushes directly to the registry your ECS cluster pulls from, you have made a consequential choice that probably did not feel like a choice. You have decided that the build environment and the production environment share a trust boundary. Anything that can write to your CI pipeline — any engineer, any compromised dependency, any malformed Dockerfile, any branch that passes tests — can, directly or indirectly, place an artifact into the registry that production infrastructure will consume without further scrutiny.

This is not a theoretical concern. Supply chain attacks against CI systems have become routine. A compromised build dependency installs a malicious binary during the build phase. The resulting image passes your existing image scan if the scanner's definitions are not current, or if the binary is not yet known to the scanner. The image gets tagged and pushed. On the next deploy, ECS pulls it and runs it in your production environment. At no point did anything behave unexpectedly from a pipeline perspective. Every light was green. That is the problem.

The deeper issue is that a single-registry architecture conflates two fundamentally different questions. The first question is: did this build succeed? The second question is: is this artifact trustworthy enough to run in production? CI answers the first question. Only a deliberate validation gate — one that runs independently of the build environment, with different permissions and different tooling — can answer the second.

## The structure of a bulkhead deployment

The architecture worth building has four distinct zones, each with clearly scoped responsibilities and explicitly limited permissions between them.

The first zone is your GitLab CI pipeline. Its job is to build. It runs your tests, compiles your code, assembles your container image, and pushes that image to the GitLab Container Registry. The GitLab registry in this architecture is intentionally treated as ephemeral and untrusted. It is a staging area. Images land there the way packages land on a loading dock: present, but not yet cleared for entry. CI runners have write access to the GitLab registry. They have no access to AWS whatsoever. Not to IAM, not to ECR, not to ECS. If your CI environment is compromised, the blast radius is bounded to the GitLab registry.

The second zone is the deliver pipeline. This is the bulkhead. It is triggered — on a tag, on a merge to a protected branch, on whatever promotion event your organization has decided represents a release candidate — and its sole purpose is to evaluate whether an image from the GitLab registry is trustworthy enough to enter the AWS trust boundary. It pulls the image, runs validation: vulnerability scanning, signature verification, policy checks, SBOM attestation, whatever your threat model requires. If validation passes, it pushes the image to ECR and tags it with a provenance marker. If validation fails, it stops there. Nothing enters AWS. The deliver pipeline is the only principal in your entire system with write access to ECR.

The third zone is ECR. In this architecture, ECR is not just a faster registry. It is a trust signal. The presence of an image in ECR means exactly one thing: the deliver pipeline evaluated it and cleared it. No image arrives in ECR through any other path. Your ECS tasks can therefore pull from ECR with confidence that the contents were not placed there by a CI runner, a developer with elevated credentials, or an automated process that bypassed validation. ECR's access policy reflects this: the deliver pipeline can write, ECS task roles can read, and nothing else has write access.

The fourth zone is the deploy pipeline and ECS cluster. The deploy pipeline runs inside AWS, typically on a runner with an IAM role scoped to the specific ECS actions it needs. It reads from ECR, updates the task definition, and triggers a rolling deployment. It has no awareness of GitLab's registry. It does not cross back outside the AWS trust boundary for any artifact. The deployment is entirely self-contained within the environment it controls.

## Why the boundary placement matters

You could draw the bulkhead in a different place. You could run validation inside the CI pipeline, before the push to GitLab's registry, and use a single registry throughout. Many teams do this. It is better than no validation at all. But it is not a bulkhead. A bulkhead only works if the compartments it separates are genuinely isolated — if flooding one compartment cannot automatically flood the other. Validation that runs inside the same environment as the build is subject to all the same compromises as the build. A malicious package can interfere with test execution. A malicious script can tamper with scanner output. The environment in which validation runs cannot be the same environment that produced the artifact being validated, if you want the validation to mean anything.

The deliver pipeline solves this because it runs in a clean context with no dependency on the build environment. It does not trust the image. It does not trust the metadata the build produced. It pulls the image, treats it as an opaque artifact of unknown provenance, and evaluates it from scratch. The only thing it takes on faith is that the image digest it pulls from the GitLab registry corresponds to what CI claims to have built — and even that can be addressed with build attestation and signed manifests if your threat model demands it.

There is also an operational argument separate from the security argument. When validation and promotion are separated from build, you can change your validation requirements without touching your build configuration. You can introduce a new scanner, tighten a policy, or add a new required attestation by changing the deliver pipeline. CI keeps running the same way it always has. The operational surface of security changes shrinks considerably.

## Permissions as documentation

One of the most underappreciated properties of this architecture is what the permission model tells you. When you look at your IAM policies and your GitLab CI variable scopes, the structure of your trust boundaries is legible. GitLab runners have credentials that can push to the GitLab registry. They have nothing in AWS. The deliver pipeline has credentials to read from the GitLab registry and write to ECR. ECS task roles can read from ECR. The deploy pipeline can describe and update ECS services. Nothing has more than it needs. Nothing can reach across a zone boundary it has no business crossing.

This matters because permissions-as-documentation is honest in a way that comments and runbooks are not. Runbooks say what is supposed to be true. IAM policies say what is actually true. When your access model is correctly scoped, reading it is equivalent to reading the architecture. When your access model has accumulated scope over time — when CI runners have ECR write access because someone needed to debug something once and never cleaned it up — the permissions tell you that the architecture has quietly collapsed. The bulkhead no longer holds because the compartments are no longer sealed.

Keeping the permission model clean is not just security hygiene. It is architectural discipline. Every time you are tempted to give a component access to something outside its designated zone — to let CI push directly to ECR "just this once," to give the deploy pipeline GitLab credentials "because it's easier" — you are being asked to trade architectural clarity for convenience. The answer should almost always be no.

## The cost

This architecture is not free. You have a third pipeline to maintain, with its own failure modes and operational requirements. The deliver pipeline becomes a single point of failure in your promotion path: if it is broken, no image reaches production regardless of how healthy your build and deploy pipelines are. You need to monitor it, alert on it, and be capable of diagnosing failures in it quickly.

The deliver pipeline also adds latency to your release cycle. Validation takes time. Scans take time. If your threat model requires extensive policy evaluation, the gap between a successful build and a deployable artifact may be measured in minutes rather than seconds. This is usually acceptable, but it is a real tradeoff that your organization needs to make consciously rather than discover in the middle of an incident.

The answer to both of these costs is not to eliminate the bulkhead. It is to treat the deliver pipeline with the same engineering seriousness as the rest of your infrastructure. It deserves good observability, clear failure messages, documented recovery procedures, and regular testing. A security boundary that cannot be maintained is not actually a security boundary.

## What this is not

A bulkhead is not a substitute for secure coding practices. An image that passes every validation check you have defined can still contain application-level vulnerabilities. The bulkhead protects you against supply chain compromise in the build environment and enforces a consistent set of standards on every artifact that reaches production. It does not protect you against vulnerabilities you have not checked for or logic errors in your application code.

A bulkhead is also not a guarantee of immutability. An image that passes validation today may have a vulnerability discovered tomorrow. Your ECR should be configured with immutable tags so that an existing image digest cannot be overwritten, and you should have a process for responding to newly discovered vulnerabilities in images that are already in production. The bulkhead tells you about the state of an artifact at the moment it crossed the boundary. Keeping that assessment current over time is a different problem, requiring different tooling.

What a bulkhead is, at its most fundamental, is a decision about what it means to trust an artifact. Defining that decision explicitly, embodying it in a pipeline stage with clear inputs and clear outputs, and enforcing it as the mandatory path between your build environment and your production environment — that is the entire value of the pattern. The implementation details matter less than the clarity of the decision. Before you build anything, you should be able to answer: what does it mean for an image to be trustworthy? Who decides? What happens when the answer is no? If those questions have clear answers, you have an architecture. If they do not, you have a pipeline.
