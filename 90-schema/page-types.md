# Page Types

Definitions and templates for each wiki page type.

## concept

Explains a product concept, feature, or object.

**Template:**
```markdown
---
type: concept
product: zoom-phone
title: {Human-readable title}
sources:
  - article_id: {ID}
    title: {Source article title}
    source_url: {URL}
confidence: high
last_reviewed: {YYYY-MM-DD}
---

# {Title}

## Summary

2–3 sentences explaining what this is and why designers should care.

## Key points

- Point 1
- Point 2

## Related

- [[related-concept]]
- [[related-task-flow]]
```

## user-role

Describes a role, its permissions, scope, and what it means for UI.

**Template:**
```markdown
---
type: user-role
product: zoom-phone
title: {Role name}
sources:
  - article_id: {ID}
    title: {Source article title}
    source_url: {URL}
confidence: high
last_reviewed: {YYYY-MM-DD}
---

# {Role Name}

## Summary

Who this role is for and their scope of control.

## Key points

- Permission boundary 1
- Permission boundary 2

## Related

- [[related-concept]]
```

## task-flow

Describes a user task: goal, steps, dependencies, failure modes.

**Template:**
```markdown
---
type: task-flow
product: zoom-phone
title: {Task name}
sources:
  - article_id: {ID}
    title: {Source article title}
    source_url: {URL}
confidence: high
last_reviewed: {YYYY-MM-DD}
---

# {Task Name}

## Summary

What the user accomplishes and what they need before starting.

## Key points

- Step or dependency 1
- Step or dependency 2

## Related

- [[prerequisite-concept]]
- [[related-constraint]]
```

## constraint

Records a design constraint, limitation, or rule.

**Template:**
```markdown
---
type: constraint
product: zoom-phone
title: {Constraint name}
sources:
  - article_id: {ID}
    title: {Source article title}
    source_url: {URL}
confidence: high
last_reviewed: {YYYY-MM-DD}
---

# {Constraint Name}

## Summary

What is constrained, why, and what designers must account for.

## Key points

- Constraint detail 1
- Constraint detail 2

## Related

- [[affected-concept]]
```

## ux-pattern

Captures a reusable interaction pattern.

**Template:**
```markdown
---
type: ux-pattern
product: zoom-phone
title: {Pattern name}
sources:
  - article_id: {ID}
    title: {Source article title}
    source_url: {URL}
confidence: high
last_reviewed: {YYYY-MM-DD}
---

# {Pattern Name}

## Summary

When this pattern applies and what problem it solves.

## Key points

- Pattern characteristic 1
- Pattern characteristic 2

## Related

- [[concept-using-this-pattern]]
```
