import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-17))
r=w0.sketch().segment((-100,-17),(-17,-17)).segment((-17,-100)).segment((17,-100)).segment((17,-17)).segment((100,-17)).segment((100,17)).segment((17,17)).segment((17,100)).segment((-17,100)).segment((-17,17)).segment((-100,17)).close().assemble().finalize().extrude(23).union(w0.workplane(offset=34/2).box(56,56,34))