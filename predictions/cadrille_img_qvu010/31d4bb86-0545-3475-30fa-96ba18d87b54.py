import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-65,0))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().push([(-87,50)]).circle(13).push([(87,50)]).circle(13).finalize().extrude(12).union(w0.sketch().segment((-97,-49),(-96,-50)).segment((97,49)).segment((96,50)).close().assemble().finalize().extrude(164)).union(w1.sketch().segment((-96,-64),(84,-64)).arc((82,-62),(80,-60)).segment((-80,-60)).arc((-82,-62),(-84,-64)).segment((78,-64)).arc((81,-62),(83,-60)).segment((-80,-60)).arc((-82,-62),(-84,-64)).close().assemble().finalize().extrude(200))