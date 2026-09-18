import cadquery as cq
w0=cq.Workplane('XY',origin=(-48,0,-100))
r=w0.sketch().segment((28,-58),(48,-58)).segment((48,-51)).arc((38,-54),(28,-51)).close().assemble().finalize().extrude(183).union(w0.sketch().push([(38,0)]).circle(8).circle(7,mode='s').finalize().extrude(200))