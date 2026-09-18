import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,30,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-87,17),(-53,17)).segment((-53,-17)).segment((53,-17)).segment((53,17)).segment((87,17)).segment((87,65)).segment((53,65)).segment((53,90)).segment((-53,90)).segment((-53,65)).segment((-87,65)).close().assemble().finalize().extrude(-53).union(w1.sketch().segment((-99,-55),(-53,-55)).arc((0,-71),(53,-55)).segment((99,-55)).segment((99,55)).segment((53,55)).arc((0,71),(-53,55)).segment((-99,55)).close().assemble().circle(49,mode='s').finalize().extrude(-200))