import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-1))
r=w0.sketch().rect(200,150).circle(37,mode='s').finalize().extrude(-13).union(w0.sketch().rect(76,76).push([(-31,10)]).circle(6,mode='s').finalize().extrude(15))