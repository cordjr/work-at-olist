# Create your views here.

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from restcalls.core.models import CallRecord, PricePolicy
from restcalls.core.serializers import CallRecordSerializer


@api_view(['POST'])
def post_record_call(request):
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


@api_view(['GET'])
def get_bill(request, number, month=None, year=None):

    return Response(status= status.HTTP_200_OK)
