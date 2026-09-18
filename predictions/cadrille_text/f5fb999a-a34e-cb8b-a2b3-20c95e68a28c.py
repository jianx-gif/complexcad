import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
r=w0.sketch().segment((29,-58),(31,-58)).segment((31,-57)).arc((30,-57),(29,-58)).assemble().finalize().extrude(-39).union(w0.sketch().push([(30,-1)]).circle(2).push([(30,-1.5)]).rect(2,3,mode='s').finalize().extrude(-25)).union(w0.sketch().push([(30,-1)]).circle(2).push([(30.5,-1)]).rect(3,2,mode='s').finalize().extrude(70))