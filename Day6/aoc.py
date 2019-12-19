def distance_from_root(tree_dict):
    total_distance = 0
    children = tree_dict["COM"]
    distance = 1
    while len(children) > 0:
        total_distance += len(children) * distance
        distance += 1
        children_next = []
        for child in children:
            if child in tree_dict.keys():
                children_next += tree_dict[child]
        children = children_next
    return total_distance


def path_to_node(tree_dict, start, target, current_path):
    if start == target:
        return current_path
    if start not in tree_dict.keys():
        return []
    path = current_path.copy()
    path.append(start)
    children = tree_dict[start]
    for child in children:
        result = path_to_node(tree_dict, child, target, path)
        if len(result) > 0:
            return result
    return []




def distance_from_you_to_santa(tree_dict):
    path_to_you = set(path_to_node(tree_dict, "COM", "YOU", []))
    path_to_santa = set(path_to_node(tree_dict, "COM", "SAN", []))
    return len(path_to_you.symmetric_difference(path_to_santa))


if __name__ == "__main__":
    mappings = {"COM": []}
    for line in open("./part1.txt"):
        (parent, child) = line.split(')')
        if parent in mappings.keys():
            mappings[parent.strip()].append(child.strip())
        else:
            mappings[parent.strip()] = [child.strip()]
    print("Combined distances from root: {}".format(distance_from_root(mappings)))
    print("Orbital transfers from you to Santa: {}".format(distance_from_you_to_santa(mappings)))
