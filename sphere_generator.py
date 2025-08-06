import numpy as np

def generate_sphere_data(subdivisions):
    """
    Genera los vértices e índices de una esfera usando el método de
    subdivisión de un icosaedro.

    Args:
        subdivisions (int): El número de veces que se subdividirá el icosaedro.
                            Cada subdivisión aumenta la resolución.

    Returns:
        tuple: Una tupla con los vértices (numpy.ndarray) y los índices (numpy.ndarray).
    """

    # Vértices de un icosaedro base (20 caras triangulares)
    t = (1.0 + np.sqrt(5.0)) / 2.0
    vertices = np.array([
        [-1, t, 0], [1, t, 0], [-1, -t, 0], [1, -t, 0],
        [0, -1, t], [0, 1, t], [0, -1, -t], [0, 1, -t],
        [t, 0, -1], [t, 0, 1], [-t, 0, -1], [-t, 0, 1]
    ], dtype=np.float32)

    # Normalizar los vértices para que estén en la superficie de una esfera unitaria
    vertices /= np.linalg.norm(vertices, axis=1, keepdims=True)

    # Índices del icosaedro
    indices = np.array([
        0, 11, 5, 0, 5, 1, 0, 1, 7, 0, 7, 10, 0, 10, 11,
        1, 5, 9, 5, 11, 4, 11, 10, 2, 10, 7, 6, 7, 1, 8,
        3, 9, 4, 3, 4, 2, 3, 2, 6, 3, 6, 8, 3, 8, 9,
        4, 9, 5, 2, 4, 11, 6, 2, 10, 8, 6, 7, 9, 8, 1
    ], dtype=np.uint32)

    # Subdivisión del icosaedro para aumentar la resolución
    for _ in range(subdivisions):
        new_indices = []
        # Mapa de aristas para evitar duplicados
        middle_points = {}

        for i in range(0, len(indices), 3):
            v1_idx, v2_idx, v3_idx = indices[i], indices[i+1], indices[i+2]

            # Encontrar los puntos medios de las aristas y normalizarlos
            m12_idx, vertices = get_middle_point(v1_idx, v2_idx, vertices, middle_points) # Actualiza 'vertices'
            m23_idx, vertices = get_middle_point(v2_idx, v3_idx, vertices, middle_points) # Actualiza 'vertices'
            m31_idx, vertices = get_middle_point(v3_idx, v1_idx, vertices, middle_points) # Actualiza 'vertices'

            # Reemplazar el triángulo grande con 4 triángulos más pequeños
            new_indices.extend([v1_idx, m12_idx, m31_idx])
            new_indices.extend([v2_idx, m23_idx, m12_idx])
            new_indices.extend([v3_idx, m31_idx, m23_idx])
            new_indices.extend([m12_idx, m23_idx, m31_idx])
        
        indices = np.array(new_indices, dtype=np.uint32)

    return vertices, indices

def get_middle_point(p1, p2, vertices, middle_points):
    """
    Calcula el punto medio de una arista y lo normaliza, agregándolo a los vértices
    si no existe ya.
    """
    smaller, larger = min(p1, p2), max(p1, p2)
    key = (smaller, larger)

    if key in middle_points:
        return middle_points[key], vertices # Devuelve el vértice existente y el array sin modificar

    v1, v2 = vertices[p1], vertices[p2]
    middle = (v1 + v2) / 2.0
    middle /= np.linalg.norm(middle)

    new_index = len(vertices)
    vertices = np.vstack([vertices, middle]) # `vstack` crea un nuevo array, no lo modifica en el lugar
    middle_points[key] = new_index

    return new_index, vertices # Devuelve el nuevo índice y el array actualizado

# --- CÓMO USAR LA FUNCIÓN PARA GENERAR LOS ARCHIVOS ---

# Generar una esfera con 3 subdivisiones
vertices_high_res, indices_high_res = generate_sphere_data(subdivisions=4)

# Guardar los archivos
np.save("vertices_high_res.npy", vertices_high_res)
np.save("indices_high_res.npy", indices_high_res)