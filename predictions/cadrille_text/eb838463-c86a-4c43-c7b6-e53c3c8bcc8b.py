import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-1,-100))
r=w0.sketch().segment((29,-1),(35,-1)).segment((35,1)).segment((31,1)).arc((30,0),(29,-1)).assemble().finalize().extrude(199).union(w0.sketch().push([(30,0)]).circle(2).push([(95.5,0)]).rect(9,104).finalize().extrude(200))