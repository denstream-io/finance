from flask import Blueprint, flash, redirect, render_template, request
from flask_login import login_user, current_user, logout_user, login_required

finance = home_bp = Blueprint(
    'finance_bp', __name__
)



@finance.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
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