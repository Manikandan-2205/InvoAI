import os
from flask import session, redirect, url_for
from functools import wraps
from datetime import datetime, timedelta

def set_claims(user_id, role="user", avatar="JD", username="John Doe", remember=False):
    session["user_id"] = user_id
    session["role"] = role
    session["username"] = username
    session["avatar"] = avatar

    if remember:
        # Persistent cookie
        session.permanent = True
        remember = os.getenv("REMEMBER_ME_EXPIRY_DAYS")
        remember_me_expiry_days = int(remember)
        session["expires_at"] = (datetime.now() + timedelta(days=remember_me_expiry_days)).timestamp()
    else:
        # Short session
        session.permanent = False
        session_timer = os.getenv("SESSION_EXPIRY_MINUTES")
        session_expiry_minutes = int(session_timer)
        session["expires_at"] = (datetime.now() + timedelta(minutes=session_expiry_minutes)).timestamp()

def remove_claims():
    session.clear() 

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
