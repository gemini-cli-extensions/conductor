# Mermaid Diagram Style Guide

This document outlines standards for creating diagrams using Mermaid syntax in documentation and specifications.

## When to Use Mermaid

Use Mermaid diagrams for:

- **Architecture diagrams**: System components and their relationships
- **Flowcharts**: Process flows, decision trees, workflows
- **Sequence diagrams**: Interactions between components over time
- **Class diagrams**: Object-oriented design and inheritance
- **ER diagrams**: Database schema and relationships
- **Gantt charts**: Project timelines and dependencies
- **State diagrams**: State machines and transitions

Use dedicated tools for:

- Complex visual designs requiring pixel-perfect control
- Diagrams needing custom icons or branding
- Presentations requiring specific styling

## Diagram Types

### Flowcharts

Use for process visualization and decision trees.

```mermaid
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Process A]
    B -->|No| D[Process B]
    C --> E[End]
    D --> E
```

**Syntax:**

- Direction: `TB` (top-bottom), `LR` (left-right), `BT`, `RL`
- Node shapes: `[]` rectangle, `{}` diamond, `()` circle, `[[]]` stadium
- Arrows: `-->` solid, `-.->` dashed, `==>` thick

### Sequence Diagrams

Use for showing interactions between actors/components.

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Database

    Client->>API: Request data
    API->>Database: Query
    Database-->>API: Return results
    API-->>Client: Response
```

**Syntax:**

- Participants: `participant Name`
- Messages: `->>` solid, `-->>` dashed/open
- Activations: `activate`/`deactivate`
- Notes: `Note over/left/right of`

### Class Diagrams

Use for object-oriented design documentation.

```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +makeSound()
    }

    class Dog {
        +fetch()
    }

    class Cat {
        +climb()
    }

    Animal <|-- Dog
    Animal <|-- Cat
```

**Syntax:**

- Visibility: `+` public, `-` private, `#` protected
- Relationships: `<|--` inheritance, `*--` composition, `o--` aggregation
- Methods: `methodName()` with types

### ER Diagrams

Use for database schema documentation.

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    CUSTOMER {
        string id PK
        string name
        string email
    }
    ORDER {
        string id PK
        string customer_id FK
        date order_date
    }
```

**Syntax:**

- Relationships: `||--o{` (one-to-many), `||--||` (one-to-one)
- Keys: `PK` primary key, `FK` foreign key
- Types: string, int, date, etc.

### Gantt Charts

Use for project timelines and milestones.

```mermaid
gantt
    title Project Timeline
    dateFormat  YYYY-MM-DD
    section Phase 1
    Planning           :done, plan, 2026-01-01, 7d
    Design            :active, design, after plan, 14d
    section Phase 2
    Development       :dev, after design, 30d
    Testing          :test, after dev, 14d
```

**Syntax:**

- Status: `:done`, `:active`, `:crit` (critical)
- Dependencies: `after task_name`
- Sections: `section Name`

## Syntax Standards

### Indentation

- Use 4 spaces for nesting
- Align related elements
- Group related nodes

```mermaid
flowchart TD
    A[Parent]
    A --> B[Child 1]
    A --> C[Child 2]
        B --> D[Grandchild]
        C --> E[Grandchild]
```

### Node Naming

- Use descriptive names: `authService` not `A1`
- CamelCase for multi-word: `userDatabase`
- Add labels for clarity: `authService[Authentication Service]`
- Avoid spaces in IDs: use hyphens or camelCase

### Comments

Use `%%` for single-line comments:

```mermaid
%% This is a comment
flowchart TD
    A[Start] --> B[End] %% inline comment
```

## Styling Guidelines

### Subgraphs

Group related elements using subgraphs:

```mermaid
flowchart TB
    subgraph Frontend
        A[React App]
        B[Redux Store]
    end

    subgraph Backend
        C[API Gateway]
        D[Microservices]
    end

    A --> C
    B --> D
```

### Styling Nodes

Use classes for consistent styling:

```mermaid
flowchart TD
    A[Start]:::start
    B[Process]
    C[End]:::end

    classDef start fill:#90EE90,stroke:#333
    classDef end fill:#FFB6C1,stroke:#333
```

### Colors

- Use semantic colors: green (start/success), red (error), yellow (warning)
- Ensure contrast ratios meet WCAG 2.1 standards
- Avoid color as the only means of conveying information

## Documentation Integration

### Embedding in Markdown

```markdown
## Architecture

The system follows a microservices pattern:

```mermaid
flowchart TB
    Client --> API
    API --> Service1
    API --> Service2
```

```

### Using Diagram References

```markdown
See the [deployment diagram](#deployment-diagram) for infrastructure details.

<a name="deployment-diagram"></a>
```mermaid
flowchart LR
    A[Load Balancer] --> B[Server 1]
    A --> C[Server 2]
```

```

## Accessibility

### Alt Text
Always provide descriptive alt text:

```markdown
![System architecture diagram showing client, API gateway, and three microservices](data:image/svg+xml;base64,...)
```

### Color Independence

- Use patterns or labels in addition to colors
- Provide text descriptions for complex diagrams
- Test with grayscale filters

```mermaid
flowchart TD
    A[Start] --> B{Decision?}
    B -->|Yes| C[Success]
    B -->|No| D[Failure]

    style C fill:#90EE90
    style D fill:#FFB6C1
```

## Version Control Best Practices

1. **Line breaks**: Put each node/connection on separate lines
2. **Comments**: Add comments explaining complex logic
3. **Versions**: Note Mermaid version compatibility
4. **Review**: Review diagram changes in PRs
5. **Testing**: Verify diagrams render correctly

```mermaid
%% Version: 10.x
%% Description: User authentication flow
flowchart TD
    %% Start node
    Start([User Login])

    %% Decision point
    Start --> Check{Valid?}

    %% Outcomes
    Check -->|Yes| Success[Dashboard]
    Check -->|No| Error[Show Error]

    %% End
    Error --> Start
```

## Common Patterns

### Decision Tree

```mermaid
flowchart TD
    Start --> A{Condition A}
    A -->|True| B{Condition B}
    A -->|False| C{Condition C}
    B -->|True| D[Action 1]
    B -->|False| E[Action 2]
    C -->|True| F[Action 3]
    C -->|False| G[Action 4]
```

### Request Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API Gateway
    participant S as Service
    participant D as Database

    C->>A: HTTP Request
    A->>A: Validate Token
    A->>S: Forward Request
    S->>D: Query
    D-->>S: Data
    S-->>A: Response
    A-->>C: HTTP Response
```

### Module Dependencies

```mermaid
flowchart LR
    subgraph Core
        Config
        Utils
    end

    subgraph Features
        Auth --> Core
        Dashboard --> Core
        Profile --> Core
    end

    subgraph UI
        Components --> Features
    end
```

## Best Practices

1. Keep diagrams focused on one concept
2. Use consistent naming conventions
3. Limit diagram complexity (break into multiple if needed)
4. Add legends for complex color schemes
5. Test rendering in target platform (GitHub, docs, etc.)
6. Use subgraphs to organize related elements
7. Include direction indicators for clarity
8. Document diagram purpose in comments
9. Review for accuracy when code changes
10. Prefer clarity over completeness

**BE CONSISTENT.** When creating diagrams, follow established patterns in the project.

*References:*

- [Mermaid Documentation](https://mermaid.js.org/)
- [Mermaid Live Editor](https://mermaid.live/)
- [GitHub Mermaid Support](https://github.blog/developer-skills/github/include-diagrams-markdown-files-mermaid/)
