import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().segment((-94,-93),(-83,-93)).segment((-83,-100)).segment((83,-100)).segment((83,-93)).segment((96,-93)).segment((96,93)).segment((83,93)).segment((83,100)).segment((-83,100)).segment((-83,93)).segment((-94,93)).close().assemble().finalize().extrude(-200)