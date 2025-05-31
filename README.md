
# 🖼️ VTracer GUI Wrapper

A simple Python GUI that acts as a wrapper around [VTracer](https://github.com/visioncortex/vtracer), allowing users to batch-convert images to SVG format using customizable options.

---

## ✅ Features

- 📁 Select multiple images using a file dialog
- ⚙️ Customize VTracer options like mode, color count, etc.
- 🔁 Automatically processes all selected images
- 📄 Outputs SVG files with sequential names in the same folder

---

## 💻 Requirements

- Python 3.7+
- VTracer (installed on your system)

Install Python dependencies:

```bash
pip install tk
````

---

## 🔧 Installing VTracer

To use this tool, you **must install VTracer** from [GitHub](https://github.com/visioncortex/vtracer):

### Option 1: Install with Cargo (Rust)

```bash
cargo install vtracer
```

### Option 2: Download Binary

Visit the [VTracer Releases Page](https://github.com/visioncortex/vtracer/releases) and download the binary for your OS. Make sure it’s accessible in your system's `PATH`.

---

## 🚀 Usage

### GUI Mode

Launch the GUI with:

```bash
python vtracer_gui.py --gui
```

A window will appear allowing you to:

* Choose multiple images
* Select vectorization options
* Start the batch conversion

### CLI Mode

You can also run it headless:

```bash
python vtracer_gui.py image1.jpg image2.png --colormode color --mode default
```

---

## 🗂️ Output

SVG files will be created in the **same directory** as the original images, named like:

```
image_0.svg
image_1.svg
...
```

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Credits

* GUI written in Python with `tkinter`
* Powered by [VTracer](https://github.com/visioncortex/vtracer)

