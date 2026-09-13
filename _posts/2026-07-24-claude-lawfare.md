---
layout: post
title: "Claude Lawfare"
date: 2026-07-24 17:45:39 +0000
permalink: "/2026/07/24/claude-lawfare/"
description: "CN: Death           I. The letter   My father died in November. Sometime between the 16th and the..."
tags: [lawtech, claude, kidsdontdothisathome, wehaveperrymasonathome]
og_type: article
devto_url: "https://dev.to/sebs/claude-lawfare-15on"
render_with_liquid: false
---
CN: Death

## I. The letter

My father died in November. Sometime between the 16th and the 19th — the death certificate gives a range, not a date, which is its own small horror to read on a form.

Months later, after the apartment was emptied and cleaned and handed back, after the trip south to collect the certificate of inheritance from the probate court and carry it, personally, to the housing cooperative's office, two letters arrived. They were dated eighteen days apart. They arrived in the same envelope, on the same day.

The gist: his membership in the cooperative would end. The shares — fourteen of them, a small four-figure sum — would be paid out to me after next year's members' meeting. A transfer of the shares themselves was "no longer possible due to the long delay."

I didn't want the money. I wanted the shares. In a housing cooperative the shares aren't an investment, they're a position: they're what makes you a member rather than a possible tenant. Converting them to cash is not a settlement, it's an eviction from a category: I could get a affordable apartment in my hometown and given I work in a org functionality for a company based there. Do your Math.

I also had the strong feeling — the specific, useless feeling you get when an institution tells you something in the passive voice — that this was wrong. Not unfair. *Wrong.* As in: incorrect. As in: someone in an office had put my file in the wrong pile and the wrong pile had a form letter attached to it.

But feeling that and knowing it are different things, and the gap between them is exactly where most people give up. That gap is made of statutes you've never read, a set of bylaws written in 1871 and amended for a century and a half, and the entirely reasonable suspicion that fighting over a four-figure sum will cost you more than the four figures.

So I did the thing that would have been science fiction three years ago. I dumped everything — the bylaws, the letters, the emails, the death certificate, the handover protocol, the whole miserable folder — into a context window and asked a language model to tell me whether I was right.

180 minutes later I had a two-page letter citing four statutes and three bylaw sections, a reference document mapping every legal provision in play, and a clear answer to the question I'd actually been asking, which was not *what are my rights* but *am I crazy.*

I was not crazy. The cooperative had applied the wrong paragraph.

---

## II. What actually happened, technically

The mechanics matter here, because the interesting part isn't "AI wrote a letter." Anyone can get an AI to write a letter. The interesting part is the shape of the reasoning, and where the machine was better than I was, and where it was worse.

**The documents were garbage and it didn't matter.** The bylaws were a scanned PDF of a printed booklet — no text layer, and the file wasn't even really a PDF, it was a zip of page images with a misleading extension. In 2019 this is where the project dies. Instead: unzip, rasterize, OCR with a German language model, and thirty-two pages of 19th-century cooperative law became searchable text. Imperfect text — the OCR rendered § as $ half the time — but searchable. The bad scan is no longer a barrier to entry. That is a bigger deal than it sounds. An enormous amount of the law that governs ordinary people's lives sits in exactly this format: scanned, unindexed, technically public and practically inaccessible.

**The core error was a paragraph mix-up, and finding it required reading two provisions side by side.** The cooperative had reasoned from the section governing *transfer of shares between living people* — which requires board approval, to which no one has a right. Hence "not possible." But when a member dies, that section doesn't apply. A different one does: the one saying membership *continues* through the heirs. Automatically. By operation of law. No application, no approval, no transfer. The entry in the members' register merely records what already happened; it doesn't create it.

That's the whole case. One paragraph substituted for another. It's not an exotic legal theory, it's a filing error with legal consequences, and once you see it you can't unsee it.

**The strongest argument came from a distinction the model made that I hadn't.** The bylaws *do* contain a six-month deadline — but the clause begins "if there are several heirs." I'm an only child of a divorced man; there is no one else. The deadline was never running. And then the move that made it airtight: that clause exists because the statute *permits* cooperatives to impose such a deadline, and the statute permits it explicitly and only "for the case of inheritance by several heirs." So even if the cooperative wanted to read its own bylaws expansively, it couldn't — the law above the bylaws doesn't allow it. The argument shifted from *that's not what your rules say* (arguable) to *your rules aren't allowed to say more* (not arguable).

I would not have found that. I know what I know, and the hierarchy between an enabling statute and a bylaw clause is not in it.

**The date the cooperative chose gave away its own reasoning.** Termination "due to death" — effective December 31st of the following year. That date can't be derived from anything except the several-heirs clause: deadline expires, membership ends at the close of that business year. So the office had assumed a community of heirs that failed to meet a deadline. The certificate of inheritance, which they had in their hands, says "sole." The date was a confession.

**And they had already called me the heir in writing.** Buried in an April email, in the middle of a paragraph about renovation costs: "son and heir of the deceased." They had accepted my inheritance for every obligation — clearing the apartment, the repairs, an outstanding invoice — and denied it for the one right attached to it. There's a Latin phrase for this and a section of the civil code, but you don't need either. You need someone to notice the sentence. The model noticed the sentence.

