import sys

import pytest

from haveibeenpwnd import check_password
from tests.resources import no_match_response
from tests.resources import match_response

# if sys.version_info.major == 3:
#     from unittest import mock
# else:
#     import mock


@mock.patch('haveibeenpwnd.main.requests')
def test_no_match(mock_requests):
    mock_requests.get.return_value.text = no_match_response

    count = check_password('super_safe_password')

    assert count == 0


@mock.patch('haveibeenpwnd.main.requests')
def test_match(mock_requests):
    mock_requests.get.return_value.text = match_response

    count = check_password('hunter2')

    assert count == 16092


@pytest.mark.parametrize('password', ['密码', 'A smiley😎'])
@mock.patch('haveibeenpwnd.main.requests')
def test_match_unicode(mock_requests, password):
    mock_requests.get.return_value.text = no_match_response

    check_password(password)
