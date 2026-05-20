# Module 1 — Reflection

**Team name**: `s-amiour`
**Branch**: `module-01/s-amiour`
**Submitted**: before Module 2 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

You started from a painful monolith. Now you're splitting it into separate services.

**What concrete problem does that split solve: and for whom?**

Think about it from three angles: the developer who has to change code, the team that has to deploy it, and the user who has to live with its failures. You don't need to cover all three, pick the one that felt most real to you today.

> From the user's perspective, this split solves the problem of total system failure. In a monolith, a memory leak or infinite loop in the notification engine would crash the entire application, kicking users offline and breaking gameplay tracking.

---

## 2. Your choice

Look at your service map. Every arrow between two services is a decision someone made.

**Pick one boundary, one place where you decided service A should not be part of service B. Explain why that line exists.**

What would break, slow down, or become harder to manage if you merged those two services back together?

> `activity-service` and `logging-service`. I separated them because they change for entirely different reasons: activity => product features, while logging => legal and compliance requirements. If they were merged, every tweak to compliance rules would risk introducing bugs into core gameplay tracking loop.

---

## 3. The tradeoff

Microservices solve the monolith's problems. But they create new ones.

**Name one thing that was simpler in the monolith and is now harder in your distributed design.**

No need to solve it: just name it honestly. This is exactly the tension the rest of the course is about.

> Debugging.. tracing a request end-to-end is now harder. In a monolith, an error provides a clear trace. Now, if a request like user finishing a game but their friends aren't notified, the bug could be hidden in any service.

---

_Keep this file. You will refer back to it during the oral presentation._
