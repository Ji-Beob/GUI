import xml.etree.ElementTree as ET


# 심볼 객체 정보
def ObjectToElement_Symbol(xml_obj):
    type = xml_obj.find("type").text
    class_ = xml_obj.find("class").text
    orientation = int(float(xml_obj.find('degree').text))
    type = xml_obj.find('type').text
    flip = xml_obj.find('flip').text
    if xml_obj.find('etc') != None:
        etc = xml_obj.find('etc').text
    else:
        etc = 'None'

    bndbox = xml_obj.find("bndbox")
    xmin = bndbox[0].text
    ymin = bndbox[1].text
    xmax = bndbox[2].text
    ymax = bndbox[3].text

    return class_, orientation, xmin, ymin, xmax, ymax, type, flip, str(etc)


# 라인 객체 정보
def ObjectToElement_Line(xml_obj):
    class_ = xml_obj.find("class").text
     
    edge = xml_obj.find("edge")
    xstart = edge[0].text
    ystart = edge[1].text
    xend = edge[2].text
    yend = edge[3].text

    if xml_obj.find("flow").text != None:
        flow = xml_obj.find("flow")
        arrows = flow[0]
        arrow_attr = []
        for i in range(0,len(arrows)):
            arrow = arrows[i]
            type = arrow[0].text
            degree = arrow[1].text
            location = arrow[2].text
            arrow_attr.append([type,degree,location])
    else:
        arrow_attr = []
        type = 'None'
        degree = 'None'
        location = 'None'
        arrow_attr.append([type,degree,location])
    
    if len(arrow_attr) == 1:
        return class_, xstart, ystart, xend, yend, type, degree, location, arrow_attr
    else:
        return class_, xstart, ystart, xend, yend, arrow_attr[0][0], arrow_attr[0][1], arrow_attr[0][2], arrow_attr


# 심볼 객체 읽기
def ParseXML_Symbol(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()                       # 최상위 tag 가져오기

    result_symbol = []
    object = 'symbol_object'

    for child in root.findall(object):
        class_, orientation, xmin, ymin, xmax, ymax, type, flip, etc = ObjectToElement_Symbol(child)
        result_symbol.append([type, class_, int(xmin), int(ymin), int(xmax), int(ymax), orientation, flip, etc])
    
    return result_symbol


# 라인 객체 읽기
def ParseXML_Line(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()                       # 최상위 tag 가져오기

    result_line = []
    object = 'line_object'

    arrow_attr = []
    for child in root.findall(object):
        class_, xstart, ystart, xend, yend, type, degree, location, arrow = ObjectToElement_Line(child)
        arrow_attr.append(arrow)
        result_line.append([class_, int(xstart), int(ystart), int(xend), int(yend), type, degree, location])
    
    return result_line, arrow_attr