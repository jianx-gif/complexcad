import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-83))
w1=cq.Workplane('YZ',origin=(68,0,0))
r=w0.sketch().push([(-8,0)]).circle(92).circle(80,mode='s').finalize().extrude(183).union(w1.sketch().arc((-34,-99),(35,-89),(24,-20)).arc((12,-65),(-34,-66)).close().assemble().finalize().extrude(32))