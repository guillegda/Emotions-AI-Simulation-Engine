
#version 330
in vec3 in_position;
uniform float time;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {
    vec3 pos = in_position;
    float deform = sin(time * 3.0 + pos.y * 10.0) * 0.1;
    pos += normalize(pos) * deform;
    gl_Position = projection * view * model * vec4(pos, 1.0);
}
