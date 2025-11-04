"""
Flask web server for AR Colorize application
Serves the web interface and provides API endpoints
"""

from flask import Flask, render_template, send_from_directory, jsonify
import os

app = Flask(__name__, 
            template_folder=os.path.dirname(os.path.abspath(__file__)),
            static_folder=os.path.dirname(os.path.abspath(__file__)))

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'index.html')

@app.route('/api/colors')
def get_colors():
    """Return available color palette"""
    colors = [
        {'name': 'Pure White', 'hex': '#FFFFFF'},
        {'name': 'Soft Cream', 'hex': '#FFF8DC'},
        {'name': 'Light Gray', 'hex': '#D3D3D3'},
        {'name': 'Sky Blue', 'hex': '#87CEEB'},
        {'name': 'Mint Green', 'hex': '#98FF98'},
        {'name': 'Peach', 'hex': '#FFDAB9'},
        {'name': 'Lavender', 'hex': '#E6E6FA'},
        {'name': 'Coral', 'hex': '#FF7F50'},
        {'name': 'Sage Green', 'hex': '#9DC183'},
        {'name': 'Warm Beige', 'hex': '#F5F5DC'},
        {'name': 'Powder Blue', 'hex': '#B0E0E6'},
        {'name': 'Blush Pink', 'hex': '#FFB6C1'}
    ]
    return jsonify(colors)

@app.route('/api/info')
def get_info():
    """Return project information"""
    info = {
        'name': 'AR COLORIZE - Real-Time Wall Repainting System',
        'description': 'An Augmented Reality application for visualizing wall color changes',
        'version': '1.0.0',
        'features': [
            'Real-time wall detection',
            'AR color overlay',
            'Interactive color palette',
            'Live camera processing',
            'Web-based interface'
        ],
        'resources': {
            'presentation': 'https://docs.google.com/presentation/d/1lm_x59cE4T_IUTqp2TxGHdF8QPpstSYu/edit?usp=sharing&ouid=113325350073162535117&rtpof=true&sd=true',
            'pitch_deck': 'https://docs.google.com/presentation/d/1G2nbHoXkZ7wLqvfVeKmrSqiUcdFWBBaT/edit?usp=sharing&ouid=113325350073162535117&rtpof=true&sd=true',
            'documentation': 'https://docs.google.com/document/d/1eZOTEHgEvpsorTx_cRki9kjD8IY8d2Bw/edit?usp=drive_link&ouid=113325350073162535117&rtpof=true&sd=true',
            'drive_folder': 'https://drive.google.com/drive/folders/10hGKmjirxh1mM4tHEsWn4F8LNMDriFOm?usp=drive_link'
        }
    }
    return jsonify(info)

if __name__ == '__main__':
    import os
    
    # Get configuration from environment variables
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', '5000'))
    
    print("Starting AR Colorize Web Server...")
    print(f"Open http://{host}:{port} in your browser")
    if debug_mode:
        print("WARNING: Running in debug mode")
    
    app.run(debug=debug_mode, host=host, port=port)
