import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-23))
w1=cq.Workplane('ZX',origin=(0,-75,0))
r=w0.sketch().circle(19).rect(20,18,mode='s').finalize().extrude(51).union(w1.sketch().segment((-7,-100),(6,-100)).segment((6,-79)).segment((5,-79)).segment((5,-67)).segment((6,-67)).segment((6,82)).segment((5,82)).segment((5,94)).segment((6,94)).segment((6,100)).segment((-7,100)).close().assemble().finalize().extrude(150))