import cadquery as cq
w0=cq.Workplane('YZ',origin=(-76,0,0))
w1=cq.Workplane('ZX',origin=(0,-58,0))
r=w0.sketch().segment((-65,-36),(-65,36)).arc((-70,0),(-65,-36)).assemble().circle(5).finalize().extrude(173).union(w1.sketch().push([(10,12)]).circle(88).circle(80,mode='s').finalize().extrude(117))