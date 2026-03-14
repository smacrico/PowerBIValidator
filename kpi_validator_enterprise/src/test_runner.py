import subprocess

def run_tests():

    subprocess.run(["pytest","generated_tests"])