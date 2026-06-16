---
title: "🪜 Layered Architecture, Part 2: Closed Layers, the Sinkhole, and Ports"
date: 2026-06-07 09:00:00 -0500
categories:
  - architecture
  - layered architecture
  - software engineering
author: steven
description:
  Part 2 of the Layered Architecture series. We go past the napkin sketch into the mechanics every serious treatment includes but Part 1 skipped: open vs. closed layers and the "layers of isolation" they buy, the Architecture Sinkhole anti-pattern (and the 80/20 rule for spotting it), and the one honest flaw in classic layering — its dependency direction. Then we fix that flaw the cheap way, with ports & adapters wired through dependency injection, using Python and FastAPI.
---

<h1><span><i class="fas fa-layer-group"></i></span> Layered Architecture — Part 2</h1>

*Closed layers, the sinkhole, and the quiet trick that makes the whole thing testable.*

> "An architecture is the set of decisions you wish you could change later — so make the boring ones cheap to reverse."

---

## 🧭 Previously, on "Simplicity That Still Works"

In [Part 1]({% post_url 2025-08-14-layered-architecture %}) we made the case that **Layered Architecture** is the grandparent pattern — the one you've already used whether you meant to or not. We walked the stack, praised its clarity, and listed its trade-offs (leaky boundaries, boilerplate, over-abstraction).

Part 1 was the napkin sketch. Part 2 is the part where we turn the napkin over and write down the three things every serious treatment of the pattern includes — and that the napkin always leaves out:

1. **Open vs. closed layers** — the rule that actually makes layering *worth something*.
2. **The Architecture Sinkhole** — the anti-pattern that quietly turns your layers into expensive postage.
3. **The honest flaw** — classic layering points its dependencies the *wrong way*, and ports fix it.

We also rebuilt the diagram. Here it is.

---

## 🖼️ The Rebuilt Diagram

![Annotated Layered Architecture](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/layered-architecture-pt2.png)

A few deliberate changes from Part 1's picture:

