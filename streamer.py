import subprocess
import time

# Define your input sources and output keys
streams = {
    "cam1": "https://www.youtube.com/watch?v=ggJVG-zFn5Y",
    "cam2": "http://youtube.com/watch?v=dmqHRNGXlnc",
    "cam3": "https://www.youtube.com/watch?v=_IFD0Ah8a-M",
    "cam4": "https://www.youtube.com/watch?v=5hFBtF9H4VU"
}

def start_stream(name, source):
    output = f"rtmp://localhost/live/{name}"

    if "youtube.com" in source or "youtu.be" in source:
        # For YouTube: use yt-dlp to pipe video to ffmpeg
        command = (
            f'yt-dlp -f best -o - "{source}" | '
            f'ffmpeg -re -i - -c:v copy -c:a copy -f flv "{output}"'
        )
        shell = True
    else:
        # For regular sources (RTSP, files)
        command = [
            "ffmpeg",
            "-re",
            "-i", source,
            "-c:v", "copy",
            "-c:a", "aac",       # safer audio fallback
            "-f", "flv",
            output
        ]
        shell = False

    print(f"Starting stream {name} from {source}")
    return subprocess.Popen(command, shell=shell)

processes = []

for name, src in streams.items():
    proc = start_stream(name, src)
    processes.append(proc)
    time.sleep(2)  # optional delay

# Keep the script alive to maintain streams
try:
    for p in processes:
        p.wait()
except KeyboardInterrupt:
    for p in processes:
        p.terminate()
