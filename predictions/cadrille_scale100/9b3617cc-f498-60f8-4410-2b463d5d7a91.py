import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().arc((14,-27),(15,-26),(16,-26)).arc((28,-12),(29,6)).arc((20,0),(30,5)).arc((-26,14),(14,-27)).assemble().finalize().extrude(13).union(w0.sketch().push([(0,-1)]).circle(18).circle(3,mode='s').finalize().extrude(55)).union(w0.sketch().push([(0,-1)]).circle(14).circle(3,mode='s').finalize().extrude(55))