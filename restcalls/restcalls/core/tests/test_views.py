import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from restcalls.core.models import CallRecord
from restcalls.core.tests.payloads import *


class StartCallRecord(APITestCase):

    def tearDown(self):
        self.client.logout()

    def test_get_201_status_code_when_valid_start_call_record_is_sent(self):
        '''
        '''
        response = self.client.post(reverse('post_record_call'),
                                    data=json.dumps(VALID_START_CALL_PAYLOAD),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_start_record_call_is_persisted_for_valid_payload(self):
        response = self.client.post(reverse('post_record_call'),
                                    data=json.dumps(VALID_START_CALL_PAYLOAD),
                                    content_type='application/json'
                                    )
        call_record = CallRecord.objects.get(call_id=VALID_START_CALL_PAYLOAD['call_id'])
        self.assertIsNotNone(call_record)

    def test_get_201_status_code_when_valid_end_call_record_is_sent(self):
        '''
        '''
        response = self.client.post(reverse('post_record_call'),
                                    data=json.dumps(VALID_END_CALL_PAYLOAD),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_400_code_when_invalid_record_is_sent(self):
        response = self.client.post(reverse('post_record_call'),
                                    data=json.dumps({}),
                                    content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_error_400_and_list_required_fields_when_empty_record_is_sent(self):
        response = self.client.post(reverse('post_record_call'),
                                    data=json.dumps({}),
                                    content_type="application/json")
        fields = ['type', 'timestamp', 'call_id']
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        for field in fields:
            self.assertIn(field, response.json())

    def test_get_error_400_and_list_source_field_when_its_not_present_in_start_call_payload(self):
        response = self.client.post(reverse('post_record_call'),
                                    data=json.dumps(START_CALL_PAYLOAD_WITHOUT_SOURCE_ATTRIBUTE),
                                    content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('source', response.json())

    def test_get_error_400_and_list_destination_field_when_its_not_present_in_start_call_payload(self):
        response = self.client.post(reverse('post_record_call'),
                                    data=json.dumps(START_CALL_PAYLOAD_WITHOUT_DESTINATION_ATTRIBUTE),
                                    content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('destination', response.json())

    def test_get_error_400_and_list_destination_and_source_fields_when_its_not_present_in_start_call_payload(self):
        response = self.client.post(reverse('post_record_call'),
                                    data=json.dumps(START_CALL_PAYLOAD_WITHOUT_DESTINATION_AND_SOURCE_ATTRIBUTE),
                                    content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('destination', response.json())
        self.assertIn('source', response.json())
