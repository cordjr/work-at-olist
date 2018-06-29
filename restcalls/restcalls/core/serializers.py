from rest_framework import serializers


class CallRecordSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    call_id = serializers.IntegerField()
    source = serializers.IntegerField(required=False)
    destination = serializers.IntegerField(required=False)
    timestamp = serializers.DateTimeField(required=True)
    type = serializers.CharField(required=True)

    def validate(self, data):
        if data['type'] == 'start':
            if 'source' not in data:
                raise serializers.ValidationError({'source': 'source should be present in start call record'})

            if 'destination' not in data:
                raise serializers.ValidationError({'destination': 'destination should be present in start call record'})

            if not data.get('source'):
                raise serializers.ValidationError({'source': 'source must contains values in start call record'})

            if not data.get('destination'):
                raise serializers.ValidationError(
                    {'destination': 'destination must contains values in start call record'})

        return data
