import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-12))
w1=cq.Workplane('YZ',origin=(72,0,0))
r=w0.sketch().arc((-97,-25),(97,-25),(-75,67)).arc((-96,25),(-97,-25)).assemble().finalize().extrude(26).union(w0.workplane(offset=56/2).moveTo(0,1).cylinder(56,25)).union(w1.sketch().push([(-50,0)]).circle(32).circle(13,mode='s').finalize().extrude(-141))