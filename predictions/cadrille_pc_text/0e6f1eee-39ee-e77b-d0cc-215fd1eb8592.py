import cadquery as cq
w0=cq.Workplane('YZ',origin=(-100,0,0))
r=w0.sketch().segment((-75,-15),(75,-15)).segment((75,15)).segment((50,15)).segment((50,5)).segment((46,5)).segment((46,15)).segment((-75,15)).close().assemble().push([(-48,4)]).circle(7,mode='s').push([(51,-8)]).circle(5,mode='s').finalize().extrude(200)