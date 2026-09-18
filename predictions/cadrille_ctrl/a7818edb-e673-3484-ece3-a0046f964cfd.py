import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,12))
r=w0.sketch().segment((-35,-40),(35,-40)).segment((35,40)).segment((11,40)).arc((10,38),(9,40)).segment((-35,40)).close().assemble().push([(0,-1)]).circle(33,mode='s').finalize().extrude(-12).union(w0.sketch().segment((-35,-16),(-27,-16)).segment((-27,-34)).segment((27,-34)).segment((27,-16)).segment((35,-16)).segment((35,16)).segment((27,16)).segment((27,34)).segment((-27,34)).segment((-27,16)).segment((-35,16)).close().assemble().finalize().extrude(-12))
