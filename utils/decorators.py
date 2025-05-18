from flask import session, redirect, url_for, flash,request,abort
from functools import wraps
from entities.service_category_entity import ServiceCategoryEntity
from entities.account_entity import AccountEntity
from entities.profile_entity import ProfileEntity



def login_required(f):
    """
    Decorator that ensures the user is logged in.
    If not, redirect to the login page.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            # User is not authenticated: send to login page
            return redirect(url_for('web.login_page'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    """
    Decorator that ensures the current user has 'user admin' role.
    If not, flash a warning and redirect to the dashboard.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'user admin':
            # Insufficient permissions: show message and back to dashboard
            flash('Permission denied.', 'warning')
            return redirect(url_for('web.dashboard_page'))
        return f(*args, **kwargs)
    return decorated

def load_account(f):
    @wraps(f)
    def decorated(uid, *args, **kwargs):
        acct = AccountEntity.query.get(uid)
        if not acct:
            abort(404)           # 或者 flash+redirect
        return f(acct, *args, **kwargs)
    return decorated

def load_profile(f):
    @wraps(f)
    def decorated(role, *args, **kwargs):
        prof = ProfileEntity.query.get(role)
        if not prof:
            abort(404)   # 或者 flash+redirect 都行
        return f(prof, *args, **kwargs)
    return decorated

def load_service_category(f):
    """根据 URL 中的 sc_id 加载实体，不存在则 404"""
    @wraps(f)
    def wrapper(sc_id, *args, **kwargs):
        category = ServiceCategoryEntity.query.get(sc_id)
        if category is None:
            abort(404)
        return f(category, *args, **kwargs)
    return wrapper

def load_listing(ensure_cleaner: bool = False):
    """
    Decorator factory.
    - If ensure_owner=True, additionally checks listing.cleaner_id == session['user_id'].
    - Otherwise only checks existence.
    """

    def decorator(f):
        @wraps(f)
        def wrapper(listing_id, *args, **kwargs):
            from entities.service_listing_entity       import ServiceListingEntity
            listing = ServiceListingEntity.query.get(listing_id)
            if not listing:
                abort(404)
            if ensure_cleaner and listing.cleaner_id != session.get('user_id'):
                abort(404)
            return f(listing, *args, **kwargs)
        return wrapper
    return decorator
