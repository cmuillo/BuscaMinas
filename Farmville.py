"""
FarmVille Ultimate - Tkinter Edition

Implementación completa según especificación del usuario.

Contiene:
- Interfaz Tkinter 580x650
- 6 parcelas (3x2) con estados y timers independientes
- Tienda con semillas y pesticida
- Inventario y selector radial de semillas
- Sistema de plagas (25% en brote)
- Sonidos con winsound (Windows)
- Guardar/Cargar partida en JSON
"""
import json
import os
import random
import time
import tkinter as tk
from tkinter import ttk, messagebox

try:
	import winsound
	HAVE_WINSOUND = True
except Exception:
	HAVE_WINSOUND = False

# --- Configuración de cultivos ---
CROPS = {
	"zanahoria": {
		"name": "Zanahoria",
		"level": 1,
		"seed_cost": 10,
		"sell_value": 20,
		"net": 10,
		"time": 4,
		"xp": 25,
	},
	"tomate": {
		"name": "Tomate",
		"level": 2,
		"seed_cost": 25,
		"sell_value": 60,
		"net": 35,
		"time": 8,
		"xp": 60,
	},
	"sandia": {
		"name": "Sandía",
		"level": 3,
		"seed_cost": 50,
		"sell_value": 130,
		"net": 80,
		"time": 14,
		"xp": 150,
	},
}

PESTICIDE_COST = 15

SAVE_FILE = "partida_farmville.json"

# Estado de parcelas
# 0: Vacía, 1: Arada, 2: Sembrado, 3: Brote, 4: Madura, 5: Infestada
STATE_COLORS = {
	0: "#7CFC00",  # verde pasto
	1: "#6B4226",  # marrón oscuro
	2: "#CD853F",  # marrón claro
	3: "#9ACD32",  # verde claro
	4: "#FF4500",  # rojo vivo
	5: "#2F4F4F",  # gris ceniza
}


class Plot:
	def __init__(self):
		self.state = 0
		self.crop_key = None
		self.remaining = 0
		self.infested = False
		self._timer_job = None


