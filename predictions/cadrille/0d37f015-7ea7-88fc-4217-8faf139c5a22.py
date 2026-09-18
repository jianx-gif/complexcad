import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-50))
w1=cq.Workplane('YZ',origin=(37,0,0))
r=w0.sketch().circle(75).circle(53,mode='s').finalize().extrude(25).union(w0.workplane(offset=150/2).cylinder(150,50)).union(w1.sketch().push([(0,-50)]).circle(46).circle(41,mode='s').finalize().extrude(-90))