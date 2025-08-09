#version 330
in vec3 in_position;
uniform float time;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform float velocidad;
uniform float rugosidad;
uniform float distorsion;

// Uniforms para la interpolación lineal
uniform int deform_mode_A; // Modo de deformación actual
uniform int deform_mode_B; // Modo de deformación al que se transiciona
uniform float blend_factor; // Factor de mezcla de 0.0 a 1.0

// Porcentaje de cada efecto para poder crear efectos hibridos
uniform float effect1_amnt_A;
uniform float effect2_amnt_A;
uniform float effect3_amnt_A;
uniform float effect1_amnt_B;
uniform float effect2_amnt_B;
uniform float effect3_amnt_B;

out vec3 v_normal;

// Función de ruido de Perlin 2D
vec2 hash(vec2 p) {
    p = vec2(dot(p, vec2(127.1, 311.7)),
             dot(p, vec2(269.5, 183.3)));
    return fract(sin(p) * 43758.5453);
}

float perlin_noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);

    vec2 u = f * f * (3.0 - 2.0 * f);

    // Cuatro esquinas de la celda
    float a = dot(hash(i + vec2(0.0, 0.0)), f - vec2(0.0, 0.0));
    float b = dot(hash(i + vec2(1.0, 0.0)), f - vec2(1.0, 0.0));
    float c = dot(hash(i + vec2(0.0, 1.0)), f - vec2(0.0, 1.0));
    float d = dot(hash(i + vec2(1.0, 1.0)), f - vec2(1.0, 1.0));

    // Interpolación
    return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
}

// Función para calcular un modo de deformación específico
float get_deform(vec3 pos, float t, int mode) {
    float deform = 0.0;
    if (mode == 0) {
        // Efecto 1: Ondas (funciona correctamente)
        deform = sin(t * velocidad + pos.y * rugosidad) * distorsion;
    } else if (mode == 1) {
        // Efecto 2: Ruido de Perlin animado sobre la superficie
        // Usamos una combinación de coordenadas polares para que el patrón no gire con el objeto
        float noise_val = perlin_noise(pos.xy * rugosidad/10 + vec2(t * velocidad/4));
        deform = noise_val * distorsion *2;
    } else if (mode == 2) {
        // Efecto 3: Pinchos animados con ruido de Perlin
        // También usando coordenadas polares
        vec2 uv_coords = vec2(atan(pos.x, pos.z), pos.y);
        float noise_val = perlin_noise(uv_coords * rugosidad + vec2(t * velocidad));
        deform = noise_val * distorsion*10;
    }
    return deform;
}

float get_hybrid_deform(vec3 pos, float t, float mode1_index, float mode2_index, float mode3_index) {
    float deform = 0.0;
    // Efecto 1: Ondas (funciona correctamente)
    deform += (sin(t * velocidad + pos.y * rugosidad) * distorsion) * mode1_index;
    // Efecto 2: Ruido de Perlin animado sobre la superficie
    // Usamos una combinación de coordenadas polares para que el patrón no gire con el objeto
    float noise_val = perlin_noise(pos.xy * rugosidad/10 + vec2(t * velocidad/4));
    deform += (noise_val * distorsion *2) * mode2_index;
    // Efecto 3: Pinchos animados con ruido de Perlin
    // También usando coordenadas polares
    vec2 uv_coords = vec2(atan(pos.x, pos.z), pos.y);
    float noise_val = perlin_noise(uv_coords * rugosidad + vec2(t * velocidad));
    deform += (noise_val * distorsion*10) * mode3_index;
    return deform;
}

void main() {
    vec3 pos = in_position;
    
    float deform_A = get_deform(in_position, time, deform_mode_A);
    vec3 pos_A = in_position + normalize(in_position) * deform_A;

    float deform_B = get_deform(in_position, time, deform_mode_B);
    vec3 pos_B = in_position + normalize(in_position) * deform_B;

    vec3 final_pos = mix(pos_A, pos_B, blend_factor);

    v_normal = normalize(final_pos);
    gl_Position = projection * view * model * vec4(final_pos, 1.0);
}