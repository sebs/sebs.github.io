---
layout: post
title: "Dora + Kanban + RelativeWeight = <3"
date: 2025-04-23 10:15:17 +0000
permalink: "/2025/04/23/dora-kanban-relativeweight-3/"
description: "DevOps is a deliberate attempt towards delivering better software faster and more reliably. Often,..."
tags: [devops, metrics, estimates]
og_type: article
devto_url: "https://dev.to/sebs/dora-kanban-relativeweight-3-47ae"
render_with_liquid: false
---
DevOps is a deliberate attempt towards delivering better software faster and more reliably. Often, it's a change that touches technology, process, and, crucially, people. Achieving the promised benefits of speed, stability, and efficiency isn't about finding a single silver bullet tool or metric. Instead, it requires building a cohesive, interconnected system where different practices amplify each other's strengths. Within this system, three fundamental pillars stand out: understanding **what** work delivers the most value, managing **how** that work progresses through the delivery pipeline, and objectively measuring **the results** of our efforts.

Let's delve into how frameworks for prioritization like Relative Weighting, flow management systems like Kanban, and key DevOps performance indicators work in concert. This powerful synergy is fundamentally fueled by a supportive organizational **Culture** and significantly accelerated by strategic **Automation**. Together, they form a dynamic engine driving continuous improvement and high performance.

**Dora and more**

Effective prioritization and smooth flow are means to an end. How do we know if these efforts are translating into tangible improvements in software delivery performance? This requires dedicated measurement using established **DevOps metrics**, particularly the four key DORA metrics. **Deployment Frequency (DF)** tracks how often changes are successfully released to production, indicating release cadence and speed. **Lead Time for Changes (LTfC)** measures the time from code commit to production deployment, reflecting pipeline efficiency and responsiveness. **Change Failure Rate (CFR)** quantifies the percentage of deployments causing failures, highlighting quality and stability issues. **Mean Time to Recovery (MTTR)** measures the average time to restore service after a failure, indicating resilience.

Beyond these core four, monitoring **Availability** (% uptime), **Error Rate** (% of failing requests), **Test Coverage** (% of code exercised by automated tests), **Infrastructure Cost**, **Automation Rate**, and **Security Metrics** (like Vulnerability Count and Time to Remediation) provides a comprehensive dashboard of system health, efficiency, and security posture. These metrics provide objective evidence of performance, moving conversations away from anecdotes and towards factual analysis. Culturally, they foster shared accountability for both speed *and* stability, demonstrating that these are not mutually exclusive goals but intertwined aspects of high-performing teams. Consistently positive metrics build internal confidence and external stakeholder trust. Poor metrics serve as clear, blameless signals pointing towards specific areas needing attention – a high CFR might trigger a review of testing practices, while a long LTfC could indicate bottlenecks in the CI/CD pipeline. The role of **automation** here is non-negotiable. Reliable collection of DF, LTfC, CFR, MTTR, Availability, and Error Rates at scale is practically impossible without automated tooling integrated into CI/CD pipelines, monitoring systems, and incident management platforms. More importantly, automation is the *engine* that drives improvement in these metrics: well done automated testing boosts quality (reducing CFR), automated deployments increase speed (improving DF and LTfC), and automated infrastructure management and recovery procedures enhance resilience (lowering MTTR).


**Relative Weigth**

Before a single line of code is written or a task is pulled into progress, the critical question is: "Are we working on the right things?" In complex environments with competing demands, relying solely on intuition or the loudest voice is a recipe for wasted effort and missed opportunities. Structured prioritization frameworks, such as the **Relative Weight** approach, bring much-needed clarity and objectivity. By systematically evaluating potential work items against dimensions like **Benefit (B)** – the value gained, **Penalty (P)** – the cost of *not* doing it, **Estimate (E)** – the required resources, and **Risk (R)** – the inherent uncertainty, we move towards data-informed decision-making. Calculating a **Priority** score, often combining these factors (e.g., `Value / Cost` where `Value = B + P` and `Cost = E + R`), allows for a rational comparison of initiatives, helping sequence work to maximize impact relative to investment.

> Surely, this is more complex than the 'just storypoints' approach from Scrum, but the constant interaction between product people providing information on the value part and tech teams working on effort and risk estimates. The extra effort is wort the time as multiple aspects of a Estimate are not intertwined. 

