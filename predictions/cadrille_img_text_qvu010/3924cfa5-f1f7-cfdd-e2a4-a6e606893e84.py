import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-60,0))
w1=cq.Workplane('XY',origin=(0,0,56))
r=w0.sketch().segment((-94,-45),(-93,-45)).arc((0,-99),(93,-45)).segment((94,-45)).segment((94,45)).segment((93,45)).arc((0,99),(-93,45)).segment((-94,45)).close().assemble().finalize().extrude(140).union(w0.sketch().arc((-89,-19),(0,-99),(89,-19)).segment((88,-19)).arc((0,-98),(-88,-19)).close().assemble().finalize().extrude(160)).union(w1.sketch().arc((-48,-59),(0,-75),(48,-59)).close().assemble().finalize().extrude(-146))