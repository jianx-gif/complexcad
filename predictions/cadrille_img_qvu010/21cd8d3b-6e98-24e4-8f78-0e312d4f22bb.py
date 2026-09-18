import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,33,0))
w1=cq.Workplane('YZ',origin=(-75,0,0))
r=w0.sketch().segment((-60,-66),(-59,-66)).arc((0,-95),(59,-66)).segment((60,-66)).segment((60,-65)).arc((95,0),(60,65)).segment((60,66)).segment((59,66)).arc((0,95),(-59,66)).segment((-60,66)).segment((-60,65)).arc((-95,0),(-60,-65)).close().assemble().push([(74,-31)]).circle(20,mode='s').finalize().extrude(-28).union(w1.sketch().arc((-99,-26),(98,22),(-97,-35)).segment((-93,-35)).arc((96,22),(-96,-26)).close().assemble().finalize().extrude(175))