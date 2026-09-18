import cadquery as cq
w0=cq.Workplane('XY',origin=(-55,0,-1))
r=w0.sketch().segment((34,-13),(55,-13)).segment((55,-1)).segment((34,-1)).arc((35,-7),(34,-13)).assemble().finalize().extrude(-9).union(w0.sketch().push([(5,0)]).circle(5).circle(4,mode='s').finalize().extrude(10)).union(w0.sketch().push([(5,0)]).circle(10).push([(5.5,0)]).rect(15,10,mode='s').finalize().extrude(101))