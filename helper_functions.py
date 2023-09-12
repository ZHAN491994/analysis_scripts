def find_dips(wavelengths, trans, thres):
    wavel, tr = [], []
    dip_wavels = []
    for i in range(len(trans)-1):
        if trans[i] > thres and trans[i+1] < thres:
            wavel.append(wavelengths[i])
            wavel.append(wavelengths[i+1])
            tr.append(trans[i])
            tr.append(trans[i+1])
        if trans[i] < thres and trans[i+1] > thres:
            wavel.append(wavelengths[i])
            wavel.append(wavelengths[i+1])
            tr.append(trans[i])
            tr.append(trans[i+1])

    for i in range(0, len(wavel), 4):
        w_l = lin_interp(thres, tr[i], wavel[i], tr[i+1], wavel[i+1])
        # w_u = lin_interp(thres, tr[i+2], wavel[i+2], tr[i+3], wavel[i+3])
        if i+2 < len(tr):
            w_u = lin_interp(thres, tr[i+2], wavel[i+2], tr[i+3], wavel[i+3])
        else:
            break
        
        dip_wavels.append((w_l + w_u) / 2)

    return dip_wavels

def find_dips_robust(wavelengths, trans, thres):
    wavel, tr = [], []
    dip_wavels = []
    find_l = False
    for i in range(len(trans)-1):
        if trans[i] > thres and trans[i+1] < thres:
            find_l = True
            wavel.append(wavelengths[i])
            wavel.append(wavelengths[i+1])
            tr.append(trans[i])
            tr.append(trans[i+1])
        
        if find_l and trans[i] < thres and trans[i+1] > thres:
            wavel.append(wavelengths[i])
            wavel.append(wavelengths[i+1])
            tr.append(trans[i])
            tr.append(trans[i+1])
            find_l = False
    
    for i in range(0, len(wavel), 4):
        w_l = lin_interp(thres, tr[i], wavel[i], tr[i+1], wavel[i+1])
        if i+2 < len(tr):
            w_u = lin_interp(thres, tr[i+2], wavel[i+2], tr[i+3], wavel[i+3])
        else: 
            break
        
        dip_wavels.append((w_l + w_u) / 2)

    return dip_wavels

def lin_interp(x, x0, y0, x1, y1):
    y = y0 + ((y1 - y0) / (x1 - x0)) * (x - x0)
    return y

def find_index(target, arr):
    for id, elem in enumerate(arr):
        if abs(elem - target) < 1e-4:
            return id