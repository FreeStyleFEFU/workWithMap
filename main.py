from bs4 import BeautifulSoup
import math


def getsqr(coordlist):
    baselat = coordlist[0][0]
    baselon = coordlist[0][1]
    degreelen = 111300
    newcoord = []
    sqr = 0
    for now in coordlist:
        newcoord.append(((now[0] - baselat) * degreelen, (now[1] - baselon) * degreelen * math.sin(baselat)))
        sqr = 0
        for i in range(len(newcoord) - 1):
            sqr += newcoord[i][0] * newcoord[i + 1][1] - newcoord[i + 1][0] * newcoord[i][1]
            sqr += newcoord[-1][0] * newcoord[0][1] - newcoord[0][0] * newcoord[-1][1]

    return abs(sqr)


def nodes_quantity(all_nodes):
    print(f'Количество всех тегов node: {len(all_nodes)}')


def empty_nodes_quantity(all_nodes):
    empty_nodes_quantity = 0
    other_nodes_quantity = 0

    for node in all_nodes:
        tags = node('tag')
        if len(tags) == 0:
            empty_nodes_quantity += 1
        else:
            other_nodes_quantity += 1

    print(f'Пустых тегов node: {empty_nodes_quantity}')
    print(f'Node с одним tag: {other_nodes_quantity}')


def gas_station_quantity(all_nodes):
    gas_station_quantity = 0

    for node in all_nodes:
        for tag in node('tag'):
            if tag['k'] == 'amenity' and tag['v'] == 'fuel':
                gas_station_quantity += 1

    print(f'Количество АЗС: {gas_station_quantity}')


def all_gas_station_quantity(soup):
    gas_station_quantity = 0

    for tag in soup.findAll('tag'):
        if tag['k'] == 'amenity' and tag['v'] == 'fuel':
            gas_station_quantity += 1

    print(f'Количество всех АЗС: {gas_station_quantity}')


def work_with_ways():
    nodes_coords = {}
    nodes_areas = {}

    xml = open('mapcity.osm', 'r', encoding='utf8').read()
    soup = BeautifulSoup(xml, 'html.parser')

    for node in soup.findAll('node'):
        nodes_coords[node['id']] = [float(node["lat"]), float(node["lon"])]

    for way in soup.findAll('way'):
        nds = way('nd')
        if nds[0]['ref'] == nds[-1]['ref']:
            if list(filter(lambda tg: tg['k'] == 'building', way('tag'))):
                id = way['id']
                coords = list(map(lambda nd: nodes_coords[nd['ref']], nds))
                nodes_areas[id] = getsqr(coords)

                print(id)
                print(coords)

    print(f'Id здания с максимальной площадью: {max(nodes_areas, key=nodes_areas.get)}')



xml = open('map2.osm', 'r', encoding='utf8').read()
soup = BeautifulSoup(xml, 'html.parser')

all_nodes = soup.findAll('node')

work_with_ways()
nodes_quantity(all_nodes)
empty_nodes_quantity(all_nodes)
gas_station_quantity(all_nodes)
all_gas_station_quantity(soup)




