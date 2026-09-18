import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('YZ',origin=(-14,0,0))
r=w0.sketch().push([(-45.5,0)]).rect(109,72).push([(-73,-1)]).circle(4,mode='s').push([(-45,0)]).circle(9,mode='s').finalize().extrude(-15).union(w0.sketch().push([(-45.5,-47.5)]).rect(55,21).push([(-45.5,47.5)]).rect(55,21).finalize().extrude(14)).union(w1.workplane(offset=114/2).moveTo(0,-8).cylinder(114,4))