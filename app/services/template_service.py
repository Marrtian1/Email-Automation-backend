import re
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.models.template import Template
from app.schemas.template import TemplateCreate, TemplateUpdate

class TemplateService:
    @staticmethod
    def render_template(template_body: str, placeholders: Dict[str, Any]) -> str:
        """
        Replaces placeholders like {{name}} with values from the placeholders dict.
        """
        rendered = template_body
        for key, value in placeholders.items():
            placeholder = f"{{{{{key}}}}}"
            rendered = rendered.replace(placeholder, str(value))
        return rendered

    @staticmethod
    def create_template(db: Session, template_in: TemplateCreate) -> Template:
        db_template = Template(**template_in.dict())
        db.add(db_template)
        db.commit()
        db.refresh(db_template)
        return db_template

    @staticmethod
    def get_template(db: Session, template_id: int) -> Template:
        return db.query(Template).filter(Template.id == template_id).first()

    @staticmethod
    def get_templates(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Template).offset(skip).limit(limit).all()

    @staticmethod
    def update_template(db: Session, db_template: Template, template_in: TemplateUpdate) -> Template:
        update_data = template_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_template, field, value)
        db.add(db_template)
        db.commit()
        db.refresh(db_template)
        return db_template

    @staticmethod
    def delete_template(db: Session, template_id: int) -> Template:
        template = db.query(Template).filter(Template.id == template_id).first()
        if template:
            db.delete(template)
            db.commit()
        return template

template_service = TemplateService()
