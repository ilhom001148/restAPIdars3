from django.core.serializers import serialize
from django.shortcuts import render
from django.template.defaultfilters import title
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Car
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework import status
from .serializers import CarSerializer
from django.db.models import Q



class CarListView(GenericAPIView):
    serializer_class = CarSerializer
    queryset = Car.objects.all()

    def get(self, request):
        search = self.request.query_params.get('search', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)

        car = self.get_queryset()

        if search:
            car = car.filter(title__icontains=search)

        if min_price:
            car = car.filter(price__gte=min_price)

        if max_price:
            car = car.filter(price__lte=max_price)


        if not car.exists():
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Mashina topilmadi',
            }, status=status.HTTP_404_NOT_FOUND)


        serializer = self.get_serializer(car, many=True)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Car list',
            'data': serializer.data
        }, status=status.HTTP_200_OK)



class CarCreateView(GenericAPIView):
    serializer_class = CarSerializer
    queryset =Car.objects.all()

    def post(self,request):
        serializer=self .get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data={
                'status':status.HTTP_201_CREATED,
                'message':'Car yaratildi',
                'data':serializer.data
            }
            return Response(data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class CarDetailView(GenericAPIView):
    serializer_class = CarSerializer
    queryset = Car.objects.all()

    def get(self,request,pk):
        car=get_object_or_404(Car,pk=pk)
        serializer = self.get_serializer(car)


        data={
            'status':status.HTTP_200_OK,
            'message':'Car detail',
            'data':serializer.data
        }
        return Response(data)


class CarUpdateView(GenericAPIView):
    serializer_class = CarSerializer
    queryset = Car.objects.all()

    def put(self,request,pk):
        car=Car.objects.filter(pk=pk).first()
        serializer=self.get_serializer(car)
        if not car:
            data={
                'status':status.HTTP_404_NOT_FOUND,
                'message':'Car topilmadi',
            }
        serializer=self.get_serializer(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data={
                'status':status.HTTP_200_OK,
                'message':'Car yangilandi',
                'data':serializer.data
            }
            return Response(data)
        return Response({
            'status':status.HTTP_400_BAD_REQUEST,
            'message':'Validatsiya xatosi',
            'errors':serializer.errors
        })


    def patch(self,request,pk):
        car=Car.objects.filter(pk=pk).first()
        serializer=self.get_serializer(car)
        if not car:
            data={
                'status':status.HTTP_404_NOT_FOUND,
                'message':'Car topilmadi'
            }
        serializer=self.get_serializer(car,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            data={
                'status':status.HTTP_200_OK,
                'message':'Car qisman yangilandi',
                'data':serializer.data
            }
            return Response(data)
        return Response({
            'status':status.HTTP_400_BAD_REQUEST,
            'message':'Validatsiya xatosi',
            'errors':serializer.errors
        })


class CarDeleteView(GenericAPIView):
    serializer_class = CarSerializer
    queryset=Car.objects.all()

    def delete(self,request,pk):
        car = Car.objects.filter(pk=pk).first()
        if not car:
            return Response(data={
                'status':status.HTTP_404_NOT_FOUND,
                'message':'Car topilmadi',
            })
        car.delete()
        return Response(data={
            'status':status.HTTP_200_OK,
            'message':'Car ochirildi',
        })



