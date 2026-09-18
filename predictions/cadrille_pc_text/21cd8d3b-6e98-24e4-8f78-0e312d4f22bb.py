import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-58,0))
w1=cq.Workplane('XY',origin=(0,0,20))
r=w0.sketch().circle(100).circle(93,mode='s').finalize().extrude(150).union(w1.sketch().segment((33,-92),(80,-92)).segment((80,-25)).segment((33,-25)).segment((33,-55)).arc((26,-64),(33,-74)).close().assemble().finalize().extrude(-20))