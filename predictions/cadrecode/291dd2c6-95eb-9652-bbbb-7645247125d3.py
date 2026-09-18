import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,12))
r=w0.sketch().circle(100).circle(65,mode='s').push([(69,56)]).circle(7,mode='s').push([(88,1)]).circle(8,mode='s').finalize().extrude(-24)