The cultural shift this enables is profound. Prioritization logic becomes transparent, fostering trust and enabling constructive dialogue between business stakeholders, product managers, and engineering teams. Instead of decisions happening behind closed doors, the criteria are open, encouraging collaboration as different perspectives contribute to assessing each factor. This cultivates a culture where decisions are grounded in shared understanding and objective assessment, rather than solely on hierarchy or opinion.  Furthermore, as automation matures within the delivery pipeline itself, providing consistent data on deployment times and failure rates, the 'Estimate' and 'Risk' inputs for prioritization become more accurate and reliable over time. 

**Kanban**

With priorities established, the focus shifts to execution. How does work actually move from concept to completion? This is where flow-based systems like **Kanban** excel. Kanban provides the principles and practices to make work visible and manage its journey through the value stream. Central to this is the visualization of workflow stages on a Kanban board and the disciplined management of **Work in Progress (WIP)** – the amount of work being actively processed at any given time. Limiting WIP is a cornerstone practice, preventing team overload and reducing the chaos of excessive context switching. It encourages a collective focus on completing tasks before starting new ones, fostering a "stop starting, start finishing" mentality.

> Devops Teams often choose Kanban over other organizational methods as taking on more operations responsibilities come with more 'unplanned' work than traditional 'project' oriented methods like scrum and the more 'ad hoc' approach to organization is often quoted as a reason.   

Kanban relies on key flow metrics to gauge efficiency. **Lead Time**, the total duration from request to delivery, measures the system's responsiveness from a customer perspective. **Cycle Time**, the duration from when work actively begins until completion, reflects internal processing speed. Tracking these, along with **Throughput** (the rate of completed items per time unit), provides invaluable insights. Visualizations like the **Cumulative Flow Diagram (CFD)** offer a powerful, holistic view, showing the distribution of work across stages over time and making bottlenecks glaringly obvious as specific bands on the chart widen disproportionately. Culturally, Kanban fosters transparency; everyone can see the state of work, identify blockers, and understand dependencies. The focus on limiting WIP promotes collaboration and swarm behavior to clear bottlenecks. The inherent visibility of flow metrics and CFD patterns naturally drives a culture of **continuous improvement (Kaizen)**, prompting regular reflection on how to streamline the process. Again, **automation** is a critical enabler. Digital Kanban tools automatically track items, calculate metrics like cycle time and throughput, and generate CFDs, freeing teams from manual tracking and providing real-time data for informed discussion and adaptation. Crucially, automation *within* the workflow – automated testing, builds, deployments – directly reduces the time items spend in active states, shrinking cycle times, smoothing the flow depicted on the CFD, and enabling the team to sustain lower, more efficient WIP limits.

**Summary of Key Calculations**

To provide a clear overview, the following table summarizes the core calculations discussed across these interconnected systems:

