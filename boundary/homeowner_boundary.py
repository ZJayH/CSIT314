from flask import (
    Blueprint, request, render_template,
    send_file, flash, redirect, url_for, abort,session
)
from utils.decorators import login_required, load_listing
from controllers.h_list_all_service_listings_controller import HomeListAllServiceListingsController
from controllers.h_search_all_service_listings_controller import HomeSearchAllServiceListingsController
from controllers.h_add_to_shortlist_controller import HomeAddToShortlistController
from controllers.h_remove_from_shortlist_controller import HomeRemoveFromShortlistController
from controllers.h_view_shortlist_controller import HomeViewShortlistController
from controllers.h_search_shortlist_controller import HomeSearchShortlistController
from controllers.h_get_shortlist_ids_controller import HomeGetShortlistIdsController
from controllers.h_list_homeowner_history_controller import HomeListHomeownerHistoryController
from controllers.h_search_homeowner_history_controller import HomeSearchHomeownerHistoryController
from controllers.h_view_listing_detail_controller import HomeoViewListingDetailController
from controllers.h_view_shortlisted_details_controller import HomeownerViewShortlistedListingController

homeowner_bp = Blueprint('homeowner', __name__, url_prefix='/homeowner')

_search_ctrl = HomeSearchAllServiceListingsController()
_list_all_ctrl = HomeListAllServiceListingsController()
_add_ctrl = HomeAddToShortlistController()
_remove_ctrl = HomeRemoveFromShortlistController()
_search_shortlist_ctrl = HomeSearchShortlistController()
_view_shortlist_ctrl = HomeViewShortlistController()
_get_shortlist_ids = HomeGetShortlistIdsController()
_search_history_ctrl = HomeSearchHomeownerHistoryController()
_list_history_ctrl = HomeListHomeownerHistoryController()
_view_listing_ctrl = HomeoViewListingDetailController()
_view_shortlisted_ctrl = HomeownerViewShortlistedListingController()



@homeowner_bp.route('/listings', methods=['GET'])
def list_service_listings_page():
    homeowner_id = session.get('user_id')
    if not homeowner_id:
        abort(403)

    shortlisted_ids = _get_shortlist_ids.handle(homeowner_id)

    q = request.args.get('q', '').strip()
    if q:
        listings = _search_ctrl.handle(q)  
    else:
        listings = _list_all_ctrl.handle()

    return render_template(
        'all_servicelistings.html',
        listings=listings,
        shortlisted_ids=shortlisted_ids,
        q=q
    )

@homeowner_bp.route('/listings/<int:listing_id>/shortlist', methods=['POST'])
@load_listing()
def toggle_shortlist(listing):
    homeowner_id = session.get('user_id')
    if not homeowner_id:
        abort(403)

    try:
        _add_ctrl.handle(homeowner_id, listing.listing_id)
        
    except ValueError:
        _remove_ctrl.handle(homeowner_id, listing.listing_id)
        

    return redirect(request.referrer or url_for('homeowner.all_servicelistings_page'))

@homeowner_bp.route('/shortlist', methods=['GET'])
def view_shortlist():
    """

    """
    homeowner_id = session.get('user_id')

    q = request.args.get('q', '').strip()
    if q:
        entries = _search_shortlist_ctrl.handle(homeowner_id, q)
    else:
        entries = _view_shortlist_ctrl.handle(homeowner_id)

    return render_template(
        'shortlist.html',
        shortlist=entries,
        q=q
    )

@homeowner_bp.route('/history', methods=['GET'])
@login_required
def service_history_page():
    """

    """
    homeowner_id = session.get('user_id')
    if not homeowner_id:
        abort(403)

    q = request.args.get('q', '').strip()
    if q:
        matches = _search_history_ctrl.handle(homeowner_id, q)
    else:
        matches = _list_history_ctrl.handle(homeowner_id)

    return render_template(
        'h_service_history.html',
        matches=matches,
        q=q
    )

@homeowner_bp.route('/listings/<int:listing_id>', methods=['GET'])
@login_required
def view_service_listing_page(listing_id):
        listing = _view_listing_ctrl.handle(listing_id)
        
        return render_template('homeowner_view_service_listing.html', listing=listing)

@homeowner_bp.route('/shortlist/listings/<int:listing_id>', methods=['GET'])
@login_required
def view_shortlisted_listing_page(listing_id):
    homeowner_id = session.get('user_id')

    listing = _view_shortlisted_ctrl.handle(homeowner_id, listing_id)

    return render_template('homeowner_view_service_listing.html', listing=listing)


