import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().arc((13,-27),(14,-26),(16,-26)).arc((14,-25),(13,-27)).assemble().finalize().extrude(-80).union(w0.sketch().circle(30).circle(25,mode='s').finalize().extrude(80))