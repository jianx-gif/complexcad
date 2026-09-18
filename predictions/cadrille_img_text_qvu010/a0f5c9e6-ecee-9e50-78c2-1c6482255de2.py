import cadquery as cq
w0=cq.Workplane('YZ',origin=(95,0,0))
w1=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().segment((-33,-67),(-21,-67)).arc((0,-71),(21,-67)).segment((33,-67)).segment((33,-62)).arc((71,0),(33,62)).segment((33,67)).segment((21,67)).arc((0,71),(-21,67)).segment((-33,67)).segment((-33,62)).arc((-71,0),(-33,-62)).close().assemble().circle(53,mode='s').finalize().extrude(-191).union(w1.sketch().circle(100).circle(99,mode='s').finalize().extrude(-159))