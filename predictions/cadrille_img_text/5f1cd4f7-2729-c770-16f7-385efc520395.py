import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().arc((-59,-90),(-57,-91),(-55,-92)).segment((-55,-90)).close().assemble().reset().face(w0.sketch().arc((-48,-96),(0,-80),(48,-60)).segment((59,96)).segment((20,99)).segment((20,96)).arc((0,80),(-20,60)).close().assemble()).finalize().extrude(200)