import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,2,0))
w1=cq.Workplane('ZX',origin=(0,31,0))
r=w0.sketch().segment((-58,46),(-12,46)).segment((-12,1)).segment((12,1)).segment((12,-1)).segment((-12,-1)).segment((-12,-46)).segment((58,-46)).segment((58,46)).segment((12,46)).segment((12,48)).segment((-58,48)).close().assemble().finalize().extrude(-58).union(w1.sketch().circle(100).circle(97,mode='s').finalize().extrude(-59))