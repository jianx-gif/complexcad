import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().push([(-15.5,0)]).rect(169,86).push([(-75,14)]).circle(7,mode='s').push([(-12.5,-1)]).rect(85,42,mode='s').finalize().extrude(-22).union(w0.workplane(offset=-17/2).moveTo(-12.5,-1).box(85,42,17)).union(w0.workplane(offset=22/2).moveTo(71.5,-0.5).box(57,29,22))