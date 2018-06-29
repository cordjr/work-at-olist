# Create your views here.

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from restcalls.core.models import CallRecord
from restcalls.core.serializers import CallRecordSerializer


@api_view(['POST'])
def post_record_call(request):
    serializer = CallRecordSerializer(data=request.data)
    if serializer.is_valid():
        call_id = serializer.data['call_id']
        data = serializer.data
        call_record = CallRecord.objects.filter(call_id=call_id)
        if not call_record:

            if data['type'] == 'start':
                CallRecord.objects.create(call_id=call_id,
                                          start_time=data['timestamp'],
                                          source_number=data['source'],
                                          destination_number=data['destination'])

        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
