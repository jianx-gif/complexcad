import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
w1=cq.Workplane('XY',origin=(0,0,-2))
r=w0.sketch().segment((-23,-27),(-14,-35)).segment((33,7)).segment((24,16)).close().assemble().finalize().extrude(-10).union(w0.sketch().segment((-23,24),(-21,24)).segment((-21,35)).arc((-22,29),(-23,24)).assemble().finalize().extrude(-11)).union(w0.sketch().segment((43,-7),(53,-7)).segment((53,8)).segment((43,8)).segment((43,3)).arc((44,1),(43,0)).close().assemble().finalize().extrude(13))
