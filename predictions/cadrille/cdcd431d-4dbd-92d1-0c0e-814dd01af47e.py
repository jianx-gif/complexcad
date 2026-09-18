import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-27))
r=w0.sketch().circle(100).circle(46,mode='s').push([(45,-45)]).circle(7,mode='s').push([(79,1)]).circle(10,mode='s').finalize().extrude(54)