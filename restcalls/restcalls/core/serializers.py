from rest_framework import serializers

from restcalls.core.models import CallRecord


class CallRecordSerializer(serializers.ModelSerializer):
    source_number = serializers.IntegerField(source='source', required=False)
    destination_number = serializers.IntegerField(source='destination', required=False)
    timestamp = serializers.DateTimeField(write_only=True)

    class Meta:
        model = CallRecord
        fields = ('call_id', 'source_number', 'destination_number', 'type')

    def validate(self, data):
        if data['type'] == 'start':
            if not data.get('source') or not data.get('destination'):
                raise serializers.ValidationError(
                    "Source and Destinations are reuired for CallRecords with type 'start'")

        return data

    def create(self, validated_data):
        pass
