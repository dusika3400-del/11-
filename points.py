from distance import find_closest

def add_two_points(p1, p2):
    """Складывает две точки"""
    return (p1[0] + p2[0], p1[1] + p2[1])

def process_all_points(points):
    """К каждой точке прибавляет ближайшую"""
    result = []
    
    for p in points:
        closest = find_closest(p, points)
        
        if closest:
            new_point = add_two_points(p, closest)
        else:
            new_point = p  # Если точка одна
        
        result.append(new_point)
    
    return result