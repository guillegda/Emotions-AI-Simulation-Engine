
#version 330
out vec4 f_color;
uniform float time;

void main() {
    float r = 0.6 + 0.4 * sin(time);
    float g = 0.5 + 0.5 * cos(time * 1.2);
    float b = 0.7 + 0.3 * sin(time * 0.8);
    float brightness = 0.3 + 0.7 * abs(sin(time * 2.0));
    f_color = vec4(r * brightness, g * brightness, b * brightness, 1.0);
}
