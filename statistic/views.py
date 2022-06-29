from django.db.models import Sum, Q, F
from django.shortcuts import render
from rest_framework import views, response, status

from categories.models import Category
from orders.models import Order, OrderProduct

# Create your views here.
from orders.permissions import OrderAPIPermission
from .serializers import UserExpenseStatisticSerializer, UserExpenseByCategory


class UserExpenseStats(views.APIView):
    permission_classes = (OrderAPIPermission,)

    def get(self, request):
        # input
        current_user = self.request.user
        year = self.request.query_params['year']

        # process
        expense_sum_of_user = \
            Order.objects.filter(account_id=current_user.id).filter(modified_at__year=year).filter(
                ~Q(status='Canceled')).aggregate(Sum('order_total'))[
                'order_total__sum']
        list_expense_statistic_by_month = []
        for month in range(1, 13):
            expense_sum_of_month = \
                Order.objects.filter(account_id=current_user.id).filter(modified_at__year=year).filter(
                    modified_at__month=str(month)).filter(~Q(status='Canceled')).aggregate(Sum('order_total'))[
                    'order_total__sum']
            if expense_sum_of_month is None:
                # Neu nguoi dung khong tieu tien trong thang do thi cho tien thang do la 0
                expense_sum_of_month = 0
            if expense_sum_of_user is None:
                # neu nguoi dung khong tieu tien vao nam da chon thi cho bua` 1 gia tri, o day cho tam la 100
                expense_sum_of_user = 100
            percent_expense = expense_sum_of_month / expense_sum_of_user * 100 if expense_sum_of_user != 0 else 0
            expense_statistic = {"month": month, "expense_sum_of_month": expense_sum_of_month,
                                 "percent_expense": round(percent_expense, 2)}
            list_expense_statistic_by_month.append(expense_statistic)

        result = UserExpenseStatisticSerializer(list_expense_statistic_by_month, many=True).data

        return response.Response(result, status=status.HTTP_200_OK)


class UserExpenseByCategoryStats(views.APIView):
    def get(self, request):
        # input
        current_user = self.request.user
        year = self.request.query_params['year']
        month = self.request.query_params['month']

        # process
        expense_sum_of_user = \
            Order.objects.filter(account_id=current_user.id).filter(modified_at__year=year).filter(
                modified_at__month=str(month)).filter(~Q(status='Canceled')).aggregate(Sum('order_total'))[
                'order_total__sum']
        categories = Category.objects.all()
        list_expense_stats_by_category = []
        for category in categories:
            expense_sum_of_category = OrderProduct.objects.filter(
                order__account_id=current_user.id).filter(order__modified_at__year=year).filter(
                order__modified_at__month=str(month)).filter(~Q(order__status='Canceled')).filter(
                product__category_id=category.id).aggregate(category_total=Sum(F('price') * F('quantity')))[
                'category_total']
            expense_stat_by_category = {"total_of_user": expense_sum_of_user, "category": category.category_name,
                                        "total": expense_sum_of_category if expense_sum_of_category is not None else 0}
            if expense_sum_of_category is not None:
                list_expense_stats_by_category.append(expense_stat_by_category)

        result = UserExpenseByCategory(list_expense_stats_by_category, many=True).data
        return response.Response(result, status=status.HTTP_200_OK)
