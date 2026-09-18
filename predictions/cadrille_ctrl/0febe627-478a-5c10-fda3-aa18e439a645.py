import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('YZ',origin=(-40,0,0))
r=w0.sketch().rect(84,64).circle(28,mode='s').finalize().extrude(-6).union(w1.sketch().rect(64,12).rect(56,2,mode='s').finalize().extrude(82))
