class MongoFilterError(Exception):
    """Base exception for all mongo_filter errors."""
    pass


class ParserError(MongoFilterError):
    """Raised when there's an error parsing the binding expression."""
    pass


class OperatorError(MongoFilterError):
    """Raised when an invalid or unsupported operator is used."""
    pass


class ValueParsingError(MongoFilterError):
    """Raised when there's an error parsing a value."""
    pass
