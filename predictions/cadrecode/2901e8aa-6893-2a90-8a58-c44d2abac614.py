import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,87))
r=w0.sketch().circle(20).circle(13,mode='s').finalize().extrude(-187).union(w0.workplane(offset=-107/2).cylinder(107,24)).union(w0.workplane(offset=13/2).cylinder(13,33))