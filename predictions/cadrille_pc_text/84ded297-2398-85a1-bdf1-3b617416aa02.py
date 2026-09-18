import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().segment((-50,-10),(-5,-10)).segment((-5,-7)).segment((-2,-7)).segment((-2,-10)).segment((50,-10)).segment((50,10)).segment((-50,10)).close().assemble().push([(-27,-3)]).circle(2,mode='s').finalize().extrude(-200)