from rest_framework import serializers


class UserExpenseStatisticSerializer(serializers.Serializer):
    month = serializers.IntegerField()
    expense_sum_of_month = serializers.IntegerField()
    percent_expense = serializers.FloatField()


class UserExpenseByCategory(serializers.Serializer):
    category = serializers.CharField()
    total = serializers.IntegerField()
