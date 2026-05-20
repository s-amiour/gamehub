# Module 2 — Reflection

**Team name**: s-amiour
**Branch**: `module-02/s-amiour`
**Submitted**: before Module 3 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

You built a service with distinct layers: models, schemas, repository, service, and routes — each with a single responsibility.

**Why not just put everything in one file and call it done?**

Think about what happens six months later when someone new joins the team, or when you need to swap SQLite for PostgreSQL. What does the layered structure protect you from?

> That change would tightly couples infrastructure to business rules. If routing, validation, and db queries are forced to live in one file, updating infra risks collapsing the endpoints. By following a layered approach, we are protected from outages and downtime.

---

## 2. Your choice

Each service owns its data exclusively — no other service is allowed to touch its database directly.

**Pick one entity your service owns (e.g. `User`, `Game`). What would go wrong if another service could write to that table directly?**

Give a concrete scenario, not a general principle.

> Consider the `User` entity. The `user-service` enforces specific business logic, such as hashing passwords via the service layer etc etc. If, for some reason, the game-service bypasses the `user-service` API and writes directly to the `users.db` file to create a new account, it bypasses the business logic entirely, resulting in unsanitized data being stored.

---

## 3. The tradeoff

You now have models, schemas, a repository, a service, and routes — five layers for what is essentially a CRUD service.

**For a system this small, what is the cost of all this structure?**

And at what point does the complexity start to pay off? Where is the tipping point?

> Development velocity. Say, for example, we add a new field for the `Game` model, we would modify the db model, update the `pydantic` schemas, and potentially alter repository and service layers. For such an app, this is over-engineering. The tipping point occurs when the service or management of the app outgrows basic CRUD operations.

---

*Keep this file. You will refer back to it during the oral presentation.*
