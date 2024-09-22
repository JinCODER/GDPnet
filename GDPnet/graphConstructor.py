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

        ## 以下逻辑判断部分需要修改
        ### 元素序数，0/1 非金/金

        if elementName[i] == 'Cl':
            G.add_node(i, elementNumber = 17)
            G.add_node(i, isMetal = 0)
        elif elementName[i] == 'Na':
            G.add_node(i, elementNumber = 11)
            G.add_node(i, isMetal = 1)
        elif elementName[i] == 'K':
            G.add_node(i, elementNumber = 19)
            G.add_node(i, isMetal = 1)
        elif elementName[i] == 'W':
            G.add_node(i, elementNumber = 74)
            G.add_node(i, isMetal = 1)
        elif elementName[i] == 'O':
            G.add_node(i, elementNumber = 8)
            G.add_node(i, isMetal = 0)
        elif elementName[i] == 'Co':
            G.add_node(i, elementNumber = 27)
            G.add_node(i, isMetal = 1)
        i += 1
    
    for j in range(len(G.nodes())):
        for k in range(len(G.nodes())):
            if j != k:
                G.add_edge(j, k)

    return G
