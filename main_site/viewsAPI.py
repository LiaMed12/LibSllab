from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SpecifSerializers
from .models import specifications


@api_view(['GET'])
def show_all_Specifit(request):
    specif = specifications.objects.all()
    serial = SpecifSerializers(specif, many=True)
    return Response(serial.data)

@api_view(['GET'])
def showSpecifit(request, pk):
    specif = specifications.objects.filter(pk=pk)
    if not specif:
        return HttpResponseBadRequest("There is no such specification.")
    else:
        serial = SpecifSerializers(specif, many=True)
        return Response(serial.data)


@api_view(['POST'])
def addSpecifit(request):
    serial = SpecifSerializers(data=request.data)
    if serial.is_valid():
        for_string_outline=serial.save()
        return HttpResponse("Added a new specification[{}]".
                            format(for_string_outline ))
    else:
        return HttpResponseServerError()


@api_view(['DELETE'])
def deleteSpecifit(request, pk):
    specif = specifications.objects.filter(pk=pk)
    if specif:
        specif.delete()
        return HttpResponse("Specification removed")
    else:
        return HttpResponseServerError()
