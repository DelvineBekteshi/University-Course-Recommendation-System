from flask import Blueprint, jsonify, request
from extensions import db
from models.audit_log import AuditLog
from services.audit_utils import get_audit_history, get_audit_logs_by_user, get_audit_logs_by_action

audit_log_bp = Blueprint('audit_log_bp', __name__)

@audit_log_bp.route('/audit-logs', methods=['GET'])
def get_audit_logs():
    """
    Retrieve all audit logs with optional filtering.
    Query parameters:
        - entity_type: Filter by entity type (User, Course, etc.)
        - action: Filter by action (CREATE, UPDATE, DELETE)
        - limit: Maximum number of records (default: 50)
    """
    entity_type = request.args.get('entity_type')
    action = request.args.get('action')
    limit = request.args.get('limit', 50, type=int)

    query = AuditLog.query

    if entity_type:
        query = query.filter_by(entity_type=entity_type.upper())
    
    if action:
        query = query.filter_by(action=action.upper())

    logs = query.order_by(AuditLog.changed_at.desc()).limit(limit).all()
    
    return jsonify({
        "total": len(logs),
        "logs": [log.to_dict() for log in logs]
    }), 200

@audit_log_bp.route('/audit-logs/entity/<entity_type>/<int:entity_id>', methods=['GET'])
def get_entity_audit_history(entity_type, entity_id):
    """
    Retrieve audit history for a specific entity.
    
    Args:
        entity_type: Type of entity (User, Course, Enrollment, Rating)
        entity_id: ID of the entity
    """
    limit = request.args.get('limit', 50, type=int)
    
    logs = get_audit_history(entity_type, entity_id, limit)
    
    return jsonify({
        "entity_type": entity_type,
        "entity_id": entity_id,
        "total": len(logs),
        "logs": logs
    }), 200

@audit_log_bp.route('/audit-logs/user/<int:user_id>', methods=['GET'])
def get_user_audit_logs(user_id):
    """
    Retrieve all changes made by a specific user.
    
    Args:
        user_id: ID of the user
    """
    limit = request.args.get('limit', 50, type=int)
    
    logs = get_audit_logs_by_user(user_id, limit)
    
    return jsonify({
        "user_id": user_id,
        "total": len(logs),
        "logs": logs
    }), 200

@audit_log_bp.route('/audit-logs/action/<action>', methods=['GET'])
def get_logs_by_action(action):
    """
    Retrieve audit logs filtered by action type.
    
    Args:
        action: Action type (CREATE, UPDATE, DELETE)
    """
    entity_type = request.args.get('entity_type')
    limit = request.args.get('limit', 50, type=int)
    
    logs = get_audit_logs_by_action(action, entity_type, limit)
    
    return jsonify({
        "action": action.upper(),
        "entity_type": entity_type,
        "total": len(logs),
        "logs": logs
    }), 200

@audit_log_bp.route('/audit-logs/<int:log_id>', methods=['GET'])
def get_audit_log(log_id):
    """
    Retrieve a specific audit log entry.
    
    Args:
        log_id: ID of the audit log
    """
    log = AuditLog.query.get_or_404(log_id)
    return jsonify(log.to_dict()), 200

@audit_log_bp.route('/audit-logs/stats', methods=['GET'])
def get_audit_stats():
    """
    Get statistics about audit logs.
    """
    total_logs = AuditLog.query.count()
    
    actions_count = db.session.query(
        AuditLog.action,
        db.func.count(AuditLog.id).label('count')
    ).group_by(AuditLog.action).all()
    
    entities_count = db.session.query(
        AuditLog.entity_type,
        db.func.count(AuditLog.id).label('count')
    ).group_by(AuditLog.entity_type).all()
    
    return jsonify({
        "total_logs": total_logs,
        "by_action": {action: count for action, count in actions_count},
        "by_entity_type": {entity: count for entity, count in entities_count}
    }), 200