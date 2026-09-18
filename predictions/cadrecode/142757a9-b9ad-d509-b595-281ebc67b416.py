import cadquery as cq
w0=cq.Workplane('YZ',origin=(-71,0,0))
w1=cq.Workplane('XY',origin=(0,0,-21))
r=w0.sketch().segment((-11,-21),(11,-15)).segment((0,35)).close().assemble().finalize().extrude(43).union(w0.workplane(offset=171/2).moveTo(0,-16.5).box(6,9,171)).union(w1.sketch().push([(-49,0)]).rect(102,102).push([(-81,-4)]).circle(3,mode='s').push([(-18,0)]).circle(1,mode='s').finalize().extrude(-14))