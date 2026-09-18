import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-87,0))
w1=cq.Workplane('XY',origin=(0,0,48))
r=w0.sketch().segment((-98,59),(-96,61)).arc((-97,-26),(-43,-83)).segment((-45,-85)).arc((26,-92),(83,-49)).segment((81,-51)).arc((82,36),(20,83)).segment((22,85)).arc((-40,92),(-96,49)).segment((-94,51)).arc((-95,50),(-95,49)).close().assemble().finalize().extrude(185).union(w1.sketch().segment((-100,-100),(-66,-100)).arc((-86,-66),(-100,-30)).close().assemble().finalize().extrude(-148))