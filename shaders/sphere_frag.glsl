
#version 330
in vec3 v_normal;
out vec4 f_color;
uniform float time;
uniform vec3 base_color;
uniform vec3 light_color1;
uniform vec3 light_color2;


void main() {
    vec3 normal = normalize(v_normal);

    

    // --- Primer foco de luz ---
    vec3 light_dir1 = normalize(vec3(0.0, 1.0, 1.0));
    float diff1 = max(dot(normal, light_dir1), 0.0);
    vec3 light_contribution1 = light_color1 * diff1 * 1.5;

    // --- Segundo foco de luz ---
    vec3 light_dir2 = normalize(vec3(0.0, -1.0, 1.0));
    float diff2 = max(dot(normal, light_dir2), 0.0);
    vec3 light_contribution2 = light_color2 * diff2;

    //Apoyo del segundo foco
    vec3 light_dir_supp = normalize(vec3(0.0, -1.0, -1.0));
    float diff_supp = max(dot(normal, light_dir_supp), 0.0);
    vec3 light_color_supp = vec3(1.0, 1.0, 1.0);
    vec3 light_contribution_supp = light_color2 * diff_supp * 5.0;

    vec3 final_light_contribution = light_contribution1 + light_contribution2 + light_contribution_supp;

    f_color = vec4(base_color * final_light_contribution, 1.0);
}
