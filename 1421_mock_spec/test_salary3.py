# mockを使ったテスト

import unittest
from unittest.mock import MagicMock
from unittest import mock

import salary


class TestSalary(unittest.TestCase):
    def test_calculation_salary(self):
        s = salary.Salary(year=2017)
        s.bonus_api.bonus_price = MagicMock(return_value=1)
        self.assertEqual(s.calculation_salary(), 101)
        # magicmockであるbonus_api.bonus_price()APIが本当に呼ばれたかテストもできる
        s.bonus_api.bonus_price.assert_called()
        # magicmockであるbonus_api.bonus_price()APIが一度だけ呼ばれたかテストできる
        s.bonus_api.bonus_price.assert_called_once()
        # magicmockであるbonus_api.bonus_price()APIの引数yearがちゃんと渡されていrうかテストできる
        s.bonus_api.bonus_price.assert_called_with(year=2017)
        # magicmockであるbonus_api.bonus_price()APIが一度だけ呼ばれ、かつ引数が2017かテストできる
        s.bonus_api.bonus_price.assert_called_once_with(year=2017)
        # magicmockであるbonus_api.bonus_price()APIが何回呼ばれたかもわかる
        self.assertEqual(s.bonus_api.bonus_price.call_count, 1)

    def test_calculation_salary_no_salary(self):
        s = salary.Salary(year=2050)
        s.bonus_api.bonus_price = MagicMock(return_value=0)
        self.assertEqual(s.calculation_salary(), 100)
        # magicmockであるbonus_api.bonus_price()APIが呼ばれないこともテストできる
        s.bonus_api.bonus_price.assert_not_called()

    # 1. デコレーターでパスを指定すると、わざわざMagicMock()としなくてよい
    @mock.patch('salary.ThirdPartyBonusRestApi.bonus_price')
    def test_calculation_salary_patch(self, mock_bonus):
        mock_bonus.return_value = 1

        s = salary.Salary(year=2017)
        salary_price = s.calculation_salary()

        self.assertEqual(salary_price, 101)
        mock_bonus.assert_called()

    # 2. デコレーターではなく、with ステートメントでもできる
    def test_calculation_salary_patch_with(self):
        # withステートメントの中だけ、mock_bonusが有効である
        with mock.patch('salary.ThirdPartyBonusRestApi.bonus_price') as mock_bonus:
            mock_bonus.return_value = 1

            s = salary.Salary(year=2017)
            salary_price = s.calculation_salary()

            self.assertEqual(salary_price, 101)
            mock_bonus.assert_called()

    def setUp(self):
        self.patcher = mock.patch('salary.ThirdPartyBonusRestApi.bonus_price')
        # patcher.start() ~ stop()の間だけ、mock_bonusが有効である
        self.mock_bonus = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    # 3. パッチャーを使ってもできる
    def test_calculation_salary_patch_patcher(self):
        self.mock_bonus.return_value = 1

        s = salary.Salary(year=2017)
        salary_price = s.calculation_salary()

        self.assertEqual(salary_price, 101)
        self.mock_bonus.assert_called()

    # 4. side_effectを使用
    def test_calculation_salary_patch_side_effect1(self):
        # return_valueを使わず、新たな関数f(year)でbonus_price(year)を書き換え、戻り値を返し、side_effectに入れる
        def f(year):
            return 1

        self.mock_bonus.side_effect = f

        s = salary.Salary(year=2017)
        salary_price = s.calculation_salary()

        self.assertEqual(salary_price, 101)
        self.mock_bonus.assert_called()

    def test_calculation_salary_patch_side_effect2(self):
        # return_valueを使わず、新たな関数f(year)でbonus_price(year)を書き換え、戻り値を返し、side_effectに入れる
        # def f(year):
        #     return 1

        # connection error例外もside_effectでテストできる
        self.mock_bonus.side_effect = ConnectionRefusedError

        s = salary.Salary(year=2017)
        salary_price = s.calculation_salary()

        self.assertEqual(salary_price, 100)
        self.mock_bonus.assert_called()

    def test_calculation_salary_patch_side_effect3(self):
        # return_valueを使わず、新たな関数f(year)でbonus_price(year)を書き換え、戻り値を返し、side_effectに入れる
        # def f(year):
        #     return 1

        # リストで返すこともできる
        self.mock_bonus.side_effect = [
            1,
            2,
            3,
            ValueError('Bankrupt!!!')
        ]

        s = salary.Salary(year=2017)
        salary_price = s.calculation_salary()
        self.assertEqual(salary_price, 101)
        s = salary.Salary(year=2018)
        salary_price = s.calculation_salary()
        self.assertEqual(salary_price, 102)
        s = salary.Salary(year=2019)
        salary_price = s.calculation_salary()
        self.assertEqual(salary_price, 103)
        s = salary.Salary(year=200)
        with self.assertRaises(ValueError):
            s.calculation_salary()

    # クラスThirdPartyBonusRestApi ごと全部Mockする場合
    # 1. デコレーターでパスを指定すると、わざわざMagicMock()としなくてよい
    @mock.patch('salary.ThirdPartyBonusRestApi', spec=True)
    def test_calculation_salary_class(self, MockRest):
        # mock_rest = MockRest.return_value
        mock_rest = MockRest()
        mock_rest.bonus_price.return_value = 1

        s = salary.Salary(year=2017)
        salary_price = s.calculation_salary()

        self.assertEqual(salary_price, 101)
        mock_rest.bonus_price.assert_called()