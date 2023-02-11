from datetime import datetime
import uuid
from src.models.mixin import JsonMixin


class User(JsonMixin):
    id: uuid.UUID
    is_trial_used: bool
    subscription_until: datetime
