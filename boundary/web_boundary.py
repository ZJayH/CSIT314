from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort, send_file
from utils.decorators import login_required, admin_required,load_service_category,load_account, load_profile
from io import BytesIO
from datetime import date, timedelta
from exceptions import DomainError,CreateError,LoginError,UpdateError


# Import all controllers
from controllers.login_controller       import AdminLoginController
from controllers.logout_controller      import AdminLogoutController
from controllers.admin_create_account_controller  import AdminCreateAccountController
from controllers.admin_list_accounts_controller   import AdminListAccountsController
from controllers.admin_update_account_controller  import AdminUpdateAccountController
from controllers.admin_search_accounts_controller  import AdminSearchAccountsController
from controllers.admin_roles_controller         import AdminRolesController
from controllers.admin_create_profile_controller  import AdminCreateProfileController
from controllers.admin_list_profiles_controller   import AdminListProfilesController
from controllers.admin_update_profile_controller  import AdminUpdateProfileController
from controllers.admin_search_profiles_controller import AdminSearchProfilesController
from controllers.admin_suspend_account_controller import AdminSuspendAccountController
from controllers.admin_suspend_profile_controller import AdminSuspendProfileController
from controllers.pm_create_service_category_controller import PmCreateServiceCategoryController
from controllers.pm_list_service_categories_controller  import PmListServiceCategoryController
from controllers.pm_update_service_category_controller import PmUpdateServiceCategoryController
from controllers.pm_delete_category_controller import PmDeleteServiceCategoryController
from controllers.pm_search_service_category_controller import PmSearchServiceCategoryController
from controllers.pm_day_report_controller import PmDayReportController
from controllers.pm_month_report_controller import PmMonthReportController
from controllers.pm_week_report_controller import PmWeekReportController
from controllers.pm_reports_page_controller import ReportsPageController

web_bp = Blueprint('web', __name__)

@web_bp.route('/')
def index():
    return redirect(url_for('web.login_page'))

# Instantiate controllers once for reuse
_login_ctrl            = AdminLoginController()
_logout_ctrl           = AdminLogoutController()
_create_account_ctrl   = AdminCreateAccountController()
_list_accounts_ctrl    = AdminListAccountsController()
_update_account_ctrl   = AdminUpdateAccountController()
_search_accounts_ctrl  = AdminSearchAccountsController()
_roles_ctrl            = AdminRolesController()
_create_profile_ctrl   = AdminCreateProfileController()
_list_profiles_ctrl    = AdminListProfilesController()
_update_profile_ctrl   = AdminUpdateProfileController()
_search_profiles_ctrl  = AdminSearchProfilesController()
_suspend_account_ctrl  = AdminSuspendAccountController()
_suspend_profile_ctrl  = AdminSuspendProfileController()
_create_sc_ctrl = PmCreateServiceCategoryController()
_list_sc_ctrl   = PmListServiceCategoryController()
_update_sc_ctrl = PmUpdateServiceCategoryController()
_delete_sc_ctrl = PmDeleteServiceCategoryController()
_search_sc_ctrl = PmSearchServiceCategoryController()
_day_report_ctrl = PmDayReportController()
_month_report_ctrl = PmMonthReportController()
_week_report_ctrl = PmWeekReportController()
_reports_page_ctrl = ReportsPageController()


@web_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    """
    Display login form on GET.
    Authenticate and set session on POST.
    """
    if request.method == 'POST':
        email = request.form['email'].strip()
        pw    = request.form['password'].strip()
        try:
            acct = _login_ctrl.handle({"email": email, "password": pw})
            session.clear()
            session['user_id'] = acct.id
            session['role']    = acct.role
            return redirect(url_for('web.dashboard_page'))
        except LoginError as e:
            flash(str(e), 'danger')

    return render_template('login.html')

@web_bp.route('/dashboard')
@login_required
def dashboard_page():
    """
    Show the main dashboard. User must be authenticated.
    """
    return render_template('dashboard.html')

