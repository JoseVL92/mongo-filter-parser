from typing import Dict

# Comparison operators mapping
COMPARISON_OPERATORS: Dict[str, str] = {
    'eq': '$eq',
    'ne': '$ne',
    'gte': '$gte',
    'lte': '$lte',
    'gt': '$gt',
    'lt': '$lt',
    'in': '$in',
    'nin': '$nin',
    'regex': '$regex',
    'all': '$all',
    'exists': '$exists'
}

# Logical operators mapping
LOGICAL_OPERATORS: Dict[str, str] = {
    '+': '$and',
    '|': '$or'
}
