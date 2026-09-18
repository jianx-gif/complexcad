import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('XY',origin=(0,0,79))
r=w0.sketch().segment((-79,10),(-67,10)).segment((-67,12)).segment((-15,-40)).segment((-15,-42)).segment((-13,-42)).segment((-11,-44)).segment((-10,-42)).segment((-9,-42)).segment((-9,-41)).segment((27,10)).segment((55,10)).arc((-13,62),(-79,10)).assemble().finalize().extrude(-200).union(w0.sketch().arc((-15,-73),(-13,-63),(-15,-53)).close().assemble().finalize().extrude(-192)).union(w1.sketch().arc((-27,19),(-26,18),(-26,17)).arc((-19,26),(-27,19)).assemble().finalize().extrude(-139))