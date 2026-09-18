import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-25,0))
w1=cq.Workplane('ZX',origin=(0,-18,0))
r=w0.sketch().segment((-100,-55),(100,-18)).segment((100,10)).segment((-100,55)).segment((-100,34)).segment((-87,47)).segment((-87,48)).segment((-86,48)).segment((-84,50)).segment((-83,48)).segment((-67,48)).segment((-67,34)).segment((-87,34)).segment((-87,39)).segment((-100,55)).close().assemble().finalize().extrude(50).union(w1.sketch().circle(39).circle(30,mode='s').finalize().extrude(35))