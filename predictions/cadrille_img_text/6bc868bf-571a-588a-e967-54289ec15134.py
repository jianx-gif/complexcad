import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-58,0))
w1=cq.Workplane('XY',origin=(0,0,-71))
r=w0.sketch().segment((-91,-45),(-79,-45)).arc((0,-95),(79,-45)).segment((91,-45)).segment((91,-25)).arc((95,0),(91,25)).segment((91,45)).segment((79,45)).arc((0,95),(-79,45)).segment((-91,45)).segment((-91,25)).arc((-95,0),(-91,-25)).close().assemble().finalize().extrude(-2).union(w0.sketch().circle(100).circle(99,mode='s').finalize().extrude(158)).union(w1.sketch().push([(0,-1)]).circle(89).circle(87,mode='s').finalize().extrude(155))