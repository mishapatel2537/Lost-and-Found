from app.models.organization import Organization
from app.models.organization_settings import OrganizationSettings
from app.utils.helpers import generate_invite_code

def create_organization(db, name):
    org = Organization(name=name,
                       invite_code=generate_invite_code())
    db.add(org)
    db.commit()
    db.refresh(org)

    #default settings
    settings = OrganizationSettings(organization_id=org.id)
    db.add(settings)
    db.commit()

    return org

def get_org_settings(db, org_id):
    return db.query(OrganizationSettings).filter_by(
        organization_id=org_id
    ).first()
