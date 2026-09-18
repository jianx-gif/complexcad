import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-36))
w1=cq.Workplane('XY',origin=(0,0,90))
r=w0.sketch().circle(36).reset().face(w0.sketch().segment((-27,-4),(-26,-4)).arc((0,-26),(26,-4)).segment((27,-4)).segment((27,4)).segment((26,4)).arc((0,26),(-26,4)).segment((-27,4)).close().assemble(),mode='s').finalize().extrude(-63).union(w0.sketch().circle(100).circle(90,mode='s').finalize().extrude(126)).union(w1.sketch().circle(82).rect(52,82,mode='s').finalize().extrude(9))