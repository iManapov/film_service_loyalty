from dataclasses import dataclass


@dataclass
class ErrorMsg:
    """Класс сообщений об ошибках."""
    is_production: str = 'This is production!'

    not_found: str = 'Not found'
    bad_request: str = 'Bad request: errors in parameters'

    promo_not_found: str = 'Promo code not found'
    promo_expired: str = 'Promo code is expired'
    promo_wrong_user: str = 'Unable to apply promo code for current user'
    promo_used: str = 'Promo already used'
    no_subs: str = 'Subscriptions not found'
    user_not_found: str = 'User not found'
    discount_not_found: str = 'Discount not found'
    film_not_found: str = 'Film not found'
    trial_subs_not_found: str = 'Trial subscription not found'


error_msgs = ErrorMsg()
