import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,11,0))
r=w0.sketch().segment((-14,100),(-6,-66)).segment((-8,-66)).segment((-8,-100)).segment((-4,-100)).segment((-4,-72)).segment((14,-72)).segment((14,-73)).segment((12,-73)).segment((12,-76)).segment((14,-76)).segment((14,-89)).arc((2,0),(-14,100)).assemble().finalize().extrude(-22)