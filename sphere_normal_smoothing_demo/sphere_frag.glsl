
#version 330
in vec3 v_normal;
out vec4 f_color;
uniform float time;

void main() {
    vec3 normal = normalize(v_normal);

    // Color base del material de la esfera
    float r = 0.6 + 0.4 * sin(time);
    float g = 0.5 + 0.5 * cos(time * 1.2);
    float b = 0.7 + 0.3 * sin(time * 0.8);
    vec3 base_color = vec3(r, g, b);

    // --- Primer foco de luz ---
    vec3 light_dir1 = normalize(vec3(0.0, 1.0, 1.0));
    // Calculamos el valor difuso para el primer foco de luz
    float diff1 = max(dot(normal, light_dir1), 0.0);
    // Asignamos un color a esta luz (ej. blanco)
    vec3 light_color1 = vec3(1.0, 1.0, 1.0);
    // Calculamos la contribución del primer foco
    vec3 light_contribution1 = light_color1 * diff1 * 0.8;

    // --- Segundo foco de luz ---
    vec3 light_dir2 = normalize(vec3(0.0, -1.0, 1.0));
    // Calculamos el valor difuso para el segundo foco de luz
    float diff2 = max(dot(normal, light_dir2), 0.0);
    // Asignamos un color a esta luz (ej. blanco)
    vec3 light_color2 = vec3(1.0, 1.0, 1.0);
    // Calculamos la contribución del segundo foco
    vec3 light_contribution2 = light_color2 * diff2 * 0.5;

    // Sumamos las contribuciones de ambas luces
    vec3 final_light_contribution = light_contribution1 + light_contribution2;

    // El color final del píxel es el color base multiplicado por la contribución total de luz
    f_color = vec4(base_color * final_light_contribution, 1.0);
}
