# Module 1 — Service Decomposition

**Duration**: 2h in class
**Branch to submit**: `module-01/s-amiour`

---

## Objective

Before writing a single line of code, you need to design the system on paper. Every decision you make here: where to draw service boundaries, who owns what data, how services talk to each other, is hard to reverse once you start coding.

This module is about slowing down and thinking like an architect, not a developer.

Read these two documents before doing anything else:

- `docs/domain.md` — what GameHub is and who uses it
- `docs/specs.md` — the tech stack and key architectural decisions

> The CTO has already laid out the `services/` folder structure. Use it as a starting point, but your job is to **justify** why each folder deserves to be its own service — not just accept it.

---

## Task 1 — Identify bounded contexts _(~40 min)_

A bounded context is a part of the system that has a clear responsibility and owns its data exclusively. No other service should reach into its database.

For each bounded context you identify, fill in the table:

| Bounded Context | Responsibilities                                                            | Owned Entities              | Team        |
| --------------- | --------------------------------------------------------------------------- | --------------              | ----------- |
| Identity        | Manages who users are, handles registration and profiles                    | User, Session               | Platform    |
| Game Library    | Acts as the source of truth for game metadata, search, and recommendations. | Game, Genre                 | Content     |
| Engagement      | Tracks active gameplay sessions, game statuses, and user libraries.         | PlaySession, LibraryItem    | Engagement  |
| Communications  | Delivers asynchronous in-app, email, or push alerts to users.               | NotificationEvent, Template | Platform    |
| Compliance      | Stores immutable, GDPR-compliant audit trails of user actions.              | AuditLog, ConsentRecord     | Data / Legal|

There is no single correct answer: what matters is that you can justify each row.

---

## Task 2 — Define service contracts _(~30 min)_

For each pair of services that need to communicate, define:

- **Direction**: A → B
- **Trigger**: what causes the call
- **Protocol**: REST or event (async)
- **Payload**: key fields exchanged

Example:

```
activity-service → logging-service
Trigger: an activity is logged
Protocol: RabbitMQ message (async — why not REST here?)
Payload: { activity_id, user_id, action, game_id, timestamp }
```

---

> User completes game session (activity-service -> logging-service)

```resp
activity-service -> logging-service
Trigger: user finishes playing a game, generating an activity record
Protocol: RabbitMQ message
Payload: { id, user_id, game_id, action, created_at }
```

> Friend receives a game alert (activity-service -> notification-service)

```resp
activity-service -> notification-service
Trigger: user starts playing a game, and their friends need to be notified.
Protocol: RabbitMQ message
Payload: { actor_id, friend_id, game_id, action, created_at }
```

> Gateway fetching user profile (gateway -> user-service)

```resp
gateway -> user-service
Trigger: client requests profile page of specific user.
Protocol: REST
Payload (Request): GET /v1/users/{user_id}
Payload (Response): { user_id, username, avatar_url, join_date }
```

---

Focus on the flows that feel non-obvious. You do not need to document every possible pair.

---

## Task 3 — Draw the service map _(~20 min)_

Draw the full GameHub service map:

- One box per service
- Arrows between services (solid line = synchronous REST, dashed line = async event)
- Label each arrow with its protocol
- One box at the top labelled **gateway** — all client requests enter here, no client ever calls a service directly

```resp
                    [ Client Applications ]
                               │
                               │ (Sync HTTP)
                               ▼
                        [ API Gateway :8000] (Traefik)
                               │
       ┌───────────┬───────────┼───────────┬
       │           │           │           │
       ▼           ▼           ▼           ▼
       :8005        :8001       :8002       :8003
  [ Auth ]      [ User ]    [ Game ]  [ Activity ]
  Service       Service     Service     Service
       │           │           │           │
       └───────────┴─────┬─────┴───────────┘
                         │
                        ---
                    (Async Events)
                        ---
                         │
                         ▼
                   (( RabbitMQ ))
                   Message Broker
                         │
             ┌───────────┴───────────┐
             │                       │
             ▼                       ▼
             :8004                  :8006
      [ Notification ]          [ Logging ]
         Service                  Service
```

This can be a sketch on paper, a whiteboard photo, or ASCII art committed to your branch.

---

## Discussion _(~15 min)_

Three questions to discuss as a team before you leave:

1. Why does `notification-service` use Node.js instead of Python like the rest? What does that tell you about microservices and technology choices?

> Sending thousands of push notifications, emails, or holding open WebSockets for live alerts is heavily I/O-bound. Node.js handles massive concurrent network connections much more efficiently than standard synchronous Python.

1. What is the risk of `activity-service` calling `logging-service` synchronously — why might you prefer an async event instead?

> If the logging-service goes down, experiences latency, or the database locks, a synchronous REST call would cause the activity-service to hang and fail. The user would be unable to log their game simply because a background audit system was slow.

2. Why does `logging-service` need a GDPR consent check before recording any activity?

> Because the logging service centralizes tracking of user habits (when they play, what they play), failing to verify consent from EU-based users before writing to the database exposes the platform to severe legal penalties.

You do not need to write these answers down — they are warm-up for your REFLECTION.md.

---

## Minimum to submit this branch

- [x] Bounded context table filled in (at least 4 services justified)
- [x] At least 3 service contracts defined
- [x] Service map committed (sketch, photo, or ASCII)
- [x] `REFLECTION.md` completed and committed

The map does not need to be perfect. It needs to be yours.