@web_bp.route('/logout')
@login_required
def logout_page():
    """
    Log out the current user: clear session and redirect to login.
    """
    _logout_ctrl.handle()
    session.clear()
    return redirect(url_for('web.login_page'))

@web_bp.route('/create-account', methods=['GET', 'POST'])
@login_required
@admin_required
def create_account_page():
    """
    Allow a 'user admin' to create a new user account.
    On GET: render creation form with role list.
    On POST: validate and persist via controller.
    """
    roles = _roles_ctrl.handle()
    if request.method == 'POST':
        payload = {
            "name":      request.form['name'].strip(),
            "email":     request.form['email'].strip(),
            "password":  request.form['password'].strip(),
            "phone":     request.form.get('phone','').strip() or None,
            "role":      request.form['role'],
            "is_active": bool(request.form.get('is_active'))
        }
        try:
            acct = _create_account_ctrl.handle(payload)
            return redirect(url_for('web.dashboard_page'))
        except CreateError as e:
            flash(str(e), 'danger')
    return render_template('create_account.html', roles=roles)

@web_bp.route('/accounts')
@login_required
@admin_required
def list_accounts_page():
    """
    List all user accounts, or search by keyword if 'q' provided.
    """
    q = request.args.get('q', '').strip()
    if q:
        accounts = _search_accounts_ctrl.handle(q)
        info_msg = f"Search results for '{q}':"
    else:
        accounts = _list_accounts_ctrl.handle()
        info_msg = None
    return render_template('accounts.html',
                           users=accounts,
                           keyword=q,
                           info_msg=info_msg)

