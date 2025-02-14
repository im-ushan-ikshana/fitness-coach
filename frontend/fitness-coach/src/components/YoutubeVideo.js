import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Lottie from 'lottie-react';
import loadingAnimation from '../assets/loading_2.json';
import './YoutubeVideo.css';

const YoutubeVideo = ({ sessionData, selectedExercise }) => {
    const [videos, setVideos] = useState([]);
    const [loading, setLoading] = useState(false);
    const [selectedVideo, setSelectedVideo] = useState(null);
    const [error, setError] = useState(null);

    // Effect to trigger search when exercise is selected
    useEffect(() => {
        if (selectedExercise) {
            let level = !(sessionData.experience_level) ? 'beginners' : sessionData.experience_level;
            let query = selectedExercise + ' for ' + level;
            searchWorkoutVideos(query);
        }
    }, [selectedExercise]);

    const searchWorkoutVideos = async (exerciseName) => {
        setLoading(true);
        setError(null);
        try {
            // Construct search query using exercise name and user's experience level
            const searchQuery = `${exerciseName} ${sessionData.experience_level} form technique`;
            
            const response = await axios.post('http://localhost:8000/youtube-search', {
                query: searchQuery,
                max_results: 10
            });
            
            setVideos(response.data.videos);
            if (response.data.videos.length > 0) {
                setSelectedVideo(response.data.videos[0]);
            }
        } catch (err) {
            setError('Failed to load workout videos. Please try again later.');
            console.error('Error fetching videos:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleVideoSelect = (video) => {
        setSelectedVideo(video);
    };

    if (!selectedExercise) {
        return (
            <div className="youtube-container">
                <div className="search-prompt">
                    <h3>Video Demonstrations</h3>
                    <p>Click on any exercise in the workout plan to see video demonstrations</p>
                </div>
            </div>
        );
    }

    return (
        <div className="youtube-container">
            <h3>Videos for: {selectedExercise}</h3>

            {loading && (
                <div className="loading-container">
                    <Lottie 
                        animationData={loadingAnimation}
                        loop={true}
                        style={{ width: 200, height: 200 }}
                    />
                    <p>Loading demonstration videos...</p>
                </div>
            )}

            {error && (
                <div className="error-message">
                    {error}
                </div>
            )}

            {videos.length > 0 && !loading && (
                <div className="video-content">
                    <div className="main-video">
                        {selectedVideo && (
                            <div className="video-player">
                                <iframe
                                    src={`https://www.youtube.com/embed/${selectedVideo.video_id}`}
                                    title={selectedVideo.title}
                                    frameBorder="0"
                                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                    allowFullScreen
                                />
                                <h3>{selectedVideo.title}</h3>
                                <p className="channel-title">by {selectedVideo.channel_title}</p>
                            </div>
                        )}
                    </div>
                    
                    <div className="video-list">
                        <h3>More Videos</h3>
                        {videos.map((video) => (
                            <div
                                key={video.video_id}
                                className={`video-item ${selectedVideo?.video_id === video.video_id ? 'selected' : ''}`}
                                onClick={() => handleVideoSelect(video)}
                            >
                                <img 
                                    src={video.thumbnail_url} 
                                    alt={video.title}
                                />
                                <div className="video-info">
                                    <h4>{video.title}</h4>
                                    <p>{video.channel_title}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default YoutubeVideo;