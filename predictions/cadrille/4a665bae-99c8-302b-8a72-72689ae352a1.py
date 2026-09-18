import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((-44,-25),(31,-25)).segment((31,25)).segment((-44,25)).segment((-44,-14)).segment((-42,-14)).segment((-42,-16)).segment((-44,-16)).close().assemble().push([(-6.5,0)]).rect(55,30,mode='s').finalize().extrude(200).union(w1.sketch().arc((43,-14),(44,0),(43,14)).close().assemble().finalize().extrude(113))