from django_filters import FilterSet
from .models import User


class UserFilter(FilterSet):

    class Meta:
        model = User

        fields = {
            'username': ['exact', 'contains'],
            'first_name': ['exact', 'contains'],
            'last_name': ['exact', 'contains'],
            'mobile': ['exact'],
            'email': ['exact', 'contains'],
            'date_joined': ['exact', 'gte', 'lte'],
        }
