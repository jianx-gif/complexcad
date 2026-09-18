import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,99,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((-65,-66),(-64,-66)).arc((-63,-64),(-61,-66)).segment((65,-66)).segment((65,66)).segment((-65,66)).close().assemble().finalize().extrude(-156).union(w0.sketch().segment((-48,59),(-44,-61)).segment((48,-59)).segment((44,61)).close().assemble().finalize().extrude(-108)).union(w1.sketch().segment((-87,-66),(87,-66)).segment((87,-64)).arc((0,-86),(-87,-64)).close().assemble().push([(59,-57)]).circle(15,mode='s').finalize().extrude(200))