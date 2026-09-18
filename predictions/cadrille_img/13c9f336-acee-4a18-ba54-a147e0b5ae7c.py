import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('YZ',origin=(-75,0,0))
r=w0.sketch().arc((10,-83),(18,-76),(25,-68)).segment((10,-68)).close().assemble().finalize().extrude(-162).union(w1.sketch().arc((-25,-83),(-19,-84),(-13,-84)).segment((-13,-100)).segment((13,-100)).segment((13,-84)).arc((29,-82),(45,-79)).arc((46,-76),(48,-76)).arc((65,-4),(25,64)).segment((25,83)).arc((19,84),(13,84)).segment((13,100)).segment((-13,100)).segment((-13,84)).arc((-19,82),(-25,81)).close().assemble().finalize().extrude(175))