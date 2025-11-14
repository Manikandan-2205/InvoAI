from flask import session, redirect, url_for
from functools import wraps
from datetime import datetime, timedelta

def set_claims(user_id, role="user"):
    session["user_id"] = user_id
    session["role"] = role
    session["expires_at"] = (datetime.now() + timedelta(minutes=30)).timestamp()

def is_authenticated():
    return "user_id" in session and not is_expired()

def is_expired():
    expires_at = session.get("expires_at")
    if not expires_at:
        return True
    return datetime.now().timestamp() > expires_at

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):        
        if not is_authenticated():
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

def has_role(required_role):
    return session.get("role") == required_role
