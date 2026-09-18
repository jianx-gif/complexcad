import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,27))
r=w0.sketch().circle(100).circle(45,mode='s').push([(43,-46)]).circle(7,mode='s').push([(80,1)]).circle(10,mode='s').finalize().extrude(-54)