import cadquery as cq
w0=cq.Workplane('YZ',origin=(-100,0,0))
w1=cq.Workplane('ZX',origin=(0,90,0))
r=w0.sketch().arc((-28,-49),(-27,-49),(-27,-50)).arc((-19,88),(48,-32)).arc((50,-31),(52,-30)).arc((-33,86),(-28,-49)).assemble().finalize().extrude(200).union(w1.sketch().arc((-13,-86),(1,-89),(14,-94)).arc((34,-9),(1,80)).segment((1,2)).segment((-13,2)).close().assemble().finalize().extrude(-180))