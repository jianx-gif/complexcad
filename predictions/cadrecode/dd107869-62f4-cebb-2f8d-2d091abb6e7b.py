import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('YZ',origin=(18,0,0))
r=w0.sketch().push([(-45.5,0)]).rect(109,72).push([(-63,0)]).circle(12,mode='s').push([(-34,0)]).rect(30,2,mode='s').push([(-17,0)]).rect(30,2,mode='s').finalize().extrude(-15).union(w0.sketch().push([(-45.5,0)]).rect(55,116).rect(55,72,mode='s').finalize().extrude(15)).union(w1.workplane(offset=82/2).moveTo(0,-7).cylinder(82,4))