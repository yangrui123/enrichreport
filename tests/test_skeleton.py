#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from enrichreport.skeleton import fib

__author__ = "YangRui"
__copyright__ = "YangRui"
__license__ = "none"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
