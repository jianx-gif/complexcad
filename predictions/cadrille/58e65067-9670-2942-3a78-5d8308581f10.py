import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,60))
r=w0.sketch().circle(100).circle(94,mode='s').finalize().extrude(-153).union(w0.workplane(offset=-147/2).cylinder(147,94)).union(w0.sketch().circle(30).push([(-11,-16)]).circle(8,mode='s').finalize().extrude(33))