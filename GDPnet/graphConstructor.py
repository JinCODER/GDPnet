def graphEncoding(energy,
                  coordinatesFrame, 
                  elementName) -> nx.Graph:
    # 从read_and_process_xyz方法给出的数据中构建图
    # energy是一个浮点数，为图的属性值
    # coordinatesFrame是一个列表，其中包含每个帧的坐标，为图的coord矩阵
    # elementName是一个列表，其中包含每个原子的元素名称，为图的节点名称
    G = nx.Graph()
    G.graph['y'] = energy

    elementAppearanceNumber = {}
    for e in elementName:
        if e in elementAppearanceNumber:
            elementAppearanceNumber[e] += 1
        else:
            elementAppearanceNumber[e] = 1

    ### 单个原子受力的计算方法有误
    atomCalculationNumber = np.array([list(elementAppearanceNumber.values())])
    energyCalculationNumber = np.array([energy])
    x, residuals, rank, s = np.linalg.lstsq(atomCalculationNumber, energyCalculationNumber, rcond=None)

    numCount = 0
    for ele in elementAppearanceNumber:
        elementAppearanceNumber[ele] = x[numCount]
        numCount += 1
    
    i = 0
    for coor in coordinatesFrame[i]:
        G.add_node(i, coord = coor)
        G.add_node(i, element = elementName[i])
        G.add_node(i, atomForce = elementAppearanceNumber[elementName[i]])

        #for e,element in enumerate(elementName):
        if elementName[i] in elementsDict:
            G.add_node(i, elementNumber = elementsDict[elementName[i]]['elementNumber'])
            G.add_node(i, isMetal = elementsDict[elementName[i]]['isMetal'])
        else:
            print(f"Element {elementName[i]} not found in the dictionary.")
        i += 1
    
    for j in range(len(G.nodes())):
        for k in range(len(G.nodes())):
            if j != k:
                G.add_edge(j, k)

    return G
