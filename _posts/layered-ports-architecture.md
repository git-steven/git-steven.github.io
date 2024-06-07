# The Architecture That Actually Works for Microservices

**Your microservice architecture is probably overengineered.** After building hundreds of microservices, I discovered that Clean Architecture creates too many layers, Hexagonal creates confusion, and traditional layered creates a mess. There's a better way.

Enter **Layered Ports Architecture**: the Goldilocks solution that keeps simplicity, ensures low coupling, and makes testing actually enjoyable.

-----

## The Problem: Architecture Extremes

Building microservices forces you to pick an architecture. The popular choices all have fatal flaws:

**Clean Architecture** promises purity but delivers complexity. Your simple database query bounces through 6 layers. You end up with duplicate entities everywhere. A basic CRUD service generates 50+ files. New developers need days just to understand the flow.

**Hexagonal Architecture** sounds cleaner with its "ports and adapters" pattern. But suddenly everything needs an interface—even your string utilities. The package structure confuses everyone ("Why is the repository interface in `domain/port/out` but implementation in `adapter/out/persistence`?"). You spend more time explaining the hexagon than writing code.

**Traditional Layered Architecture** keeps it simple: Controller → Service → Repository. But everything is tightly coupled. Testing requires mocking frameworks doing dark magic with reflection. Want to swap your database? Rewrite half your service layer. Want to add caching? Good luck.

Each architecture sits at an extreme: either overengineered beyond recognition or underengineered into brittleness.

-----

## The Breakthrough: Strategic Interfaces

After watching teams struggle with these architectures, I had a realization:

> **What if we kept the familiar layered structure but added interfaces only where we actually need flexibility?**

Not everywhere. Not for utilities. Just at architectural boundaries where testability and swappability matter.

-----

## Layered Ports Architecture

Here's the approach that changed everything:

```
┌─────────────────────────────────────────────────────┐
│              PRESENTATION LAYER                     │
│   Controllers (concrete) → DTOs (records)           │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
               ┌──────────┐
               │  PORT    │  ← Interface ONLY at boundary
               │ interface│
               └─────┬────┘
                     │
                     ▼
┌────────────────────┴────────────────────────────────┐
│              SERVICE LAYER                          │
│   ServiceImpl → Domain Models (semi-rich)           │
│              → Mappers (concrete)                   │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
               ┌──────────┐
               │  PORT    │  ← Interface ONLY at boundary
               │ interface│
               └─────┬────┘
                     │
                     ▼
┌────────────────────┴────────────────────────────────┐
│           PERSISTENCE LAYER                         │
│   RepositoryImpl → Dynamic SQL → Database           │
└─────────────────────────────────────────────────────┘
```

### The Rules Are Simple

**Create an interface when:**
- ✅ Crossing architectural layers (Controller → Service, Service → Repository)
- ✅ You need to mock in tests
- ✅ You might swap implementations

**Use concrete classes when:**
- ❌ Building simple utilities
- ❌ Creating mappers
- ❌ Defining domain models

That's it. No philosophical debates. No purity tests. Just pragmatic boundaries.

-----

## Why This Works: Three Key Benefits

### 1. Simplicity That Scales

Developers understand the structure immediately. No training sessions. No architecture diagrams on the wall. It's the familiar Controller → Service → Repository pattern they already know, just with strategic improvements.

A junior developer can navigate the codebase in minutes, not days. When they ask "Where do I add this feature?" the answer is obvious.

### 2. Low Coupling Where It Counts

By placing interfaces at layer boundaries, we get flexibility without the overhead:

```java
@ApplicationScoped
public class ProductServiceImpl implements ProductService {
    // Inject interfaces, not implementations
    private final ProductRepository productRepository;

    public ProductServiceImpl(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }
}
```

Want to swap PostgreSQL for MongoDB? Change the repository implementation. The service layer never knows.

Want to add caching? Create a `CachingProductRepository` decorator. Zero changes to business logic.

But your `ProductMapper` that converts DTOs? It's a concrete class. It will never change. Why pretend otherwise?

### 3. Testability of Units

Testing becomes trivial:

```java
@ExtendWith(MockitoExtension.class)
class ProductServiceTest {
    @Mock ProductRepository repository;
    @InjectMocks ProductServiceImpl service;

    @Test
    void shouldCreateProduct() {
        when(repository.save(any())).thenReturn(product);

        var result = service.createProduct(command);

        verify(repository).save(any());
    }
}
```

No Spring context. No PowerMock. No reflection gymnastics. Just clean, fast unit tests that actually test your business logic.

-----

## Real Code Example

Here's what Layered Ports Architecture looks like in practice:

