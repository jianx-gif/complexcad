import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('YZ',origin=(41,0,0))
r=w0.sketch().arc((-74,-63),(-59,-69),(-44,-63)).close().assemble().reset().face(w0.sketch().arc((-39,-61),(48,59),(-33,-65)).segment((-33,-58)).arc((47,57),(-39,-55)).close().assemble()).finalize().extrude(-200).union(w1.sketch().push([(0,-16)]).circle(84).circle(70,mode='s').finalize().extrude(-10))