import uuid

def generate_invite_code():
    return str(uuid.uuid4())[:8].upper()