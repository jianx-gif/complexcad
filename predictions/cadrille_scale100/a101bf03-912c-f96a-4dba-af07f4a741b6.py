import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-3))
r=w0.sketch().arc((-87,-10),(-86,-12),(-86,-14)).arc((87,10),(-87,-10)).assemble().finalize().extrude(6).union(w0.sketch().segment((27,-1),(27,1)).segment((28,1)).arc((22,-1),(28,-1)).close().assemble().finalize().extrude(7))