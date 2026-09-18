import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('XY',origin=(0,0,65))
r=w0.sketch().segment((-98,-6),(98,-6)).segment((98,6)).segment((65,6)).arc((57,3),(49,6)).segment((-98,6)).close().assemble().finalize().extrude(-200).union(w0.sketch().arc((-58,59),(-57,51),(-54,43)).segment((-54,42)).arc((-56,31),(-56,20)).arc((-57,19),(-58,18)).close().assemble().finalize().extrude(-134)).union(w1.sketch().arc((-1,-90),(22,-76),(43,-58)).arc((16,-1),(58,47)).arc((39,73),(12,90)).arc((18,-1),(-1,-90)).assemble().finalize().extrude(-153))