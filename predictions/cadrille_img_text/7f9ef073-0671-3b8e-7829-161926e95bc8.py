import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,29,0))
w1=cq.Workplane('YZ',origin=(85,0,0))
r=w0.sketch().arc((-67,-39),(100,0),(-67,39)).close().assemble().finalize().extrude(-74).union(w1.sketch().segment((29,-13),(35,-13)).arc((48,-16),(61,-13)).segment((67,-13)).segment((67,-9)).arc((82,28),(67,65)).segment((67,69)).segment((61,69)).arc((48,72),(35,69)).segment((29,69)).segment((29,65)).arc((14,28),(29,-9)).close().assemble().push([(48,28)]).circle(33,mode='s').finalize().extrude(-151))