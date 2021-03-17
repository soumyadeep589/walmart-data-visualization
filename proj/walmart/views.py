from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from walmart.models import Product
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


@csrf_exempt
def index(request):
    return render(request, 'index.html')



class ChartData(APIView):

    def get(self, request, format=None):
        products = Product.objects.filter(product_id=489882644).values()
        name=products[0]["name"]
        dates = [elem["created_on"].date() for elem in products]
        prices = [elem["display_price"] for elem in products]
        data = {
                "name": name,
                "dates": dates,
                "prices": prices,
        }
        return Response(data)

    