import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,90,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-58,-45),(58,45)).arc((-15,38),(-58,-45)).assemble().finalize().extrude(-126).union(w1.sketch().arc((-95,-14),(-62,1),(-27,7)).arc((-27,13),(-19,13)).arc((14,29),(48,45)).arc((47,47),(47,49)).arc((47,51),(48,53)).arc((48,55),(50,57)).arc((53,69),(55,81)).arc((77,81),(95,90)).segment((-95,90)).close().assemble().finalize().extrude(-200))