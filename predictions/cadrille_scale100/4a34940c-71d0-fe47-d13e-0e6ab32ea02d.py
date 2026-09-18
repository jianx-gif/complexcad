import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,40))
r=w0.sketch().push([(0,23)]).circle(2).circle(1,mode='s').finalize().extrude(-80).union(w0.sketch().push([(0,23)]).circle(7).push([(0,23.5)]).rect(4,11,mode='s').finalize().extrude(-41)).union(w0.sketch().push([(0,-22)]).circle(8).push([(0,-23)]).circle(3,mode='s').push([(26,0)]).circle(4).finalize().extrude(-40))