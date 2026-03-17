import json
from datetime import datetime
from typing import Any, Dict, Optional
from extensions import db
from models.audit_log import AuditLog


def log_audit(
    entity_type: str,
    entity_id: int,
    action: str,
    old_values: Optional[Dict[str, Any]] = None,
    new_values: Optional[Dict[str, Any]] = None,
    changed_by: Optional[int] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> AuditLog:
    """
    Record an audit log entry for entity changes.
    
    Args:
        entity_type: Type of entity (User, Course, Enrollment, Rating)
        entity_id: ID of the entity
        action: Action performed (CREATE, UPDATE, DELETE)
        old_values: Previous values (for UPDATE/DELETE)
        new_values: New values (for CREATE/UPDATE)
        changed_by: User ID who made the change
        ip_address: IP address of the requester
        user_agent: User agent string
        
    Returns:
        Created AuditLog object
    """
    audit_entry = AuditLog(
        entity_type=entity_type.upper(),
        entity_id=entity_id,
        action=action.upper(),
        old_values=json.dumps(old_values) if old_values else None,
        new_values=json.dumps(new_values) if new_values else None,
        changed_by=changed_by,
        changed_at=datetime.utcnow(),
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    db.session.add(audit_entry)
    db.session.commit()
    
    return audit_entry


def get_audit_history(entity_type: str, entity_id: int, limit: int = 50) -> list:
    """
    Retrieve audit history for a specific entity.
    
    Args:
        entity_type: Type of entity
        entity_id: ID of the entity
        limit: Maximum number of records to return
        
    Returns:
        List of audit log entries
    """
    logs = AuditLog.query.filter_by(
        entity_type=entity_type.upper(),
        entity_id=entity_id
    ).order_by(AuditLog.changed_at.desc()).limit(limit).all()
    
    return [log.to_dict() for log in logs]


def get_audit_logs_by_user(user_id: int, limit: int = 50) -> list:
    """
    Retrieve all changes made by a specific user.
    
    Args:
        user_id: User ID
        limit: Maximum number of records to return
        
    Returns:
        List of audit log entries
    """
    logs = AuditLog.query.filter_by(
        changed_by=user_id
    ).order_by(AuditLog.changed_at.desc()).limit(limit).all()
    
    return [log.to_dict() for log in logs]


def get_audit_logs_by_action(action: str, entity_type: Optional[str] = None, limit: int = 50) -> list:
    """
    Retrieve audit logs filtered by action type.
    
    Args:
        action: Action type (CREATE, UPDATE, DELETE)
        entity_type: Optional filter by entity type
        limit: Maximum number of records to return
        
    Returns:
        List of audit log entries
    """
    query = AuditLog.query.filter_by(action=action.upper())
    
    if entity_type:
        query = query.filter_by(entity_type=entity_type.upper())
    
    logs = query.order_by(AuditLog.changed_at.desc()).limit(limit).all()
    
    return [log.to_dict() for log in logs]
