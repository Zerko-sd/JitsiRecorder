# JitsiRecorder
Built this because Jibri and I stopped being friends.

After spending an unreasonable amount of time fighting Jibri, reading logs that felt like ancient runes, restarting containers for emotional support, and questioning every life decision that led me here, I finally accepted the truth: Jibri was never going to work the way I needed it to. So instead of debugging one more mysterious Chrome/XMPP/Prosody-related issue at 3 AM, I did the only sane thing left I built my own recorder. This project is powered by spite, caffeine, and the firm belief that if something refuses to cooperate long enough, it deserves to be replaced entirely. It may not be pretty, it may not be orthodox, but it records Jitsi meetings reliably, without gaslighting me, and honestly… that’s all I ever wanted.


Jitsi Recorder Bot (Playwright + FFmpeg)

A lightweight, headless Jitsi Meet recorder bot built using Python, Playwright, Chromium, and FFmpeg.

This project joins a Jitsi meeting as a bot, captures audio/video headlessly, and records it without using Jibri.
Built for experimentation, automation, and scalable recording architectures.


##⚠️ Important Disclaimer

This project is exerimental.
It is NOT a drop-in replacement for Jibri and NOT production-ready by default.
Recording WebRTC reliably without Jibri comes with real technical limitations.
Use this project for:
MVPs
Internal tools
Controlled environments
Research & experimentation


##Features

Headless Chromium bot powered by Playwright
Automatically joins Jitsi rooms
Fully Dockerized
No Jibri, no Xorg, no virtual framebuffer
FFmpeg-based recording pipeline
One container = one meeting (by design)


##What This Project Does NOT Do

No server-side SFU stream tapping
No multi-room recording in a single container
No guaranteed perfect audio/video sync
No official Jitsi recording hooks
If you need broadcast-grade, guaranteed recording, use Jibri.


How It Works
Jitsi Meeting
↓
Headless Chromium (Playwright)
↓
Bot joins as a participant
↓
WebRTC media rendered in browser
↓
Media captured
↓
FFmpeg records to file or stream
This is client-side recording, not server-side.


#Requirements

Docker
~2 GB shared memory (--shm-size=2gb)
Stable CPU (Chromium + WebRTC is resource-heavy)
A Jitsi Meet instance (public or self-hosted)

##🐳 Docker Setup
Build the image
docker build -t jitsi-recorder-py .

Run the recorder
docker run --rm --shm-size=2gb \
  -e ROOM_URL="https://meet.jitsi/your-room-name" \
  -v $(pwd)/recordings:/app/recordings \
  jitsi-recorder-py


Recorded files will be written to the recordings/ directory.

Environment Variables
Variable	Description
ROOM_URL	Full Jitsi meeting URL
RECORD_DURATION	Recording duration in seconds (optional)
OUTPUT_FILE	Output filename (optional)

Rules for Reliable Recording

One bot per meeting
Do not reuse a container for multiple rooms.

Always allocate shared memory
Chromium will crash without sufficient /dev/shm.

Expect high resource usage
Headless does not mean lightweight.

Join muted
Prevent echo loops and feedback.

Stable network required
Packet loss directly affects recording quality.

No direct JVB access
This project does not tap server-side media streams.

🔊 Audio & Video Notes
Browser audio capture is fragile
Audio routing differs across OS and container runtimes
Perfect A/V sync is not guaranteed
Edge cases are expected under load
These are inherent WebRTC constraints.

 Why Not Jibri?
Jibri:
Requires Xorg
Runs best on full VMs
Supports only one recording per instance
Is harder to scale horizontally
This project explores a lighter, more flexible alternative, accepting the tradeoffs openly.

Scaling Model
Scaling is achieved through replication, not multiplexing.

Meeting A → Recorder Container A
Meeting B → Recorder Container B
Meeting C → Recorder Container C

Works well with:
Docker
Kubernetes
Nomad
ECS

Tested On
Docker Desktop (Windows + WSL)
Public Jitsi Meet
Self-hosted Jitsi (Docker-based)

Legal & Ethical Notice
Recording meetings may be subject to:
Local laws
User consent requirements
Platform policies
You are responsible for compliance.

🧠 Final Note
If you need official, supported, guaranteed recording → use Jibri.
If you want control, experimentation, and scale-friendly architecture → this project is for you.
