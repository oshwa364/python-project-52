from django import forms
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter

from task_manager.labels.models import Label

from .models import Task


class TaskFilter(FilterSet):
    labels = ModelChoiceFilter(
        queryset=Label.objects.all(),
        label='Метка',
    )
    
    self_tasks = BooleanFilter(
        label='Только свои задачи',
        widget=forms.CheckboxInput,
        method='get_self_tasks',
    )

    def get_self_tasks(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(author=user)
        return queryset
    
    class Meta:
        model = Task
        fields = ['status', 'executor']