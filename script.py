import pyautogui
import time
import datetime
from github import Github
from pynput import keyboard  # <-- works perfectly on macOS

# ----------------------------
# GITHUB CONFIGURATION
# ----------------------------
GITHUB_TOKEN = "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" 
REPO_NAME = "arya-007/tmp"
COMMIT_MESSAGE = "Add or update screenshot"


# ----------------------------
# FUNCTION TO TAKE AND UPLOAD A SCREENSHOT
# ----------------------------
def take_and_upload_screenshot():
    try:
        print("\n📸 Taking screenshot...")
        time.sleep(1)

        screenshot = pyautogui.screenshot()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"screenshot_{timestamp}.png"
        screenshot.save(filename)

        print(f"✅ Screenshot saved locally as {filename}")

        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)

        with open(filename, "rb") as f:
            content = f.read()

        try:
            contents = repo.get_contents(filename)
            repo.update_file(contents.path, COMMIT_MESSAGE, content, contents.sha)
            print("🔄 File updated in the GitHub repo.")
        except Exception:
            repo.create_file(filename, COMMIT_MESSAGE, content)
            print("🆕 File created in the GitHub repo.")

        print("✅ Upload complete!\n")

    except Exception as e:
        print(f"❌ Error: {e}")


# ----------------------------
# HOTKEY LISTENER (Command + Shift + S)
# ----------------------------
current_keys = set()


def on_press(key):
    try:
        if key in (keyboard.Key.cmd, keyboard.Key.shift_l, keyboard.Key.shift_r):
            current_keys.add(key)
        elif hasattr(key, "char") and key.char == "s":
            # Check if both Command and Shift are held
            if keyboard.Key.cmd in current_keys and (
                keyboard.Key.shift_l in current_keys
                or keyboard.Key.shift_r in current_keys
            ):
                take_and_upload_screenshot()
    except Exception as e:
        print("Error in key press:", e)


def on_release(key):
    if key in current_keys:
        current_keys.remove(key)
    if key == keyboard.Key.esc:
        print("👋 Exiting listener...")
        return False


def main():
    print("👂 Listening for Command + Shift + S to take a screenshot.")
    print("Press Esc to quit.\n")

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    main()
