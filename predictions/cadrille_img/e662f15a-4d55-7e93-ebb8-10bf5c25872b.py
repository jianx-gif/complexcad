import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-92,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((-58,89),(58,89)).arc((0,98),(-58,89)).assemble().finalize().extrude(185).union(w1.sketch().arc((-38,-50),(0,-60),(38,-50)).segment((38,-48)).arc((40,-38),(38,-28)).segment((38,-26)).segment((-38,-26)).segment((-38,-28)).arc((-40,-38),(-38,-48)).close().assemble().finalize().extrude(200))