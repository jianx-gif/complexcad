import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-22))
r=w0.sketch().circle(37).circle(22,mode='s').finalize().extrude(-11).union(w0.sketch().circle(100).circle(88,mode='s').circle(22).finalize().extrude(44)).union(w0.sketch().circle(95).push([(-84,14)]).circle(14,mode='s').push([(0,0)]).circle(70,mode='s').finalize().extrude(55))