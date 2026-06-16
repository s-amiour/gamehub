# Module 4 — Reflection

**Team name**: s-amiour
**Branch**: `module-04/s-amiour`
**Submitted**: before Module 5 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

In Module 3, services called each other directly over HTTP. Now activity-service drops a message into a broker and moves on — it never waits for a reply.

**What does the activity-service gain by not waiting? And what does the notification-service gain by consuming at its own pace?**

Think about what happens under load, or when notification-service is temporarily down.

> Speed and resilience. It can quickly respond to the user and won't fail or slow down just because a secondary feature is struggling. The notification-service gains the advantage of not getting overwhelmed by concurrent requests as a result of pulling messages from the queue at a steady pace, preventing crashes.

---

## 2. Your choice

In Module 3 you already knew how to call another service directly over HTTP — you did it for user validation and game enrichment.

**Why not use the same approach for notifications? What does introducing a broker give you that a direct HTTP call doesn't?**

Think about what happens if notification-service is slow, or crashes mid-message.

> Again, it all comes down to the criticality of the features: user validation is a strict dependency for the activity to be created, whereas notifying the user isn't. So, in order to guarantee an efficient performance of activity creation, especiially in high traffic conditions, we must asynchronously publish notifications. In addition, the broker provides us a safety net: if the notification-service crashes mid-message, RabbitMQ simply holds onto the pending messages until the service is back online.

---

## 3. The tradeoff

With synchronous REST, you get an immediate answer: success or failure. With async messaging, the activity is saved and the message is sent — but you have no idea if the notification was ever delivered.

**How would a user know if their notification was never sent? How would you know as a developer?**

What visibility do you lose when you go async?

> A user wouldn't immediately know a notification failed; they would only notice the absence of an alert on their friend's screen. Unlike Sync messaging, we don't get the 500 error. Because activity-service only knows if RabbitMQ accepted the message, we have to rely on secondary monitoring tools like RabbitMQ's Dead Letter Queues or server logs.

---

*Keep this file. You will refer back to it during the oral presentation.*
