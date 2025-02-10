import subprocess

from lxcext.core.runner.abc_runner import Runner


class RunPretend(Runner):
    def run_command(command, debug=False, pretend=False):
        """Run a shell command and print debug information if enabled."""
        if debug or pretend:
            print(f"[DEBUG] Command: {command}")
        if not pretend:
            subprocess.run(command, shell=True, check=True)

