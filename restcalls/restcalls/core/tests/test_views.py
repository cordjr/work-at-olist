import json
from datetime import datetime
from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from restcalls.core.models import CallRecord
from restcalls.core.tests.payloads import *


class RecordCallViewTest(APITestCase):

    def tearDown(self):
        self.client.logout()

    def test_get_201_status_code_when_valid_start_call_record_is_sent(self):
        '''        '''
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
        self.assertIsNotNone(call_record.start_time)
        self.assertIsNotNone(call_record)

    def test_get_201_status_code_when_valid_end_call_record_is_sent(self):
        '''
        '''
        response = self.client.post(reverse('post_record_call'),
                                    data=json.dumps(VALID_END_CALL_PAYLOAD),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_call_price_must_be_filled_when_record_call_is_filled_with_start_and_end_fields(self):
        self.client.post(reverse('post_record_call'),
                         data=json.dumps(VALID_START_CALL_PAYLOAD),
                         content_type='application/json'
                         )
        self.client.post(reverse('post_record_call'),
                         data=json.dumps(VALID_END_CALL_PAYLOAD),
                         content_type='application/json'
                         )

        call_record = CallRecord.objects.get(call_id=VALID_START_CALL_PAYLOAD['call_id'])
        self.assertIsNotNone(call_record)
        self.assertIsNotNone(call_record.call_price)

    def test_end_record_call_is_persisted_for_valid_payload(self):
        response = self.client.post(reverse('post_record_call'),
                                    data=json.dumps(VALID_END_CALL_PAYLOAD),
                                    content_type='application/json'
                                    )
        call_record = CallRecord.objects.get(call_id=VALID_END_CALL_PAYLOAD['call_id'])
        self.assertIsNotNone(call_record.end_time)
        self.assertIsNotNone(call_record)

    def test_get_400_code_when_empty_record_is_sent(self):
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


class BillViewTest(APITestCase):

    def tearDown(self):
        self.client.logout()

    def load_data(self):
        call_list = [
            CallRecord(call_id=70, start_time=datetime.strptime("2016-02-29T12:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
                       end_time=datetime.strptime("2016-02-29T14:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
                       source_number=99988526423, destination_number=99988526423, call_price=Decimal('0.23')),
            CallRecord(call_id=71, start_time=datetime.strptime("2017-12-12T15:07:13Z", "%Y-%m-%dT%H:%M:%SZ"),
                       end_time=datetime.strptime("2017-12-12T15:14:56Z", "%Y-%m-%dT%H:%M:%SZ"),
                       source_number=99988526423, destination_number=99988526423, call_price=Decimal('0.23')),
            CallRecord(call_id=72, start_time=datetime.strptime("2017-12-12T22:47:56Z", "%Y-%m-%dT%H:%M:%SZ"),
                       end_time=datetime.strptime("2017-12-12T22:50:56Z", "%Y-%m-%dT%H:%M:%SZ"),
                       source_number=99988526423, destination_number=99988526423, call_price=Decimal('0.23')),
            CallRecord(call_id=73, start_time=datetime.strptime("2017-12-12T21:57:13Z", "%Y-%m-%dT%H:%M:%SZ"),
                       end_time=datetime.strptime("2017-12-12T22:10:56Z", "%Y-%m-%dT%H:%M:%SZ"),
                       source_number=99988526423, destination_number=99988526423, call_price=Decimal('0.23')),
            CallRecord(call_id=74, start_time=datetime.strptime("2017-12-12T04:57:13Z", "%Y-%m-%dT%H:%M:%SZ"),
                       end_time=datetime.strptime("2017-12-12T06:10:56Z", "%Y-%m-%dT%H:%M:%SZ"),
                       source_number=99988526423, destination_number=99988526423, call_price=Decimal('0.23')),
            CallRecord(call_id=75, start_time=datetime.strptime("2017-12-12T21:57:13Z", "%Y-%m-%dT%H:%M:%SZ"),
                       end_time=datetime.strptime("2017-12-13T22:10:56Z", "%Y-%m-%dT%H:%M:%SZ"),
                       source_number=99988526423, destination_number=99988526423, call_price=Decimal('0.23')),
            CallRecord(call_id=76, start_time=datetime.strptime("2017-12-12T15:07:58Z", "%Y-%m-%dT%H:%M:%SZ"),
                       end_time=datetime.strptime("2017-12-12T15:12:56Z", "%Y-%m-%dT%H:%M:%SZ"),
                       source_number=99988526423, destination_number=99988526423, call_price=Decimal('0.23')),
            CallRecord(call_id=77, start_time=datetime.strptime("2018-02-28T21:57:13Z", "%Y-%m-%dT%H:%M:%SZ"),
                       end_time=datetime.strptime("2018-03-01T22:10:56Z", "%Y-%m-%dT%H:%M:%SZ"),
                       source_number=99988526423, destination_number=99988526423, call_price=Decimal('0.23'))]
        CallRecord.objects.bulk_create(call_list)

    def test_should_return_for_6_records_mont_12_and_year_2017(self):
        self.load_data()
        path = reverse('get_bill', kwargs={'number': 99988526423, 'month': 12, 'year': 2017})

        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 6)

    def test_should_return_1_record(self):
        self.load_data()
        path = reverse('get_bill', kwargs={'number': 99988526423})

        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_should_return_404_error_when_passing_incomplete_path(self):
        self.load_data()
        path = reverse('get_bill', kwargs={'number': 99988526423})
        path += "20-"
        response = self.client.get(path)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
