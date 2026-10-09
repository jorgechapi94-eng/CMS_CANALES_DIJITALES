import requests
from flask import Blueprint, jsonify, current_app

radio_bp = Blueprint('radio', __name__, url_prefix='/api/radio')

@radio_bp.route('/status', methods=['GET'])
def get_radio_status():
    status_url = current_app.config.get('ICECAST_STATUS_URL')
    
    fallback_data = {
        'title': 'Desconocido',
        'artist': 'UPEC Radio',
        'listeners': 0,
        'bitrate': 0,
        'genre': 'Radio'
    }
    
    if not status_url:
        return jsonify(fallback_data), 200
        
    try:
        response = requests.get(status_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        sources = data.get('icestats', {}).get('source', [])
        if isinstance(sources, dict):
            sources = [sources]
            
        live_source = None
        for s in sources:
            if s.get('listenurl', '').endswith('/live'):
                live_source = s
                break
                
        if not live_source and sources:
            live_source = sources[0]
            
        if live_source:
            return jsonify({
                'title': live_source.get('title', fallback_data['title']),
                'artist': live_source.get('artist', fallback_data['artist']),
                'listeners': live_source.get('listeners', 0),
                'bitrate': live_source.get('bitrate', 0),
                'genre': live_source.get('genre', fallback_data['genre'])
            }), 200
            
        return jsonify(fallback_data), 200
        
    except Exception as e:
        return jsonify(fallback_data), 200
