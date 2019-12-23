#=========================================================================
# StructuralRTLIRGenL3Pass_test.py
#=========================================================================
# Author : Peitian Pan
# Date   : May 19, 2019
"""Test the generation of level 1 structural RTLIR."""

from pymtl3.passes.rtlir.structural.StructuralRTLIRGenL3Pass import (
    StructuralRTLIRGenL3Pass,
)
from pymtl3.passes.rtlir.structural.StructuralRTLIRSignalExpr import *
from pymtl3.testcases import (
    CaseArrayBits32IfcInComp,
    CaseBits32IfcInComp,
    CaseConnectValRdyIfcComp,
)

from .StructuralRTLIRGenL1Pass_test import gen_connections


def test_L3_ifc_view_attr():
  a = CaseBits32IfcInComp.DUT()
  a.elaborate()
  a.apply( StructuralRTLIRGenL3Pass( gen_connections( a ) ) )
  ns = a._pass_structural_rtlir_gen
  comp = CurComp(a, 's')
  assert ns.connections == \
    [(InterfaceAttr(CurCompAttr(comp, 'in_'), 'foo'), CurCompAttr(comp, 'out'))]

def test_L3_ifc_view_index():
  a = CaseArrayBits32IfcInComp.DUT()
  a.elaborate()
  a.apply( StructuralRTLIRGenL3Pass( gen_connections( a ) ) )
  ns = a._pass_structural_rtlir_gen
  comp = CurComp(a, 's')
  assert ns.connections == \
    [(InterfaceAttr(InterfaceViewIndex(CurCompAttr(comp, 'in_'), 1), 'foo'),
     CurCompAttr(comp, 'out'))]

def test_L3_ifc_view_connection():
  a = CaseConnectValRdyIfcComp.DUT()
  a.elaborate()
  a.apply( StructuralRTLIRGenL3Pass( gen_connections( a ) ) )
  ns = a._pass_structural_rtlir_gen
  comp = CurComp(a, 's')
  ref = \
    [
      (InterfaceAttr(CurCompAttr(comp, 'in_'), 'msg'),
      InterfaceAttr(CurCompAttr(comp, 'out'), 'msg')),
      (InterfaceAttr(CurCompAttr(comp, 'in_'), 'val'),
      InterfaceAttr(CurCompAttr(comp, 'out'), 'val')),
      (InterfaceAttr(CurCompAttr(comp, 'out'), 'rdy'),
      InterfaceAttr(CurCompAttr(comp, 'in_'), 'rdy')),
    ]
  # The order of ports is non-deterministic?
  assert ns.connections[0] in ref
  assert ns.connections[1] in ref
  assert ns.connections[2] in ref
