from django.test import TestCase

from restcalls.core.serializers import CallRecordSerializer
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



