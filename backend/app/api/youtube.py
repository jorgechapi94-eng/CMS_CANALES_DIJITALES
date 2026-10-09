import time
import requests
from flask import Blueprint, request, jsonify, current_app

youtube_bp = Blueprint('youtube', __name__, url_prefix='/api/youtube')

_cache = {
    'data': None,
    'timestamp': 0
}

@youtube_bp.route('/latest', methods=['GET'])
def get_latest_videos():
    limit = request.args.get('limit', 12, type=int)
    limit = min(limit, 50)
    
    now = time.time()
    ttl = current_app.config.get('YOUTUBE_CACHE_TTL', 1800)
    
    # Return cache if valid
    if _cache['data'] is not None and (now - _cache['timestamp'] < ttl):
        return jsonify(_cache['data'][:limit]), 200
        
    api_key = current_app.config.get('YOUTUBE_API_KEY')
    playlist_id = current_app.config.get('YOUTUBE_UPLOADS_PLAYLIST_ID')
    
    if not api_key or not playlist_id:
        return jsonify({'error': 'YouTube API not configured'}), 500
        
    try:
        url = 'https://www.googleapis.com/youtube/v3/playlistItems'
        params = {
            'part': 'snippet',
            'playlistId': playlist_id,
            'maxResults': 50,
            'key': api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        videos = []
        for item in data.get('items', []):
            snippet = item.get('snippet', {})
            video_id = snippet.get('resourceId', {}).get('videoId')
            if video_id:
                videos.append({
                    'id': video_id,
                    'title': snippet.get('title'),
                    'description': snippet.get('description'),
                    'publishedAt': snippet.get('publishedAt'),
                    'thumbnails': snippet.get('thumbnails'),
                    'youtubeUrl': f'https://www.youtube.com/watch?v={video_id}'
                })
                
        # Update cache
        _cache['data'] = videos
        _cache['timestamp'] = now
        
        return jsonify(videos[:limit]), 200
        
    except Exception as e:
        # Fallback to stale cache on failure
        if _cache['data'] is not None:
            return jsonify(_cache['data'][:limit]), 200
        return jsonify({'error': str(e)}), 500
