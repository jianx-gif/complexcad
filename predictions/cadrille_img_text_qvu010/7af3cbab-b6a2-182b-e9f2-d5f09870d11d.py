import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,89,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().push([(0,-1)]).circle(53).circle(4,mode='s').finalize().extrude(-156).union(w1.sketch().arc((-96,-44),(0,-91),(96,-44)).segment((75,-44)).arc((73,-46),(70,-44)).close().assemble().finalize().extrude(-200))