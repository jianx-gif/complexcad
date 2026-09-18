import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,8))
r=w0.sketch().push([(0,-0.5)]).rect(80,49).push([(-21,1)]).circle(2,mode='s').push([(0,-1)]).circle(14,mode='s').finalize().extrude(-8).union(w0.sketch().segment((0,-40),(8,-40)).segment((8,-10)).arc((15,0),(8,10)).segment((8,40)).segment((0,40)).segment((0,10)).arc((-7,0),(0,-10)).close().assemble().finalize().extrude(6)).union(w0.sketch().push([(0,-1)]).circle(10).circle(4,mode='s').finalize().extrude(18))
