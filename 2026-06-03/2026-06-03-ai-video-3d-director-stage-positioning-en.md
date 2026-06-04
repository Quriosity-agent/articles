# Practical Control of Character Blocking in AI Video: A 3D Director Stage Is Not a Cooler UI, but a Verifiable Spatial Plan

> **TL;DR:** TanLuAI’s X Article demonstrates a very concrete problem: in AI video, multi-character blocking, camera angle, shot size, and action are hard to control with text prompts alone. The value of a 3D director stage is that it turns “where characters are, where the camera is, where objects are, and what poses characters hold” into an editable spatial sketch before generation. The recommended workflow is to feed the camera screenshot together with character references, scene references, and prompts into a video model such as Seedance 2.0. This is not just a UI feature; it moves AI video from “write a prompt and hope” toward “previsualize the scene, then generate the shot.”

- **Source:** [TanLuAI X Article](https://x.com/TanLuAI/status/2062167075540676650?s=20)
- **Topic:** AI video / 3D director stage / character positioning / camera control / Seedance 2.0
- **Tags:** AI video / director stage / 3D previs / character blocking / camera planning / Seedance 2.0 / reference-image workflow

![3D director stage workflow overview](imgs/ai-video-3d-director-stage-positioning/contact-sheet-1.webp)

## 1. The real problem: AI video has generation, but not enough blocking control

Modern AI video models can generate highly complex scenes, but multi-character shots still often fail: characters drift, foreground/background relationships collapse, camera angles are wrong, character spacing does not match the story, and movement does not follow spatial direction. A traditional prompt may say: “a woman sits in the foreground, two men stand behind her, shot from the left in a medium view.” The problem is that the model may not reliably map that sentence into geometry.

TanLuAI’s tutorial solves the issue in a practical way: do not compress character positions, poses, and camera placement into one prompt. Build the spatial structure first in a **3D director stage**, then use the camera screenshot as reference material for the video model.

This is an important shift in AI video production:

- prompts describe semantics and style;
- character reference images preserve identity;
- scene images preserve world and art direction;
- the 3D director stage controls spatial layout, camera, and pose;
- the video model synthesizes these constraints into motion.

In other words, the 3D director stage does not replace prompting. It extracts the part that prompts handle poorly: spatial control.

## 2. What is a 3D director stage?

TanLuAI defines the director stage as an operating panel for planning screen content and camera position in advance. Character blocking, poses, object placement, camera position, camera angle, and shot size can all be planned in one interface.

From the tutorial screenshots, this kind of tool usually includes:

1. a 3D workspace;
2. built-in human models or uploaded characters;
3. geometric primitives for placeholders, props, walls, furniture, and obstacles;
4. move, scale, and rotate controls;
5. pose presets and joint-level editing;
6. multiple camera views;
7. switching between director view and camera view;
8. screenshot capture and sending the shot back to the generation canvas.

It is essentially a lightweight previs tool. The goal is not final visual quality; the goal is to lock down narrative space before generation.

## 3. Two ways to create the director stage: blank space vs scene anchoring

The article mentions two setup paths.

The first is to create a director stage directly on a blank canvas. This gives the user an empty 3D space where characters and objects can be placed freely. It is useful for abstract composition, product shots, simple relationship diagrams, or cases where no fixed scene image exists yet.

The second is to generate a 720-degree panorama from a scene image and then create a director stage from that panorama. In this mode, character blocking and camera placement happen inside a concrete environment instead of a black-box space. This is better for narrative video, cinematic shots, and multi-character blocking inside a stable scene.

One practical detail matters: set the aspect ratio as soon as you enter the director stage. Blocking, shot size, and composition all depend on the final frame. If you build the shot first and switch from landscape to portrait later, the spatial relationship may break.

## 4. Core operations: place objects first, then tune spatial relationships

The workflow can be summarized in five steps.

### 4.1 Add characters and objects

The director stage supports built-in character models and uploaded local characters. Geometric models can add simple shapes. These shapes are more useful than they look: they can represent tables, columns, walls, foreground occluders, props, frame boundaries, and depth references.

In AI video, a geometric primitive does not have to be the final object. It communicates spatial intent. A cylinder can mean “foreground object.” A box can mean “table.” Distance between characters and props can constrain depth and framing.

### 4.2 Move, scale, and rotate

The tutorial emphasizes that the first button on the bottom toolbar switches between move, scale, and rotate modes:

- **Move:** x-axis left/right, y-axis up/down, z-axis forward/back;
- **Scale:** x-axis wider/narrower, y-axis taller/shorter, z-axis thicker/thinner;
- **Uniform scale:** keep proportions consistent;
- **Rotate:** after switching to the spherical control, adjust direction across multiple angles.

This turns phrases like “stand beside,” “move forward,” “face the camera,” and “turn around” into visible 3D operations.

### 4.3 Adjust character poses

After selecting a character, the right-side pose list provides multiple pose presets. Users can also customize joints. This is crucial for AI video because pose often defines the first frame of motion: sitting, standing, running, turning, reaching, kneeling, and so on. If these are only described in text, the model may infer a different body structure.

The advantage of 3D posing is that the body state is fixed first. The video model can then apply style and motion generation on top.

![3D director stage transform and pose controls](imgs/ai-video-3d-director-stage-positioning/contact-sheet-2.webp)

### 4.4 Adjust camera position

The tutorial says the fourth button on the bottom toolbar can switch among multiple camera angles, and users can also move each camera manually. This determines whether the final screenshot is a wide shot, medium shot, close-up, top-down view, low angle, side shot, or subjective view.

This is where the director stage becomes truly directorial. It is not just placing characters; it decides where the audience sees from. Many AI video failures are not drawing failures. They are unplanned camera failures.

### 4.5 Switch views, capture screenshots, and send them to the canvas

After placing characters, objects, scene elements, and cameras, users can capture the camera view. The screenshot appears in the camera-screenshot area and can be sent to the canvas through the main button or the thumbnail button.

The article highlights a useful detail: when you are in “camera view,” you cannot edit. To continue adjusting the scene, switch back to “director view.” This matters because the workflow constantly alternates between observing the final frame and editing the underlying space.

## 5. How to use camera screenshots: treat them as spatial references, not only keyframes

The article gives two methods.

The first is to use the director-stage camera screenshot directly as a scene anchor or keyframe. The author does not strongly recommend this for East Asian-themed videos, because image models may struggle to preserve East Asian facial consistency.

The second, recommended method is to feed the director-stage screenshot together with character references, scene references, and other materials into Seedance 2.0. The screenshot handles spatial structure, character references handle identity consistency, scene references handle art direction, and the prompt handles motion, emotion, and narrative.

This is important. A director-stage screenshot does not have to become the final frame. It can be a spatial constraint. If used as the only keyframe, the model may inherit the rough look of the 3D mannequins. If used as one reference among several, the model can separate spatial structure from visual quality.

![Camera screenshots and final reference-material workflow](imgs/ai-video-3d-director-stage-positioning/contact-sheet-3.webp)

## 6. Why this workflow fits models like Seedance 2.0

The original article uses Seedance 2.0. For newer video models, reference images are no longer merely “style references.” They can divide the job into several constraints: character reference, scene reference, camera/blocking reference, and pose/action reference.

This differs sharply from single-prompt generation:

| Dimension | Single-prompt workflow | 3D director stage + reference workflow |
|---|---|---|
| Character blocking | Text description, easy to drift | Explicitly constrained by 3D positions and camera screenshots |
| Character consistency | Relies on prompt and model memory | Supported by character reference images |
| Scene consistency | May be redrawn across shots | Supported by scene or panorama references |
| Camera angle | Often unstable in text | Camera position is visualized |
| Action start | Inferred by the model | Pose model defines the starting state |
| Iteration | Rewrite prompts after failure | Return to the stage and adjust space |

The value of the 3D director stage is not simply “better-looking output.” It makes failures diagnosable: if spacing is wrong, adjust positions; if the angle is wrong, change camera; if the pose is wrong, edit the skeleton; if the face is wrong, add character references.

## 7. Practical SOP for creators

To turn this into a stable workflow, use the following process:

1. **Set aspect ratio first:** landscape, portrait, or square before blocking.
2. **Place the main character first:** then add supporting characters and objects.
3. **Use geometry to express spatial intent:** tables, walls, foreground occlusion, and distance can all be represented with simple shapes.
4. **Solve one blocking problem per shot:** do not overload one stage with too many characters, movements, and camera transitions.
5. **Check composition from the target camera before capture:** verify character size, direction, and foreground/background relationships.
6. **Do not use the screenshot alone:** pair it with character and scene references.
7. **Use the prompt for motion and cinematic language:** let the director stage carry the geometry instead of overloading the prompt with spatial details.
8. **Keep stage files and screenshot versions:** they help maintain shot continuity and make revisions easier.

## 8. Implications for QCut and AI-video tools

This director-stage workflow is highly relevant to AI-video product design. The future of AI video tools is not just “prompt in, video out.” It is about splitting creative intent into editable layers:

- character layer: identity, clothing, face, body type;
- scene layer: environment, lighting, style;
- spatial layer: positions of characters and objects;
- camera layer: shot size, angle, movement path;
- action layer: pose, starting motion, direction;
- text layer: prompt, narration, dialogue;
- timeline layer: shot order, rhythm, edit points.

A 3D director stage is the visual editor for the spatial and camera layers. It turns AI video from one-shot generation into a production pipeline that can be decomposed, reused, and debugged.

## 9. My take: AI video is moving from prompt engineering to production engineering

TanLuAI’s article looks like a basic operations tutorial, but the deeper direction is clear: AI video increasingly needs concepts from traditional film production — previs, storyboards, camera placement, blocking, and asset management.

In the single-prompt era, creators were guessing what the model would do. In the director-stage workflow, creators start turning outcomes into verifiable intermediate states. That makes AI video feel more like a real production system: build the space, choose the camera, provide character and scene references, then ask the model to generate.

The strongest AI video tools may not be the ones with the most model buttons. They will be the tools that connect **director intent → spatial plan → reference assets → video generation → editing iteration** into one loop. The 3D director stage is one of the first pieces of that loop.
