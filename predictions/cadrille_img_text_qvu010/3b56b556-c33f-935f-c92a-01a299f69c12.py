import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-43,0))
w1=cq.Workplane('XY',origin=(0,0,95))
r=w0.sketch().arc((-95,83),(-53,45),(-10,8)).segment((-10,-83)).segment((10,-83)).segment((10,8)).arc((53,45),(95,83)).close().assemble().finalize().extrude(119).union(w1.sketch().arc((-60,-39),(-58,-41),(-55,-43)).segment((-55,-39)).close().assemble().finalize().extrude(-195))