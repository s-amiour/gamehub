# Module 6 — Reflection

**Team name**: s-amiour
**Branch**: `module-06/s-amiour`
**Submitted**: before Module 7 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

The gateway now validates every JWT before forwarding a request. Individual services no longer need to check identity themselves.

**What does centralising authentication at the gateway buy you?** What would the alternative look like — if every service validated tokens on its own?

Think about what happens when you need to rotate the secret key, or add a new service to the system.

> Centralizing authN at gateway creates a single point of enforcement, sig. simplifying the system since we don't implement redundant token validation logic in every service. If every service validated tokens independently, rotating the secret key given the possible addition of new services would be cumbersome and inefficient for maintainability.

---

## 2. Your choice

When activity-service calls user-service internally, it uses a Machine-to-Machine (M2M) token — not a user's token.

**Why can't it just reuse the user's token that arrived in the original request?**

What would break, or what door would you accidentally leave open, if services passed user tokens between themselves?

> Reusing a user's token for internal network calls violates the principle of least privilege by giving the downstream service the dangerous ability to impersonate the user anywhere in the system. Using M2M tokens prevents lateral privilege escalation if a service is compromised.

---

## 3. The tradeoff

The gateway and the auth-service share the same `SECRET_KEY` to verify tokens without making a network call on every request.

**What is the security risk of sharing this key?** What happens if it leaks?

And what would the alternative look like — verifying tokens by calling auth-service on every request instead? What does that cost you?

> Sharing the `SECRET_KEY` introduces a critical vulnerability where a leaked key allows an attacker to cryptographically forge valid JWTs and bypass the gateway's identity checks entirely. Calling the `auth-service` to verify every request eliminates the shared secret risk but introduces severe latency.

---

*Keep this file. You will refer back to it during the oral presentation.*
