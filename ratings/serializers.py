from rest_framework import serializers

from accounts.serializers import AccountSerializer
from ratings.models import Rating
from store.serializers import ProductSerializer


class RatingSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    modified_at = serializers.DateTimeField(format="%d %b %Y")

    class Meta:
        model = Rating
        fields = ['account', 'star_num', 'comment', 'modified_at']
