from rest_framework import serializers


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
