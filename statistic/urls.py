from django.urls import path
from .views import UserExpenseStats, UserExpenseByCategoryStats

urlpatterns = [
    path('user-expense', UserExpenseStats.as_view(), name='user-expense'),
    path('user-expense-by-category', UserExpenseByCategoryStats.as_view(), name='user-expense-by-category')
]
