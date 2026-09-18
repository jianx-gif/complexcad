import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('YZ',origin=(29,0,0))
r=w0.sketch().segment((-21,-34),(19,-35)).segment((21,34)).segment((-19,35)).close().assemble().circle(25,mode='s').finalize().extrude(-100).union(w0.sketch().circle(39).circle(5,mode='s').finalize().extrude(-92)).union(w1.workplane(offset=14/2).moveTo(-1,97).box(60,4,14))
