from playwright.sync_api import sync_playwright
import time
import os

# --- CONFIGURATION ---
# We append config params to the URL to force the bot to join muted and without video.
# 1. startWithAudioMuted=true  -> Stops the "pulsing" sound
# 2. startWithVideoMuted=true  -> Stops the green video stream
# 3. prejoinPageEnabled=false  -> Skips the "Hair Check" screen for faster joining
BASE_URL = "https://meet.jit.si/AcidPovertiesAidExplicitly"
MEETING_URL = f"{BASE_URL}#config.startWithAudioMuted=true&config.startWithVideoMuted=true&config.prejoinPageEnabled=false"

OUTPUT_DIR = "recordings"
HEADLESS = True 
DURATION_SECONDS = 60

def run_recorder():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    with sync_playwright() as p:
        # Launch options optimized for WebRTC/Video
        # We still need the "fake" devices so Chrome doesn't error out, 
        # but Jitsi will keep them muted/off thanks to the URL params.
        browser = p.chromium.launch(
            headless=HEADLESS,
            args=[
                "--use-fake-ui-for-media-stream", 
                "--use-fake-device-for-media-stream",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ]
        )

        context = browser.new_context(
            viewport={"width": 1920, "height": 1080}, # 1080p recording
            record_video_dir=OUTPUT_DIR,
            record_video_size={"width": 1920, "height": 1080},
            permissions=["camera", "microphone"], # Permissions granted so Jitsi doesn't block access
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        page = context.new_page()
        
        print(f"🚀 Navigating to {BASE_URL}...")
        page.goto(MEETING_URL)

        # --- JITSI AUTOMATION LOGIC ---
        
        # 1. Handle "Enter your name" input 
        # (Might be skipped due to prejoinPageEnabled=false, but kept for safety)
        try:
            name_input = page.locator("input[type='text']").first
            if name_input.is_visible(timeout=5000):
                print("✍️ Entering display name...")
                name_input.fill("Recorder Bot")
                name_input.press("Enter")
        except:
            pass # Input didn't appear, likely auto-joined

        # 2. Click "Join meeting"
        # (With prejoinPageEnabled=false, this is often skipped automatically)
        try:
            join_button = page.locator("button[aria-label='Join meeting']")
            if join_button.is_visible(timeout=3000):
                join_button.click()
                print("✅ Clicked Join Meeting")
            else:
                # Fallback: check for text-based button
                text_join = page.locator("text=Join meeting")
                if text_join.is_visible(timeout=1000):
                    text_join.click()
                    print("✅ Clicked Join Meeting (Text Match)")
                else:
                    print("ℹ️ No join button found (likely auto-joined).")
        except:
            pass

        # 3. Final Verification (Optional)
        # We wait for the 'toolbox' to appear, which signifies we are truly IN the meeting
        try:
            page.wait_for_selector(".toolbox-content", timeout=10000)
            print("✅ Successfully inside the meeting.")
        except:
            print("⚠️ Warning: Could not detect meeting toolbar. Recording might be of the loading screen.")

        # --- RECORDING PHASE ---
        print(f"🎥 Recording started. Running for {DURATION_SECONDS} seconds...")
        
        # Keep the browser open to record
        time.sleep(DURATION_SECONDS)

        print("🛑 Time up. Closing context to save video...")
        
        # Closing the context triggers the video save.
        context.close()
        browser.close()

    # --- POST-PROCESSING ---
    rename_latest_recording()

def rename_latest_recording():
    try:
        # Find the most recently created .webm file in the output dir
        files = [os.path.join(OUTPUT_DIR, f) for f in os.listdir(OUTPUT_DIR) if f.endswith(".webm")]
        if not files:
            print("❌ No recording found.")
            return

        latest_file = max(files, key=os.path.getctime)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        new_name = os.path.join(OUTPUT_DIR, f"meeting_recording_{timestamp}.webm")
        
        os.rename(latest_file, new_name)
        print(f"💾 Recording saved successfully: {new_name}")
        
    except Exception as e:
        print(f"Error renaming file: {e}")

if __name__ == "__main__":
    run_recorder()