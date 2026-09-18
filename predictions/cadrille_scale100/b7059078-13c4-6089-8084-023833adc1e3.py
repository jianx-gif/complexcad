import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,1,0))
r=w0.workplane(offset=-101/2).moveTo(-1,36).cylinder(101,2).union(w0.sketch().arc((-38,-8),(35,-15),(-15,36)).arc((-35,17),(-38,-8)).assemble().push([(0,-1)]).circle(34,mode='s').finalize().extrude(13)).union(w0.sketch().push([(0,-1)]).circle(32).circle(29,mode='s').finalize().extrude(49))