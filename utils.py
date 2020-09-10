from random import sample

def print_node_zipcode_stats(g):
    num_nodes = len(g.nodes())
    num_nodes_missing_zipcodes = len([x for x in g.nodes() if not g.nodes()[x].get('zipcode')])

    print('number of nodes: ' + str(num_nodes))
    print('number of nodes missing zipcodes: ' + str(num_nodes_missing_zipcodes))
    print('percent missing zips: ' + str((num_nodes_missing_zipcodes / num_nodes)))


def random_nodes(g, num=1):
    random_nodes = sample(list(g.nodes()), num)

    return [g.nodes()[x] for x in random_nodes]


def decode_polyline(polyline_str):
    '''Pass a Google Maps encoded polyline string; returns list of lat/lon pairs
       WRITTEN BY mgd722
    '''
    index, lat, lng = 0, 0, 0
    coordinates = []
    changes = {'latitude': 0, 'longitude': 0}

    # Coordinates have variable length when encoded, so just keep
    # track of whether we've hit the end of the string. In each
    # while loop iteration, a single coordinate is decoded.
    while index < len(polyline_str):
        # Gather lat/lon changes, store them in a dictionary to apply them later
        for unit in ['latitude', 'longitude']:
            shift, result = 0, 0

            while True:
                byte = ord(polyline_str[index]) - 63
                index += 1
                result |= (byte & 0x1f) << shift
                shift += 5
                if not byte >= 0x20:
                    break

            if (result & 1):
                changes[unit] = ~(result >> 1)
            else:
                changes[unit] = (result >> 1)

        lat += changes['latitude']
        lng += changes['longitude']

        coordinates.append((lat / 100000.0, lng / 100000.0))

    return coordinates
