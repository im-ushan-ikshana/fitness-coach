from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from typing import List, Dict, Optional

class YouTubeSearch:
    """
    A class to handle YouTube search operations using the YouTube Data API.
    """
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the YouTube API client.
        
        Args:
            api_key (str, optional): YouTube Data API key. If not provided, will try to get from environment.
        """
        self.api_key = api_key or os.getenv('YOUTUBE_API_KEY')
        if not self.api_key:
            raise ValueError("YouTube API key is required. Set YOUTUBE_API_KEY environment variable or pass it directly.")
        
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    async def search_workout_videos(
        self,
        query: str,
        max_results: int = 5,
        relevance_keywords: List[str] = None,
        video_duration: str = 'medium'
    ) -> List[Dict]:
        """
        Search for workout videos on YouTube based on specific criteria.
        
        Args:
            query (str): The main search query
            max_results (int): Maximum number of results to return
            relevance_keywords (List[str], optional): Additional keywords to filter results
            video_duration (str): Duration filter ('short', 'medium', 'long')
            
        Returns:
            List[Dict]: List of video information including id, title, description, and thumbnail
        """
        try:
            # Enhance search query with relevance keywords if provided
            if relevance_keywords:
                query = f"{query} {' '.join(relevance_keywords)}"

            # Set up search parameters
            search_params = {
                'q': query,
                'part': 'snippet',
                'maxResults': max_results,
                'type': 'video',
                'videoDuration': video_duration,
                'regionCode': 'US',  # Default to US region
                'relevanceLanguage': 'en'
            }

            # Execute search request
            search_response = self.youtube.search().list(**search_params).execute()

            # Process and format results
            videos = []
            for item in search_response.get('items', []):
                video_data = {
                    'video_id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'thumbnail_url': item['snippet']['thumbnails']['medium']['url'],
                    'channel_title': item['snippet']['channelTitle'],
                    'published_at': item['snippet']['publishedAt']
                }
                videos.append(video_data)

            return videos

        except HttpError as e:
            raise Exception(f"An error occurred while searching YouTube: {str(e)}")

    async def get_video_details(self, video_id: str) -> Dict:
        """
        Get detailed information about a specific video.
        
        Args:
            video_id (str): YouTube video ID
            
        Returns:
            Dict: Detailed video information
        """
        try:
            video_response = self.youtube.videos().list(
                part='snippet,contentDetails,statistics',
                id=video_id
            ).execute()

            if not video_response.get('items'):
                raise ValueError(f"No video found with ID: {video_id}")

            video_data = video_response['items'][0]
            return {
                'video_id': video_id,
                'title': video_data['snippet']['title'],
                'description': video_data['snippet']['description'],
                'duration': video_data['contentDetails']['duration'],
                'view_count': video_data['statistics']['viewCount'],
                'like_count': video_data.get('statistics', {}).get('likeCount', 'N/A'),
                'channel_title': video_data['snippet']['channelTitle'],
                'thumbnail_url': video_data['snippet']['thumbnails']['high']['url']
            }

        except HttpError as e:
            raise Exception(f"An error occurred while fetching video details: {str(e)}")