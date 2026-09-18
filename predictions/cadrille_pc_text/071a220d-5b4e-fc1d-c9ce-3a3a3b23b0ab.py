import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,80))
w1=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().circle(99).rect(120,120,mode='s').finalize().extrude(-160).union(w1.sketch().segment((-90,-15),(-50,-15)).arc((-71,0),(-90,15)).close().assemble().finalize().extrude(-200))