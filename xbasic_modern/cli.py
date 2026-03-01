import sys
import os
import subprocess
import argparse

def get_resource_path(relative_path):
    # This works when running from the source tree
    return os.path.join(os.path.dirname(__file__), relative_path)

def main():
    parser = argparse.ArgumentParser(description="XBasic-Modern Toolchain")
    parser.add_argument("input", help="XBasic-Modern source file (.sl)")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: {args.input} not found.")
        sys.exit(1)

    pkg_root = os.path.dirname(__file__)
    compiler_bin = os.path.join(os.getcwd(), "compiler") # Built by Makefile in root for now
    sim_dir = get_resource_path("simulator")
    asm_py = os.path.join(sim_dir, "asm", "asm.py")

    # 1. Compile
    print(f"--- Compiling {args.input} ---")
    subprocess.check_call([compiler_bin, args.input], stdout=open("output.asm", "w"))

    # 2. Assemble
    print("--- Assembling ---")
    with open("memory.list", "w") as f:
        subprocess.check_call([sys.executable, asm_py, "output.asm"], stdout=f)

    # 3. Simulate
    print("--- Simulating ---")
    # Need to run iverilog in the sim_dir context or provide full paths
    # For simplicity, let's copy files to current dir or use -I
    # Actually, let's just use the existing run.sh logic but in Python
    rtl_files = [
        "alu.v", "cpu_control.v", "cpu_registers.v", "cpu.v", "machine.v", "parameters.v",
        "library/clock.v", "library/counter.v", "library/ram.v", "library/register.v", "library/tristate_buffer.v",
        "tb/machine_tb.v"
    ]
    rtl_paths = [os.path.join(sim_dir, "rtl", f) if not f.startswith("library") and not f.startswith("tb") 
                 else os.path.join(sim_dir, "rtl", f) for f in rtl_files]
    
    # We need to handle the relative includes in Verilog as well
    # Easiest way: cd to simulation dir and run
    cmd = ["iverilog", "-o", "computer", "-Wall", f"-I{sim_dir}"] + rtl_paths
    subprocess.check_call(cmd)
    subprocess.check_call(["vvp", "-n", "computer"])

if __name__ == "__main__":
    main()
