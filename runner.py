import subprocess
import time
import os
import glob
from concurrent.futures import ProcessPoolExecutor

minutes = 30  # timeout in minutes, you can change this value
log_dir = "logs" # Log directory, change as needed

def run_instance(file, t_out, log_dir):
    base = os.path.basename(file).replace(".txt", "")
    log_file = os.path.join(log_dir, f"{base}.log")
    filename = os.path.splitext(os.path.basename(file))[0]

    print(f"[{time.strftime('%H:%M')}] Running main.py with input {filename}...", flush=True)

    start = time.time()
    try:
        with open(file, "r") as fin, open(log_file, "w") as fout:
            process = subprocess.Popen(
                ["python", "main.py"],
                stdin=fin,
                stdout=fout,
                stderr=subprocess.STDOUT
            )
            try:
                process.wait(timeout=t_out)
            except subprocess.TimeoutExpired:
                process.kill()
                fout.write(f"\n--- Execution timed out after {t_out} seconds ---\n")
                print(f"[{time.strftime('%H:%M')}] Timeout: {filename}", flush=True)
                return filename, False

        end = time.time()
        minutes, seconds = divmod(end - start, 60)
        with open(log_file, "a") as fout:
            fout.write(f"\n--- Finished in {end - start:.2f} seconds ---\n")

        print(f"[{time.strftime('%H:%M')}] Finished {filename} in {minutes:.0f}m{seconds:.2f}s\n", flush=True)
        return filename, True

    except Exception as e:
        with open(log_file, "a") as fout:
            fout.write(f"\n--- Error: {e} ---\n")
        print(f" Error running {filename}: {e}", flush=True)
        return filename, False


def main():
    input_dir = "instances"

    # Prepare input directory
    os.makedirs(log_dir, exist_ok=True)

    # Clean log directory
    for f in glob.glob(os.path.join(log_dir, "*")):
        try:
            os.remove(f)
        except Exception as e:
            print(f"[WARNING] Could not remove {f}: {e}")

    t_out = 60 * minutes
    files = sorted(glob.glob(os.path.join(input_dir, "*.txt")))

    # Number of workers = available cores or number of instances
    max_workers = min(len(files), os.cpu_count() or 4)

    print(f" Running {len(files)} instances in up to {max_workers} processes...\n")

    # Runs in parallel
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for file in files:
            executor.submit(run_instance, file, t_out, log_dir)


    print(f"All files processed. Check the {log_dir} directory for outputs.")


if __name__ == "__main__":
    main()
