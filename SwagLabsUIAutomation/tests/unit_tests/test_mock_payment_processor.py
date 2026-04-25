from unittest.mock import Mock, patch

import pytest
import requests


def process_payment(amount):
    response = requests.post('https://fake-payment-api.com/pay', json={'user_id': 'user1', 'amount': amount})
    return response


# 1. Build fake_response
# 2. Set mock_post.return_value = fake_response
# 3. Call real function
# 4. Assert on response
# 5. Assert on mock
@pytest.mark.unit_test
@patch('requests.post')
def test_mocked_payment_success(mock_post):
    # setting a response that mock will return
    fake_response = {'status': 'SUCCESS', 'txn_id': 'TXN123'}

    # 1. Build a fake response object
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = fake_response

    # 2. Tell the mock: when requests.post is called, return this fake response
    mock_post.return_value = mock_response

    # 3. Call the real function — this triggers requests.post internally
    real_call = process_payment(1000)

    # 4. Assert the response is what we expect
    assert real_call.status_code == 200
    assert real_call.json()['status'] == 'SUCCESS'
    assert real_call.json()['txn_id'] == 'TXN123'

    # 5. Assert the mock was actually called once
    mock_post.assert_called_once()


@pytest.mark.unit_test
@patch('requests.post')
def test_mocked_payment_failure(mock_post):
    fake_response = {'status': 'FAILED', 'error': 'INVALID_AMOUNT'}

    # Mock -
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = fake_response

    mock_post.return_value = mock_response

    real_call = process_payment(-1)

    assert real_call.status_code == 400
    assert real_call.json()['status'] == 'FAILED'
    assert real_call.json()['error'] == 'INVALID_AMOUNT'

    mock_post.assert_called_once()


@pytest.mark.unit_test
@patch('requests.post')
def test_mocked_payment_success_called_with_correct_payload(mock_post):
    fake_response = {'status': 'SUCCESS', 'txn_id': 'TXN123'}

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = fake_response

    mock_post.return_value = mock_response

    real_call = process_payment(500)

    assert real_call.status_code == 200
    assert real_call.json()['status'] == 'SUCCESS'
    assert real_call.json()['txn_id'] == 'TXN123'

    mock_post.assert_called_once_with('https://fake-payment-api.com/pay',
                                             json={'user_id': 'user1', 'amount': 500})
