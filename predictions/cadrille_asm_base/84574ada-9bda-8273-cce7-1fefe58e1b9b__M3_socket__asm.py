import cadquery as cq
w0=cq.Workplane('YZ',origin=(59,0,0))
w1=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().segment((-42,13),(-36,-14)).segment((42,-1)).segment((36,26)).close().assemble().finalize().extrude(-119).union(w1.sketch().segment((-81,-3),(39,-3)).arc((41,1),(42,-3)).segment((81,-3)).segment((81,9)).segment((-81,9)).close().assemble().finalize().extrude(-200))