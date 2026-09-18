import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.workplane(offset=-2/2).cylinder(2,5).union(w0.sketch().segment((-20,7),(-17,-13)).segment((20,-7)).segment((17,13)).close().assemble().finalize().extrude(10)).union(w0.sketch().circle(15).push([(4,0)]).circle(4,mode='s').finalize().extrude(80))