from django_filters import rest_framework as filters
from .models import Job

class JobsFilter(filters.FilterSet):

    # SEARCH API
    keyword = filters.CharFilter(field_name='title', lookup_expr='icontains')
    location = filters.CharFilter(field_name='address', lookup_expr='icontains')

    # FILTERS
    min_salary = filters.NumberFilter(field_name='salary' or 0, lookup_expr='gte')
    max_salary = filters.NumberFilter(field_name='salary' or 1000000, lookup_expr='lte')

    class Meta:
        model = Job
        fields = ('keyword', 'location', 'education', 'experience', 'jobType', 'industry', 'min_salary', 'max_salary')
