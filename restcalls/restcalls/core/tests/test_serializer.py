from datetime import datetime, timedelta
from decimal import Decimal

from django.test import TestCase

from restcalls.core.models import CallRecord
from restcalls.core.serializers import CallRecordSerializer, BillSerializer, PricePolicySerilizer
from restcalls.core.tests.payloads import *


class CallRecordSerializerTest(TestCase):

    def test_should_have_not_validation_errors_for_valid_start_call_payload(self):
        serializer = CallRecordSerializer(data=VALID_START_CALL_PAYLOAD)

        self.assertTrue(serializer.is_valid(raise_exception=True))
        self.assertTrue(len(serializer.errors) == 0)

    def test_should_have_not_validation_errors_for_valid_end_call_payload(self):
        serializer = CallRecordSerializer(data=VALID_END_CALL_PAYLOAD)

        self.assertTrue(serializer.is_valid(raise_exception=True))
        self.assertTrue(len(serializer.errors) == 0)

    def test_should_have_validation_error_when_start_call_has_not_source_attribute(self):
        serializer = CallRecordSerializer(data=START_CALL_PAYLOAD_WITHOUT_SOURCE_ATTRIBUTE)

        self.assertFalse(serializer.is_valid())
        self.assertTrue([error for error in serializer.errors if 'source' in error])

    def test_should_have_validation_error_when_start_call_has_not_destination_attribute(self):
        serializer = CallRecordSerializer(data=START_CALL_PAYLOAD_WITHOUT_DESTINATION_ATTRIBUTE)
        self.assertFalse(serializer.is_valid())
        self.assertTrue([error for error in serializer.errors if 'destination' in error])

    def test_should_have_validation_error_when_start_call_source_has_none_value(self):
        serializer = CallRecordSerializer(data=START_CALL_PAYLOAD_WITH_NONE_SOURCE)

        self.assertFalse(serializer.is_valid())
        self.assertTrue([error for error in serializer.errors if 'source' in error])

    def test_should_have_validation_error_when_start_call_has_destination_with_none_value(self):
        serializer = CallRecordSerializer(data=START_CALL_PAYLOAD_WITH_NONE_DESTINATION)

        self.assertFalse(serializer.is_valid())
        self.assertTrue([error for error in serializer.errors if 'destination' in error])

    def test_should_have_valdation_error_when_end_call_has_timestamp_with_none_value(self):
        serializer = CallRecordSerializer(data=END_CALL_PAYLOAD_WITH_NONE_TITMESTAMP)

        self.assertFalse(serializer.is_valid())
        self.assertTrue([error for error in serializer.errors if 'timestamp' in error])


class BillSerializerTest(TestCase):

    def test_should_serialize_call_record_according_to_bill_pattern(self):
        call_record = CallRecord()
        sample_date = datetime.now()
        call_record.start_time = sample_date - timedelta(seconds=60 * 5.5)
        call_record.end_time = sample_date
        call_record.source_number = 99987456895
        call_record.destination_number = 99987456894
        call_record.call_price = Decimal('0.68')
        serializer = BillSerializer(call_record)
        data = serializer.data
        self.assertIsNotNone(data)
        for key in ('call_start_time', 'call_start_date', 'destination', 'call_duration', 'call_price'):
            self.assertIn(key, data.keys())

        self.assertRegex(data['call_duration'], r'\d+h\d+m\d+s', "call duration should be like '0h2m1s'")


class PricePolicySerializerTest(TestCase):

    def test_should_serialize_to_price_policy_when_payload_is_valid(self):
        serializer = PricePolicySerilizer(data=VALID_PRICE_POLICY_PAYLOAD)
        self.assertTrue(serializer.is_valid(raise_exception=True))
