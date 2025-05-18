# boundary/admin_account_boundary.py

from flask import Blueprint, request, jsonify
from controllers.admin_create_account_controller import AdminCreateAccountController

admin_account_bp = Blueprint(
    'admin_account',       # endpoint namespace
    __name__, 
    url_prefix='/api/admin/accounts'
)

_create_ctrl = AdminCreateAccountController()

@admin_account_bp.route('', methods=['POST'])
def create_account_api():
    """
    POST /api/admin/accounts
    Body JSON: {name,email,password,phone?,role,is_active}
    """
    payload = request.get_json(force=True)
    try:
        acct = _create_ctrl.handle(payload)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify(acct.to_dict()), 201
