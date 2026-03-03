# Changelog

All notable changes to the **Emotional Sphere Visualization Engine** will be documented in this file.

## [1.1.0] - 2025-08-21
### Added
- **Recording Module:** Integrated OpenCV support to export simulations directly to `.mp4` format.
- **Enhanced Prompting:** Added strict JSON formatting rules to the Gemini API client to prevent parsing errors.
- **Post-Processing:** Added a Gaussian Blur fragment shader with adjustable `blur_strength` for high-intensity emotions.

### Changed
- **Architecture Shift:** Migrated from a concurrent execution model to a sequential two-stage pipeline (UI -> Analysis -> Render) to resolve thread blocking between `customtkinter` and `glfw`.
- **Lighting Model:** Updated the Phong reflection weights to better highlight the "Rim Light".

### Fixed
- Resolved a memory leak in the Framebuffer Object (FBO) during prolonged simulation sessions.
- Fixed an issue where the Gemini API would return multiple intensities for a single fragment.

---

## [1.0.0] - 2025-08-02
### Added
- **Core Engine:** First stable release of the OpenGL rendering core using ModernGL.
- **Emotion Mapping:** Implementation of Plutchik’s Wheel of Emotions into the 3D displacement logic.
- **Dynamic Shaders:** Created the primary Vertex Shader supporting Sinusoidal and dual Perlin Noise (Spherical and Planar) deformations.
- **UI Interface:** Initial dashboard built with `customtkinter` for text input and emotion visualization triggers.

### Changed
- Improved the interpolation algorithm (`blend_factor`) to allow smoother transitions between primary and secondary emotions.

---

## [0.5.0] - 2025-07-18
### Added
- **Proof of Concept:** Basic sphere generation using `pyrr` for MVP (Model-View-Projection) matrices.
- **API Integration:** Initial connection with Google Gemini API for sentiment fragmenting.
- **Draft Shaders:** Simple vertex displacement based on time variables.