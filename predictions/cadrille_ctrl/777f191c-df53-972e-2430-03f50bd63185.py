import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,4))
r=w0.sketch().segment((-45,-3),(-39,-3)).arc((-32,-24),(-14,-36)).segment((-14,-39)).segment((6,-45)).segment((8,-39)).arc((32,-24),(40,3)).segment((45,6)).segment((39,13)).segment((37,12)).arc((25,31),(3,40)).segment((3,45)).segment((-6,45)).segment((-6,40)).arc((-32,24),(-40,-3)).segment((-45,-3)).close().assemble().finalize().extrude(-4).union(w0.sketch().circle(15).circle(3,mode='s').finalize().extrude(8))
