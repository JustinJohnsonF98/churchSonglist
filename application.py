"""
Church Song App
Single-file Python application (Tkinter GUI + optional CLI) to manage a songs.json

Features:
- Load/save songs to songs.json (auto-creates if missing)
- GUI with list, search, add, edit, delete
- Add/Edit popup includes Title and Number fields and a Submit button
- Live search/filter
- Optional simple CLI mode for quick adds (run with --cli)

How to run:
- Make sure you have Python 3 installed.
- Save this file as church_song_app.py in a folder.
- Run: python church_song_app.py
- Or CLI: python church_song_app.py --cli

"""
import json
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import List, Dict

SONGS_FILE = "songs.json"

def load_songs() -> List[Dict]:
    if not os.path.exists(SONGS_FILE):
        # create an empty file
        with open(SONGS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)
        return []
    try:
        with open(SONGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                # normalize to list of dicts with title and optional number
                normalized = []
                for item in data:
                    if isinstance(item, dict):
                        title = item.get("title") or item.get("name") or ""
                        number = item.get("number") or item.get("num") or ""
                        normalized.append({"title": str(title), "number": str(number)})
                    elif isinstance(item, str):
                        normalized.append({"title": item, "number": ""})
                return normalized
            else:
                return []
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load {SONGS_FILE}: {e}")
        return []


def save_songs(songs: List[Dict]):
    try:
        with open(SONGS_FILE, "w", encoding="utf-8") as f:
            json.dump(songs, f, indent=2, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save {SONGS_FILE}: {e}")


class AddEditDialog(simpledialog.Dialog):
    def __init__(self, parent, title="Add Song", song=None):
        self.song = song or {"title": "", "number": ""}
        super().__init__(parent, title=title)

    def body(self, master):
        ttk.Label(master, text="Title:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.title_var = tk.StringVar(value=self.song.get("title", ""))
        self.title_entry = ttk.Entry(master, textvariable=self.title_var, width=40)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(master, text="Number (optional):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.num_var = tk.StringVar(value=self.song.get("number", ""))
        self.num_entry = ttk.Entry(master, textvariable=self.num_var, width=20)
        self.num_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        return self.title_entry

    def apply(self):
        title = self.title_var.get().strip()
        number = self.num_var.get().strip()
        if not title:
            messagebox.showwarning("Validation", "Title cannot be empty")
            self.result = None
            return
        self.result = {"title": title, "number": number}


class SongApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Church Song App")
        self.geometry("600x400")
        self.minsize(520, 300)

        self.songs = load_songs()
        self.filtered = list(self.songs)

        self._build_ui()
        self._refresh_list()

    def _build_ui(self):
        top = ttk.Frame(self)
        top.pack(fill=tk.X, padx=8, pady=8)

        ttk.Label(top, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._on_search())
        self.search_entry = ttk.Entry(top, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 6))

        add_btn = ttk.Button(top, text="Add", command=self._on_add)
        add_btn.pack(side=tk.LEFT, padx=4)
        edit_btn = ttk.Button(top, text="Edit", command=self._on_edit)
        edit_btn.pack(side=tk.LEFT, padx=4)
        del_btn = ttk.Button(top, text="Delete", command=self._on_delete)
        del_btn.pack(side=tk.LEFT, padx=4)

        # list and scrollbar
        mid = ttk.Frame(self)
        mid.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0,8))

        self.listbox = tk.Listbox(mid, activestyle='none')
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind('<Double-1>', lambda e: self._on_edit())

        scrollbar = ttk.Scrollbar(mid, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        bottom = ttk.Frame(self)
        bottom.pack(fill=tk.X, padx=8, pady=6)
        ttk.Label(bottom, text="Total:").pack(side=tk.LEFT)
        self.total_lbl = ttk.Label(bottom, text="0")
        self.total_lbl.pack(side=tk.LEFT, padx=(4,10))

        save_btn = ttk.Button(bottom, text="Save", command=self._on_save)
        save_btn.pack(side=tk.RIGHT, padx=4)
        import_btn = ttk.Button(bottom, text="Import from text...", command=self._on_import)
        import_btn.pack(side=tk.RIGHT, padx=4)

    def _format_item(self, song: Dict) -> str:
        num = song.get('number')
        if num:
            return f"{song.get('title')} — {num}"
        return song.get('title')

    def _refresh_list(self):
        self.listbox.delete(0, tk.END)
        for s in self.filtered:
            self.listbox.insert(tk.END, self._format_item(s))
        self.total_lbl.config(text=str(len(self.filtered)))

    def _on_search(self):
        q = self.search_var.get().lower().strip()
        if not q:
            self.filtered = list(self.songs)
        else:
            self.filtered = [s for s in self.songs if q in s.get('title','').lower() or q in s.get('number','').lower()]
        self._refresh_list()

    def _on_add(self):
        dlg = AddEditDialog(self, title="Add Song")
        if dlg.result:
            self.songs.append(dlg.result)
            self._on_search()  # refresh filtered
            self._auto_save()

    def _selected_index(self):
        sel = self.listbox.curselection()
        if not sel:
            return None
        idx = sel[0]
        # map filtered index to songs index
        item = self.filtered[idx]
        try:
            real_idx = self.songs.index(item)
            return real_idx
        except ValueError:
            return None

    def _on_edit(self):
        real_idx = self._selected_index()
        if real_idx is None:
            messagebox.showinfo("Edit", "Select a song to edit (double-click or select + Edit)")
            return
        song = self.songs[real_idx]
        dlg = AddEditDialog(self, title="Edit Song", song=song)
        if dlg.result:
            self.songs[real_idx] = dlg.result
            self._on_search()
            self._auto_save()

    def _on_delete(self):
        real_idx = self._selected_index()
        if real_idx is None:
            messagebox.showinfo("Delete", "Select a song to delete")
            return
        song = self.songs[real_idx]
        if messagebox.askyesno("Delete", f"Delete '{song.get('title')}'?"):
            del self.songs[real_idx]
            self._on_search()
            self._auto_save()

    def _on_save(self):
        save_songs(self.songs)
        messagebox.showinfo("Save", f"Saved {len(self.songs)} songs to {SONGS_FILE}")

    def _auto_save(self):
        try:
            save_songs(self.songs)
        except Exception:
            pass

    def _on_import(self):
        # simple import: paste lines of "Title - Number" or just title per line
        text = simpledialog.askstring("Import", "Paste songs, one per line. Optionally use 'Title - Number' format.")
        if not text:
            return
        new = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            if ' - ' in line:
                title, num = line.split(' - ', 1)
                new.append({"title": title.strip(), "number": num.strip()})
            else:
                new.append({"title": line, "number": ""})
        self.songs.extend(new)
        self._on_search()
        self._auto_save()
        messagebox.showinfo("Import", f"Imported {len(new)} songs")


def run_cli():
    # Very small CLI interface for quick adds and listing
    songs = load_songs()
    args = sys.argv[2:]
    if not args:
        print("Church Song App - CLI\nUsage:\n  --list         list songs\n  --add 'Title' [Number]   add a song\n  --remove N     remove by index (use --list to see indexes)")
        return
    if args[0] == '--list':
        for i, s in enumerate(songs):
            print(f"{i}: {s.get('title')} {('- ' + s.get('number')) if s.get('number') else ''}")
        return
    if args[0] == '--add' and len(args) >= 2:
        title = args[1]
        number = args[2] if len(args) >= 3 else ""
        songs.append({"title": title, "number": number})
        save_songs(songs)
        print(f"Added: {title}")
        return
    if args[0] == '--remove' and len(args) == 2:
        try:
            idx = int(args[1])
            if 0 <= idx < len(songs):
                removed = songs.pop(idx)
                save_songs(songs)
                print(f"Removed: {removed.get('title')}")
            else:
                print("Index out of range")
        except ValueError:
            print("Invalid index")
        return
    print("Unknown CLI command")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        run_cli()
    else:
        app = SongApp()
        app.mainloop()
