import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse


class StartCallRecord(TestCase):

    def setUp(self):
        self.cli = Client()

    def valid_payload(self):
        return {
            "id":  456,
            "type":  "start"
            "timestamp":  "2017-06-06T10:11:02.900Z"
            "call_id":  999
            "source":  5598984182608
            "destination":  559999874562
        }

    def invalid_payload(self):
        return {
            "id":  455,
            "type":  ""
            "timestamp":  "2017-06-06T10:11:02.900Z"
            "call_id":  999
            "source":  5598984182608
            "destination":  559999874562
        }

    def test_shoud_get_201_status_code_when_valid_start_call_record_is_sent(self):
        response = self.cli.post(reverse('post_record_call'),
                                 data=json.dump(self.valid_payload()),
                                 content_type="application/json")
        self.assertEqual(resonse.status, status.HTTP_201_CREATED)

    def test_shoud_receive_valtest_shoud_get_400_code_when_invalid_record_is_sent(self):
        response = self.cli.post(reverse('post_record_call'),
                                 data=json.dump(self.invalid_payload()),
                                 content_type="application/json")
        self.assertEqual(resonse.status, status.HTTP_400_BAD_REQUEST)
