import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((91,-49),(100,-49)).segment((100,-47)).segment((93,-47)).arc((92,-48),(91,-49)).assemble().finalize().extrude(100).union(w0.sketch().push([(0,50)]).circle(4).push([(0,49.5)]).rect(4,5,mode='s').finalize().extrude(100))