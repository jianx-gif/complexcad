import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-87,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().circle(99).reset().face(w0.sketch().segment((-92,-29),(-86,-37)).segment((-53,-13)).arc((-56,-8),(-58,-2)).close().assemble(),mode='s').reset().face(w0.sketch().arc((53,13),(56,8),(58,2)).segment((92,29)).segment((86,37)).close().assemble(),mode='s').finalize().extrude(162).union(w1.sketch().circle(100).circle(100,mode='s').finalize().extrude(200))