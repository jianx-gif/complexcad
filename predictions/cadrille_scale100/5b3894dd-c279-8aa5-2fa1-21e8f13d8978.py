import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,20,0))
r=w0.sketch().arc((24,-25),(24,-23),(26,-23)).arc((-25,24),(24,-25)).assemble().push([(14,10)]).circle(16,mode='s').finalize().extrude(-20).union(w0.sketch().arc((-19,-1),(1,-19),(21,1)).arc((1,20),(-19,-1)).assemble().finalize().extrude(-20)).union(w0.workplane(offset=40/2).moveTo(0,0.5).box(20,29,40))