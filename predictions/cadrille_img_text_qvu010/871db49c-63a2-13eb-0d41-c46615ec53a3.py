import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().arc((-94,-40),(-72,-62),(-43,-74)).segment((-43,-67)).segment((-17,-67)).segment((-17,-74)).arc((23,-48),(43,-5)).segment((94,40)).segment((87,48)).arc((55,45),(74,69)).segment((43,74)).arc((11,48),(-23,28)).arc((-52,-10),(-94,-40)).assemble().circle(22,mode='s').finalize().extrude(200)