| Metric Name                      | Calculation / Formula                                            | Context / Source System            |
| :------------------------------- | :--------------------------------------------------------------- | :--------------------------------- |
| Value                            | `Benefit + Penalty`                                              | Relative Weight             |
| Cost                             | `Estimate + Risk`                                                | Relative Weight             |
| Priority                         | `Value / Cost`                                                   | Relative Weight             |
| Relative Benefit                 | `Benefit / Sum of all Benefits`                                  | Relative Weight             |
| Relative Penalty                 | `Penalty / Sum of all Penalties`                                 | Relative Weight             |
| Relative Estimate                | `Estimate / Sum of all Estimates`                                | Relative Weight             |
| Relative Risk                    | `Risk / Sum of all Risks`                                        | Relative Weight             |
| Weighted Priority                | `(w1*B + w2*P) / (w3*E + w4*R)`                                  | Relative Weight             |
| Deployment Frequency (DF)        | `Number of Deployments / Time Period`                            | DevOps               |
| Lead Time for Changes (LTfC)     | `Deployment Time - Commit Time`                                  | DevOps               |
| Change Failure Rate (CFR)        | `(Num Failed Deployments / Total Deployments) * 100%`            | DevOps     |
| Mean Time to Recovery (MTTR)     | `Total Downtime during Incidents / Number of Incidents`          | DevOps               |
| Mean Time Between Failures (MTBF)| `Total Uptime / Number of Failures`                              | DevOps                |
| Availability (%)                 | `(Total Uptime / (Total Uptime + Total Downtime)) * 100%`        | DevOps                |
| Error Rate (%)                   | `(Number of Errors / Total Number of Requests) * 100%`           | DevOps               |
| Infrastructure Cost              | `Tracked monetary cost over time (e.g., $/month)`                | DevOps               |
| Automation Rate (%)              | `(Num Automated Steps / Total Steps in Process) * 100%`          | DevOps             |
| Test Coverage (%)                | `(Lines/Branches Covered by Tests / Total Lines/Branches) * 100%`| DevOps    |
| Security Vulnerability Count     | `Sum of vulnerabilities identified by severity`                    | DevOps               |
| Time to Remediation (Security) | `Remediation Deployment Time - Vulnerability Detection Time`     | DevOps               |
| Security Incidents               | `Count of security events over time`                             | DevOps               |
| Lead Time (Kanban)             | `Completion Date/Time - Request Date/Time`                       | Kanban                     |
| Cycle Time (Kanban)            | `Completion Date/Time - Work Started Date/Time`                  | Kanban                     |
| Work in Progress (WIP)         | `Count of items in active workflow states`                       | Kanban                     |
| Throughput (Kanban)            | `Number of Completed Work Items / Time Period`                   | Kanban                     |

*Note: Some terms like 'Lead Time' appear in both DevOps and Kanban contexts but measure slightly different start/end points; the table clarifies the specific definition used.*

**The Engine in Motion: Culture and Automation as Catalysts**

These systems – prioritization, flow management, and performance measurement – are not isolated silos. They form a dynamic, interconnected engine. Effective **Relative Weighting** ensures that the items entering the **Kanban** system are those most likely to deliver value. Kanban optimizes the flow of this work, aiming to reduce **Lead Time** and **Cycle Time** while maintaining stability. **DevOps Metrics** then provide the crucial feedback loop, validating whether the prioritized work is being delivered quickly (DF, LTfC) and reliably (CFR, MTTR, Availability).

This feedback is where the engine truly gains momentum. Consistently long Kanban cycle times for certain types of work might influence future Risk/Estimate inputs in the prioritization phase. A high Change Failure Rate measured by DevOps metrics could trigger specific process improvements within the Kanban workflow, such as adding a dedicated review step or enhancing automated testing. Difficulty hitting Deployment Frequency targets might highlight bottlenecks visible on the CFD, prompting investment in pipeline **automation**.

**Culture** acts as the essential lubricant and the guiding philosophy for this engine. A culture of transparency ensures that prioritization logic, workflow status, and performance metrics are visible and understood by all. A commitment to continuous improvement leverages the data from Kanban and DevOps metrics to collaboratively refine processes, not assign blame. Cross-functional collaboration is vital for accurate prioritization inputs and for collectively tackling impediments revealed by flow or performance metrics.

**Automation**, meanwhile, is both the high-octane fuel and the fine-tuned mechanics of the engine. It makes the reliable, real-time collection of Kanban and DevOps metrics feasible. It directly accelerates the engine by reducing manual toil, shrinking cycle times, increasing deployment frequency, and enabling faster recovery from failures. It underpins the ability to rapidly iterate, deploy prioritized changes, and gather the crucial feedback needed for the next cycle of improvement.

**Conclusion: Building a Unified System**

Viewing prioritization frameworks, Kanban, and DevOps metrics as separate disciplines limits their potential. Their true power emerges when they are integrated into a single, coherent system focused on delivering value. Building such a system requires more than just implementing tools; it demands nurturing a **culture** rooted in transparency, collaboration, data-driven decisions, and relentless improvement. It also necessitates a strategic commitment to **automation**, not just for efficiency, but as a fundamental enabler of speed, stability, measurement, and feedback. By understanding and actively managing the interplay between *what* we choose to work on, *how* that work flows through our system, and *how* we measure the outcomes we can gain a pretty good understanding of how well a process and team works. 
You don't have to use all of the above, but for some you might already have the data available to you - No matter if you practice 'DevOps' or not.
