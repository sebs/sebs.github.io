---
layout: post
title: "Extreme Left Shifting"
date: 2025-06-27 20:58:09 +0000
permalink: "/2025/06/27/extreme-left-shifting/"
description: "Extreme left shifting lets developers run the full build and deploy pipeline locally: faster feedback, Makefile-based CI/CD, paved paths and trade-offs."
tags: [devops, software-architecture]
og_type: article
devto_url: "https://dev.to/sebs/extreme-left-shifting-1lnm"
render_with_liquid: false
---
Left shifting refers to moving software development lifecycle activities to earlier stages in the process. While this concept traditionally applies to testing and security practices, organizations are extending it to include build and deployment processes. This approach involves enabling developers to execute the complete software delivery pipeline on their local machines, using the same tools and processes that run in production CI/CD systems.

The core principle is eliminating differences between local development environments and production deployment processes. When developers can build, test, and deploy applications locally using identical procedures to those used in CI/CD pipelines, they can identify integration issues, configuration problems, and deployment failures before committing code to shared repositories. This reduces the time between making a change and receiving feedback about its correctness.

This implementation of left shifting addresses feedback loop delays inherent in traditional development workflows. Instead of committing code, waiting for CI/CD systems to process changes, and then responding to failures, developers can validate their work immediately in their local environment. The approach requires infrastructure and tooling investments to make production-grade deployment processes available and practical for local execution.

## Left Shifting in Software Development

![Chart of effort across the lifecycle: the shift-left model peaks at plan and develop, the traditional model peaks at deploy](/assets/posts/extreme-left-shifting/cqtrtbg3phqov3rr4r0b.webp)

Left shifting moves activities from later stages of the software development lifecycle to earlier stages [1]. IBM Engineering defines it as "a practice in software development in which teams focus on quality, work on problem prevention instead of detection, and begin testing earlier than usual in the development cycle" [2]. The practice originated in quality assurance, where testing activities were moved from post-development phases into the development process itself.

Traditional software development creates handoffs between specialized teams. Developers write code, quality assurance teams test it, security teams review it, and operations teams deploy it. Each handoff introduces delays and potential for miscommunication. Issues discovered late in this process require more effort to fix than those found early.

Most left shifting implementations focus on integrating testing and security tools into development environments. Developers run unit tests locally and use security scanning plugins in their IDEs. However, the actual build and deployment processes typically remain centralized in CI/CD systems. This creates a gap between what developers can validate locally and what happens in production deployment.

Extending left shifting to include deployment processes means providing developers with the same tools and configurations used in production. This requires containerization, infrastructure as code, and deployment automation that can execute consistently across different environments. The developer's machine becomes capable of running the complete software delivery pipeline, not just a subset of it.

This approach differs from traditional local development in scope and fidelity. Instead of simplified local environments that approximate production behavior, developers work with environments that replicate production deployment processes. The same scripts, configurations, and tools used in CI/CD systems are available locally, ensuring consistency between development and production environments.

## Left Shifting in the Design Phase

Left shifting principles extend beyond implementation to the design phase of software development. Traditional design processes often defer technical constraints and operational considerations until later stages, leading to designs that are difficult to implement, deploy, or maintain. Applying left shifting to design means incorporating deployment, operational, and infrastructure concerns during the initial design phase.

Design-phase left shifting involves several practices. Architects and designers consider deployment patterns, infrastructure requirements, and operational constraints when creating system designs. They evaluate how applications will be built, tested, and deployed before finalizing architectural decisions. This prevents designs that are theoretically sound but practically difficult to implement or operate.

Infrastructure as code principles apply to design-phase left shifting. Instead of designing systems and then determining how to deploy them, teams design systems with deployment automation in mind. They consider how infrastructure will be provisioned, configured, and managed as part of the design process. This ensures that operational requirements influence architectural decisions rather than being retrofitted later.

Security considerations become part of the design process rather than a post-implementation review. Threat modeling, security requirements, and compliance constraints inform design decisions. Teams identify security boundaries, authentication mechanisms, and data protection requirements during design rather than discovering security gaps during implementation or testing.

Performance and scalability requirements influence design decisions when left shifting is applied to the design phase. Teams consider how applications will handle load, scale across infrastructure, and maintain performance under various conditions. They design monitoring, alerting, and observability into systems rather than adding these capabilities after deployment.

