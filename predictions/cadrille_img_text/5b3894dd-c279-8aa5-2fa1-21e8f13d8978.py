import cadquery as cq
w0=cq.Workplane('YZ',origin=(35,0,0))
w1=cq.Workplane('XY',origin=(0,0,-34))
r=w0.sketch().push([(0,16)]).circle(84).circle(71,mode='s').finalize().extrude(-125).union(w1.sketch().arc((-91,40),(-90,-53),(-10,-98)).arc((-10,-94),(-9,-98)).arc((10,-93),(27,-85)).arc((-65,-59),(-91,40)).assemble().finalize().extrude(134))