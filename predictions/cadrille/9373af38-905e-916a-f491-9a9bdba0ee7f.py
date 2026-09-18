import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-31))
w1=cq.Workplane('YZ',origin=(30,0,0))
r=w0.sketch().push([(-65,0)]).circle(35).circle(11,mode='s').finalize().extrude(-19).union(w0.sketch().push([(69,0)]).circle(31).circle(24,mode='s').finalize().extrude(116)).union(w1.sketch().push([(0,-55)]).circle(38).circle(31,mode='s').finalize().extrude(-90))