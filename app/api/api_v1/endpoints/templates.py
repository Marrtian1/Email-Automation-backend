from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.api import deps
from app.core.db import get_db
from app.schemas.template import Template, TemplateCreate, TemplateUpdate
from app.services.template_service import template_service

router = APIRouter()

@router.post("/", response_model=Template)
def create_template(
    *,
    db: Session = Depends(get_db),
    template_in: TemplateCreate,
    current_user = Depends(deps.get_current_user)
):
    return template_service.create_template(db=db, template_in=template_in)

@router.get("/", response_model=List[Template])
def read_templates(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(deps.get_current_user)
):
    return template_service.get_templates(db=db, skip=skip, limit=limit)

@router.get("/{template_id}", response_model=Template)
def read_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(deps.get_current_user)
):
    template = template_service.get_template(db=db, template_id=template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@router.put("/{template_id}", response_model=Template)
def update_template(
    *,
    db: Session = Depends(get_db),
    template_id: int,
    template_in: TemplateUpdate,
    current_user = Depends(deps.get_current_user)
):
    template = template_service.get_template(db=db, template_id=template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template_service.update_template(db=db, db_template=template, template_in=template_in)

@router.delete("/{template_id}", response_model=Template)
def delete_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(deps.get_current_user)
):
    template = template_service.delete_template(db=db, template_id=template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@router.post("/{template_id}/render")
def render_template(
    template_id: int,
    placeholders: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user = Depends(deps.get_current_user)
):
    template = template_service.get_template(db=db, template_id=template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    rendered_body = template_service.render_template(template.body, placeholders)
    return {
        "subject": template.subject,
        "rendered_body": rendered_body
    }
