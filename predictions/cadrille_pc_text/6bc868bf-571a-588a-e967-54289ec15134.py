import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,99))
r=w0.sketch().circle(92).circle(72,mode='s').finalize().extrude(-198).union(w0.sketch().segment((-42,-90),(-42,-86)).segment((-37,-86)).segment((-37,-92)).arc((39,92),(-42,-90)).assemble().circle(94,mode='s').finalize().extrude(-102))