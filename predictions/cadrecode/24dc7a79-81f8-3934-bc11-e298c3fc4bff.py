import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-16))
r=w0.sketch().rect(182,92).push([(65,23)]).circle(4,mode='s').finalize().extrude(-9).union(w0.sketch().push([(-44.5,0)]).rect(111,70).push([(-44,0)]).circle(13,mode='s').finalize().extrude(5)).union(w0.workplane(offset=41/2).moveTo(95.5,1).box(9,2,41))