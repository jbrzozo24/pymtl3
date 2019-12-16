#=========================================================================
# RTLIRTranslator_L5_cases_test.py
#=========================================================================
# Author : Peitian Pan
# Date   : May 23, 2019
"""Test the RTLIR transaltor."""

import pytest

from pymtl3.passes.rtlir.util.test_utility import get_parameter

from .TestRTLIRTranslator import TestRTLIRTranslator
from ..behavioral.test.BehavioralTranslatorL5_test import \
    test_generic_behavioral_L5 as behavioral


def run_test( case, m ):
  if not m._dsl.constructed:
    m.elaborate()
  tr = TestRTLIRTranslator(m)
  tr.translate( m )
  src = tr.hierarchy.src
  assert src == case.REF_SRC

@pytest.mark.parametrize(
  'case', get_parameter('case', behavioral)
)
def test_generic_L5( case ):
  run_test( case, case.DUT() )
