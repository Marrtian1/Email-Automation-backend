from datetime import datetime, timezone
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.models.rule import Rule
from app.models.template import Template
from app.schemas.rule import RuleBase
from app.schemas.token import TokenPayload
from app.services.template_service import template_service
from app.services.email_engine import email_engine


class RuleService:
    @staticmethod
    def create_rule(db: Session, rule_in: RuleBase) -> Rule:
        db_rule = Rule(**rule_in.dict())
        db.add(db_rule)
        db.commit()
        db.refresh(db_rule)
        return db_rule

    @staticmethod
    def get_rules(db: Session, skip: int = 0, limit: int = 100) -> List[Rule]:
        return db.query(Rule).offset(skip).limit(limit).all()

    @staticmethod
    def get_rule(db: Session, rule_id: int) -> Rule:
        return db.query(Rule).filter(Rule.id == rule_id).first()

    @staticmethod
    def delete_rule(db: Session, rule_id: int) -> Rule:
        rule = db.query(Rule).filter(Rule.id == rule_id).first()
        if rule:
            db.delete(rule)
            db.commit()
        return rule

    @staticmethod
    def evaluate_condition(condition: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """
        Evaluate condition dict against context dict.
        Example condition: {"user.is_new": true}
        Example context: {"user": {"is_new": True}, "timestamp": "..."}
        """
        for key, expected_value in condition.items():
            parts = key.split(".")
            value = context
            for part in parts:
                if isinstance(value, dict):
                    value = value.get(part)
                else:
                    return False
            if value != expected_value:
                return False
        return True

    @staticmethod
    def trigger_rule(db: Session, rule: Rule, context: Dict[str, Any]):
        """Trigger a rule: get template, render, and send email."""
        template = template_service.get_template(db, rule.template_id)
        if not template:
            return {"status": "error", "message": "Template not found"}

        placeholders = context.get("placeholders", {})
        rendered_body = template_service.render_template(template.body, placeholders)
        rendered_subject = template.subject

        recipient = context.get("recipient")
        if not recipient:
            return {"status": "error", "message": "No recipient in context"}

        try:
            email_engine.send_email(
                recipient=recipient,
                subject=rendered_subject,
                body=rendered_body,
                is_html=True
            )
            return {"status": "success", "message": f"Email sent for rule {rule.id}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def evaluate_user_registration_rules(db: Session, user_context: Dict[str, Any]):
        """Evaluate all user_registration rules against user context."""
        rules = db.query(Rule).filter(Rule.trigger_type == "user_registration").all()
        results = []
        for rule in rules:
            if RuleService.evaluate_condition(rule.condition, user_context):
                results.append(RuleService.trigger_rule(db, rule, user_context))
        return results

    @staticmethod
    def evaluate_time_based_rules(db: Session):
        """Evaluate time_based rules for current time."""
        now = datetime.now(timezone.utc)
        rules = db.query(Rule).filter(Rule.trigger_type == "time_based").all()
        results = []
        for rule in rules:
            condition = rule.condition
            # Expect condition to have a "time" field (ISO string)
            if "time" in condition:
                target_time = datetime.fromisoformat(condition["time"].replace("Z", "+00:00"))
                if target_time <= now:
                    results.append(RuleService.trigger_rule(db, rule, {"time": now}))
        return results

    @staticmethod
    def evaluate_api_trigger_rules(db: Session, api_context: Dict[str, Any]):
        """Evaluate api_trigger rules against api context."""
        rules = db.query(Rule).filter(Rule.trigger_type == "api_trigger").all()
        results = []
        for rule in rules:
            if RuleService.evaluate_condition(rule.condition, api_context):
                results.append(RuleService.trigger_rule(db, rule, api_context))
        return results


rule_service = RuleService()
