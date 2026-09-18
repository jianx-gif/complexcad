import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
w1=cq.Workplane('ZX',origin=(0,-50,0))
r=w0.sketch().arc((-56,-46),(-45,-43),(-35,-43)).arc((28,43),(-30,-45)).arc((-24,-61),(-26,-78)).arc((39,64),(-56,-46)).assemble().finalize().extrude(-162).union(w0.sketch().arc((-28,-99),(12,-1),(70,80)).arc((-59,31),(-28,-99)).assemble().finalize().extrude(-16)).union(w1.sketch().arc((-39,12),(-40,10),(-38,9)).arc((56,31),(-39,12)).assemble().finalize().extrude(-50))