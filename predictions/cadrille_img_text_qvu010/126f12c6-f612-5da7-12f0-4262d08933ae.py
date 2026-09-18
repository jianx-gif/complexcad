import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-77,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((-65,-16),(84,-28)).arc((85,-24),(86,-20)).segment((-64,-8)).close().assemble().finalize().extrude(166).union(w1.sketch().segment((-97,-81),(-81,-81)).arc((-79,-78),(-77,-81)).segment((97,-81)).segment((97,-78)).segment((-97,-78)).close().assemble().finalize().extrude(200))