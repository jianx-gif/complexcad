import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-92))
w1=cq.Workplane('YZ',origin=(-59,0,0))
r=w0.sketch().segment((-66,-11),(-26,-11)).arc((-48,26),(-66,66)).close().assemble().finalize().extrude(182).union(w0.sketch().segment((-95,-16),(-66,-16)).segment((-66,-46)).segment((-63,-46)).segment((-63,-16)).segment((39,28)).segment((-95,28)).close().assemble().finalize().extrude(192)).union(w1.sketch().arc((-94,-43),(-64,-33),(-34,-27)).arc((-28,19),(10,48)).arc((13,54),(17,60)).segment((-94,60)).close().assemble().push([(-21,-39)]).circle(15,mode='s').finalize().extrude(143))