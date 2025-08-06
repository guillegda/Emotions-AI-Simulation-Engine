
#version 330
in vec2 uv;
out vec4 fragColor;
uniform sampler2D texture0;
uniform vec2 resolution;

void main() {
    vec2 texel = 1.0 / resolution;
    vec3 color = texture(texture0, uv).rgb * 4.0;
    color += texture(texture0, uv + vec2(texel.x, 0.0)).rgb;
    color += texture(texture0, uv - vec2(texel.x, 0.0)).rgb;
    color += texture(texture0, uv + vec2(0.0, texel.y)).rgb;
    color += texture(texture0, uv - vec2(0.0, texel.y)).rgb;
    color /= 8.0;
    fragColor = vec4(color, 1.0);
}
