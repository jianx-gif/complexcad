import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('YZ',origin=(-58,0,0))
r=w0.sketch().arc((-46,-59),(-37,-54),(-28,-50)).arc((-38,-52),(-46,-59)).assemble().finalize().extrude(200).union(w1.sketch().arc((46,90),(-58,-61),(99,33)).arc((17,18),(46,90)).assemble().push([(10,-14)]).circle(69,mode='s').finalize().extrude(137))