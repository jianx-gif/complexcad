import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,90,0))
w1=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().arc((-31,-66),(-28,-68),(-25,-70)).segment((31,66)).segment((25,70)).close().assemble().finalize().extrude(-179).union(w1.sketch().arc((-90,15),(-62,-39),(-35,-93)).segment((55,-93)).segment((55,45)).arc((51,50),(48,55)).segment((-35,55)).arc((-38,52),(-41,50)).arc((-67,34),(-90,15)).assemble().finalize().extrude(-200))