from datetime import datetime
from datetime import timedelta, date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from restcalls.core.models import CallRecord, PricePolicy, PriceRule


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

                                         )

    def test_record_insertion_with_valid_data(self):
        record = self.create_valid_record_call()
        self.assertTrue(record.call_id)
        record_retrieved = CallRecord.objects.get(call_id=record.call_id)
        self.assertEqual(record, record_retrieved,
                         "Record retrieved must be equals to record created")

    def test_should_throw_an_errror_when_call_id_is_not_filled(self):
        try:
            record = self.create_a_record_call_without_call_id()
            record.clean_fields()
        except ValidationError as ex:
            self.assertIn("call_id", ex.error_dict)

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

    def test_total_minutes_should_be_calculated_precisely(self):
        record = self.create_valid_record_call()
        self.assertEqual(record.total_minutes, 2)


class PricePolicyTest(TestCase):
    def create_policy_test(self):
        sample_date = date.today()
        start_date = sample_date - timedelta(days=60)
        end_date = sample_date
        price_police = PricePolicy.objects.create(start=start_date,
                                                  end=end_date,
                                                  standing_rate=Decimal(0.16))

        return price_police

    def test_police_insertion_with_valid_data(self):
        price_police = self.create_policy_test()
        self.assertIsNotNone(price_police.id)

    def price_policy_with_rules(self):
        policy = PricePolicy.objects.create(standing_rate=Decimal('0.18'),
                                            start=datetime.strptime("2018-05-01", "%Y-%m-%d"),
                                            end=datetime.strptime("2018-09-01", "%Y-%m-%d"))
        PriceRule.objects.create(policy=policy,
                                 start_time=datetime.strptime("06:00", "%H:%M"),
                                 end_time=datetime.strptime("22:00", "%H:%M"),
                                 value=Decimal('0.09'),
                                 type='S')
        PriceRule.objects.create(policy=policy,
                                 start_time=datetime.strptime("22:0", "%H:%M"),
                                 end_time=datetime.strptime("06:00", "%H:%M"),
                                 value=Decimal('0.04'),
                                 type='R')
        return policy

    def test_calculate_price_when_start_and_end_is_only_in_standard_price_rule(self):
        policy = self.price_policy_with_rules()
        start = datetime.strptime('2018-06-01 18:00:00', '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime('2018-06-01 18:15:00', '%Y-%m-%d %H:%M:%S')
        price = policy.calculate_price(start, end)
        self.assertEqual(price, Decimal('1.53'))

    def test_calculate_call_price_when_start_and_end_is_between_2_price_rules(self):
        policy = self.price_policy_with_rules()

        start = datetime.strptime('2018-06-01 21:59:00', '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime('2018-06-01 22:05:00', '%Y-%m-%d %H:%M:%S')

        price = policy.calculate_price(start, end)
        self.assertEqual(price, Decimal('0.47'))


class PriceRuleTest(TestCase):

    def test_rule_insertion_with_valid_data(self):
        policy = PricePolicy.objects.create(standing_rate=Decimal('0.18'),
                                            start=datetime.strptime("2018-05-01", "%Y-%m-%d"),
                                            end=datetime.strptime("2018-09-01", "%Y-%m-%d"))
        rule = PriceRule.objects.create(policy=policy,
                                        start_time=datetime.strptime("06:00", "%H:%M"),
                                        end_time=datetime.strptime("22:00", "%H:%M"),
                                        value=Decimal('0.09'),
                                        type='S')

        self.assertIsNotNone(rule.id)

    def test_rule_insertion_with_no_policy(self):
        try:
            rule = PriceRule.objects.create(policy=None,
                                            start_time=datetime.strptime("06:00", "%H:%M"),
                                            end_time=datetime.strptime("22:00", "%H:%M"),
                                            value=Decimal('0.09'),
                                            type='S')
        except ValidationError as ex:
            self.assertIn('policy', ex.error_dict)
            return
        self.fail('A validation error shuld be thrown')

    def test_rule_insertion_with_no_start_time(self):
        try:
            policy = PricePolicy.objects.create(standing_rate=Decimal('0.18'),
                                                start=datetime.strptime("2018-05-01", "%Y-%m-%d"),
                                                end=datetime.strptime("2018-09-01", "%Y-%m-%d"))
            PriceRule.objects.create(policy=policy,
                                     start_time=None,
                                     end_time=datetime.strptime("22:00", "%H:%M"),
                                     value=Decimal('0.09'),
                                     type='S')
        except ValidationError as ex:
            self.assertIn('start_time', ex.error_dict)
            return

        self.fail('A validation error shuld be thrown')

    def test_rule_insertion_with_no_end_time(self):
        try:
            policy = PricePolicy.objects.create(standing_rate=Decimal('0.18'),
                                                start=datetime.strptime("2018-05-01", "%Y-%m-%d"),
                                                end=datetime.strptime("2018-09-01", "%Y-%m-%d"))
            PriceRule.objects.create(policy=policy,
                                     start_time=datetime.strptime("06:00", "%H:%M"),
                                     end_time=None,
                                     value=Decimal('0.09'),
                                     type='S')
        except ValidationError as ex:
            self.assertIn('end_time', ex.error_dict)
            return

        self.fail('A validation error shuld be thrown')

    def test_rule_insertion_with_no_value(self):
        try:
            policy = PricePolicy.objects.create(standing_rate=Decimal('0.18'),
                                                start=datetime.strptime("2018-05-01", "%Y-%m-%d"),
                                                end=datetime.strptime("2018-09-01", "%Y-%m-%d"))
            PriceRule.objects.create(policy=policy,
                                     start_time=datetime.strptime("06:00", "%H:%M"),
                                     end_time=datetime.strptime("22:00", "%H:%M"),
                                     value=None,
                                     type='S')
        except ValidationError as ex:
            self.assertIn('value', ex.error_dict)
            return

        self.fail('A validation error shuld be thrown')

    def test_rule_insertion_with_no_type(self):
        try:
            policy = PricePolicy.objects.create(standing_rate=Decimal('0.18'),
                                                start=datetime.strptime("2018-05-01", "%Y-%m-%d"),
                                                end=datetime.strptime("2018-09-01", "%Y-%m-%d"))
            PriceRule.objects.create(policy=policy,
                                     start_time=datetime.strptime("06:00", "%H:%M"),
                                     end_time=datetime.strptime("22:00", "%H:%M"),
                                     value=Decimal('0.09'),
                                     type=None)
        except ValidationError as ex:
            self.assertIn('type', ex.error_dict)
            return

        self.fail('A validation error shuld be thrown')
