
import requests
from urllib.parse import quote_plus

from decouple import config
from wtforms.validators import ValidationError


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = config("API_KEY")
        url = f"https://cloud.iexapis.com/stable/stock/{quote_plus(symbol)}/quote?token={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None
 
class NoDuplicates():

    def __init__(self, model, field, message=u'This element already exists.'):
        self.model = model
        self.field = field

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)
