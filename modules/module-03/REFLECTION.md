# Module 3 — Reflection

**Team name**: s-amiour
**Branch**: `module-03/s-amiour`
**Submitted**: before Module 4 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

All client requests now go through the gateway. No client ever calls a service directly.

**Why does that single entry point exist? What would the client's life look like without it?**

Think about what the client would need to know and manage if it talked to each service on its own port.

> API gateway simplifies client communication by acting as a unified entry point (port 8000). Without it, clients would need to track the specific ports of every backend service, causing significant maintenance overhead whenever services are added or relocated.

---

## 2. Your choice

The activity-service makes two outbound calls: one to validate the user (with retry logic), one to fetch game data (with a null fallback if it fails).

**Why are these two calls treated differently? Why does one retry and the other just give up gracefully?**

What is the consequence for the user in each case if the downstream service is unavailable?

> User validation is a strict dependency. The activity must not be saved if the user does not exist, as this prevents invalid data entry. Fetching game details is supplementary. If the game service fails, the activity should still be saved with null value for game data, ensuring the primary operation succeeds without unnecessary disruption.

---

## 3. The tradeoff

Every time a client creates an activity, three services are involved synchronously. They all have to be running, healthy, and fast.

**What is the systemic risk of chaining synchronous calls like this?**

What happens to the user experience if the slowest service in the chain takes 3 seconds to respond?

> While synchronizing calls simplifies the system, it creates a bottleneck. You cannot access any data until all data is ready, meaning a single slow service forces the entire system to wait those full 3 seconds. Waiting >= 3 secs is, as you know, a disincentive for the user.

---

*Keep this file. You will refer back to it during the oral presentation.*
