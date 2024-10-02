import tkinter as tk
from tkinter import ttk, scrolledtext
import json
import datetime
import re
from collections import defaultdict
import os

class SimpleSIEM:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple SIEM Dashboard")
        self.root.geometry("800x600")
        
        # Initialize data structures
        self.alerts = []
        self.log_patterns = {
            'FAILED_LOGIN': r'Failed login attempt from IP: (\d+\.\d+\.\d+\.\d+)',
            'SUSPICIOUS_ACTIVITY': r'Suspicious activity detected: (.*)',
            'MALWARE_DETECTED': r'Malware signature detected: (.*)',
        }
        
        self.setup_gui()
        self.load_sample_data()

    def setup_gui(self):
        # Create main frames
        self.dashboard_frame = ttk.Frame(self.root)
        self.dashboard_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create tabs
        self.tab_control = ttk.Notebook(self.dashboard_frame)
        
        # Alert Dashboard Tab
        self.alert_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.alert_tab, text='Alert Dashboard')
        
        # Log Monitoring Tab
        self.log_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.log_tab, text='Log Monitor')
        
        self.tab_control.pack(expand=True, fill=tk.BOTH)

        # Setup Alert Dashboard
        self.setup_alert_dashboard()
        
        # Setup Log Monitor
        self.setup_log_monitor()

    def setup_alert_dashboard(self):
        # Alert Statistics
        stats_frame = ttk.LabelFrame(self.alert_tab, text="Alert Statistics")
        stats_frame.pack(fill=tk.X, padx=5, pady=5)

        self.stats_labels = {
            'Total Alerts': ttk.Label(stats_frame, text="Total Alerts: 0"),
            'Critical Alerts': ttk.Label(stats_frame, text="Critical Alerts: 0"),
            'High Alerts': ttk.Label(stats_frame, text="High Alerts: 0")
        }

        for label in self.stats_labels.values():
            label.pack(side=tk.LEFT, padx=10, pady=5)

        # Alert List
        self.alert_tree = ttk.Treeview(self.alert_tab, columns=('Time', 'Severity', 'Type', 'Description'))
        self.alert_tree.heading('Time', text='Time')
        self.alert_tree.heading('Severity', text='Severity')
        self.alert_tree.heading('Type', text='Type')
        self.alert_tree.heading('Description', text='Description')
        self.alert_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def setup_log_monitor(self):
        # Log Viewer
        self.log_text = scrolledtext.ScrolledText(self.log_tab)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Control Panel
        control_frame = ttk.Frame(self.log_tab)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(control_frame, text="Load Sample Logs", command=self.load_sample_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Clear Logs", command=self.clear_logs).pack(side=tk.LEFT, padx=5)

    def load_sample_data(self):
        # Sample security events
        sample_events = [
            {
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'severity': 'High',
                'type': 'Failed Login',
                'description': 'Failed login attempt from IP: 192.168.1.100'
            },
            {
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'severity': 'Critical',
                'type': 'Malware Detection',
                'description': 'Malware signature detected: Trojan.Generic.123456'
            }
        ]

        # Clear existing data
        for item in self.alert_tree.get_children():
            self.alert_tree.delete(item)

        # Load sample events
        for event in sample_events:
            self.alert_tree.insert('', tk.END, values=(
                event['timestamp'],
                event['severity'],
                event['type'],
                event['description']
            ))

        # Update statistics
        self.update_statistics()

    def clear_logs(self):
        self.log_text.delete(1.0, tk.END)

    def update_statistics(self):
        alerts = self.alert_tree.get_children()
        critical_alerts = sum(1 for alert in alerts if self.alert_tree.item(alert)['values'][1] == 'Critical')
        high_alerts = sum(1 for alert in alerts if self.alert_tree.item(alert)['values'][1] == 'High')

        self.stats_labels['Total Alerts'].config(text=f"Total Alerts: {len(alerts)}")
        self.stats_labels['Critical Alerts'].config(text=f"Critical Alerts: {critical_alerts}")
        self.stats_labels['High Alerts'].config(text=f"High Alerts: {high_alerts}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleSIEM(root)
    root.mainloop()
