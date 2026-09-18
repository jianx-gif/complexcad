import cadquery as cq
w0=cq.Workplane('XY',origin=(-43,-100,-13))
r=w0.sketch().segment((38,-43),(43,-43)).segment((43,-31)).arc((41,-38),(38,-43)).assemble().finalize().extrude(-7).union(w0.sketch().push([(41,0)]).circle(3).circle(2,mode='s').finalize().extrude(29)).union(w0.sketch().push([(41,0)]).circle(3).circle(2,mode='s').finalize().extrude(33))