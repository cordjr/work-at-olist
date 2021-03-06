# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework.response import Response

from restcalls.core.models import CallRecord, PricePolicy
from restcalls.core.serializers import CallRecordSerializer, BillSerializer, PricePolicySerilizer


@swagger_auto_schema(method='post',
                     operation_id='post call',
                     operation_description="Create or fill call records according to type",
                     request_body=CallRecordSerializer,
                     responses={200: '', 400: ''})
@api_view(['POST'])
def post_record_call(request):
    '''
    post:
      ##create or fill a record call

    '''
    serializer = CallRecordSerializer(data=request.data)

    if serializer.is_valid():
        call_id = serializer.data['call_id']
        data = serializer.validated_data
        call_record = CallRecord.objects.filter(call_id=data['call_id']).first()
        if data['type'] == 'start':
            if not call_record:
                call_record = CallRecord.objects.create(call_id=call_id,
                                                        start_time=data['timestamp'],
                                                        source_number=data['source'],
                                                        destination_number=data['destination'])
            else:
                call_record.start_time = data['timestamp']
                call_record.source_number = data['source']
                call_record.destination_number = data['destination']
                call_record.save()

        else:

            if not call_record:
                call_record = CallRecord.objects.create(call_id=call_id,
                                                        end_time=data['timestamp']
                                                        )
            else:
                call_record.end_time = data['timestamp']
                call_record.save()

        if call_record.start_time and call_record.end_time:
            price_policy = PricePolicy.objects.filter(start__lte=call_record.start_time).filter(
                end__gte=call_record.end_time).first()
            if not price_policy:
                price_policy = PricePolicy.objects.latest('end')
            price = price_policy.calculate_price(call_record.start_time, call_record.end_time)
            call_record.call_price = price
            call_record.save()

        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get',
                     operation_id='get_bill',
                     operation_description="Retrieve bills according to month and year parameters",

                     responses={200: BillSerializer, 400: ''},
                     )
@api_view(['GET'])
def get_bill(request, number, month=None, year=None):
    query = CallRecord.objects.filter(source_number=number)
    if not _month_and_year_is_valid(month, year):
        return Response("Month nad year shuld be both blank or both filled", status=status.HTTP_400_BAD_REQUEST)
    if month and year:
        query = query.filter(start_time__month=month, start_time__year=year)
    else:
        result = CallRecord.objects.values('start_time').latest(field_name='start_time')
        if result:
            last_date = result['start_time']
        query = query.filter(start_time__month=last_date.month, start_time__year=last_date.year)

    serializer = BillSerializer(query.all(), many=True)
    return Response(serializer.data)


def _month_and_year_is_valid(month, year):
    return bool(month) == bool(year)


class PricePolicyView(ListCreateAPIView, UpdateAPIView):
    queryset = PricePolicy.objects.last()
    serializer_class = PricePolicySerilizer
