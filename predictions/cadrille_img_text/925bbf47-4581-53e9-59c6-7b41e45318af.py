import cadquery as cq
w0=cq.Workplane('YZ',origin=(-71,0,0))
w1=cq.Workplane('ZX',origin=(0,-28,0))
r=w0.sketch().arc((-40,66),(-33,62),(-27,57)).arc((-32,63),(-40,66)).assemble().reset().face(w0.sketch().arc((27,45),(33,51),(40,57)).arc((33,62),(27,66)).arc((32,56),(27,45)).assemble()).finalize().extrude(171).union(w1.sketch().arc((-59,84),(0,-53),(59,84)).close().assemble().push([(23,29)]).circle(53,mode='s').finalize().extrude(19))