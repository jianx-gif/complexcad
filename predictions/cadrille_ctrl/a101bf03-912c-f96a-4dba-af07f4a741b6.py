import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-3))
r=w0.sketch().circle(88).circle(5,mode='s').finalize().extrude(6).union(w0.sketch().segment((27,-1),(27,1)).segment((28,1)).arc((27,2),(27,3)).arc((27,4),(28,4)).arc((29,5),(31,5)).arc((31,6),(32,6)).arc((2,1),(32,-3)).arc((30,-3),(29,-1)).close().assemble().finalize().extrude(7))
