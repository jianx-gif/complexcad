import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,86,0))
w1=cq.Workplane('YZ',origin=(-85,0,0))
r=w0.sketch().segment((-45,-79),(45,-79)).segment((45,-34)).arc((0,-51),(-45,-34)).close().assemble().finalize().extrude(-172).union(w1.sketch().segment((-29,-87),(29,-87)).segment((29,-68)).arc((51,0),(29,68)).segment((29,87)).segment((-29,87)).segment((-29,68)).arc((-51,0),(-29,-68)).close().assemble().finalize().extrude(185))