The design phase also incorporates testing strategies and quality assurance approaches. Teams design applications with testability in mind, considering how different components will be tested in isolation and integration. They plan test data management, test environment requirements, and automated testing approaches as part of the design process.

This integration of operational concerns into design requires collaboration between traditionally separate teams. Architects work with operations teams to understand infrastructure constraints and deployment requirements. Security teams participate in design reviews to ensure security requirements are addressed early. Platform teams provide input on deployment automation and infrastructure capabilities.

The result is designs that are inherently more deployable, operable, and maintainable. By considering the complete software lifecycle during design, teams create systems that align with operational realities rather than requiring significant modifications during implementation and deployment phases.

## Feedback Loop Characteristics in Development Workflows

Feedback loops in software development roughly consist of action, observation, and adjustment cycles. Tim Cochran remarks that developers perform approximately 200 micro-feedback loops per day [3]. These range from running unit tests to deploying complete application stacks. The time between action and feedback affects development workflow and code quality.

Traditional CI/CD workflows create extended feedback loops. A developer makes a code change, commits it to version control, waits for the CI system to process the change, execute build and test pipelines, and report results. This process typically takes 15-30 minutes or longer, depending on pipeline complexity and system load. During this time, the developer either waits or switches to other tasks.

Local execution of build and deployment processes reduces feedback time to minutes or seconds. Developers can run the same processes that execute in CI/CD systems without waiting for remote infrastructure. This enables more immediate validation of changes and rapid iteration on solutions.

The difference in feedback time affects development patterns. With fast local feedback, developers make smaller, incremental changes and test them immediately. With slow remote feedback, developers tend to batch changes and test them less frequently. The batching approach increases the risk of integration issues and makes debugging more difficult when problems occur.

Context switching represents another aspect of feedback loop efficiency. When developers wait for remote systems, they often switch to other tasks to maintain productivity. Returning to the original task requires rebuilding mental context about the code and problem being solved. This overhead compounds across multiple feedback cycles throughout the day.

Local feedback loops eliminate context switching by providing immediate results. Developers maintain focus on their current task and can iterate rapidly without interruption. This enables deeper engagement with the problem and more thorough exploration of solutions. Combined with Pair Programming, this small change in architecture can have many postive effects on output and quality. 

## Cognitive Load and Complexity Management

Left shifting build and deployment processes increases the cognitive load on developers. They must understand not only application code but also build systems, deployment configurations, infrastructure requirements, and operational procedures. This expanded scope of responsibility can overwhelm developers who prefer to focus on business logic implementation.

The cognitive load manifests in several areas. Developers need to learn container orchestration, infrastructure as code, deployment automation, and monitoring tools. They must maintain local environments that mirror production complexity, including databases, message queues, external service dependencies, and security configurations. They need to understand how changes affect the entire system, not just their immediate code.

Organizations address this complexity through "paved paths" - pre-configured tooling and processes that abstract underlying complexity [5]. A paved path provides developers with simple interfaces to complex deployment processes. For example, a single command might orchestrate container builds, database migrations, service deployments, and health checks without requiring developers to understand each step.

Creating effective paved paths requires significant investment from platform and infrastructure teams. These teams must identify common patterns, create reusable tooling, write documentation, and provide ongoing support. The tooling must be reliable, well-documented, and maintained as technology and requirements evolve.

Paved paths must balance abstraction with transparency. Developers need simple interfaces for routine tasks but also need access to underlying details when debugging or customizing behavior. The abstraction should hide complexity without creating black boxes that become obstacles when problems occur.

Different types of applications and development patterns may require different paved paths. A microservices architecture has different deployment requirements than a monolithic application. A data processing pipeline has different infrastructure needs than a web application. Organizations must create multiple paths while maintaining common patterns and shared tooling where possible.

The effectiveness of paved paths depends on organizational structure and team responsibilities. Platform teams must have clear ownership of the tooling and sufficient resources to maintain it. Development teams must have training and support to use the tools effectively. The division of responsibilities must be clear to avoid gaps in ownership or duplicated effort.


## Implementation Approaches for Local-First CI/CD

Local-first CI/CD requires designing pipelines as portable, environment-agnostic workflows. Rather than embedding logic in CI/CD platform-specific configurations, the approach treats CI/CD systems as wrappers for underlying build and deployment scripts. This ensures the same logic executes consistently in local and remote environments.

