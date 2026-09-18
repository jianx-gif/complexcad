import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().push([(-6,0)]).rect(188,140).rect(94,48,mode='s').finalize().extrude(-12).union(w0.sketch().segment((89,-2),(100,-2)).segment((100,2)).segment((89,2)).arc((90,0),(89,-2)).assemble().finalize().extrude(13))