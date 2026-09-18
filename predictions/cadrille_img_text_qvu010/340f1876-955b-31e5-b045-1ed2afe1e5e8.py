import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,57,0))
w1=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().circle(96).reset().face(w0.sketch().segment((-95,29),(-67,-4)).arc((-54,-49),(-12,-69)).segment((16,-93)).segment((95,-29)).segment((67,4)).arc((54,49),(12,69)).segment((-16,93)).close().assemble(),mode='s').finalize().extrude(-123).union(w1.sketch().segment((-100,-100),(-42,-100)).arc((-96,0),(-42,100)).segment((-100,100)).close().assemble().finalize().extrude(-83))