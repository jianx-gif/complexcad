import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().segment((-75,-15),(75,-15)).segment((75,15)).segment((25,15)).segment((25,5)).segment((-25,5)).segment((-25,15)).segment((-75,15)).close().assemble().push([(-48,4)]).circle(7,mode='s').push([(50,6)]).circle(9,mode='s').finalize().extrude(-200)