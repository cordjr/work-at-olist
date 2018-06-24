from datetime import datetime, timedelta, date

from django.test import TestCase

from restcalls.core.models import CallRecord, PricePolice


# Create your tests here.
class CallRecordTest(TestCase):

    def create_valid_record_call(self):
        sample_date = datetime.now()
        start_time = sample_date - timedelta(minutes=2)
        end_time = sample_date
        return CallRecord.objects.create(source_number=559821344448,
                                         call_id=55,
                                         destination_number=1334455664,
                                         start_time=start_time,
                                         end_time=end_time,
                                         minute_price=0.09
                                         )

    def test_record_insertion_with_valid_data(self):
        record = self.create_valid_record_call()
        self.assertTrue(record.call_id)
        record_retrieved = CallRecord.objects.get(call_id=record.call_id)
        self.assertEqual(record, record_retrieved, "Record retrieved must be equals to record created")

    def test_total_price_should_be_calculated_precisely(self):
        record = self.create_valid_record_call()
        self.assertEqual(record.total_price, 0.18)

    def test_total_minutes_should_be_calculated_precisely(self):
        record = self.create_valid_record_call()
        self.assertEqual(record.total_minutes, 2)


class PricePoliceTest(TestCase):

    def test_police_insertion_with_valid_data(self):
        sample_date = date.today()
        start_date = sample_date - timedelta(days=60)
        end_date = sample_date
        price_police = PricePolice.objects.create(start=start_date,
                                                  end=end_date)
        self.assertIsNotNone(price_police.id)
