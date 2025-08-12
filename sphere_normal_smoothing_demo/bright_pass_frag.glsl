#version 330 core
out vec4 FragColor;
in vec2 uv;

uniform sampler2D screenTexture;
uniform float bloomThreshold;

void main()
{
    vec4 color = texture(screenTexture, uv);
    float brightness = dot(color.rgb, vec3(0.2126, 0.7152, 0.0722));
    if (brightness > bloomThreshold) {
        FragColor = color;
    } else {
        FragColor = vec4(0.0, 0.0, 0.0, 1.0);
    }
}