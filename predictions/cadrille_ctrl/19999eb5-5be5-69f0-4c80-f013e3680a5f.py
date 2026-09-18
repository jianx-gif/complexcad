import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,3))
w1=cq.Workplane('YZ',origin=(-41,0,0))
r=w0.sketch().segment((-49,-39),(-41,-39)).segment((-41,39)).segment((-49,39)).segment((-49,1)).arc((-47,-1),(-49,-3)).close().assemble().finalize().extrude(-4).union(w0.sketch().push([(0,-1)]).rect(82,50).circle(20,mode='s').finalize().extrude(6)).union(w1.sketch().push([(0,4)]).circle(25).circle(5,mode='s').finalize().extrude(57))
