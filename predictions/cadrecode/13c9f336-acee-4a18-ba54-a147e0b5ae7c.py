import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().segment((-75,-8),(75,-8)).segment((75,8)).segment((61,8)).segment((61,4)).segment((-75,4)).close().assemble().push([(0,-5.5)]).rect(10,3,mode='s').push([(0,5.5)]).rect(10,3,mode='s').finalize().extrude(-200)