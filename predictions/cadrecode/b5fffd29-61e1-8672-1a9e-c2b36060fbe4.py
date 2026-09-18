import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,12))
w1=cq.Workplane('XY',origin=(0,0,13))
r=w0.sketch().segment((-99,-45),(99,-45)).segment((99,45)).segment((-32,45)).segment((-32,31)).segment((-99,31)).close().assemble().finalize().extrude(-12).union(w1.sketch().rect(200,150).rect(80,90,mode='s').finalize().extrude(-26))