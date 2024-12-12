"""Field builder module for constructing MongoDB field filters."""
from typing import Dict, Any

from .exceptions import OperatorError
from .operators import COMPARISON_OPERATORS
from .value_parser import parse_value

class FieldBuilder:
    """Builds MongoDB filters for individual fields."""

    def __init__(self, query_params: Dict[str, Any]):
        self.query_params = query_params

    def build_field_filter(self, field: str) -> Dict[str, Any]:
        """Build filter for a single field."""
        value = self.query_params[field]

        if '__' in field:
            base_field, op = field.split('__', 1)
            if op not in COMPARISON_OPERATORS:
                raise OperatorError(f"Unsupported operator: {op}")

            # Special handling for regex operator
            if op == 'regex':
                return {
                    base_field: {
                        '$regex': value,  # No need to parse regex patterns
                        '$options': 'i'  # Case insensitive
                    }
                }

            return {
                base_field: {
                    COMPARISON_OPERATORS[op]: parse_value(value)
                }
            }

        # Direct equality comparison
        return {field: parse_value(value)}

    @staticmethod
    def merge_field_filters(filters: Dict[str, Any], new_filter: Dict[str, Any], operator: str = '$and') -> Dict[str, Any]:
        """Merge multiple filters for the same field."""
        base_field = next(iter(new_filter))

        if base_field not in filters:
            filters[base_field] = new_filter[base_field]
            return filters

        if operator == '$and':
            # For AND operations, merge conditions
            if isinstance(filters[base_field], dict) and isinstance(new_filter[base_field], dict):
                filters[base_field].update(new_filter[base_field])
        else:
            # For OR operations, create an $or array of conditions
            conditions = []

            # Convert existing condition to proper format
            existing_condition = {
                base_field: filters[base_field]
            }
            conditions.append(existing_condition)

            # Add new condition
            conditions.append(new_filter)

            # Replace with $or array
            filters[base_field] = {'$or': conditions}

        return filters
