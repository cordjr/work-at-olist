from rest_framework import serializers

from restcalls.core.models import CallRecord


class CallRecordSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    call_id = serializers.IntegerField()
    source = serializers.IntegerField(required=False)
    destination = serializers.IntegerField(required=False)
    timestamp = serializers.DateTimeField(required=True)
    type = serializers.CharField(required=True)

    def validate(self, data):
        errors = {}
        if data['type'] == 'start':
            if 'source' not in data:
                errors['source'] = 'source should be present in start call record'

            if 'destination' not in data:
                errors['destination'] = 'destination should be present in start call record'

            if not data.get('source'):
                errors['source'] = 'source must contains values in start call record'

            if not data.get('destination'):
                errors['destination'] = 'destination must contains values in start call record'

        if errors:
            raise serializers.ValidationError(
                errors)

        return data


class BillSerializer(serializers.ModelSerializer):
    destination = serializers.SerializerMethodField()
    call_start_date = serializers.SerializerMethodField()
    call_start_time = serializers.SerializerMethodField()
    call_duration = serializers.SerializerMethodField()
    call_price = serializers.SerializerMethodField()

    def get_call_start_date(self, obj):
        return obj.start_time.date()

    def get_call_start_time(self, obj):
        return obj.start_time.time()

    def get_destination(self, obj):
        return obj.destination_number

    def get_call_duration(self, obj):

        total_seconds = obj.time_delta.seconds
        if not total_seconds:
            return "0h0m0s"

        periods = [
            ('h', 60 * 60),
            ('m', 60),
            ('s', 1)
        ]
        strings = []
        for period_name, period_seconds in periods:
            if total_seconds >= period_seconds:
                period_value, total_seconds = divmod(total_seconds, period_seconds)
                strings.append("{}{}".format(period_value, period_name))
            else:
                strings.append("{}{}".format(0, period_name))
        return "".join(strings)

    def get_call_price(self, obj):
        return obj.call_price

    class Meta:
        model = CallRecord
        fields = ('call_start_time', 'call_start_date', 'destination', 'call_duration', 'call_price')
