import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,31))
r=w0.sketch().arc((-18,-24),(-17,-23),(-16,-23)).arc((-17,-23),(-18,-24)).assemble().finalize().extrude(-101).union(w0.sketch().circle(30).circle(23,mode='s').finalize().extrude(31)).union(w0.workplane(offset=39/2).cylinder(39,15))