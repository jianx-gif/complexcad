import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,40))
r=w0.sketch().arc((14,26),(15,25),(16,25)).segment((16,26)).close().assemble().finalize().extrude(-80).union(w0.sketch().push([(0,-1)]).circle(30).circle(24,mode='s').finalize().extrude(-40)).union(w0.sketch().segment((-24,-13),(-13,-26)).segment((-12,-25)).segment((-23,-11)).close().assemble().finalize().extrude(-40))
