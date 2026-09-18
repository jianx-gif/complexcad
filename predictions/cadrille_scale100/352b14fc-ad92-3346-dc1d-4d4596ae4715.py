import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,40))
r=w0.sketch().arc((11,-39),(12,-37),(14,-38)).arc((11,-36),(11,-39)).assemble().finalize().extrude(-119).union(w0.sketch().circle(40).circle(35,mode='s').finalize().extrude(40)).union(w0.sketch().circle(35).push([(-24,20)]).circle(10,mode='s').push([(15,-16)]).circle(2,mode='s').finalize().extrude(48))