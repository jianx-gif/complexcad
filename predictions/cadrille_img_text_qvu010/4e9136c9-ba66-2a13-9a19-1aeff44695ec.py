import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-57,0))
w1=cq.Workplane('YZ',origin=(-1,0,0))
r=w0.sketch().arc((-54,-42),(-42,-56),(-27,-66)).close().assemble().reset().face(w0.sketch().segment((-18,61),(18,42)).arc((4,56),(-18,61)).assemble()).reset().face(w0.sketch().arc((27,-61),(48,-43),(58,-19)).close().assemble()).reset().face(w0.sketch().segment((61,39),(70,27)).arc((67,33),(61,39)).assemble()).finalize().extrude(157).union(w1.sketch().arc((-99,-46),(68,74),(-48,-88)).arc((-37,-80),(-33,-66)).arc((49,59),(-57,-46)).arc((-78,-49),(-99,-46)).assemble().finalize().extrude(58))