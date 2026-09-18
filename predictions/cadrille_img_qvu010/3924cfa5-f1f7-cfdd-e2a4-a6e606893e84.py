import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-59,0))
w1=cq.Workplane('XY',origin=(0,0,56))
r=w0.sketch().segment((-57,-39),(57,-39)).segment((57,39)).segment((-57,39)).segment((-57,3)).arc((-84,-3),(-57,-9)).close().assemble().finalize().extrude(12).union(w0.sketch().segment((-93,-43),(89,-99)).segment((93,-84)).segment((93,43)).segment((-89,99)).close().assemble().finalize().extrude(159)).union(w1.sketch().arc((-49,-99),(0,-84),(49,-99)).segment((49,-63)).arc((0,-78),(-49,-63)).close().assemble().finalize().extrude(-129))