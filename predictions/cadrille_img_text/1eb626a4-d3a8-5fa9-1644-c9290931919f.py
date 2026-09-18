import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().arc((-50,-38),(50,40),(-48,-40)).segment((-37,-40)).arc((43,38),(-49,-28)).segment((-50,-28)).close().assemble().finalize().extrude(-200).union(w0.sketch().arc((-99,-44),(64,56),(-36,-93)).arc((-29,-89),(-24,-83)).arc((51,49),(-87,-18)).arc((-93,-30),(-99,-44)).assemble().finalize().extrude(-24))