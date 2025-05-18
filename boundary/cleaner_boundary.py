from flask import (
    Blueprint, request, render_template,
    redirect, url_for, flash, session,abort
)
from utils.decorators import login_required,load_listing

from controllers.c_create_service_listing_controller import CleanerCreateServiceListingController
from controllers.pm_list_service_categories_controller  import PmListServiceCategoryController
from controllers.c_list_service_listings_controller import CleanerListServiceListingsController
from controllers.c_delete_service_listing_controller import CleanerDeleteServiceListingController
from controllers.c_update_service_listing_controller import CleanerUpdateServiceListingController
from controllers.c_search_service_listings_controller import CleanerSearchServiceListingsController
from controllers.c_views_controller import CleanerViewController
from controllers.c_shortlisted_controller import CleanerShortlistedController
from controllers.c_list_confirmed_matches_controller import CleanerListConfirmedMatchesController
from controllers.c_search_confirmed_matches_controller import CleanerSearchConfirmedMatchesController
from controllers.c_listing_detail_controller import CleanerListingDetailsController
from controllers.c_confirm_match_detail_controller import CleanerConfirmedMatchDetailController



cleaner_bp = Blueprint('cleaner', __name__, url_prefix='/cleaner')

_create_listing_ctrl = CleanerCreateServiceListingController()
_list_cat_ctrl = PmListServiceCategoryController()
_list_listings_ctrl = CleanerListServiceListingsController()
_update_listing_ctrl = CleanerUpdateServiceListingController()
_delete_listing_ctrl = CleanerDeleteServiceListingController()
_search_listings_ctrl = CleanerSearchServiceListingsController()
_view_ctrl = CleanerViewController()
_shortlisted_ctrl = CleanerShortlistedController()
_search_confirmed_ctrl = CleanerSearchConfirmedMatchesController()
_list_confirmed_ctrl = CleanerListConfirmedMatchesController()
_view_listing_ctrl = CleanerListingDetailsController()
_view_match_ctrl = CleanerConfirmedMatchDetailController()

@cleaner_bp.route('/listings/create', methods=['GET', 'POST'])
@login_required
def create_service_listing_page():
    categories = _list_cat_ctrl.handle()

    if request.method == 'POST':
        desc_raw   = request.form.get('description', '').strip()
        price_raw  = request.form.get('price',       '').strip()
        cat_raw    = request.form.get('category_id', '').strip()
        errors     = []

        price = float(price_raw)
        category_id = int(cat_raw)
        cleaner_id = session.get('user_id')
        listing = _create_listing_ctrl.handle({
                'cleaner_id':  cleaner_id,
                'description': desc_raw,
                'price':       price,
                'category_id': category_id
            })
        
        return redirect(url_for('web.dashboard_page'))


    return render_template(
        'create_listing.html',
        categories=categories
    )

@cleaner_bp.route('/listings', methods=['GET'])
@login_required
def list_service_listings_page():
    """

    """
    cleaner_id = session.get('user_id')
    if not cleaner_id:
        abort(403)

    q = request.args.get('q', '').strip()
    if q:
        listings = _search_listings_ctrl.handle({'cleaner_id': cleaner_id, 'keyword': q})
    else:
        listings = _list_listings_ctrl.handle(cleaner_id)

    metrics = {
        l.listing_id: {
            'views':     _view_ctrl.get_views(l.listing_id),
            'shortlist': _shortlisted_ctrl.get_shortlist_count(l.listing_id)
        }
        for l in listings
    }

    return render_template(
        'servicelistings.html',
        listings=listings,
        q=q,
        metrics=metrics
    )

@cleaner_bp.route('/listings/<int:listing_id>', methods=['GET'])
@login_required
def view_service_listing_page(listing_id):
    cleaner_id = session.get('user_id')
    listing = _view_listing_ctrl.handle(cleaner_id, listing_id)
    views = _view_ctrl.get_views(listing_id)
    shortlist = _shortlisted_ctrl.get_shortlist_count(listing_id)
    return render_template(
    'view_service_listing.html',
    listing=listing,
    views=views,
    shortlist=shortlist,
)

@cleaner_bp.route('/listings/<int:listing_id>/edit', methods=['GET','POST'])
@login_required
@load_listing(ensure_cleaner=True)
def edit_service_listing_page(listing):
    categories = _list_cat_ctrl.handle()

    if request.method == 'POST':
        desc_raw = request.form.get('description','').strip()
        price_raw = request.form.get('price','').strip()
        cat_raw   = request.form.get('category_id','').strip()
        errors = []

        price = float(price_raw)
        category_id = int(cat_raw)
        
        _update_listing_ctrl.handle({
                'listing_id':  listing.listing_id,
                'description': desc_raw,
                'price':       price,
                'category_id': category_id
            })
        
        return redirect(url_for('cleaner.list_service_listings_page'))
        

    return render_template(
        'edit_service_listing.html',
        listing    = listing,
        categories = categories
    )

@cleaner_bp.route('/listings/<int:listing_id>/delete', methods=['POST'])
@login_required
@load_listing(ensure_cleaner=True)
def delete_service_listing_page(listing):
    try:
        _delete_listing_ctrl.handle(listing.listing_id)
        flash(f"Deleted listing ID={listing.listing_id}", 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('cleaner.list_service_listings_page'))

@cleaner_bp.route('/confirmed_matches', methods=['GET'])
@login_required
def list_confirmed_matches_page():
    """

    """
    cleaner_id = session.get('user_id')
    if not cleaner_id:
        abort(403)

    q = request.args.get('q', '').strip()
    if q:
        matches = _search_confirmed_ctrl.handle(cleaner_id, q)
            
    else:
        matches = _list_confirmed_ctrl.handle(cleaner_id)

    

    return render_template(
        'c_confirmed_matches.html',
        matches=matches,
        q=q
    )

@cleaner_bp.route('/matches/<int:match_id>', methods=['GET'])
@login_required
def view_confirmed_match_page(match_id):
    cleaner_id = session.get('user_id')
    match = _view_match_ctrl.handle(cleaner_id, match_id)
    return render_template('view_confirmed_match.html', match=match)