import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-16,0))
w1=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().push([(0,28)]).circle(21).push([(21,29)]).circle(3,mode='s').finalize().extrude(-11).union(w0.sketch().arc((19,84),(24,73),(28,61)).arc((39,76),(56,84)).close().assemble().finalize().extrude(11)).union(w1.sketch().arc((-20,-61),(11,-76),(43,-84)).arc((56,-1),(80,81)).arc((27,95),(-20,75)).close().assemble().finalize().extrude(-184))