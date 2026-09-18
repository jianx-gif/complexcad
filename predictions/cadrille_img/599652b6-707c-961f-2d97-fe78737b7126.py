import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-11,0))
w1=cq.Workplane('ZX',origin=(0,-29,0))
r=w0.sketch().push([(13,13)]).circle(87).circle(73,mode='s').finalize().extrude(11).union(w1.sketch().push([(13,13)]).circle(87).push([(13,12)]).circle(71,mode='s').push([(13,13)]).circle(38).finalize().extrude(59))