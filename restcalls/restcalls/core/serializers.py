from rest_framework import serializers

from restcalls.core.models import CallRecord, PricePolicy, PriceRule


class CallRecordSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    call_id = serializers.IntegerField(help_text=' Call identification')
    source = serializers.IntegerField(required=False,
                                      help_text='number thet start a call. required only if type is start')
    destination = serializers.IntegerField(required=False,
                                           help_text='number that receive a call.  required only if type is start')
    timestamp = serializers.DateTimeField(required=True)
    type = serializers.ChoiceField(choices=('end', 'start'), required=True)

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
    class Meta:
        model = CallRecord
        fields = ('destination', 'call_start_date', 'call_start_time', 'call_duration', 'call_price')

    destination = serializers.IntegerField(source="destination_number")
    call_start_date = serializers.SerializerMethodField(help_text="start date in format 'dd/MM/YYYY'")
    call_start_time = serializers.SerializerMethodField(help_text=" start time in format 'HH:MM'")
    call_duration = serializers.SerializerMethodField(
        help_text="call duration (hour, minute and seconds): e.g. 0h35m42s")
    call_price = serializers.DecimalField(decimal_places=2, max_digits=20)

    def get_call_start_date(self, obj):
        return obj.start_time.date()

    def get_call_start_time(self, obj):
        return obj.start_time.time()

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


class PriceRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceRule
        fields = ('start_time', 'end_time', 'value', 'type')


class PricePolicySerilizer(serializers.ModelSerializer):
    rules = PriceRuleSerializer(many=True)

    class Meta:
        model = PricePolicy
        fields = ('start', 'end', 'standing_rate', 'rules')

    def create(self, validated_data):
        rules = validated_data.pop('rules')
        policy = PricePolicy.objects.create(**validated_data)
        for rule in rules:
            price_rule = PriceRule.objects.create(**rule)
            price_rule.policy = policy

    def update(self, instance, validated_data):
        rules = validated_data.pop('rules')
        policy = PricePolicy.objects.filter(id=validated_data['id']).first()
        for rule_dict in rules:
            price_rule = PriceRule(**rule_dict)
            price_rule.save()
