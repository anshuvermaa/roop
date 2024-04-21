import subprocess
import os
from utils import get_uploads_dir


def run_command(cmd, workdir=None):
    print('cmd is',cmd)
    result = subprocess.run(
        cmd, text=True, cwd=workdir, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    print('result is',result)
    if result.returncode != 0:
        error_details = f"Command '{' '.join(cmd)}' failed with return code {result.returncode}. "
        error_details += f"STDOUT: {result.stdout} "
        error_details += f"STDERR: {result.stderr}"
        print('error_details is',error_details)
        raise Exception(error_details)
    return result






def run_faceswap_inference(source_path, target_path, outfile_path):
    print("target_path"+target_path)
    print("source_path"+source_path)
    print("outfile_path"+outfile_path)

    cmd = [
        "python",
        "run.py",
        "--source",
        source_path,
        "--target",
        target_path,
        "--output",
        outfile_path,
        "--execution-provider",
        "cuda"
    ]
    try:
      result = run_command(cmd)
      print("result is",result)
    except Exception as e:
        print("error is in result",e)


    # result = run_command(cmd, workdir="wav2lip-hq")

    if not os.path.exists(outfile_path):
        error_msg = result.stderr if result.stderr else result.stdout
        raise Exception(f"Error: {error_msg}")

    return outfile_path
