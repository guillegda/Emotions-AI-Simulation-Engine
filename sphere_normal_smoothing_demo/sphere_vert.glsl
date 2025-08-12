#version 330
in vec3 in_position;
uniform float time;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform float velocidad;
uniform float rugosidad;
uniform float distorsion;

uniform int deform_mode_A;
uniform int deform_mode_B;
uniform float blend_factor;

uniform float effect1_amnt_A;
uniform float effect2_amnt_A;
uniform float effect3_amnt_A;
uniform float effect1_amnt_B;
uniform float effect2_amnt_B;
uniform float effect3_amnt_B;

out vec3 v_normal;

vec2 hash(vec2 p) {
    p = vec2(dot(p, vec2(127.1, 311.7)),
             dot(p, vec2(269.5, 183.3)));
    return fract(sin(p) * 43758.5453);
}

float perlin_noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    vec2 u = f * f * (3.0 - 2.0 * f);

    float a = dot(hash(i + vec2(0.0, 0.0)), f - vec2(0.0, 0.0));
    float b = dot(hash(i + vec2(1.0, 0.0)), f - vec2(1.0, 0.0));
    float c = dot(hash(i + vec2(0.0, 1.0)), f - vec2(0.0, 1.0));
    float d = dot(hash(i + vec2(1.0, 1.0)), f - vec2(1.0, 1.0));

    return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
}

// Función que calcula la deformación para un modo específico
float get_single_deform(vec3 pos, float t, int mode) {
    float deform = 0.0;
    if (mode == 0) {
        deform = sin(t * velocidad + pos.y * rugosidad) * distorsion;
    } else if (mode == 1) {
        float noise_val = perlin_noise(pos.xy * rugosidad/10 + vec2(t * velocidad/4));
        deform = noise_val * distorsion * 2;
    } else if (mode == 2) {
        vec2 uv_coords = vec2(atan(pos.x, pos.z), pos.y);
        float noise_val = perlin_noise(uv_coords * rugosidad + vec2(t * velocidad));
        deform = noise_val * distorsion * 10;
    }
    return deform;
}

// Función que mezcla los efectos según los porcentajes
float get_hybrid_deform(vec3 pos, float t, float amnt1, float amnt2, float amnt3) {
    float deform1 = get_single_deform(pos, t, 0) * amnt1;
    float deform2 = get_single_deform(pos, t, 1) * amnt2;
    float deform3 = get_single_deform(pos, t, 2) * amnt3;
    return deform1 + deform2 + deform3;
}

void main() {
    vec3 pos = in_position;

    float deform_A, deform_B;

    // Calculamos la deformación para el modo actual (A)
    if (deform_mode_A == 3) {
        // Modo Híbrido
        deform_A = get_hybrid_deform(in_position, time, effect1_amnt_A, effect2_amnt_A, effect3_amnt_A);
    } else {
        // Modos puros
        deform_A = get_single_deform(in_position, time, deform_mode_A);
    }

    // Calculamos la deformación para el modo siguiente (B)
    if (deform_mode_B == 3) {
        // Modo Híbrido
        deform_B = get_hybrid_deform(in_position, time, effect1_amnt_B, effect2_amnt_B, effect3_amnt_B);
    } else {
        // Modos puros
        deform_B = get_single_deform(in_position, time, deform_mode_B);
    }

    vec3 pos_A = in_position + normalize(in_position) * deform_A;
    vec3 pos_B = in_position + normalize(in_position) * deform_B;
    vec3 final_pos = mix(pos_A, pos_B, blend_factor);

    v_normal = normalize(final_pos);
    gl_Position = projection * view * model * vec4(final_pos, 1.0);
}