class FarmvilleApp:
	def __init__(self, root):
		self.root = root
		root.title("FarmVille Ultimate")
		root.geometry("580x650")
		root.resizable(False, False)

		# Stats
		self.money = 100
		self.level = 1
		self.xp = 0
		self.xp_threshold = 100

		# Inventory
		self.inventory = {"zanahoria": 0, "tomate": 0, "sandia": 0, "pesticide": 0}

		# Plots (3x2 = 6)
		self.plots = [Plot() for _ in range(6)]

		# Selected seed for sowing
		self.selected_seed = tk.StringVar(value="zanahoria")

		self.build_ui()
		self.update_header()
		self.update_store_ui()

	# ---------- UI ----------
	def build_ui(self):
		header = ttk.Frame(self.root)
		header.pack(fill=tk.X, padx=8, pady=6)

		self.money_label = ttk.Label(header, text="$0", font=(None, 12, "bold"))
		self.money_label.pack(side=tk.LEFT, padx=6)

		self.level_label = ttk.Label(header, text="Nivel: 1", font=(None, 12))
		self.level_label.pack(side=tk.LEFT, padx=12)

		self.xp_label = ttk.Label(header, text="XP: 0/100", font=(None, 12))
		self.xp_label.pack(side=tk.LEFT, padx=12)

		# Notebook
		self.notebook = ttk.Notebook(self.root)
		self.notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)

		# Mi Granja
		self.tab_farm = ttk.Frame(self.notebook)
		self.notebook.add(self.tab_farm, text="🚜 Mi Granja")
		self.build_farm_tab(self.tab_farm)

		# Tienda
		self.tab_shop = ttk.Frame(self.notebook)
		self.notebook.add(self.tab_shop, text="🏪 Tienda")
		self.build_shop_tab(self.tab_shop)

		# Partida
		self.tab_save = ttk.Frame(self.notebook)
		self.notebook.add(self.tab_save, text="💾 Partida")
		self.build_save_tab(self.tab_save)

	def build_farm_tab(self, parent):
		left = ttk.Frame(parent)
		left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6, pady=6)

		# Grid 3x2 (we'll place 3 columns x 2 rows)
		self.plot_buttons = []
		for r in range(2):
			for c in range(3):
				idx = r * 3 + c
				btn = tk.Button(left, text=f"Parcel {idx+1}", bg=STATE_COLORS[0], width=16, height=6,
								command=lambda i=idx: self.on_plot_click(i))
				btn.grid(row=r, column=c, padx=6, pady=6)
				self.plot_buttons.append(btn)

		# Right panel: seed selector + inventory
		right = ttk.Frame(parent, width=160)
		right.pack(side=tk.RIGHT, fill=tk.Y, padx=6, pady=6)

		ttk.Label(right, text="Seleccionar Semilla:").pack(anchor=tk.NW, pady=4)
		for key in ["zanahoria", "tomate", "sandia"]:
			r = ttk.Radiobutton(right, text=f"{CROPS[key]['name']} (0)", value=key, variable=self.selected_seed)
			r.pack(anchor=tk.NW, pady=2)

		ttk.Separator(right, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=8)
		self.inv_label = ttk.Label(right, text=self.inventory_text())
		self.inv_label.pack(anchor=tk.NW)

	def build_shop_tab(self, parent):
		frame = ttk.Frame(parent)
		frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

		ttk.Label(frame, text="Tienda - Comprar semillas y pesticida", font=(None, 11, 'bold')).pack(pady=6)

		self.shop_buttons = {}
		for key, props in CROPS.items():
			frm = ttk.Frame(frame)
			frm.pack(fill=tk.X, pady=4)
			name = props['name']
			ttk.Label(frm, text=f"{name} - Semilla ${props['seed_cost']} | Venta ${props['sell_value']} | Requiere Nivel {props['level']}").pack(side=tk.LEFT)
			btn = ttk.Button(frm, text="Comprar Semilla", command=lambda k=key: self.buy_seed(k))
			btn.pack(side=tk.RIGHT)
			self.shop_buttons[key] = btn

		# Pesticida
		pest_frm = ttk.Frame(frame)
		pest_frm.pack(fill=tk.X, pady=8)
		ttk.Label(pest_frm, text=f"Pesticida - ${PESTICIDE_COST}").pack(side=tk.LEFT)
		self.pest_btn = ttk.Button(pest_frm, text="Comprar Pesticida", command=self.buy_pesticide)
		self.pest_btn.pack(side=tk.RIGHT)

	def build_save_tab(self, parent):
		frame = ttk.Frame(parent)
		frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
		ttk.Label(frame, text="Guardar / Cargar Partida", font=(None, 11, 'bold')).pack(pady=6)
		ttk.Button(frame, text="Guardar Partida", command=self.save_game).pack(pady=6)
		ttk.Button(frame, text="Cargar Partida", command=self.load_game).pack(pady=6)
		ttk.Label(frame, text="Archivo: " + SAVE_FILE).pack(pady=4)

	# ---------- UI Helpers ----------
	def inventory_text(self):
		return f"Semillas: Zanahoria ({self.inventory['zanahoria']})  Tomate ({self.inventory['tomate']})  Sandía ({self.inventory['sandia']})\nPesticida: {self.inventory['pesticide']}"

	def update_header(self):
		self.money_label.config(text=f"$ {self.money}")
		self.level_label.config(text=f"Nivel: {self.level}")
		self.xp_label.config(text=f"XP: {self.xp}/{int(self.xp_threshold)}")

	def update_store_ui(self):
		# Update shop buttons according to level
		for key, btn in self.shop_buttons.items():
			required = CROPS[key]['level']
			if self.level >= required:
				btn.state(['!disabled'])
			else:
				btn.state(['disabled'])

		# Update radiobutton labels showing counts
		# Find radiobutton children in right panel
		right_children = self.tab_farm.winfo_children()[-1].winfo_children()
		rb_index = 1
		for widget in right_children:
			if isinstance(widget, ttk.Radiobutton):
				key = widget['value']
				widget.config(text=f"{CROPS[key]['name']} ({self.inventory[key]})")
				rb_index += 1

		# inventory label
		self.inv_label.config(text=self.inventory_text())

	def refresh_plot_ui(self, idx):
		plot = self.plots[idx]
		btn = self.plot_buttons[idx]
		color = STATE_COLORS.get(plot.state, "#000000")
		btn.config(bg=color)
		text = ""
		if plot.state == 0:
			text = f"Parcel {idx+1}\n(Vacía)"
		elif plot.state == 1:
			text = "Arada\nClic para Sembrar"
		elif plot.state == 2:
			text = "Sembrado"
		elif plot.state == 3:
			text = f"Brote\n{plot.crop_key and CROPS[plot.crop_key]['name'] or ''}\n{plot.remaining}s"
		elif plot.state == 4:
			text = "¡COSECHAR!"
		elif plot.state == 5:
			text = "⚠️ [PLAGA] ⚠️\nClic con Pesticida"
		btn.config(text=text)

	# ---------- Plot Logic ----------
	def on_plot_click(self, idx):
		plot = self.plots[idx]
		# Click behavior by state
		if plot.state == 0:
			plot.state = 1
			self.refresh_plot_ui(idx)
		elif plot.state == 1:
			# Try to sow selected seed if available
			seed = self.selected_seed.get()
			if self.inventory.get(seed, 0) > 0:
				# consume seed
				self.inventory[seed] -= 1
				plot.crop_key = seed
				plot.state = 2
				plot.remaining = 0
				self.refresh_plot_ui(idx)
				# small delay to move to brote
				self.root.after(700, lambda i=idx: self._enter_brote(i))
				self.update_store_ui()
			else:
				messagebox.showinfo("Semilla insuficiente", "No tienes semillas de ese tipo. Compra en la tienda.")
		elif plot.state == 2:
			# Sembrado: bloqueado (no-op)
			pass
		elif plot.state == 3:
			# brote / en crecimiento: no-op
			pass
		elif plot.state == 4:
			# cosechar
			key = plot.crop_key
			if key and key in CROPS:
				value = CROPS[key]['sell_value']
				xp_gain = CROPS[key]['xp']
				self.money += value
				self.add_xp(xp_gain)
				# sonido
				self.play_success_sound()
			# reset
			self._reset_plot(idx)
			self.update_header()
			self.update_store_ui()
		elif plot.state == 5:
			# infestado: cure if pesticide in inventory
			if self.inventory['pesticide'] > 0:
				self.inventory['pesticide'] -= 1
				plot.infested = False
				# resume growth as brote
				plot.state = 3
				# resume timer with remaining (if 0, then immediately mature)
				if plot.remaining <= 0:
					self._mature_plot(idx)
				else:
					self._start_plot_timer(idx)
				self.update_store_ui()
			else:
				messagebox.showinfo("Plaga", "Necesitas pesticida para curar esta parcela. Cómpralo en la tienda.")

	def _enter_brote(self, idx):
		plot = self.plots[idx]
		if plot.state != 2:
			return
		plot.state = 3
		crop = CROPS.get(plot.crop_key)
		if not crop:
			# safety
			plot.state = 0
			plot.crop_key = None
			self.refresh_plot_ui(idx)
			return
		plot.remaining = crop['time']
		# chance of plaga 25%
		if random.random() < 0.25:
			plot.state = 5
			plot.infested = True
			# play plaga sound
			self.play_plague_sound()
			self.refresh_plot_ui(idx)
			return
		plot.infested = False
		self._start_plot_timer(idx)

	def _start_plot_timer(self, idx):
		plot = self.plots[idx]
		# cancel previous if any
		if plot._timer_job:
			try:
				self.root.after_cancel(plot._timer_job)
			except Exception:
				pass
			plot._timer_job = None

		def tick():
			if plot.state != 3:
				return
			plot.remaining -= 1
			if plot.remaining <= 0:
				self._mature_plot(idx)
			else:
				self.refresh_plot_ui(idx)
				plot._timer_job = self.root.after(1000, tick)

		self.refresh_plot_ui(idx)
		plot._timer_job = self.root.after(1000, tick)

	def _mature_plot(self, idx):
		plot = self.plots[idx]
		plot.state = 4
		plot.remaining = 0
		self.refresh_plot_ui(idx)
		# success sound
		self.play_success_sound()

	def _reset_plot(self, idx):
		plot = self.plots[idx]
		# cancel timer
		if plot._timer_job:
			try:
				self.root.after_cancel(plot._timer_job)
			except Exception:
				pass
			plot._timer_job = None
		plot.state = 0
		plot.crop_key = None
		plot.remaining = 0
		plot.infested = False
		self.refresh_plot_ui(idx)

	# ---------- Economy / Shop ----------
	def buy_seed(self, key):
		props = CROPS[key]
		if self.level < props['level']:
			messagebox.showinfo("Bloqueado", "Tu nivel es insuficiente para comprar estas semillas.")
			return
		if self.money < props['seed_cost']:
			messagebox.showinfo("Fondos insuficientes", "No tienes suficiente dinero.")
			return
		self.money -= props['seed_cost']
		self.inventory[key] += 1
		self.update_header()
		self.update_store_ui()

	def buy_pesticide(self):
		if self.money < PESTICIDE_COST:
			messagebox.showinfo("Fondos insuficientes", "No tienes suficiente dinero.")
			return
		self.money -= PESTICIDE_COST
		self.inventory['pesticide'] += 1
		self.update_header()
		self.update_store_ui()

	# ---------- XP / Level ----------
	def add_xp(self, amount):
		self.xp += amount
		leveled = False
		while self.xp >= self.xp_threshold:
			self.xp -= int(self.xp_threshold)
			self.level += 1
			self.xp_threshold *= 1.6
			leveled = True
		if leveled:
			messagebox.showinfo("Subiste de nivel", f"Has alcanzado Nivel {self.level}!")
		self.update_header()
		self.update_store_ui()

	# ---------- Sonidos ----------
	def play_success_sound(self):
		if not HAVE_WINSOUND:
			return
		try:
			winsound.Beep(1500, 80)
			winsound.Beep(2000, 80)
		except Exception:
			pass

	def play_plague_sound(self):
		if not HAVE_WINSOUND:
			return
		try:
			winsound.Beep(350, 500)
		except Exception:
			pass

	# ---------- Persistencia ----------
	def save_game(self):
		data = {
			"money": self.money,
			"level": self.level,
			"xp": self.xp,
			"xp_threshold": self.xp_threshold,
			"inventory": self.inventory,
			"plots": [],
			"saved_at": time.time(),
		}
		for p in self.plots:
			data['plots'].append({
				'state': p.state,
				'crop_key': p.crop_key,
				'remaining': p.remaining,
				'infested': p.infested,
			})
		try:
			with open(SAVE_FILE, 'w', encoding='utf-8') as f:
				json.dump(data, f, indent=2)
			messagebox.showinfo("Guardado", f"Partida guardada en {SAVE_FILE}")
		except Exception as e:
			messagebox.showerror("Error", f"No se pudo guardar: {e}")

	def load_game(self):
		if not os.path.exists(SAVE_FILE):
			messagebox.showinfo("No existe", f"No se encontró {SAVE_FILE}")
			return
		try:
			with open(SAVE_FILE, 'r', encoding='utf-8') as f:
				data = json.load(f)
		except Exception as e:
			messagebox.showerror("Error", f"No se pudo leer: {e}")
			return

		# apply
		self.money = data.get('money', self.money)
		self.level = data.get('level', self.level)
		self.xp = data.get('xp', self.xp)
		self.xp_threshold = data.get('xp_threshold', self.xp_threshold)
		inv = data.get('inventory', {})
		for k in ['zanahoria', 'tomate', 'sandia', 'pesticide']:
			self.inventory[k] = inv.get(k, 0)

		plots_data = data.get('plots', [])
		for i, pinfo in enumerate(plots_data[:6]):
			p = self.plots[i]
			# cancel any running timers
			if p._timer_job:
				try:
					self.root.after_cancel(p._timer_job)
				except Exception:
					pass
				p._timer_job = None

			p.state = pinfo.get('state', 0)
			p.crop_key = pinfo.get('crop_key')
			p.remaining = pinfo.get('remaining', 0)
			p.infested = pinfo.get('infested', False)

			# If it's growing and not infested, restart timer with remaining
			if p.state == 3 and not p.infested and p.remaining > 0:
				self._start_plot_timer(i)
			# If matured, ensure state 4
			if p.state == 4:
				self.refresh_plot_ui(i)
			# If infested, show infestation
			if p.state == 5:
				self.refresh_plot_ui(i)

		self.update_header()
		self.update_store_ui()
		messagebox.showinfo("Cargado", "Partida cargada correctamente.")


def main():
	root = tk.Tk()
	app = FarmvilleApp(root)
	# initial render of plots
	for i in range(6):
		app.refresh_plot_ui(i)
	root.mainloop()


if __name__ == '__main__':
	main()