**Where it was worse than me, and this matters more than the wins:** at one point a draft stated a fact about my own case more precisely than I could actually back up. Not invented — I had told it so, and it had reasonably taken my word. But a confident, checkable, *false-if-challenged* factual claim sitting in the middle of an otherwise solid letter is exactly the thing that gets a good case laughed out of a room. The fix was to restate it in a form that was still true if someone pushed. Same argumentative force, no exposure.

The model flagged the risk itself, which is to its credit. But I had to be in the room to know which version of the fact would survive contact with the other side. **The machine can tell you which sentence is dangerous. It cannot tell you which one is true.** That's the whole division of labor, and everything below follows from it.

---

## III. The politics of having this thing

Here's the part I've been circling.

What happened in those 180 minutes was not that I got legal advice. I got something more specific and, I think, more consequential: **I got parity.**

The cooperative's office has a process. The process has been run hundreds of times. It has form letters, an internal sequence, precedent, and — decisively — the knowledge that almost nobody on the receiving end will check. That last asymmetry is the load-bearing one. Institutions are not usually malicious. They are usually *routinized*, and routine plus asymmetric knowledge produces outcomes indistinguishable from malice while everyone involved keeps a clear conscience.

The traditional fix is a lawyer. The traditional fix costs more than the thing you're fighting over, which is why the traditional fix mostly doesn't get used, which is why the routine keeps producing the same outcome. Every small wrong sits below the threshold where the remedy makes economic sense. That's not a bug in the legal system, that's the equilibrium the legal system rests on.

A capable model collapses the cost of *the first 180 percent* of that work to roughly zero. Not the last ten. Not the courtroom, not the strategy under adversarial pressure, not the judgment about which fights are worth having. But the reading, the mapping, the finding of the wrong paragraph, the drafting, the citation-checking — the part that turns a feeling into a claim. That part is now free.

I want to be careful about the triumphalism here, because there are three things about this that worry me.

**First: this cuts both ways, and the other way has more money.** If I can produce a well-cited demand letter in 180 minutes, so can a debt collector, a patent troll, a landlord's management company, a firm that sends ten thousand letters a month hoping two percent pay. The cost of *generating* legal pressure has fallen for everyone, and the people who were already generating legal pressure at industrial scale have better tooling and no scruples about volume. A world where everyone can produce a plausible legal threat instantly is not obviously a world with more justice in it. It may just be a world with more letters.

The asymmetry doesn't vanish. It moves. What used to be an asymmetry of *access to expertise* becomes an asymmetry of *capacity to absorb noise*. Institutions can absorb noise. Individuals can't.

**Second: fluency is not correctness, and this failure mode is nastier than the old one.** The false date almost went out. It was in a paragraph that read beautifully. A wrong claim wrapped in correct citations and confident structure is more dangerous than obvious nonsense, because obvious nonsense gets caught. There is a specific new hazard — a person with no legal training, holding a document that *looks* exactly like competent legal work, with no ability to tell which sentences are load-bearing and which are fabricated. They will send it. Some of them will send it into situations far more consequential than a dispute over cooperative shares.

The thing that made this work was not the model's competence. It was that I could check the facts it asserted, because the facts were about my own life. Every single time I caught something, it was a fact about *me* — what had actually happened, and how much of it I could prove. That's the domain where a layperson retains real epistemic authority. Push into a domain where the user can't check anything and the same fluency becomes a liability with a nice typeface.

**Third, and this is the one that actually keeps me up: this capability is contingent, and it is nobody's right.** I used a frontier model, on a good day, with a large context window, with tools that let it run OCR and search the web and render documents. None of that is guaranteed to exist next year in the form it exists today, at a price I can pay, for the uses I want to put it to.

Access can be tiered. Capability can be routed — a query about something sensitive can quietly get answered by a smaller model, and you may not be told. Terms of service can carve out legal use entirely, and there are real liability reasons a provider might want them to. Regulation could mandate that carve-out in the name of consumer protection, which would protect consumers from bad legal advice by protecting them from any legal advice at all, in the way that a locked hospital protects you from infection.

And the people who'd be least affected by all of that are the ones who already have lawyers.

The most darkly funny version of this: the institutions on the other side of these disputes will absolutely have the enterprise tier. Legal-tech procurement is a line item. A large housing company, an insurer, a collections agency — they will have the good model, integrated, with a compliance wrapper and an indemnity clause. The question is whether the person on the receiving end of the form letter has anything at all.

That, and not model capability, is the political question. The technology to close the gap exists. It worked. I have the letter, cited and dated and in the mail. The open question is whether that stays true for people with less time, less education, less money, and a worse case than mine — or whether this turns out to have been a brief window in which the tools were unusually good and unusually available, before the pricing and the liability lawyers and the regulators sorted everyone back into the categories they came from.

---

I don't know how the dispute ends. The deadline I set falls in the middle of August. If nothing happens I have two more letters ready — one to the supervisory board, one to the auditing association that reviews the cooperative's administration, including, as it happens, the correct maintenance of the members' register.

Both were drafted in about twenty minutes.

That's the part I can't stop thinking about. Not that a machine helped me win an argument. That a fight I would have lost by default — not on the merits, by *default*, by exhaustion, by the sheer administrative friction of being one person against a process — became a fight I could actually have.

For now.
