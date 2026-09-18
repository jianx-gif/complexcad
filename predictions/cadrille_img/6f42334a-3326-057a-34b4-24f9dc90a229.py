import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
w1=cq.Workplane('XY',origin=(0,0,26))
r=w0.sketch().arc((-97,-35),(-35,-59),(28,-39)).segment((97,-3)).segment((97,-2)).segment((29,-37)).arc((-20,35),(-95,39)).arc((-94,37),(-93,35)).arc((-94,33),(-94,31)).arc((-96,29),(-97,27)).close().assemble().finalize().extrude(-185).union(w0.sketch().arc((-74,-10),(-15,-19),(35,-51)).arc((14,79),(-74,-10)).assemble().finalize().extrude(-175)).union(w1.sketch().push([(0,-15)]).circle(20).circle(13,mode='s').finalize().extrude(-10))