from datetime import datetime, timedelta, date

from django.core.exceptions import ValidationError
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

    def create_a_record_call_without_call_id(self):
        sample_date = datetime.now()
        start_time = sample_date - timedelta(minutes=2)
        end_time = sample_date
        return CallRecord.objects.create(source_number=559821344448,
                                         call_id=None,
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

    def test_should_throw_an_errror_when_call_id_is_not_filled(self):
        try:
            record = self.create_a_record_call_without_call_id()
            record.clean_fields()
        except Exception as ex:
            print(ex)
            self.assertIsNotNone(ex)
            return
        self.fail("An exception shuld be thrown")

    def test_should_throw_validation_erros_when_start_time_is_after_end_date(self):
        record = self.create_valid_record_call()
        record.start_time = datetime.now() + timedelta(minutes=20)
        try:
            record.full_clean()
        except ValidationError as ex:
            self.assertIsNotNone(ex)
            return

        self.fail("a validation error should be thrown")

    def test_total_price_should_be_calculated_precisely(self):
        record = self.create_valid_record_call()
        self.assertEqual(record.total_price, 0.18)

    def test_total_minutes_should_be_calculated_precisely(self):
        record = self.create_valid_record_call()
        self.assertEqual(record.total_minutes, 2)


class PricePoliceTest(TestCase):
    def create_police_test(self):
        sample_date = date.today()
        start_date = sample_date - timedelta(days=60)
        end_date = sample_date
        price_police = PricePolice.objects.create(start=start_date,
                                                  end=end_date)
        return price_police

    def test_police_insertion_with_valid_data(self):
        price_police = self.create_police_test()
        self.assertIsNotNone(price_police.id)

    def test_should_throw_validation_erros_when_start_time_is_after_end_date(self):
        poclicy = self.create_police_test()
        poclicy.start = date.today() + timedelta(days=20)
        try:
            poclicy.full_clean()
        except ValidationError as ex:
            self.assertIsNotNone(ex)
            return

        self.fail("a validation error should be throw")
