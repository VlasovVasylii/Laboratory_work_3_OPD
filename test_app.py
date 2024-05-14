import unittest
from app import app, calc_diff_payment, calc_annuity_payment


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_calc_diff_payment(self):
        loan_amount = 100000
        loan_term = 12
        interest_rate = 5
        result = calc_diff_payment(loan_amount, loan_term, interest_rate)
        a, b = map(float, result[0].split(', ..., '))
        self.assertGreaterEqual(a, 8750.00 - 100)
        self.assertLessEqual(a, 8750.00 + 100)

        self.assertGreaterEqual(b, 8368.06 - 100)
        self.assertLessEqual(b, 8368.06 + 100)

        self.assertGreaterEqual(result[1], 2708.33 - 100)
        self.assertLessEqual(result[1], 2708.33 + 100)

        self.assertGreaterEqual(result[2], 102708.33 - 100)
        self.assertLessEqual(result[2], 102708.33 + 100)

    def test_calc_diff_payment_wrong(self):
        loan_amount = 700000
        loan_term = 60
        interest_rate = 6
        result = calc_diff_payment(loan_amount, loan_term, interest_rate)

        a, b = map(float, result[0].split(', ..., '))

        if a < 15167 - 500 or a > 15167 + 500 or b < 11225.00 - 500 or\
                b > 11725.00 + 500 or result[1] < 87875 - 500 or result[1] > 87875 + 500 \
                or result[2] < 787875 - 500 or result[2] > 787875 + 500:
            self.assertEqual(0, 1)

    def test_calc_annuity_payment(self):
        loan_amount = 100000
        loan_term = 12
        interest_rate = 5
        result = calc_annuity_payment(loan_amount, loan_term, interest_rate)
        self.assertGreaterEqual(result[0], 8561 - 100)
        self.assertLessEqual(result[0], 8561 + 100)

        self.assertGreaterEqual(result[1], 2729 - 100)
        self.assertLessEqual(result[1], 2729 + 100)

        self.assertGreaterEqual(result[2], 102729 - 100)
        self.assertLessEqual(result[2], 102729 + 100)

    def test_calc_annuity_payment_wrong(self):
        loan_amount = 700000
        loan_term = 60
        interest_rate = 6
        result = calc_annuity_payment(loan_amount, loan_term, interest_rate)

        if result[0] < 13000 or result[0] > 14000 or result[1] < 111400 or\
                result[1] > 112500 or result[2] < 811400 or result[2] > 812500:
            self.assertEqual(0, 1)


if __name__ == '__main__':
    unittest.main()
