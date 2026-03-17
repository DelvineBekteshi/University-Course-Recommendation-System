from extensions import db
from datetime import datetime
from sqlalchemy import Text, Index

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    entity_type = db.Column(db.String(50), nullable=False)  # 'User', 'Course', 'Enrollment', 'Rating'
    entity_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(50), nullable=False)  # 'CREATE', 'UPDATE', 'DELETE'
    old_values = db.Column(Text)  # JSON string of previous values
    new_values = db.Column(Text)  # JSON string of new values
    changed_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))  # User who made the change
    changed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ip_address = db.Column(db.String(45))  # IPv4 or IPv6
    user_agent = db.Column(db.String(255))

    __table_args__ = (
        Index('idx_entity_type_id', 'entity_type', 'entity_id'),
        Index('idx_changed_at', 'changed_at'),
        Index('idx_action', 'action'),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "action": self.action,
            "old_values": self.old_values,
            "new_values": self.new_values,
            "changed_by": self.changed_by,
            "changed_at": self.changed_at.isoformat() if self.changed_at else None,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
        }