**Service Interface (The Port):**
```java
public interface ProductService {
    Product createProduct(CreateProductCommand command);
    Product getProduct(ProductId id);
    void updatePrice(ProductId id, Money newPrice);
}
```

**Service Implementation:**
```java
@ApplicationScoped
public class ProductServiceImpl implements ProductService {
    private final ProductRepository repository;

    @Override
    @Transactional
    public Product createProduct(CreateProductCommand command) {
        // Business logic lives in the domain
        Product product = Product.create(
            command.name(),
            command.price(),
            command.createdBy()
        );

        return repository.save(product);
    }
}
```

**Domain Model (Semi-Rich):**
```java
public class Product {
    private Money price;

    public static Product create(String name, Money price, UserId createdBy) {
        validateName(name);
        validatePrice(price);
        return new Product(...);
    }

    public void changePrice(Money newPrice) {
        validatePrice(newPrice);

        // Business rule in the domain, not service
        if (newPrice.lessThan(price.multiply(0.5))) {
            throw new BusinessRuleException(
                "Price cannot decrease by more than 50%"
            );
        }

        this.price = newPrice;
    }
}
```

Notice how business logic lives in the domain model, not scattered across service classes. The domain knows its rules. The service orchestrates.

-----

## Beyond Java: Python/FastAPI Example

The pattern translates beautifully to other languages:

```python
# Service interface using Protocol
class ProductService(Protocol):
    async def create_product(self, command: CreateProductCommand) -> Product: ...

# Service implementation
class ProductServiceImpl:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def create_product(self, command: CreateProductCommand) -> Product:
        # Business logic in domain
        product = Product.create(
            command.name,
            command.price,
            command.created_by
        )
        return await self.product_repo.save(product)

# Domain model with business logic
@dataclass
class Product:
    @staticmethod
    def create(name: str, price: Money, created_by: UserId) -> 'Product':
        Product._validate_name(name)
        Product._validate_price(price)
        return Product(...)

    def change_price(self, new_price: Money):
        if new_price < self.price * 0.5:
            raise BusinessRuleException("Price cannot decrease by more than 50%")
        self.price = new_price
```

Same architecture, same benefits, different syntax.

-----

## Comparing the Architectures

When I compared [Clean Architecture](https://git-steven.github.io/architecture/clean%20architecture/software%20engineering/clean-architecture/) to our Layered Ports approach, the differences were stark.

Clean Architecture creates beautiful concentric circles of abstraction. It's architecturally pure, academically sound, and completely impractical for most microservices. You don't need 5 layers and 8 different model classes for a service that manages products.

Hexagonal Architecture improves on Clean by reducing concepts to just "ports" and "adapters." But it goes too far—suddenly everything is a port. Your team spends more time debating what's a port than shipping features.

Traditional Layered Architecture goes the opposite direction: no abstractions at all. Fast to build, impossible to test, painful to maintain.

**Layered Ports Architecture sits in the sweet spot:**

| Aspect | Traditional | Layered Ports | Hexagonal | Clean |
|--------|------------|---------------|-----------|-------|
| Learning curve | 1 hour | 3 hours | 2 days | 3 days |
| Files for CRUD | ~15 | ~20 | ~40 | ~50+ |
| Testability | Poor | Excellent | Excellent | Excellent |
| Flexibility | Low | High | Very High | Very High |
| Cognitive load | Low | Low | High | Very High |

-----

## When to Use Layered Ports

**Perfect for:**
- Standard microservices with 5-50 endpoints
- Teams who value pragmatism over purity
- Services that need solid testing
- Multi-tenant applications
- Long-term maintenance (2-5+ years)

**Skip it when:**
- Building a simple script or prototype → Use basic layered
- Handling multiple protocols and databases → Consider Hexagonal
- Implementing complex domain logic with full DDD → Consider Clean

-----

## The Bottom Line

After building hundreds of microservices, I've learned that architecture extremes don't work. You need something practical that developers can understand, modify, and test without a PhD in software architecture.

Layered Ports Architecture delivers:
- **Simplicity**: Familiar structure anyone can navigate
- **Low coupling**: Interfaces only where flexibility matters
- **Testability**: Clean unit tests without framework magic

It's not the most theoretically pure. It won't win architecture beauty contests. But it will ship features faster, onboard developers quicker, and maintain easier than anything else I've tried.

Stop overengineering your microservices. Stop underengineering them too.

**Start with layers. Add ports at boundaries. Keep logic in domains.**

Simple. Practical. Battle-tested.

-----

*This architecture emerged from real production needs, not ivory tower theory. It's been validated across hundreds of services. Try it on your next microservice—you might never go back.*