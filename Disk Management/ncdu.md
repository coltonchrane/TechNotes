# ncdu (NCurses Disk Usage) Guide

`ncdu` is a disk usage analyzer with an ncurses interface. It is designed to find space hogs on a remote server where you don't have an entire graphical setup, but it is useful even on regular desktop systems.

## Basic Usage

To scan the current directory:
```bash
ncdu
```

To scan a specific directory:
```bash
ncdu /path/to/directory
```

To scan the entire filesystem (starting at root):
```bash
ncdu /
```

### Useful Flags
- `-x`: Stay on the same filesystem (don't cross mount points).
- `-r`: Read-only mode (prevents accidental deletion).
- `-o <filename>`: Export the results to a file for later viewing.
- `-f <filename>`: Import a previously exported result file.

---

## Navigation and Shortcuts

Once `ncdu` is running, use these keys to navigate and interact:

### Movement
- **Up/Down** or **j/k**: Move the cursor.
- **Right** or **Enter**: Open/descend into the selected directory.
- **Left** or **<**: Go back to the parent directory.

### Sorting
- **n**: Sort by name (ascending/descending).
- **s**: Sort by size (ascending/descending).
- **C**: Sort by number of items.
- **M**: Sort by last modified time (requires `-e` flag).

### Display Options
- **g**: Toggle between graph, percentage, or both.
- **a**: Toggle between showing disk usage and apparent size.
- **e**: Show/hide hidden files.
- **i**: Show information about the selected item.

### Actions
- **d**: Delete the selected file or directory (asks for confirmation).
- **q**: Quit `ncdu`.

---

## Remote Usage
To scan a remote directory and view it locally:
```bash
ssh user@remote "ncdu -o- /path/to/dir" | ncdu -f-
```
This runs the scan on the remote server, pipes the output to your local machine, and displays it in your local `ncdu` instance.
