import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('YZ',origin=(-40,0,0))
r=w0.sketch().segment((-42,-32),(42,-32)).segment((42,32)).segment((-42,32)).segment((-42,-19)).segment((-39,-19)).segment((-39,-23)).segment((-42,-23)).close().assemble().finalize().extrude(6).union(w1.sketch().segment((-30,-6),(30,-6)).segment((30,0)).segment((17,0)).segment((17,4)).segment((-17,4)).segment((-17,0)).segment((-30,0)).close().assemble().push([(0,-2.5)]).rect(2,5,mode='s').finalize().extrude(80))