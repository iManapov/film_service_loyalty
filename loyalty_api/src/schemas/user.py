from datetime import datetime
import uuid
from src.schemas.mixin import JsonMixin


class User(JsonMixin):
    """User schema"""

    id: uuid.UUID
    is_trial_used: bool
    subscription_until: datetime
