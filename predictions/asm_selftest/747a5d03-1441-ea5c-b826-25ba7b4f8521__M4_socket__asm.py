parts = [base]
parts.append(place(fastener("bearing", 30, 0), axis=(0, 0, 1), point=(0, 0, 13), seat=-4.5, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 30, 1), axis=(0, 0, 1), point=(34.5, 0, 3), seat=3, flip=True))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 1), axis=(0, 0, 1), point=(34.5, 0, 3), seat=27, flip=False))
