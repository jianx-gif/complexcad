import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,10,0))
w1=cq.Workplane('ZX',origin=(0,29,0))
r=w0.sketch().segment((-31,-85),(31,-85)).segment((31,-71)).arc((74,0),(31,71)).segment((31,85)).segment((-31,85)).segment((-31,71)).arc((-74,0),(-31,-71)).close().assemble().circle(12,mode='s').finalize().extrude(-11).union(w1.sketch().circle(100).circle(94,mode='s').finalize().extrude(-59))