import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().segment((-95,-84),(-93,-84)).segment((-93,-100)).segment((93,-100)).segment((93,-84)).segment((96,-84)).segment((96,84)).segment((93,84)).segment((93,100)).segment((-93,100)).segment((-93,84)).segment((-95,84)).close().assemble().finalize().extrude(-200)