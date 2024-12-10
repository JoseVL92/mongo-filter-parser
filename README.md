# MongoDB Query Filter Builder

A Python utility for converting URL query parameters into MongoDB filter queries with support for complex logical operations and various comparison operators.

## Features

- Convert URL query strings or dictionaries into MongoDB filter queries
- Support for multiple comparison operators
- Logical operations (AND/OR) with proper precedence
- Case-insensitive regex matching
- Field exclusion support using Pydantic models
- URL-safe logical operators (`+` for AND, `|` for OR)

## Installation (still not deployed)

```bash
pip install mongo_filter_parser
```

## Quick Start

```python
from mongo_filter_parser import build_mongo_filter

# Using a URL query string
query = "price__lte=7.8&created_at__lt=2024-05-08&is_verified=false&__binding__=(price__lte|created_at__lt)"
filter_dict = build_mongo_filter(query)

# Using a dictionary
params = {
    "price__lte": "7.8",
    "created_at__lt": "2024-05-08",
    "is_verified": "false",
    "__binding__": "(price__lte|created_at__lt)"
}
filter_dict = build_mongo_filter(params)
```

## Supported Operators

### Comparison Operators

| Query Syntax | MongoDB Operator | Description |
|-------------|------------------|-------------|
| `__eq` | `$eq` | Equal to |
| `__ne` | `$ne` | Not equal to |
| `__gte` | `$gte` | Greater than or equal |
| `__lte` | `$lte` | Less than or equal |
| `__gt` | `$gt` | Greater than |
| `__lt` | `$lt` | Less than |
| `__in` | `$in` | In array |
| `__nin` | `$nin` | Not in array |
| `__regex` | `$regex` | Regular expression (case-insensitive) |
| `__all` | `$all` | All elements match |
| `__exists` | `$exists` | Field exists |

### Logical Operators

- `+` for AND operations (URL-safe alternative to &)
- `|` for OR operations
- Use parentheses `()` for grouping

## Usage Examples

### Basic Filtering

```python
from mongo_filter_parser import build_mongo_filter

# Simple equality
query = "status=active"
# Result: {"status": "active"}

# Comparison operators
query = "price__lte=100&quantity__gte=10"
# Result: {"price": {"$lte": 100}, "quantity": {"$gte": 10}}

# Case-insensitive regex search
query = "email__regex=user@example"
# Result: {"email": {"$regex": "user@example", "$options": "i"}}
```

### Logical Operations

```python
# OR operation
query = "status=inactive&last_activity__lt=2020-01-01&__binding__=status|last_activity__lt"
# Result: {"$or": [{"status": "active"}, {"last_activity": {"$lt": "2020-01-01"}}]}

# AND operation
query = "price__lte=100&quantity__gte=10&__binding__=price__lte+quantity__gte"
# Result: {"$and": [{"price": {"$lte": 100}}, {"quantity": {"$gte": 10}}]}

# Complex grouping
query = "created_at__lt=2024-05-08&is_verified=false&has_evolved=true&__binding__=((created_at__lt|is_verified)+has_evolved)"
# Result: {"$and": [{"$or": [{"created_at": {"$lt": "2024-05-08"}}, {"is_verified": false}]}, {"has_evolved": true}]}
```

### Field Exclusion

```python
from pydantic import BaseModel
from mongo_filter import build_mongo_filter

class PaginationParams(BaseModel):
    page: int
    page_size: int

# Exclude pagination parameters from the filter
query = "page=1&page_size=10&status=active"
filter_dict = build_mongo_filter(query, exclude_model=PaginationParams)
# Result: {"status": "active"}
```

## Value Parsing

The module automatically parses values into appropriate Python types:

- Integers: `"123"` → `123`
- Floats: `"123.45"` → `123.45`
- Booleans: `"true"` → `True`, `"false"` → `False`
- Null values: `"null"` or `"none"` → `None`
- ISO dates: `"2024-01-15T14:30:00Z"` → `datetime` object
- Lists: `"[1, 2, 3]"` → `[1, 2, 3]`