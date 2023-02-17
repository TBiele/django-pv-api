from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Yield

from .serializers import YieldSerializer


class YieldViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows specific yields (by post code) to be viewed.
    """

    http_method_names = ["get"]
    queryset = Yield.objects.all()
    serializer_class = YieldSerializer


@api_view(["GET"])
def get_pv_yield(request):
    """
    For a given post code, return the specific yield, multiplying with capacity, if it is given in the request.
    """
    plz = request.GET.get("plz")
    capacity = request.GET.get("capacity")
    try:
        yield_obj = Yield.objects.get(plz__startswith=plz[:2])
        specific_yield = yield_obj.pv_yield
        total_yield = (
            specific_yield if not capacity else specific_yield * float(capacity)
        )
        data = {"plz": plz, "pv_yield": total_yield}
        return Response(data)
    except Yield.DoesNotExist:
        return Response({"error": f"Yield for PLZ {plz} not found"})
