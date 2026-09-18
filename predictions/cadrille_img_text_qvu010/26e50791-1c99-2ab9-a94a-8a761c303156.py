import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-37,0))
r=w0.sketch().arc((-86,29),(-74,38),(-61,45)).arc((-76,40),(-86,29)).assemble().finalize().extrude(-53).union(w0.sketch().circle(100).circle(99,mode='s').finalize().extrude(112)).union(w0.sketch().arc((1,-82),(5,-81),(9,-80)).arc((10,-79),(12,-79)).arc((16,-78),(19,-78)).arc((-10,81),(1,-82)).assemble().finalize().extrude(130))