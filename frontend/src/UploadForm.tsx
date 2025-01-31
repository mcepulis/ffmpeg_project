import { useState } from 'react';
import axios from 'axios';

const UploadForm = () => {
    const [videoFile, setVideoFile] = useState<File | null>(null);
    const [audioFile, setAudioFile] = useState<File | null>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.name === 'video') {
            setVideoFile(e.target.files?.[0] ?? null);
        } else if (e.target.name === 'audio') {
            setAudioFile(e.target.files?.[0] ?? null);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!videoFile || !audioFile) {
            alert('Please select both video and audio files.');
            return;
        }

        const formData = new FormData();
        formData.append('video', videoFile);
        formData.append('audio', audioFile);
        
        console.log("Video file:", videoFile);
        console.log("Audio file:", audioFile);

        try {
            const response = await axios.post('http://127.0.0.1:8000/api/upload-and-merge/', formData, {
                headers: {
                    'Content-Type':'multipart/form-data'
                }
            });
            console.log('FIle uploaded successfully', response.data);
        } catch (error) {
            console.error('Error uploading file', error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
           <div>
                <label>Video:</label>
                <input type="file" name="video" accept="video/mp4" onChange={handleFileChange} />
            </div>
            <div>
                <label>Audio:</label>
                <input type="file" name="audio" accept="video/mp4" onChange={handleFileChange} />
            </div>
            <button type="submit">Upload</button>
        </form>
    )
}

export default UploadForm;