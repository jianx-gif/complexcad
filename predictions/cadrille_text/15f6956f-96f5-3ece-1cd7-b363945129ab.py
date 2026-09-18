import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-3))
r=w0.sketch().segment((92,-43),(92,-37)).segment((97,-37)).arc((100,-34),(100,-30)).arc((98,-29),(100,-28)).arc((33,10),(92,-43)).assemble().finalize().extrude(70).union(w0.sketch().push([(50,-5)]).circle(20).push([(50,-4.5)]).rect(24,13,mode='s').finalize().extrude(77))