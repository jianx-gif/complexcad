import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().arc((11,-12),(12,-11),(13,-11)).segment((13,-10)).segment((11,-10)).close().assemble().finalize().extrude(-50).union(w0.sketch().arc((17,-24),(17,-21),(19,-23)).arc((28,-11),(29,4)).segment((29,-6)).segment((17,-6)).segment((17,13)).segment((27,13)).arc((-29,8),(17,-24)).assemble().push([(9,0)]).circle(10,mode='s').finalize().extrude(50)).union(w0.workplane(offset=50/2).moveTo(9,0).cylinder(50,11))
