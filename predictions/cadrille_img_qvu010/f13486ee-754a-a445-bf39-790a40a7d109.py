import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-46))
w1=cq.Workplane('ZX',origin=(0,53,0))
r=w0.sketch().arc((10,-90),(75,-55),(83,18)).arc((71,-48),(10,-90)).assemble().finalize().extrude(111).union(w0.sketch().arc((-87,51),(-51,1),(-10,-44)).segment((-10,-48)).segment((-6,-48)).arc((37,-61),(79,-51)).arc((-51,-39),(-87,51)).assemble().finalize().extrude(146)).union(w1.sketch().push([(-1,0)]).circle(83).circle(71,mode='s').finalize().extrude(24))