@web_bp.route('/accounts/<int:uid>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
@load_account
def edit_account_page(acct):
    """
    Edit a specific account.  
    """
    roles = _roles_ctrl.handle()
    if request.method == 'POST':
        data = {
            'id':        acct.id,
            'name':      request.form['name'].strip(),
            'email':     request.form['email'].strip(),
            'phone':     request.form.get('phone','').strip() or None,
            'role':      request.form['role'],
            'is_active': bool(request.form.get('is_active'))
        }
        try:
            _update_account_ctrl.handle(data)
            return redirect(url_for('web.list_accounts_page'))
        except UpdateError as e:
            flash(str(e), 'danger')
    return render_template('edit_account.html',
                           acct=acct,
                           roles=roles)

@web_bp.route('/accounts/<int:uid>/suspend', methods=['POST'])
@login_required
@admin_required
def suspend_account(uid):
    """
    Suspend the given account (set is_active=False).
    """
    _suspend_account_ctrl.handle(uid)

    return redirect(url_for('web.list_accounts_page'))

@web_bp.route('/manage-roles')
@login_required
@admin_required
def list_profiles_page():
    """
    Display or search user profiles (roles) for management.
    """
    q = request.args.get('q', '').strip()
    if q:
        profiles = _search_profiles_ctrl.handle(q)
        info_msg = f"Search results for '{q}':"
    else:
        profiles = _list_profiles_ctrl.handle()
        info_msg = None
    return render_template('manage_roles.html',
                           profiles=profiles,
                           keyword=q,
                           info_msg=info_msg)

@web_bp.route('/create-role', methods=['GET', 'POST'])
@login_required
@admin_required
def create_role_page():
    """
    Allow creation of a new profile (role).
    """
    if request.method == 'POST':
        payload = {
            'role':        request.form['role'].strip(),
            'description': request.form.get('description','').strip(),
            'is_active':   bool(request.form.get('is_active'))
        }
        try:
            _create_profile_ctrl.handle(payload)
            return redirect(url_for('web.list_profiles_page'))
        except CreateError as e:
            flash(str(e), 'danger')
    return render_template('create_role.html')

@web_bp.route('/profiles/<role>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
@load_profile
def edit_profile_page(prof):
    """
    Edit an existing profile.  
    @load_profile decorator ensures 'prof' is loaded.
    """
    if request.method == 'POST':
        payload = {
            'role':        prof.role,
            'description': request.form.get('description','').strip(),
            'is_active':   bool(request.form.get('is_active'))
        }
        _update_profile_ctrl.handle(payload)
        return redirect(url_for('web.list_profiles_page'))
    return render_template('edit_profile.html', profile=prof)

@web_bp.route('/profiles/<role>/suspend', methods=['POST'])
@login_required
@admin_required
def suspend_profile(role):
    """
    Suspend a profile (set is_active=False), preventing users of that
    role from logging in.
    """
    _suspend_profile_ctrl.handle(role)

    return redirect(url_for('web.list_profiles_page'))

@web_bp.route('/service_categories', methods=['GET'])
def list_categories_page():
    """
    """
    q = request.args.get('q', '').strip()
    if q:
        categories = _search_sc_ctrl.handle(q)
    else:
        categories = _list_sc_ctrl.handle()
    return render_template(
        'categories.html',
        categories=categories,
        q=q
    )


@web_bp.route('/service_categories/create', methods=['GET', 'POST'])
def create_service_category_page():

    if request.method == 'POST':
        payload = {
            "name": request.form['name'].strip(),
            "description": request.form.get('description', '').strip() or None
        }
        try:
            sc = _create_sc_ctrl.handle(payload)
            return redirect(url_for('web.list_categories_page'))
        except CreateError as e:
            flash(str(e), 'danger')

    return render_template('create_category.html')

@web_bp.route('/service_categories/<int:sc_id>/edit', methods=['GET','POST'])
@load_service_category
def edit_service_category_page(category):
    """
    """
    if request.method == 'POST':
        payload = {
            "id":          category.id,               # 可以不用，但保留给 Controller
            "name":        request.form['name'].strip(),
            "description": request.form.get('description','').strip() or None
        }
        try:
            updated = _update_sc_ctrl.handle(payload)
            return redirect(url_for('web.list_categories_page'))
        except UpdateError as e:
            flash(str(e), 'danger')
    return render_template('edit_category.html', category=category)


@web_bp.route('/service_categories/<int:sc_id>/delete', methods=['POST'])
@load_service_category
def delete_service_category_page(category):
    _delete_sc_ctrl.handle(category.id)
    return redirect(url_for('web.list_categories_page'))

@web_bp.route('/reports', methods=['GET'])
def reports_page():
    today = date.today()

    # last 30 days for “daily”
    dates = [(today - timedelta(days=i)).isoformat() for i in range(0, 30)]

    # last 12 Mondays for “weekly”
    mondays = []
    this_monday = today - timedelta(days=today.weekday())
    for i in range(0, 12):
        mondays.append( (this_monday - timedelta(weeks=i)).isoformat() )

    # last 6 months for “monthly”
    months = []
    for i in range(0, 6):
        m = (today.month - i - 1) % 12 + 1
        y = today.year - ((today.month - i - 1) // 12)
        months.append(f"{y:04d}-{m:02d}")

    return render_template(
      'reports.html',
      dates=dates,
      weeks=mondays,
      months=months
    )

@web_bp.route('/reports/daily.xlsx', methods=['GET'])
def download_daily_report():
    raw = request.args.get('date','').strip()
    stream = _day_report_ctrl.handle_daily(raw or None)
    return send_file(
        stream, as_attachment=True,
        download_name=f"daily_{raw or 'latest'}.xlsx",
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@web_bp.route('/reports/weekly.xlsx', methods=['GET'])
def download_weekly_report():
    raw = request.args.get('week_start','').strip()
    stream = _week_report_ctrl.handle_weekly(raw or None)
    return send_file(
        stream, as_attachment=True,
        download_name=f"weekly_{raw or 'latest'}.xlsx",
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@web_bp.route('/reports/monthly.xlsx', methods=['GET'])
def download_monthly_report():
    raw = request.args.get('month','').strip()
    stream = _month_report_ctrl.handle_monthly(raw or None)
    return send_file(
        stream, as_attachment=True,
        download_name=f"monthly_{raw or 'latest'}.xlsx",
        mimetype='application/vnd.openxmlformats-officedocument-spreadsheetml.sheet'
    )