Makefiles provide a common implementation pattern for this approach. A Makefile defines build, test, and deployment operations as discrete targets that can be invoked individually or in combination. The same Makefile targets execute locally and in CI/CD systems, ensuring consistency between environments [4].

A typical Makefile structure includes targets for dependency installation, code quality checks, testing at multiple levels, build processes, and deployment operations:

```makefile
deps:
	npm install
	docker-compose pull

lint:
	eslint src/
	prettier --check src/

test.unit:
	npm run test:unit

test.integration:
	docker-compose up -d postgres redis
	npm run test:integration
	docker-compose down

build:
	npm run build
	docker build -t myapp:latest .

deploy.local:
	docker-compose up -d
	./scripts/wait-for-services.sh
	./scripts/run-migrations.sh

ci: deps lint test.unit test.integration build
```

The corresponding CI/CD configuration becomes a simple wrapper that invokes Makefile targets:

```yaml
jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run CI pipeline
        run: make ci
      - name: Deploy
        run: make deploy.staging
```

This approach eliminates the common problem of CI/CD configurations becoming complex, environment-specific scripts. The CI system invokes the same Makefile targets that developers use locally, ensuring identical behavior across environments.

Container technology enables environment portability by packaging applications and dependencies in consistent runtime environments. Docker Compose allows complex multi-service applications to be deployed locally with the same container images and configurations used in production. This provides developers with realistic local environments that closely mirror production behavior.

Environment-aware configuration allows the same deployment scripts to adapt to different contexts without becoming environment-specific. This involves using environment variables, configuration files that can be overridden, and conditional logic that adapts to available infrastructure. The deployment process runs consistently while producing appropriate results for each environment.

Service dependencies present challenges for local deployment. Production applications often depend on external services, databases, and infrastructure that cannot be replicated locally. Organizations address this through service mocking, lightweight local alternatives, and hybrid approaches where some services run locally while others are accessed remotely.

Data management requires special consideration in local environments. Production databases contain large datasets that are impractical to replicate locally. Local development typically uses smaller, synthetic datasets that provide realistic behavior without the overhead of production data volumes. Database migration scripts must work correctly with both production and local datasets.

## Implementation Challenges and Considerations

Resource constraints on developer machines limit the complexity of local environments. Modern applications often require substantial memory, CPU, and storage when running complete service stacks locally. Not all developers have hardware capable of running sophisticated local environments, particularly in organisations with diverse hardware standards. At first, some new specs for hardware will feel fancy, but given it directly reduces the time a person is waiting for work to complete - it is easy to get into 'break even' financially with more expensive 'bottom right' configurations.

Selective service deployment addresses resource limitations by allowing developers to run subsets of the complete system locally. Core services that developers actively modify run locally, while peripheral services are accessed through development or staging environments. Service virtualization tools provide lightweight alternatives to resource-intensive services.

Security requirements complicate local deployment in organizations with strict compliance needs. Security teams may restrict developers from running privileged containers, accessing production-like credentials, or deploying certain types of services locally. These restrictions require careful design of local environments that provide realistic behavior without exposing sensitive resources.

Sanitized local environments address security concerns by using synthetic data, mock external services, and local credential management systems. These environments provide necessary authentication and authorization behavior without exposing production secrets or sensitive data. Container security policies can enforce restrictions while enabling required local deployment capabilities.

Network dependencies and external service integration require special handling in local environments. Applications that integrate with third-party APIs, payment processors, or external data sources need local alternatives or mock implementations. These alternatives must provide realistic behavior for development and testing while avoiding actual external service calls.

Configuration management becomes more complex when the same application must run in local, staging, and production environments with different infrastructure, security, and scaling requirements. Configuration systems must support environment-specific overrides while maintaining consistency in core application behavior.

Debugging and observability in local environments require tools and practices that mirror production capabilities. Developers need access to logs, metrics, and tracing information to understand application behavior and diagnose issues. Local observability stacks must provide useful insights without the overhead of production monitoring systems.

Team coordination and shared understanding become important when multiple developers work with local deployment processes. Teams need consistent tooling, documentation, and practices to ensure that local environments behave similarly across team members. Differences in local setup can lead to environment-specific issues that are difficult to reproduce and debug.


## Organizational Structure and Process Changes

