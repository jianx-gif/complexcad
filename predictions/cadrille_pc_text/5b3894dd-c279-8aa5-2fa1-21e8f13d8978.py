import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-86,0))
w1=cq.Workplane('YZ',origin=(57,0,0))
r=w0.sketch().circle(100).push([(47,27)]).circle(36,mode='s').finalize().extrude(58).union(w0.workplane(offset=172/2).cylinder(172,43)).union(w1.sketch().push([(-10,0)]).circle(57).circle(53,mode='s').finalize().extrude(-113))