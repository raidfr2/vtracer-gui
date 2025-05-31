#!/usr/bin/env python3
"""
VTracer Image Vectorizer Script
Converts raster images to vector format using VTracer
Uses your specified parameter settings
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

def check_vtracer_installed():
    """Check if VTracer is installed and accessible"""
    try:
        result = subprocess.run(['vtracer', '--help'], 
                              capture_output=True, text=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_vtracer():
    """Provide instructions for installing VTracer"""
    print("\nVTracer is not installed or not found in PATH.")
    print("To install VTracer:")
    print("1. Install Rust: https://rustup.rs/")
    print("2. Install VTracer: cargo install vtracer")
    print("3. Or download prebuilt binaries from: https://github.com/visioncortex/vtracer")
    return False

def vectorize_image(input_path, output_path=None, colormode='color', hierarchical='stacked', 
                   mode='spline', filter_speckle=4, color_precision=6, gradient_step=55,
                   corner_threshold=105, segment_length=7.5, splice_threshold=0):
    """
    Vectorize a single image using VTracer with your specified parameters
    """
    input_path = Path(input_path)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Generate output path if not provided
    if output_path is None:
        output_path = input_path.with_suffix('.svg')
    else:
        output_path = Path(output_path)
    
    # Build VTracer command with your specified parameters
    cmd = [
        'vtracer',
        '--input', str(input_path),
        '--output', str(output_path),
        '--colormode', colormode,
        '--hierarchical', hierarchical,
        '--mode', mode,
        '--filter_speckle', str(filter_speckle),
        '--color_precision', str(color_precision),
        '--gradient_step', str(gradient_step),
        '--corner_threshold', str(corner_threshold),
        '--segment_length', str(segment_length),
        '--splice_threshold', str(splice_threshold)
    ]
    
    try:
        print(f"Vectorizing: {input_path.name}")
        print(f"Command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        print(f"✓ Successfully created: {output_path}")
        return output_path
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error vectorizing {input_path.name}:")
        print(f"  {e.stderr}")
        raise

def select_files_gui():
    """Open file dialog to select images"""
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    file_types = [
        ('Image files', '*.png *.jpg *.jpeg *.bmp *.tiff *.gif'),
        ('PNG files', '*.png'),
        ('JPEG files', '*.jpg *.jpeg'),
        ('All files', '*.*')
    ]
    
    files = filedialog.askopenfilenames(
        title="Select images to vectorize",
        filetypes=file_types
    )
    
    root.destroy()
    return files

def get_next_svg_filename(output_dir):
    svg_files = list(output_dir.glob('*.svg'))
    numbers = []
    for f in svg_files:
        try:
            n = int(f.stem)
            numbers.append(n)
        except ValueError:
            continue
    next_num = max(numbers, default=0) + 1
    return output_dir / f"{next_num}.svg"

def run_gui():
    import threading
    root = tk.Tk()
    root.title("VTracer Image Vectorizer")
    root.geometry("500x600")
    script_dir = Path(os.path.abspath(os.path.dirname(__file__)))

    # File selection
    files_var = tk.StringVar()
    def select_files():
        files = filedialog.askopenfilenames(
            title="Select images to vectorize",
            filetypes=[('Image files', '*.png *.jpg *.jpeg *.bmp *.tiff *.gif'), ('All files', '*.*')]
        )
        files_var.set(';'.join(files))
        files_list.delete(0, tk.END)
        for f in files:
            files_list.insert(tk.END, f)

    tk.Label(root, text="Input Images:").pack(anchor='w', padx=10, pady=(10,0))
    tk.Button(root, text="Select Images", command=select_files).pack(anchor='w', padx=10)
    files_list = tk.Listbox(root, height=4, width=60)
    files_list.pack(padx=10, pady=(0,10))

    # Output directory
    output_dir_var = tk.StringVar()
    def select_output_dir():
        d = filedialog.askdirectory(title="Select output directory")
        if d:
            output_dir_var.set(d)
    tk.Label(root, text="Output Directory:").pack(anchor='w', padx=10)
    out_frame = tk.Frame(root)
    out_frame.pack(anchor='w', padx=10)
    tk.Entry(out_frame, textvariable=output_dir_var, width=40).pack(side='left')
    tk.Button(out_frame, text="Browse", command=select_output_dir).pack(side='left', padx=5)

    # VTracer parameters
    param_frame = tk.LabelFrame(root, text="VTracer Parameters")
    param_frame.pack(fill='x', padx=10, pady=10)
    params = {
        'colormode': tk.StringVar(value='color'),
        'hierarchical': tk.StringVar(value='stacked'),
        'mode': tk.StringVar(value='spline'),
        'filter_speckle': tk.IntVar(value=4),
        'color_precision': tk.IntVar(value=6),
        'gradient_step': tk.IntVar(value=55),
        'corner_threshold': tk.IntVar(value=105),
        'segment_length': tk.DoubleVar(value=7.5),
        'splice_threshold': tk.IntVar(value=0),
    }
    row = 0
    tk.Label(param_frame, text="Color Mode:").grid(row=row, column=0, sticky='w')
    tk.OptionMenu(param_frame, params['colormode'], 'color', 'binary').grid(row=row, column=1, sticky='w')
    row += 1
    tk.Label(param_frame, text="Hierarchical:").grid(row=row, column=0, sticky='w')
    tk.OptionMenu(param_frame, params['hierarchical'], 'stacked', 'cutout').grid(row=row, column=1, sticky='w')
    row += 1
    tk.Label(param_frame, text="Mode:").grid(row=row, column=0, sticky='w')
    tk.OptionMenu(param_frame, params['mode'], 'spline', 'polygon', 'pixel').grid(row=row, column=1, sticky='w')
    row += 1
    tk.Label(param_frame, text="Filter Speckle:").grid(row=row, column=0, sticky='w')
    tk.Entry(param_frame, textvariable=params['filter_speckle'], width=8).grid(row=row, column=1, sticky='w')
    row += 1
    tk.Label(param_frame, text="Color Precision:").grid(row=row, column=0, sticky='w')
    tk.Entry(param_frame, textvariable=params['color_precision'], width=8).grid(row=row, column=1, sticky='w')
    row += 1
    tk.Label(param_frame, text="Gradient Step:").grid(row=row, column=0, sticky='w')
    tk.Entry(param_frame, textvariable=params['gradient_step'], width=8).grid(row=row, column=1, sticky='w')
    row += 1
    tk.Label(param_frame, text="Corner Threshold:").grid(row=row, column=0, sticky='w')
    tk.Entry(param_frame, textvariable=params['corner_threshold'], width=8).grid(row=row, column=1, sticky='w')
    row += 1
    tk.Label(param_frame, text="Segment Length:").grid(row=row, column=0, sticky='w')
    tk.Entry(param_frame, textvariable=params['segment_length'], width=8).grid(row=row, column=1, sticky='w')
    row += 1
    tk.Label(param_frame, text="Splice Threshold:").grid(row=row, column=0, sticky='w')
    tk.Entry(param_frame, textvariable=params['splice_threshold'], width=8).grid(row=row, column=1, sticky='w')

    # Status area
    status_text = tk.Text(root, height=10, width=60, state='disabled')
    status_text.pack(padx=10, pady=10)
    def log(msg):
        status_text.config(state='normal')
        status_text.insert(tk.END, msg + '\n')
        status_text.see(tk.END)
        status_text.config(state='disabled')

    def do_vectorize():
        files = files_var.get().split(';') if files_var.get() else []
        if not files:
            messagebox.showerror("No files", "Please select at least one image file.")
            return
        outdir = output_dir_var.get().strip() or None
        if outdir:
            outdir = Path(outdir)
            outdir.mkdir(parents=True, exist_ok=True)
        else:
            outdir = script_dir
        # Collect params
        vparams = {k: v.get() for k, v in params.items()}
        successful = 0
        failed = 0
        for file_path in files:
            try:
                input_path = Path(file_path)
                output_path = get_next_svg_filename(outdir)
                log(f"Vectorizing: {input_path.name} ...")
                vectorize_image(
                    input_path,
                    output_path,
                    **vparams
                )
                log(f"✓ Successfully created: {output_path}")
                successful += 1
            except Exception as e:
                log(f"✗ Failed to process {file_path}: {e}")
                failed += 1
        log(f"\n--- Summary ---\nSuccessful: {successful}\nFailed: {failed}\nTotal: {len(files)}\n")

    def start_vectorize_thread():
        threading.Thread(target=do_vectorize, daemon=True).start()

    tk.Button(root, text="Start Vectorization", command=start_vectorize_thread, bg="#4CAF50", fg="white").pack(pady=10)
    root.mainloop()

def main():
    parser = argparse.ArgumentParser(description='Vectorize images using VTracer with optimized settings')
    parser.add_argument('files', nargs='*', help='Input image files')
    parser.add_argument('--output-dir', '-o', help='Output directory for SVG files')
    parser.add_argument('--gui', action='store_true', help='Use GUI file picker')
    parser.add_argument('--simple-gui', action='store_true', help='Launch the simple GUI')
    
    # VTracer parameters with your specified defaults
    parser.add_argument('--colormode', choices=['color', 'binary'], 
                       default='color', help='Color mode (B/W or Color)')
    parser.add_argument('--hierarchical', choices=['stacked', 'cutout'], 
                       default='stacked', help='Cutout or Stacked')
    parser.add_argument('--mode', choices=['spline', 'polygon', 'pixel'], 
                       default='spline', help='Curve fitting mode (PIXEL/Polygon/Spline)')
    parser.add_argument('--filter-speckle', type=int, default=4, 
                       help='Filter Speckle - cleaner (default: 4)')
    parser.add_argument('--color-precision', type=int, default=6, 
                       help='Color Precision - more accurate (default: 6)')
    parser.add_argument('--gradient-step', type=int, default=55, 
                       help='Gradient Step - less layers (default: 55)')
    parser.add_argument('--corner-threshold', type=int, default=105, 
                       help='Corner Threshold - smoother (default: 105)')
    parser.add_argument('--segment-length', type=float, default=7.5, 
                       help='Segment Length - more coarse (default: 7.5)')
    parser.add_argument('--splice-threshold', type=int, default=0, 
                       help='Splice Threshold - less accurate (default: 0)')
    
    args = parser.parse_args()
    
    # Check if VTracer is installed
    if not check_vtracer_installed():
        install_vtracer()
        return 1
    
    # Get input files
    if args.gui or not args.files:
        files = select_files_gui()
        if not files:
            print("No files selected.")
            return 0
    else:
        files = args.files
    
    # Prepare output directory
    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = Path(os.path.abspath(os.path.dirname(__file__)))
    
    # Process files
    successful = 0
    failed = 0
    
    print(f"\nProcessing {len(files)} file(s) with your optimized settings...")
    print("Settings:")
    print(f"  Color Mode: {args.colormode}")
    print(f"  Hierarchical: {args.hierarchical}")
    print(f"  Mode: {args.mode}")
    print(f"  Filter Speckle: {args.filter_speckle}")
    print(f"  Color Precision: {args.color_precision}")
    print(f"  Gradient Step: {args.gradient_step}")
    print(f"  Corner Threshold: {args.corner_threshold}")
    print(f"  Segment Length: {args.segment_length}")
    print(f"  Splice Threshold: {args.splice_threshold}")
    print()
    
    for file_path in files:
        try:
            input_path = Path(file_path)
            
            output_path = get_next_svg_filename(output_dir)
            
            vectorize_image(
                input_path, 
                output_path,
                colormode=args.colormode,
                hierarchical=args.hierarchical,
                mode=args.mode,
                filter_speckle=args.filter_speckle,
                color_precision=args.color_precision,
                gradient_step=args.gradient_step,
                corner_threshold=args.corner_threshold,
                segment_length=args.segment_length,
                splice_threshold=args.splice_threshold
            )
            successful += 1
            
        except Exception as e:
            print(f"✗ Failed to process {file_path}: {e}")
            failed += 1
    
    print(f"\n--- Summary ---")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total: {len(files)}")
    
    if args.simple_gui:
        run_gui()
        return 0
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