- **Four layers, not five.** The canonical layered pattern is four sequential layers (Mark Richards' *Software Architecture Patterns* names them Presentation, Business, Persistence, Database). What Part 1 drew as a fifth "Shared" band was never really a *layer* — so…
- **Shared and Cross-Cutting are now perpendicular rails.** They run *across* the stack on the left, because every layer uses them and they depend on no layer. A layer is a *step in the request's journey*; a rail is a *shelf every step reaches for*. Different things; different geometry.
- **The right side finally earns its space.** Part 1's right panel was a legend that re-printed each layer's name. The new one is a per-layer **field card**: the classes you'd actually find there, what the layer is *for*, and — just as important — what it must **never** contain.
- **The arrows mean something.** Downward arrows are the one-way dependency rule. The single orange arrow pointing *up* into the `UserRepository` port is the whole back half of this article: a dependency that's been deliberately **inverted**.

---

## 🔒 Open vs. Closed Layers

Here's the rule Part 1 hand-waved past, and it's the one that makes layering more than decorative.

A layer is **closed** when a request *must* pass through it to reach the layer below. Presentation can't reach into the Domain without going through the Service layer; the Service can't skip to the database without going through Infrastructure. Closed layers create what Richards calls **layers of isolation**: a change inside one layer can't ripple outward, because nothing is allowed to reach past its neighbor to touch it.

That isolation is the entire payoff. It's *why* you can swap PostgreSQL for MongoDB and only the Infrastructure layer notices. Break the closure — let a controller call the repository "just this once" — and you've spent the isolation you were paying for. The layers are still drawn on the diagram; they just don't *do* anything anymore.

A layer is **open** when callers are allowed to *bypass* it. That sounds like cheating, but it's a legitimate, deliberate tool — our **Shared / Common** rail is open on purpose. A value type like `Money` or a shared `Contract` is meant to be reached directly by anyone. Forcing every access to `Money` to tunnel through an intermediate layer would be ceremony with no benefit.

The discipline is this:

> **Closed by default. Open only where you can say out loud why bypassing is safe.**

An open layer you *chose* is architecture. An open layer that *happened* is a leak.

---

## 🚰 The Architecture Sinkhole

Now the failure mode that closed layers invite if you're not watching.

A **sinkhole** is a request that falls straight through every layer doing *nothing* on the way down:

```
POST /users/{id}/email
  → UserController.get_email(id)      # just calls the service
    → UserService.get_email(id)       # just calls the repository
      → UserRepository.get_email(id)  # just runs the query
```

Three layers, three method calls, zero decisions. Each layer is a pass-through — a tube. You've paid for four objects, three hops, and a fistful of DTO mapping to do what a single function could. Do this everywhere and your "layered architecture" is really an elaborate, well-indented way to forward a database call to the browser.

Richards gives a usable heuristic — the **80/20 rule**:

- If roughly **20%** of your requests are simple pass-throughs and **80%** do real work in each layer, that's healthy. Pure CRUD endpoints *should* be cheap.
- If the ratio inverts — **80%** of requests are tubes — the layering is overhead, not structure. That's the sinkhole, and the fix isn't "add another layer." It's to **open** the layers that aren't earning their place, and let the cheap reads go straight to the data.

The point of measuring is to stop treating "we have layers" as a virtue in itself. Layers are a cost you pay for isolation. If a request doesn't need the isolation, don't make it pay.

---

## 🧭 The Honest Flaw: Which Way Do Dependencies Point?

Here's the thing the napkin never admits.

Trace the arrows on a *classic* closed stack. Presentation depends on Service. Service depends on the Domain. And the Domain… depends on **Infrastructure**, because that's where persistence lives and the business logic needs to load and save things. The dependency chain runs **top → bottom**, which means your most valuable, most stable, most framework-free code — the Domain — ends up depending on your most volatile, most replaceable code: the database client, the queue SDK, the HTTP libraries.

That's backwards, and you feel it the first time you try to unit-test a domain rule and discover you need a live Postgres connection to do it. The thing that should be the *easiest* to test in isolation is welded to the thing that's *hardest* to stand up.

This single observation is the seed of every "better" pattern that followed Layered — Hexagonal, Onion, Clean, and the **Layered Ports Architecture** we'll get to. They all do the same core move:

> Don't make the Domain depend on Infrastructure. Make Infrastructure depend on the **Domain's terms**.

That move has a name: the **Dependency Inversion Principle**. And you don't need a new architecture to start using it — you need a *port*.

---

## 🔌 Ports & Adapters: Inverting the Dependency

A **port** is an interface that the inner layer *owns* and *defines in its own vocabulary*. An **adapter** is an outer-layer class that implements that interface. The inner layer depends on the port; the adapter depends on the port; nobody depends on the concrete database class. The arrow that used to point *down* into Infrastructure now points *up* into the port.

![Ports and Adapters — inverting the dependency](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/layered-architecture-pt2-ports.png)

In Python, the cleanest way to express a port is a [`typing.Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol) — **structural** typing, so an adapter satisfies the port just by having the right shape. No base class, no inheritance, no import from Infrastructure back into the core.

### The port (defined in the core)

```python
from typing import Protocol

class UserRepository(Protocol):
  """Port: the core's own vocabulary for loading users."""
  def get(self, user_id: str) -> User | None: ...
```

### The use case (knows only the port)

```python
class PlaceOrderUseCase:
  """Service-layer use case; depends on the abstraction, not the database."""

  def __init__(self, users: UserRepository) -> None:
    self._users = users

  def run(self, user_id: str, order: Order) -> Receipt:
    user: User | None = self._users.get(user_id)
    receipt: Receipt = Receipt.declined(user_id)
    if user is not None and order.is_valid_for(user):
      receipt = order.place_for(user)
    return receipt
```

Notice what `PlaceOrderUseCase` *doesn't* import: no `psycopg`, no SQL, no framework. It is pure, and it is trivially unit-testable.

### The adapter (lives in Infrastructure)

```python
class PostgresUserRepo:
  """Adapter: structurally satisfies UserRepository — no inheritance needed."""

  def __init__(self, pool: Pool) -> None:
    self._pool = pool

  def get(self, user_id: str) -> User | None:
    row: Row | None = self._pool.fetch_one(
      "SELECT id, name FROM users WHERE id = %s", user_id
    )
    return User.from_row(row) if row is not None else None
```

### Wiring it up at the composition root (FastAPI)

The one place that's *allowed* to know both the port and the concrete adapter is the **composition root** — the edge of the app where everything gets assembled. With FastAPI, `Depends` *is* your dependency-injection container; no extra framework required.

```python
from fastapi import Depends, FastAPI

app: FastAPI = FastAPI()

def get_user_repo() -> UserRepository:
  """Composition root: choose the concrete adapter here, and only here."""
  return PostgresUserRepo(pool)

def get_place_order(
  users: UserRepository = Depends(get_user_repo),
) -> PlaceOrderUseCase:
  return PlaceOrderUseCase(users)

@app.post("/orders")
def place_order(
  cmd: PlaceOrderCommand,
  use_case: PlaceOrderUseCase = Depends(get_place_order),
) -> ReceiptDTO:
  receipt: Receipt = use_case.run(cmd.user_id, cmd.to_order())
  return ReceiptDTO.from_domain(receipt)
```

The concrete `PostgresUserRepo` appears exactly **once**, in `get_user_repo`. Everywhere else — the controller, the use case, the domain — speaks only `UserRepository`. The implementation is *hidden* behind the port.

### The payoff: swap the adapter, change nothing

Because the core depends on the port and never on the database, a test supplies a different adapter and the core can't tell the difference:

```python
class FakeUserRepo:
  """Also satisfies UserRepository — in-memory, zero infrastructure."""

  def __init__(self, users: dict[str, User]) -> None:
    self._users = users

  def get(self, user_id: str) -> User | None:
    return self._users.get(user_id)

def test_places_order_for_known_user() -> None:
  repo: FakeUserRepo = FakeUserRepo({"u-1dea": User(id="u-1dea", name="Ada")})
  use_case: PlaceOrderUseCase = PlaceOrderUseCase(repo)
  receipt: Receipt = use_case.run("u-1dea", a_small_order())
  assert receipt.is_placed
```

No database, no fixtures, no `docker compose up` just to assert a business rule. And in an integration test you can flip the *whole app* over to a fake with one line at the composition root:

```python
app.dependency_overrides[get_user_repo] = lambda: FakeUserRepo({...})
```

That's the entire trick. Same layers, same diagram, one inverted arrow — and the Domain is finally free.

---

## 🧭 Where This Leads: Toward LPA

If a single port between the Service and Infrastructure layers buys you this much, the obvious question is: *why stop at one boundary?*

That's exactly the question the **Layered Ports Architecture (LPA)** answers. LPA keeps the familiar four-layer stack — nobody has to relearn the mental model — but puts a **formal port at every boundary**, so each adjacent pair talks only through a contract implemented by an adapter in the layer beneath. You get the teachability of Layered with the decoupling of Hexagonal, and teams can build adjacent layers in parallel without stepping on each other.

We'll give LPA the full treatment — including the **Port Generalization Rule** — in its own article. Part 2's job was just to show you the move that makes it work, on the smallest possible example.

---

## 🗝️ Key Takeaways

- **Closed layers buy isolation; open layers spend it deliberately.** Default to closed; open only where you can name the reason.
- **Watch the 80/20 ratio.** If most requests are pass-throughs, you have a sinkhole — open the layers that aren't earning their keep instead of adding more.
- **Classic layering points its dependencies the wrong way** — the Domain ends up shackled to Infrastructure. That's the real reason it gets hard to test.
- **A port inverts that arrow.** Define the interface in the core (a `typing.Protocol`), implement it in Infrastructure, and wire the concrete adapter once at the composition root via dependency injection.
- **You don't need a new architecture to get most of the benefit** — you need one well-placed port. LPA is just that idea, applied everywhere.

Layered Architecture isn't wrong. It's just *unfinished* — and a port is the smallest possible finishing move.

> "Simplicity is the soul of efficiency." — *Austin Freeman*

---

### 🔗 References & Further Reading

- [Mark Richards — *Software Architecture Patterns* (O'Reilly)](https://www.oreilly.com/library/view/software-architecture-patterns/9781491971439/) — open/closed layers, layers of isolation, the sinkhole anti-pattern, and the 80/20 rule.
- [The Architecture Sinkhole Anti-Pattern](https://candost.blog/notes/45a/) — a concise walk-through with the 80/20 heuristic.
- [Alistair Cockburn — Hexagonal Architecture (Ports & Adapters)](https://alistair.cockburn.us/hexagonal-architecture/) — the original framing of ports and adapters.
- [Robert C. Martin — The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) — the Dependency Inversion Principle as an architectural rule.
- [Clean Architecture vs. Layered: Dependency Inversion for Testable Apps](https://medium.com/@yegor-sychev/how-clean-architecture-differs-from-layered-e11862d073da) — the dependency-direction critique, worked through.
- [Python docs — `typing.Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol) — structural typing for ports.
- Part 1: [Simplicity That Still Works: Layered Architecture]({% post_url 2025-08-14-layered-architecture %}).

---

*Written for the Architectures Project, 2026.*
