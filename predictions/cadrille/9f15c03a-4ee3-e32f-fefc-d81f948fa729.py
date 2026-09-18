import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,15))
w1=cq.Workplane('ZX',origin=(0,-65,0))
r=w0.sketch().segment((-50,-85),(50,-85)).segment((50,-58)).arc((0,-78),(-50,-58)).close().assemble().finalize().extrude(-40).union(w1.sketch().segment((-25,-98),(-23,-98)).segment((-23,-100)).segment((23,-100)).segment((23,-98)).segment((25,-98)).segment((25,98)).segment((23,98)).segment((23,100)).segment((-23,100)).segment((-23,98)).segment((-25,98)).close().assemble().rect(48,180,mode='s').finalize().extrude(150))