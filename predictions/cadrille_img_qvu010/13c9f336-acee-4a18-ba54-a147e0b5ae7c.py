import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('XY',origin=(0,0,-61))
r=w0.sketch().segment((-99,-16),(76,-16)).segment((76,-11)).segment((83,-11)).arc((82,0),(83,11)).segment((76,11)).segment((76,16)).segment((-99,16)).close().assemble().finalize().extrude(200).union(w1.sketch().arc((-76,-16),(0,-93),(99,-16)).segment((96,-16)).arc((0,-88),(-96,-16)).close().assemble().finalize().extrude(126))