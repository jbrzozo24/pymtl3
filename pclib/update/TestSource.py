from pymtl import *
from collections import deque
from pclib.valrdy import valrdy_to_str

class TestSource( Updates ):

  def __init__( s, input_ ):
    assert type(input_) == list, "TestSrc only accepts a list of inputs!" 

    s.input_ = deque( input_ ) # deque.popleft() is faster
    s.out = 0

    @s.update
    def up_src():
      if not s.input_:
        s.out = 0
      else:
        s.out = s.input_.popleft()

  def done( s ):
    return not s.input_

  def line_trace( s ):
    return "%s" % s.out

class TestSourceValRdy( Updates ):

  def __init__( s, nmsgs = 1, input_ = [] ):
    assert type(input_) == list, "TestSrc only accepts a list of inputs!" 

    s.input_ = deque( input_ ) # deque.popleft() is faster
    s.msg = [0] * nmsgs
    s.val = s.rdy = 0

    @s.update_on_edge
    def up_src():
      if not s.input_:
        s.msg = [0] * nmsgs
        s.val = 0
      else:
        s.msg = s.input_[0]
        s.val = 1
        if s.rdy:
          s.input_.popleft()

  def done( s ):
    return not s.input_

  def line_trace( s ):
    return valrdy_to_str( s.msg, s.val, s.rdy )

class StreamSource( Updates ):

  def __init__( s, nmsgs = 1 ):
    s.msg = [0] * nmsgs
    s.val = s.rdy = 0
    s.ts  = 0

    @s.update_on_edge
    def up_src():
      s.msg = ( s.ts+95827*(s.ts&1), s.ts+(19182)*(s.ts&1) )
      s.val = 1
      if s.rdy:
        s.ts += 1

  def done( s ):
    return not s.input_

  def line_trace( s ):
    return valrdy_to_str( s.msg, s.val, s.rdy )
