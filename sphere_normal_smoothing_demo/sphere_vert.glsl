
#version 330
in vec3 in_position;
uniform float time;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform int deform_mode; // <-- Nuevo uniform para seleccionar el modo

out vec3 v_normal;

void main() {
    vec3 pos = in_position;
    float deform = 0.0; // Valor de deformación inicial

    if (deform_mode == 0) {
        // Efecto 1: Ondas (el que ya tenías)
        deform = sin(time * 3.0 + pos.y * 10.0) * 0.1;
    } else if (deform_mode == 1) {
        // Efecto 2: Burbujas aleatorias (efecto de "ruido")
        // Necesitas una función de ruido, como 'noise' o 'perlin_noise'
        // Este es solo un ejemplo simplificado que puedes usar:
        deform = fract(sin(dot(pos.xy, vec2(12.9898, 78.233))) * 43758.5453) * 0.2;
    } else if (deform_mode == 2) {
        // Efecto 3: Pinchos
        // Un simple efecto de "punta" que se activa y desactiva
        float dist_from_center = length(pos);
        deform = sin(time * 5.0) * dist_from_center * 0.5;
    }
    // Puedes añadir más efectos con más 'else if'

    pos += normalize(pos) * deform;
    v_normal = normalize(pos);
    gl_Position = projection * view * model * vec4(pos, 1.0);
}
