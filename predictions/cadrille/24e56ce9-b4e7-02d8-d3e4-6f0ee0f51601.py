import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-75))
r=w0.sketch().circle(100).push([(-1,-84)]).circle(8,mode='s').finalize().extrude(-25).union(w0.sketch().circle(75).reset().face(w0.sketch().segment((-61,-5),(-20,-72)).segment((61,-22)).segment((20,45)).close().assemble(),mode='s').finalize().extrude(130)).union(w0.sketch().circle(50).circle(20,mode='s').finalize().extrude(175))