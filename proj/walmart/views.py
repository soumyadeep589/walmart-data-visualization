from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from walmart.models import Product
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
import json
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

    
class SearchView(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("search")
        products = Product.objects.filter(name__icontains=kw).values().distinct()[:10]
        res = []
        for product in products:
            same_name_products = Product.objects.filter(name=product["name"]).values()
            dates = [elem["created_on"].date().strftime('%d-%m-%y') for elem in same_name_products]
            prices = [float(elem["display_price"]) for elem in same_name_products]
            data = {
                    "name": product["name"],
                    "dates": dates,
                    "prices": prices,
            }
            res.append(data)

        context["results"] = res
        return context