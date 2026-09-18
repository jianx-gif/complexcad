import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-2,0))
w1=cq.Workplane('XY',origin=(0,0,37))
r=w0.sketch().segment((-100,-11),(-97,-23)).arc((-89,-45),(-74,-65)).segment((-71,-77)).segment((-62,-74)).arc((45,-82),(97,11)).segment((100,11)).segment((97,23)).arc((89,45),(74,65)).segment((71,77)).segment((62,74)).arc((-45,82),(-97,-11)).close().assemble().circle(64,mode='s').finalize().extrude(-1).union(w0.sketch().circle(88).circle(64,mode='s').finalize().extrude(20)).union(w1.workplane(offset=-37/2).moveTo(-83,-2).cylinder(37,16))