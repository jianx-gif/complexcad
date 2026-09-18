parts = [base]
parts.append(place(fastener("screw", 'M5-0.8', 16, 0), axis=(0, 0, 1), point=(-15, 0, 26), seat=-4, flip=True))
parts.append(place(fastener("nut", 'M5-0.8', 'M5', 0), axis=(0, 0, 1), point=(-15, 0, 26), seat=4, flip=False))
parts.append(place(fastener("screw", 'M5-0.8', 16, 1), axis=(0, 0, 1), point=(15, 0, 26), seat=-4, flip=True))
parts.append(place(fastener("nut", 'M5-0.8', 'M5', 1), axis=(0, 0, 1), point=(15, 0, 26), seat=4, flip=False))
