import cadquery as cq
w0=cq.Workplane('YZ',origin=(-100,0,0))
r=w0.sketch().segment((-75,-8),(-39,-8)).segment((-39,-4)).segment((-18,-4)).segment((-18,-8)).segment((75,-8)).segment((75,8)).segment((-75,8)).close().assemble().push([(33,-1.5)]).rect(54,9,mode='s').finalize().extrude(200)