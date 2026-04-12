from app.models.invite_code import InviteCode
from app.models.organization import Organization
from app.utils.invite import generate_invite_code
from datetime import datetime

def create_invite_code(db, organization_id):
    organization = db.query(Organization).filter(Organization.id == organization_id).first()
    if not organization:
        raise Exception("Organization not found")

    code = generate_invite_code()

    invite = InviteCode(
        code=code,
        organization_id=organization_id
    )

    db.add(invite)
    db.commit()
    db.refresh(invite)

    return invite


def validate_invite_code(db, code):
    invite = db.query(InviteCode).filter(
        InviteCode.code == code
    ).first()

    if not invite:
        raise Exception("Invalid invite code")

    if not invite.is_active:
        raise Exception("Invite code disabled")

    if invite.used_count is None or invite.max_uses is None:
        raise Exception("Invite code is not configured correctly")

    if invite.used_count >= invite.max_uses:
        raise Exception("Invite code limit reached")

    if invite.expires_at is None:
        raise Exception("Invite code is not configured correctly")

    if invite.expires_at < datetime.utcnow():
        raise Exception("Invite code expired")

    return invite