Local-first development requires coordination between development, platform, security, and operations teams. Clear ownership and responsibility for local development tooling prevents initiatives from stalling or failing to meet requirements. Without dedicated ownership, local development capabilities often become inconsistent or outdated as applications and infrastructure evolve.

Platform teams typically take responsibility for creating and maintaining local development tooling. These teams need expertise in both development and operations to create solutions that meet the needs of both communities. They must understand application requirements, infrastructure constraints, and operational procedures to design effective local development environments.

Developer training and support become necessary when expanding developer responsibilities to include deployment and operations tasks. Developers need to understand new tools, processes, and troubleshooting techniques. This training represents an investment in time and resources that organizations must plan for and support.

Documentation and knowledge sharing systems must cover local development processes, troubleshooting guides, and best practices. As local development tooling becomes more sophisticated, the documentation must keep pace to ensure developers can use the tools effectively. Poor documentation leads to inconsistent usage and reduces the effectiveness of local development capabilities.

Change management processes must account for local development requirements when updating infrastructure, deployment processes, or application dependencies. Changes that affect production deployment must also be reflected in local development tooling to maintain consistency. This requires coordination between teams and clear communication about changes that affect local environments.

Quality gates and validation processes need to account for local development workflows. Organizations must decide which validations can be performed locally versus which require centralized CI/CD systems. Some checks, such as integration testing with external services or security scanning with proprietary tools, may not be practical for local execution.

Metrics and monitoring of local development effectiveness help organizations understand the impact of their investments. Key indicators include time from code change to feedback, frequency of CI/CD pipeline failures, developer satisfaction with local tooling, and time spent on environment setup and maintenance. These metrics guide improvements and justify continued investment in local development capabilities.

Cultural change accompanies the technical implementation of local-first development. Developers must adapt to expanded responsibilities and new workflows. Operations teams must adjust to developers having more direct control over deployment processes. Management must support the investment required to create and maintain local development capabilities.

Gradual implementation helps manage cultural and technical changes. Organizations can start with pilot projects that demonstrate local development capabilities before expanding to broader teams. This approach allows teams to learn and refine processes before committing to organization-wide changes.

## Summary

Extreme Left shifting build and deployment processes to developer machines extends the traditional concept of moving activities earlier in the development lifecycle. This approach enables developers to execute complete software delivery pipelines locally or in the cloud using the same tools and processes used in production CI/CD systems.

The implementation requires treating CI/CD pipelines as wrappers for portable deployment logic rather than as the source of truth for build and deployment processes. Makefiles and similar tools provide consistent interfaces for executing deployment operations across different environments. Container technology enables environment portability by packaging applications and dependencies consistently.

Cognitive load management becomes critical as developers take on expanded responsibilities for deployment and operations. Paved paths abstract complexity while providing access to underlying details when needed. Platform teams must create and maintain tooling that balances simplicity with transparency.

Technical challenges include resource constraints on developer machines, security requirements, legacy system integration, and service dependency management. Organizations address these through selective service deployment, sanitized local environments, incremental modernization, and hybrid approaches that combine local and remote resources.

Organizational changes accompany technical implementation. Clear ownership of local development tooling, developer training programs, updated documentation, and change management processes support successful adoption. Gradual implementation allows teams to learn and refine processes before organization-wide deployment.

The approach represents a specific implementation of left shifting principles focused on eliminating the gap between local development and production deployment. Success depends on technical implementation, organizational support, and ongoing investment in tooling and processes that enable developers to work effectively with expanded responsibilities.

## References

[1] Praecipio Consulting. (2024, March 14). "Maximizing Efficiency and Quality: The Shift Left Approach in DevOps." https://www.praecipio.com/resources/articles/shift-left-in-devops

[2] IBM Engineering. "What is shift left?" IBM Topics. https://www.ibm.com/topics/shift-left

[3] Cochran, T. (2021, January 26). "Maximizing Developer Effectiveness." Martin Fowler's Blog. https://martinfowler.com/articles/developer-effectiveness.html

[4] Lunbeck, N. (2025, April 30). "Local-first CI/CD with Makefiles." Shipyard Blog. https://shipyard.build/blog/local-first-cicd-with-makefiles/

[5] Protsenko, M., & Linders, B. (2023, April 21). "Dark Side of DevOps - the Price of Shifting Left and Ways to Make it Affordable." InfoQ. https://www.infoq.com/articles/devops-shifting-left/
