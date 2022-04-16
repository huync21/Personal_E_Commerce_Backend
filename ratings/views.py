from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ratings.models import Rating
from ratings.permissions import RatingApiPermission
from ratings.serializers import RatingSerializer
from store.models import Product


class RatingViewSet(ModelViewSet):
    serializer_class = RatingSerializer
    pagination_class = None
    permission_classes = (RatingApiPermission,)

    def get_queryset(self):
        product_id = self.request.query_params.get('product_id')
        list_rating_of_product = Rating.objects.filter(product_id=product_id).order_by('-created_at')
        return list_rating_of_product

    def create(self, request, *args, **kwargs):
        account = request.user
        account_id = account.id
        product_id = self.request.query_params.get('product_id')
        product = Product.objects.get(id=product_id)
        if product is None:
            return Response(data={"error": "No product found to add rating"},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            rating_from_request = request.data

            # Check xem da co rating của người dùng cho product này chưa,
            # nếu có thì update, nếu không thì tạo mới

            # Check
            list_rating_of_product = Rating.objects.filter(product_id=product_id)
            rating_of_user = None
            for r in list_rating_of_product:
                if r.account_id == account_id:
                    rating_of_user = r
                    break

            # Nếu chưa có rating của người dùng cho product thì tạo mới
            if rating_of_user is None:
                saved_rating = Rating.objects.create(account_id=account_id, product_id=product_id,
                                                     star_num=rating_from_request["star_num"],
                                                     comment=rating_from_request["comment"])
                serialized_rating = self.get_serializer(saved_rating)
                return Response(data={"message": "You have rated successfully!",
                                      "rating": serialized_rating.data},
                                status=status.HTTP_200_OK
                                )
            else:  # Nếu không thì update
                rating_of_user.star_num = rating_from_request["star_num"]
                rating_of_user.comment = rating_from_request["comment"]
                rating_of_user.save()
                serialized_rating = self.get_serializer(rating_of_user)
                return Response(data={"message": "Your rating has been updated successfully!",
                                      "rating": serialized_rating.data},
                                status=status.HTTP_200_OK
                                )

    @action(methods=["get"], detail=False, url_path="average-star", url_name="average-star")
    def average_star(self, request):
        product_id = self.request.query_params.get("product_id")
        list_rating_of_product = Rating.objects.filter(product_id=product_id)
        total_star = 0
        one_star = 0
        two_star = 0
        three_star = 0
        four_star = 0
        five_star = 0
        for p in list_rating_of_product:
            star_num_of_product = p.star_num
            total_star += star_num_of_product
            match star_num_of_product:
                case 1:
                    one_star += 1
                case 2:
                    two_star += 1
                case 3:
                    three_star += 1
                case 4:
                    four_star += 1
                case 5:
                    five_star += 1
                case _:
                    pass

        number_of_ratings = len(list_rating_of_product)
        average_star = float(total_star) / float(number_of_ratings) if number_of_ratings != 0 else 0
        one_star_rate = one_star / number_of_ratings * 100 if number_of_ratings != 0 else 0
        two_star_rate = two_star / number_of_ratings * 100 if number_of_ratings != 0 else 0
        three_star_rate = three_star / number_of_ratings * 100 if number_of_ratings != 0 else 0
        four_star_rate = four_star / number_of_ratings * 100 if number_of_ratings != 0 else 0
        five_star_rate = five_star / number_of_ratings * 100 if number_of_ratings != 0 else 0

        return Response(data={"number_of_ratings": number_of_ratings,
                              "average_star": round(average_star, 1),
                              "one_star_rate": round(one_star_rate, 2),
                              "two_star_rate": round(two_star_rate, 2),
                              "three_star_rate": round(three_star_rate,2),
                              "four_star_rate": round(four_star_rate,2),
                              "five_star_rate": round(five_star_rate, 2)}
                        , status=status.HTTP_200_OK)
