import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-38))
w1=cq.Workplane('XY',origin=(0,0,-15))
r=w0.sketch().push([(-14,0)]).circle(38).circle(31,mode='s').finalize().extrude(-40).union(w0.sketch().push([(-58,0)]).circle(38).push([(-58.5,0)]).rect(43,56,mode='s').finalize().extrude(7)).union(w0.sketch().push([(65,0)]).circle(35).circle(31,mode='s').finalize().extrude(123)).union(w1.sketch().push([(65,0)]).circle(30).circle(25,mode='s').finalize().extrude(63))