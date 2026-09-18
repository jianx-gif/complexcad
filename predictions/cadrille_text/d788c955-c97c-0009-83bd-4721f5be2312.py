import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,0,-71))
r=w0.sketch().segment((26,-62),(26,-58)).arc((24,-54),(26,-50)).segment((26,-46)).arc((22,-54),(26,-62)).assemble().finalize().extrude(101).union(w0.sketch().push([(0,5)]).circle(7).circle(6,mode='s').finalize().extrude(142)).union(w0.workplane(offset=143/2).moveTo(0,5).cylinder(143,3))