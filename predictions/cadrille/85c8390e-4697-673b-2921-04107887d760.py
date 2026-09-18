import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-33))
r=w0.sketch().circle(100).push([(94,2)]).circle(2,mode='s').finalize().extrude(66)