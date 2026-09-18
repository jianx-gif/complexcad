import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
r=w0.sketch().segment((-40,-1),(-38,-1)).arc((0,-40),(38,-1)).segment((40,-1)).segment((40,1)).segment((38,1)).arc((0,40),(-38,1)).segment((-40,1)).close().assemble().finalize().extrude(-10).union(w0.sketch().circle(15).push([(-13,-1)]).circle(2,mode='s').finalize().extrude(8))