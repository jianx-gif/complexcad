import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('XY',origin=(0,0,13))
r=w0.sketch().push([(-6.5,0)]).rect(75,50).rect(55,30,mode='s').finalize().extrude(-200).union(w1.sketch().arc((38,25),(41,0),(39,-25)).segment((44,-25)).segment((44,25)).close().assemble().finalize().extrude(-23))