---
layout: post
title: "Facing the Shai-Hulud Worm: Where the Hell is Easystreet?"
date: 2025-09-19 20:39:15 +0000
permalink: "/2025/09/19/facing-the-shai-hulud-worm-where-the-hell-is-easystreet/"
description: "Defenses against each stage of the Shai-Hulud npm worm: phishing training, 2FA, signed commits, scoped tokens, key rotation and locked-down containers."
tags: [supply-chain-security, devops]
og_type: article
devto_url: "https://dev.to/sebs/facing-the-shai-hulud-worm-where-the-hell-is-easystreet-4b60"
render_with_liquid: false
---


The recent Shai-Hulud supply chain attack on the NPM ecosystem has reminded the javascript development community that they face risks at many levels.  The attack, which employed a self-replicating malware to propagate through the NPM registry, was not a straightforward smash-and-grab operation.  It was a planned campaign that employed a variety of attack vectors and vulnerabilities to accomplish its goals.

 The following diagram is featured in an early [article](https://www.trendmicro.com/en_us/research/25/i/npm-supply-chain-attack.html) by Trend Micro:

 ![Trend Micro diagram of the Shai-Hulud npm attack chain, from phishing and credential theft to repo exposure and exfiltration](/assets/posts/facing-the-shai-hulud-worm-where-the-hell-is-easystreet/5trrcj25bsll14hgoz8t.webp)

 I wanted to offer some advice as someone who uses Node on a daily basis and has code published on NPM. I am also passionate about open-source ecosystems. Regrettably, I am unable to write a doom-and-gloom post about Node, JavaScript, or TypeScript, despite the fact that it appears to attract a large audience.  We should review all the stages and generate some ideas on how to make it at least more difficult to replicate them in your codebase.

 > The attack commenced with a targeted phishing campaign that was directed at NPM package maintainers.  The fraudulent emails were crafted to deceive developers into disclosing their credentials by posing as legitimate NPM security alerts.  Once the perpetrators had compromised a developer's account, they were able to publish malicious package updates.

 In all sincerity, it is recommended that you undergo phishing training.  The instant you believe you have a comprehensive understanding of phishing, it is imperative that you update your software specifically on this subject.  This game is contrived at every stage, and it must become second nature to refrain from clicking on links.  Particularly when you are responsible for safeguarding a key for NPM, it is crucial to develop proficiency in this area.  I am not attributing guilt or blame to any individual for the insecurity, panic, or other emotions that motivated the individual to click on the link and input their credentials.

 > Upon obtaining access, the attackers uploaded malicious versions of popular NPM packages.  The Shai-Hulud worm, a self-replicating payload that executed upon installation, was present in these products.

 [Use 2FA on npm when publishing a package](http://docs.npmjs.com/requiring-2fa-for-package-publishing-and-settings-modification).  I also experienced the "push to main ship to npm" phase at one time; however, this has a disadvantage, as we can observe.  The additional task is worthwhile.  It would be beneficial if the Agile and DevOps communities would cease to oversell the concept of "200 deploys per day" as a mere feature. 

 > The embedded bash script in the malicious JavaScript is utilized to implement a routine for credential theft, propagation, and persistence.

 The intriguing method employed here is that the credentials are not the initial item to be extracted; rather, a conduit is established to ensure their persistence.  This necessitates a commit to the repository.  Commits may also be [signed](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits).

 Mitigations against an additional YAML file in the GitHub Actions folder are present, with branch protections on a file/folder basis.  Organize your possessions and subsequently secure them.  A 'shattering the glass procedure' is not an issue for processes such as the addition of a new pipeline YAML.  It is also possible to maintain a codeowners file; however, this is a component of the repository, which is related to branch protections.  Therefore, human intervention is required for any modification to the "actions" folder.  Regarding automated instruments that facilitate credential theft:

 In your pipeline, you could utilize a container to construct and execute your application tests, linting, and other tasks.  Therefore, you can be certain that no accidental credentials are disclosed.  Pipelines with lengthy credentials lists are a minor antipattern that arises when the build and release pipelines are not separated.  The same is true for "well-settled development machines"—the convenience of being able to perform every task.

 It appears that a Docker container can be restricted in its network access on a DNS basis as well.  I have never done that before, but the following information is available on [Medium](https://medium.com/faun/docker-container-networking-and-security-59535493b35d).  The traffic for the extraction is not reaching the URLs, despite the fact that Npm is installing from a single source.  The use of a DNS-based Nginx proxy may not be the definitive solution for DNS shenanigans. However, in the event of a 'drive-by attack' such as this, the extraction phase via a third-party domain may not be successful when all traffic is throttled except for a limited number of domains.  'Logging a thing' is an uncommon occurrence in which it is necessary to prevent the issue.  Docker's attempt to establish an internet connection should be cause for alarm and necessitate an immediate response. 

 > Retrieves the username and the OAuth scopes that have been granted.  Determines whether the token possesses the necessary workflow and repository permissions.

 All right.  Here are a few straightforward ones.  The 'one token all-area access' that is unfortunately quite typical in a SaaS cloud-native internet can be replaced with more precise permissions.  GitHub has undergone significant changes; the majority of features related to token permissions are quite antiquated, and the default GITHUB_TOKEN [has permissions that can be configured](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token).  Once more: if you require tokens with a significant amount of permission scope, examine your pipeline and divide it into the distinct concerns of building and distributing.  This is the point at which it is advisable to purchase a GitHub account for each user, as it is quite costly. It is advisable to refrain from accepting contributions from colleagues who are using non-org accounts.  In general, tokens are static authentication information that must be utilized for a limited period.  Temporally restricted passwords (e.g., SSH).  Attempt to modify (roll) them and document the time required to do so.  This is a critical process that should be completed at numerous stages of the development lifecycle.

 - Has the initial production deployment been completed?  Roll the keys and deploy them once more.  To ensure that the procedure is effective, roll the keys for the individual who departs the team or, in the worst-case scenario, is laid off.
 - the keys are rolled after a predetermined period has elapsed.  Even better, they should become invalid after a certain period.
 - Security updates in dependencies: If the issue was data exfiltration in your supply chain, you can either read all the changelogs or presume that the keys have been compromised and roll them back.

 If feasible, eliminate static keys to the greatest extent feasible; alternative approaches are frequently advantageous.  Consider automating and "institutionalizing" the process of procuring and resetting those keys if your initial thought was "that is a lot of effort for little gain." 

 > Copies all private repositories that have been identified.  Executes a full-repository mirror cloning with a comprehensive history.

 These clones are made public under the user's identity, which presents a challenge that cannot be resolved through DNS.  We operate on GitHub and essentially trust Git—anythingHub.  The GitHub host can be blocked in a container or other virtual machine.  This is merely for the sake of expediency during the final exfiltration.  The prohibition of this method of exfiltration will undoubtedly lead to the development of an alternative method.  We are not prevailing by design; it is a game of cat and mouse.  It may be advantageous to "assume breach" and at least incorporate techniques from the comprehensive "Zero Trust" concept.  I will undoubtedly disregard the section regarding the potential consequences of my codebase becoming public domain. 

 > Utilization of a webhook to extract credentials

 Once more, why are our pipelines permitted to communicate with this domain?  ---

 I do not wish to extend the discussion beyond what is necessary by writing a lengthy opinion article on the current state of Javascript and NPM.  This quote from [Tante](https://bsky.app/profile/tante.cc/post/3lz2sac5oh22u) identifies the source of the issue:

 > There is a professionalization trap: In theory, everyone has the ability to generate everything flawlessly.  The appearance of CMSs is both clean and professional, and recording equipment has become more affordable.  That is a snare.  It restricts your expression and homogenizes everything.

 The elder I get, the more frequently I will opt for "ugly but more secure" over "professional."  Upon reviewing the initial load of infected repositories, I discovered numerous items that are inconvenient to lack (e.g., ANSI colors for the terminal?) and are incorporated into other modules, even if they are enumerated multiple times.

 To misquote an additional intelligent entity: 

 > At times, the sole viable course of action is to refrain from participating.

 (Wargames, Joshua)
