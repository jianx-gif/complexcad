import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().segment((-75,-10),(75,-10)).segment((75,10)).segment((71,10)).segment((71,-6)).segment((62,-6)).segment((62,-10)).segment((60,-10)).segment((60,-5)).segment((-70,-5)).segment((-70,10)).segment((-75,10)).close().assemble().finalize().extrude(-200)