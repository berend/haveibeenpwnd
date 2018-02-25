# -*- coding: utf-8 -*-
import mock
import pytest

from haveibeenpwnd import check_email
from haveibeenpwnd import check_password
from tests.resources import breaches
from tests.resources import match_response
from tests.resources import no_match_response


@mock.patch('haveibeenpwnd.main.requests')
def test_no_match(mock_requests):
    mock_requests.get.return_value.text = no_match_response

    count = check_password('super_safe_password')

    assert count == {'count': 0}


@mock.patch('haveibeenpwnd.main.requests')
def test_match(mock_requests):
    mock_requests.get.return_value.text = match_response

    count = check_password('hunter2')

    assert count == {'count': 16092}


@pytest.mark.parametrize('password', ['密码', 'A smiley😎'])
@mock.patch('haveibeenpwnd.main.requests')
def test_match_unicode(mock_requests, password):
    mock_requests.get.return_value.text = no_match_response

    check_password(password)


@mock.patch('haveibeenpwnd.main.requests')
def test_check_email(mock_requests):
    mock_requests.get.return_value.text = breaches

    response = check_email('text@example.com')

    assert response
