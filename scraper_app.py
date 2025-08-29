import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import threading
import time
from scraper_core import TippmixProScraper

class ScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TippmixPro scraper API by B3RC1")
        
        # Set window icon if icon.ico exists
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass  # Icon file doesn't exist, use default
        self.root.geometry("800x600")
        
        # Initialize scraper with Selenium enabled by default and optimized timing
        self.scraper = TippmixProScraper(use_selenium=True)
        self.scraping_thread = None
        self.is_scraping = False
        
        # Settings file
        self.settings_file = "scraper_settings.json"
        
        # Theme configuration
        self.current_theme = "light"
        self.themes = {
            "light": {
                "bg": "#f0f0f0",
                "fg": "#000000",
                "button_bg": "#e1e1e1",
                "entry_bg": "#ffffff",
                "text_bg": "#ffffff",
                "text_fg": "#000000",
                "frame_label_bg": "#f0f0f0"
            },
            "dark": {
                "bg": "#2b2b2b",
                "fg": "#ffffff",
                "button_bg": "#404040",
                "entry_bg": "#3c3c3c",
                "text_bg": "#3c3c3c",
                "text_fg": "#ffffff",
                "frame_label_bg": "#2b2b2b"
            }
        }
        
        # Setup UI first, then load settings
        self.setup_ui()
        self.load_settings()
        # Update theme combo box to reflect loaded theme
        self.theme_var.set(self.current_theme)
        self.apply_theme(self.current_theme)
        
        # Bind closing event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def load_settings(self):
        """Load settings from JSON file"""
        try:
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
                self.url_var.set(settings.get('url', ''))
                self.interval_var.set(settings.get('interval', '30'))
                self.output_file_var.set(settings.get('output_file', 'scraped_data.json'))
                self.current_theme = settings.get('theme', 'light')
        except FileNotFoundError:
            pass
    
    def save_settings(self):
        """Save settings to JSON file"""
        settings = {
            'url': self.url_var.get(),
            'interval': self.interval_var.get(),
            'output_file': self.output_file_var.get(),
            'theme': self.current_theme,
        }
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f, indent=2)
            self.log_message("Settings saved to " + self.settings_file)
    
    def setup_ui(self):
        """Setup the user interface"""
        # Variables
        self.url_var = tk.StringVar()
        self.interval_var = tk.StringVar(value="30")
        self.output_file_var = tk.StringVar(value="scraped_data.json")
        self.theme_var = tk.StringVar(value=self.current_theme)
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # URL input
        ttk.Label(main_frame, text="Website URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=50)
        self.url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # Polling interval
        ttk.Label(main_frame, text="Polling Interval (seconds):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.interval_entry = ttk.Entry(main_frame, textvariable=self.interval_var, width=10)
        self.interval_entry.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(5, 0))

        # Output file
        ttk.Label(main_frame, text="Output JSON File:").grid(row=4, column=0, sticky=tk.W, pady=5)
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        output_frame.columnconfigure(0, weight=1)
        
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_file_var)
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(output_frame, text="Browse", command=self.browse_file).grid(row=0, column=1)
        
        # Theme selector
        ttk.Label(main_frame, text="Theme:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.theme_combo = ttk.Combobox(main_frame, textvariable=self.theme_var, 
                                       values=["light", "dark"], state="readonly", width=10)
        self.theme_combo.grid(row=5, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        self.theme_combo.bind('<<ComboboxSelected>>', self.on_theme_change)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=9, column=0, columnspan=2, pady=10)
        
        self.start_button = ttk.Button(buttons_frame, text="Start Scraping", command=self.start_scraping)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(buttons_frame, text="Stop Scraping", command=self.stop_scraping, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(buttons_frame, text="Save Settings", command=self.save_settings).pack(side=tk.LEFT, padx=5)
        
        # Log area
        ttk.Label(main_frame, text="Log", font=("TkDefaultFont", 10, "bold")).grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        log_frame = ttk.Frame(main_frame)
        log_frame.grid(row=11, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(log_frame, height=10, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for log
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        # Configure main frame row weights
        main_frame.rowconfigure(11, weight=1)
    
    def on_theme_change(self, event=None):
        """Handle theme change"""
        self.current_theme = self.theme_var.get()
        self.apply_theme(self.current_theme)
    
    def apply_theme(self, theme_name):
        """Apply the selected theme"""
        try:
            theme = self.themes[theme_name]
            
            # Configure root window
            self.root.configure(bg=theme['bg'])
            
            # Configure text widgets
            self.log_text.configure(
                bg=theme['text_bg'],
                fg=theme['text_fg'],
                insertbackground=theme['fg']
            )
            
            # Configure ttk style
            style = ttk.Style()
            style.configure('TFrame', background=theme['bg'])
            style.configure('TLabel', background=theme['bg'], foreground=theme['fg'])
            style.configure('TButton', background=theme['button_bg'])
            style.configure('TEntry', fieldbackground=theme['entry_bg'], foreground='#000000', insertcolor='#000000')
            style.configure('TCombobox', fieldbackground=theme['entry_bg'], foreground='#000000', 
                          background=theme['entry_bg'], selectbackground=theme['button_bg'], selectforeground='#000000')
            style.configure('TLabelframe', background=theme['bg'])
            style.configure('TLabelframe.Label', background=theme['frame_label_bg'], foreground=theme['fg'])
            
            # Apply style to all widgets
            self._apply_style_to_widget(self.root, theme_name)
            
        except Exception as e:
            print(f"Error applying theme: {e}")
    
    def _apply_style_to_widget(self, widget, theme_name):
        """Recursively apply style to widget and its children"""
        try:
            theme = self.themes[theme_name]
            
            # Apply to known ttk widget types
            widget_type = str(type(widget))
            if 'ttk.Frame' in widget_type:
                widget.configure(style='TFrame')
            elif 'ttk.LabelFrame' in widget_type:
                widget.configure(style='TLabelframe')
            elif 'ttk.Label' in widget_type:
                widget.configure(style='TLabel')
            elif 'ttk.Button' in widget_type:
                widget.configure(style='TButton')
            elif 'ttk.Entry' in widget_type:
                widget.configure(style='TEntry')
            elif 'ttk.Combobox' in widget_type:
                widget.configure(style='TCombobox')
            
            # Apply to children
            for child in widget.winfo_children():
                self._apply_style_to_widget(child, theme_name)
                
        except Exception as e:
            pass  # Ignore errors for unknown widget types
    
    def start_scraping(self):
        """Start the scraping process"""
        if not self.validate_inputs():
            return
        # Open the page first
        try:
            original_url = self.url_var.get()
            
            # For TippmixPro scraper, show URL conversion
            if isinstance(self.scraper, TippmixProScraper):
                converted_url = self.scraper.convert_tippmixpro_url(original_url)
                if converted_url != original_url:
                    self.log_message(f"URL converted to: {converted_url}")
                    self.scraper.open_page(converted_url)
                    self.log_message("Page opened successfully!")
            
        except Exception as e:
            self.log_message(f"Error opening page: {e}")
            return
        
        # Start scraping thread
        self.is_scraping = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        interval = int(self.interval_var.get())
        output_file = self.output_file_var.get()
        
        self.scraping_thread = threading.Thread(
            target=self.scraping_worker,
            args=(interval, output_file),
            daemon=True
        )
        self.scraping_thread.start()
        
        self.log_message("Scraping started")
    
    def stop_scraping(self):
        """Stop the scraping process"""
        self.is_scraping = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        # Close the page
        self.scraper.close_page()
        
        self.log_message("Scraping stopped")
    
    def scraping_worker(self, interval, output_file):
        """Worker thread for scraping"""
        while self.is_scraping:
            try:
                # Scrape current page (gets fresh content from browser)
                data = self.scraper.scrape_market_titles()
                
                if data:
                    self.save_data(data, output_file)
                    self.log_message(f"Data scraped and saved to {output_file}")
                else:
                    self.log_message("No betting options found yet...")
                
                # Wait for next interval
                time.sleep(interval)
                
            except Exception as e:
                self.log_message(f"Error during scraping: {e}")
                time.sleep(interval)
    
    def save_data(self, data, filename):
        """Save scraped data to JSON file (overwrites existing content)"""
        try:
            # Create a single dictionary with timestamp
            data_with_timestamp = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "data": data
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data_with_timestamp, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.log_message(f"Error saving data: {e}")
    
    def validate_inputs(self):
        """Validate user inputs"""
        if not self.url_var.get().strip():
            messagebox.showerror("Error", "Please enter a website URL")
            return False
        
        # Validate URL ends with /all or /all/
        url = self.url_var.get().strip()
        if not (url.endswith('/all') or url.endswith('/all/')):
            messagebox.showerror("Error", "URL must end with '/all' or '/all/'")
            return False
        
        try:
            interval = int(self.interval_var.get())
            if interval <= 0:
                messagebox.showerror("Error", "Polling interval must be greater than 0")
                return False
        except ValueError:
            messagebox.showerror("Error", "Polling interval must be a valid number")
            return False
        
        if not self.output_file_var.get().strip():
            messagebox.showerror("Error", "Please enter an output file name")
            return False
        
        return True
    
    def browse_file(self):
        """Browse for output file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.output_file_var.set(filename)
    
    def log_message(self, message):
        """Add message to log"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # Use after() to safely update GUI from thread
        self.root.after(0, lambda: self.log_text.insert(tk.END, log_entry))
        self.root.after(0, lambda: self.log_text.see(tk.END))
    
    def on_closing(self):
        """Handle application closing"""
        # Show warning if scraping is active
        if self.is_scraping:
            result = messagebox.askyesno(
                "Confirm Exit", 
                "Scraping is currently active. Are you sure you want to close the application?"
            )
            if not result:
                return  # User cancelled, don't close
        
        # Stop scraping if active
        if self.is_scraping:
            self.stop_scraping()
        elif self.scraper.is_page_open:
            self.scraper.close_page()
        
        self.save_settings()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = ScraperApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()