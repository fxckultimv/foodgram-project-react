from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum
from .validators import SlugValidator, min_amount

User = get_user_model()