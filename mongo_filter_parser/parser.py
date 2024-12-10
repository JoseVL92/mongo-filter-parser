from typing import Any, List
from dataclasses import dataclass


@dataclass
class LogicalExpression:
    operator: str
    operands: List[Any]


class BindingParser:
    def __init__(self, binding_str: str):
        self.binding_str = binding_str
        self.pos = 0

    def parse(self) -> LogicalExpression:
        return self._parse_or()

    def _parse_or(self) -> Any:
        """Parse OR expressions with lowest precedence."""
        expr = self._parse_and()

        while self.pos < len(self.binding_str):
            self._skip_whitespace()
            if self.pos >= len(self.binding_str) or self.binding_str[self.pos] != '|':
                break

            self.pos += 1  # Skip '|'
            right = self._parse_and()
            expr = LogicalExpression('|', [expr, right])

        return expr

    def _parse_and(self) -> Any:
        """Parse AND expressions with higher precedence."""
        expr = self._parse_primary()

        while self.pos < len(self.binding_str):
            self._skip_whitespace()
            if self.pos >= len(self.binding_str) or self.binding_str[self.pos] != '+':
                break

            self.pos += 1  # Skip '+'
            right = self._parse_primary()
            expr = LogicalExpression('+', [expr, right])

        return expr

    def _parse_primary(self) -> Any:
        """Parse primary expressions (fields or parenthesized expressions)."""
        self._skip_whitespace()

        if self.binding_str[self.pos] == '(':
            self.pos += 1  # Skip opening parenthesis
            expr = self._parse_or()  # Start with lowest precedence inside parentheses
            self._skip_whitespace()

            if self.pos >= len(self.binding_str) or self.binding_str[self.pos] != ')':
                raise ValueError("Missing closing parenthesis")
            self.pos += 1  # Skip closing parenthesis
            return expr

        return self._parse_field()

    def _parse_field(self) -> str:
        """Parse a field name."""
        start = self.pos
        while self.pos < len(self.binding_str) and self.binding_str[self.pos] not in ('+', '|', ')', ' '):
            self.pos += 1
        if start == self.pos:
            raise ValueError("Expected field name")
        return self.binding_str[start:self.pos]

    def _skip_whitespace(self):
        """Skip whitespace characters."""
        while self.pos < len(self.binding_str) and self.binding_str[self.pos].isspace():
            self.pos += 1
