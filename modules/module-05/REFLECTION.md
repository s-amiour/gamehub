# Module 5 — Reflection

**Team name**: s-amiour
**Branch**: `module-05/s-amiour`
**Submitted**: before Module 6 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

The game-service now has two models for the same data: SQLite for writes, Redis for reads. They store the same games in two different shapes.

**Why go through the trouble of maintaining two representations of the same data?**

Think about what kind of queries each model is optimised for, and what would happen if you tried to use the write model for high-traffic read operations.

> The main reason for CQRS (segragating DB model into two, each with a distinct responsability) is operation performance. The write model, SQLite, handles data integrity constraints and ACID transactions. On the other hand, the read model, Redis, is responsible for returning stored data as efficiently as possible by pre-computing and storing denormalized views to serve user's needs. If we force the write model to handle read operations as well, it is susceptible to performance bottlenecks due to the competition between the read queries and the write locks.

---

## 2. Your choice

The logging-service checks GDPR consent before recording any activity. If a user has not opted in, the log is silently dropped.

**What does this consent check force you to accept about your data?** It is incomplete by design — some activities will never be recorded.

From a system design perspective: where is the right place to enforce this rule — in the logging-service, in the activity-service, or at the gateway? Why?

> This forces the system to be limited to only recording consented activity, thereby preventing it for storing global metrics. Inherently, the rule should be explicitly configured in the `logging-service`, as it separates operation concerns and allows for fast fire-and-forget operations without needing to somehow parse the request url further to access such rules, if they are stated in other services.

---

## 3. The tradeoff

With CQRS, your write model and read model can drift out of sync — a game is updated in SQLite but the Redis projection still shows the old data.

**In what scenario does this inconsistency matter to the user? In what scenario is it completely acceptable?**

Is there a class of applications where eventual consistency is never acceptable? What are they?

> Again, as mentioned in the the `Discussion` section of the `exercise.md` file, inconsistency is unacceptable in impactful operations like changing the username or password, whereas it is not harmful in scenarios of aggregate data like global leaderboards, hypothetically. Eventual consistency is unacceptable in systems requiring strict correctness and safety rules. Examples include healthcare/medical records (inconsistency in medications could lead to unreasonable decisions) and strict inventory booking (consistent details are vital for booking seats or rooms in reservations).

---

*Keep this file. You will refer back to it during the oral presentation.*
