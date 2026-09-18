import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,84,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-96,-76),(45,-90)).segment((46,-86)).segment((-95,-72)).close().assemble().finalize().extrude(-101).union(w1.sketch().segment((-99,17),(-63,17)).arc((-55,-38),(-18,-84)).segment((-18,-49)).arc((-55,0),(-18,49)).segment((-18,84)).arc((-55,70),(-63,25)).segment((-99,25)).close().assemble().reset().face(w1.sketch().arc((18,49),(55,38),(63,-1)).segment((99,-1)).segment((99,25)).segment((63,25)).arc((55,38),(45,49)).close().assemble()).finalize().extrude(-200))