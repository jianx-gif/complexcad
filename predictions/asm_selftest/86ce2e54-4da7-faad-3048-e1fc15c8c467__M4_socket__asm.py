parts = [base]
parts.append(place(fastener("screw", 'M4-0.7', 10, 0), axis=(0, 0, 1), point=(-20, 0, 0.25), seat=3.55, flip=True))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 0), axis=(0, 0, 1), point=(-20, 0, 0.25), seat=7.75, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 10, 1), axis=(0, 0, 1), point=(20, 0, 0.25), seat=3.55, flip=True))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 1), axis=(0, 0, 1), point=(20, 0, 0.25), seat=7.75, flip=False))
