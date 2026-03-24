---
layout: default
title: Compress Image CLI
parent: Disk Management
nav_order: 1
---

# Compressing JPGs to 1MB using jpegoptim

### The jpegoptim utility is the most direct way to hit a target file size on Ubuntu because it automatically calculates the necessary compression levels for you.

------------------------------
1. Installation
If you don't have it yet, install it via the official repository:

sudo apt update && sudo apt install jpegoptim

2. Basic Usage (Target Size)
To force an image to be under 1MB (1000k), use the --size flag:
```bash
jpegoptim --size=1000k yourimage.jpg
```

* Warning: This command overwrites the original file by default.

3. Advanced Options

* Keep Original: To save the compressed version in a different folder (preserving the original), use the -d (directory) flag:

```bash
mkdir compressed_images
jpegoptim --size=1000k -d ./compressed_images yourimage.jpg
```
* Strip Metadata: To shave off extra kilobytes by removing EXIF/GPS data:
```bash
jpegoptim --strip-all --size=1000k yourimage.jpg
```
* Batch Process: To compress all JPGs in your current folder to under 1MB:
```bash
jpegoptim --size=1000k *.jpg
```

4. Troubleshooting

* "Size goal too small": If jpegoptim can't reach 1MB even at its lowest quality setting, the physical dimensions (pixels) of your image are likely too large. You will need to resize the image (e.g., using ImageMagick) before compressing.
* Simulate first: Add the -n (dry run) flag to see the results without actually changing any files:
```bash
jpegoptim -n --size=1000k yourimage.jpg
```



