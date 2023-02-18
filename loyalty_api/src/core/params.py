from dataclasses import dataclass

from fastapi import Query, Path
from pydantic import Required


@dataclass
class Params:
    """API request parameters"""

    user_id: Query = Query(
        default=Required,
        title="User id"
    )

    promo_code: Query = Query(
        default=Required,
        title="Promo code"
    )

    promo_id: Path = Path(
        default=Required,
        title="Promocode UUID"
    )

    subs_id: Query = Query(
        default=Required,
        title="Subscription UUID"
    )

    discount_id: Path = Path(
        default=Required,
        title="Discount UUID"
    )

    film_id: Query = Query(
        default=Required,
        title='Film UUID'
    )


params = Params()
