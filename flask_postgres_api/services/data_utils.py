import re
from typing import Any, Dict

def sanitize_string(value: str, min_length: int = 1, max_length: int = 255) -> str:
    """
    Sanitize string by trimming, normalizing spaces, and removing invalid characters.
    
    Args:
        value: Input string
        min_length: Minimum allowed length
        max_length: Maximum allowed length
        
    Returns:
        Sanitized string
        
    Raises:
        ValueError: If string is invalid after sanitization
    """
    if not isinstance(value, str):
        raise ValueError("Value must be a string")
    
    # Strip leading/trailing whitespace
    value = value.strip()
    
    # Normalize multiple spaces to single space
    value = re.sub(r'\s+', ' ', value)
    
    # Check length constraints
    if len(value) < min_length:
        raise ValueError(f"String too short (minimum {min_length} characters)")
    if len(value) > max_length:
        raise ValueError(f"String exceeds maximum length ({max_length} characters)")
    
    return value


def sanitize_email(email: str) -> str:
    """
    Sanitize and validate email address.
    
    Args:
        email: Email address to sanitize
        
    Returns:
        Sanitized email
        
    Raises:
        ValueError: If email is invalid
    """
    email = email.strip().lower()
    
    # Simple email validation regex
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        raise ValueError("Invalid email format")
    
    return email


def normalize_category(category: str, allowed_categories: list) -> str:
    """
    Normalize category to match allowed values (case-insensitive).
    
    Args:
        category: Category to normalize
        allowed_categories: List of allowed categories
        
    Returns:
        Normalized category
        
    Raises:
        ValueError: If category not in allowed list
    """
    category = category.strip()
    
    # Case-insensitive match
    for allowed in allowed_categories:
        if category.lower() == allowed.lower():
            return allowed
    
    raise ValueError(f"Invalid category: {category}")


def remove_null_fields(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove fields with None/null values from dictionary.
    
    Args:
        data: Dictionary to clean
        
    Returns:
        Dictionary without null fields
    """
    return {k: v for k, v in data.items() if v is not None}


def compare_changes(old_data: Dict[str, Any], new_data: Dict[str, Any]) -> Dict[str, tuple]:
    """
    Compare two dictionaries and return only changed fields.
    
    Args:
        old_data: Previous values
        new_data: New values
        
    Returns:
        Dictionary with format {field: (old_value, new_value)}
    """
    changes = {}
    
    all_keys = set(old_data.keys()) | set(new_data.keys())
    
    for key in all_keys:
        old_val = old_data.get(key)
        new_val = new_data.get(key)
        
        if old_val != new_val:
            changes[key] = (old_val, new_val)
    
    return changes
