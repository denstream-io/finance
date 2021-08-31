from flask import Blueprint, flash, redirect, render_template, request
from flask_login import login_user, current_user, logout_user, login_required
from time import strftime

from my_app import db
from ..forms import BuyForm
from ..helpers import lookup
from ..models import TransactionHistory, UserActivities, User

finance = home_bp = Blueprint(
    'finance_bp', __name__
)



@finance.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    form = BuyForm()
    
    if form.validate_on_submit():
        quote = lookup(form.symbol.data)
        if quote is not None:
            share_price = quote["price"]

            total_cost = share_price * int(form.shares.data)
            user_share = UserActivities.query.filter(id=current_user.id).shares

            #user_ = User.query.join(UserActivities).filter(User.id == skill_name).all()

            if not user_share:
                user = User.query.filter(id=current_user.id)
                user_cash = user.cash
                # check if user has enough fund
                if total_cost > user_cash:
                    return flash("not enough balance", 400)
                # remove the share cost from balance
                cash_balance = user_cash - total_cost
                # Take note of time of purchase
                date = strftime("%m-%d-%Y %H:%M")
                transaction = TransactionHistory(
                        id=current_user.id, 
                        symbol=form.symbol.data,
                        price=lookup(form.symbol.data)["price"],
                        shares=form.shares.data,
                        date=date
                    )
                db.session.add(transaction)
                # Update the balance in the users database
                balance = User.query.get(id=current_user.id)
                balance.cash = cash_balance
                

                # push transaction details into database
                user_activities = UserActivities(
                    id=current_user.id,
                    symbol=form.symbol.data,
                    name=lookup(form.symbol.data).name, # DEBUG!
                    shares=form.shares.data,
                    price=lookup(form.symbol.data).price, # DEBUG!
                    total=total_cost 
                )
                return redirect("home_bp.index")
            else:
                # Get the number of new shares
                new_share = int(form.shares.data)
                # lookup the price for the share
                price = lookup(form.symbol.data).price # DEBUG!
                # pull out the old number of share
                old_share = User.query.filter(id=current_user.id).shares
                # Add to the old share
                total_shares = old_share + new_share
                # Calculate the new share price
                new_share_price = price * new_share
                # add the new share price to the old price of that same stock
                total_price = new_share_price + total_cost
                # pull out new user cash
                user_cash = User.query.filter(id=current_user.id).cash
                # check if user has enough fund
                if new_share_price > user_cash:
                    return flash("not enough balance", 400)
                # remove the share price from the user cash
                new_cash_balance = user_cash - new_share_price

                # Take note of time of sale
                date = strftime("%m-%d-%Y %H:%M")
                transaction = TransactionHistory(
                        id=current_user.id, 
                        symbol=form.symbol.data,
                        price=lookup(form.symbol.data).price, # DEBUG! 
                        shares=form.shares.data,
                        date=date
                    )
                balance = User.query.get(id=current_user.id)
                balance.cash = new_cash_balance
            
                user_activities = UserActivities.query.get(id=current_user.id)
                user_activities.shares=total_shares
                user_activities.price=total_price

            return redirect("home_bp.index")
        else:
            flash("Invalid symbol")
    return render_template(
        "finance/buy.html",
        form=form,
        title='buy.',
        template='buy-page',
        body="check your account dashboard."
    )
        



@finance.route("/sell")
@login_required
def sell():
    pass


@finance.route("/history")
@login_required
def history():
    pass


@finance.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    pass