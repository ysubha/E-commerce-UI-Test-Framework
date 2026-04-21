import allure
import pytest

from SwagLabsUIAutomation.utils.price_calculator import PriceCalculator


@allure.feature('Unit Test')
@allure.story('Calculate Tax')
@pytest.mark.unit_test
@pytest.mark.parametrize(('amount', 'expected_tax'), [(100, 8.00), (99.9, 7.99)])
def test_calculate_tax(amount, expected_tax):
    price_cal_obj = PriceCalculator()
    assert price_cal_obj.calculate_tax(amount) == expected_tax


@allure.feature('Unit Test')
@allure.story('Calculate Total')
@pytest.mark.unit_test
@pytest.mark.parametrize(('amount', 'net_price'), [(100, 108.00), (99.9, 107.89)])
def test_calculate_total(amount, net_price):
    price_cal_obj = PriceCalculator()
    assert price_cal_obj.calculate_total(amount) == net_price


@allure.feature('Unit Test')
@allure.story('Calculate Net Price')
@pytest.mark.unit_test
@pytest.mark.parametrize(('product_details', 'net_amount'),
                         [([], 0.00), ([{"price": 9.99}], 9.99), ([{"price": 9.99}, {"price": 15.99}], 25.98)])
def test_calculate_net_price(product_details, net_amount):
    price_cal_obj = PriceCalculator()
    assert price_cal_obj.calculate_net_price(product_details) == net_amount
