import { useState, useRef, useEffect } from 'react';
import {
  Box,
  Button,
  Typography,
  CircularProgress,
} from '@mui/material';
import { Videocam, Stop, Refresh } from '@mui/icons-material';

interface VideoRecorderProps {
  onUpload: (file: File) => void;
  isAnalyzing: boolean;
}

export default function VideoRecorder({ onUpload, isAnalyzing }: VideoRecorderProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [recordedVideoUrl, setRecordedVideoUrl] = useState<string | null>(null);
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);

  const videoRef = useRef<HTMLVideoElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  // Request camera access
  useEffect(() => {
    const requestCamera = async () => {
      try {
        const mediaStream = await navigator.mediaDevices.getUserMedia({
          video: { width: 1280, height: 720 },
          audio: true,
        });
        setStream(mediaStream);
        setHasPermission(true);

        if (videoRef.current) {
          videoRef.current.srcObject = mediaStream;
        }
      } catch (err) {
        console.error('Error accessing camera:', err);
        setHasPermission(false);
      }
    };

    requestCamera();

    // Cleanup
    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  const startRecording = () => {
    if (!stream) return;

    chunksRef.current = [];
    const mediaRecorder = new MediaRecorder(stream, {
      mimeType: 'video/webm',
    });

    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        chunksRef.current.push(event.data);
      }
    };

    mediaRecorder.onstop = () => {
      const blob = new Blob(chunksRef.current, { type: 'video/webm' });
      const url = URL.createObjectURL(blob);
      setRecordedVideoUrl(url);
    };

    mediaRecorderRef.current = mediaRecorder;
    mediaRecorder.start();
    setIsRecording(true);
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const handleAnalyze = () => {
    if (recordedVideoUrl && chunksRef.current.length > 0) {
      const blob = new Blob(chunksRef.current, { type: 'video/webm' });
      const file = new File([blob], `recorded_${Date.now()}.webm`, {
        type: 'video/webm',
      });
      onUpload(file);
    }
  };

  const handleReset = () => {
    setRecordedVideoUrl(null);
    chunksRef.current = [];
  };

  if (hasPermission === false) {
    return (
      <Box
        sx={{
          p: 10,
          textAlign: 'center',
          border: '3px solid',
          borderColor: 'error.main',
          borderRadius: 3,
          bgcolor: 'rgba(244, 67, 54, 0.02)',
        }}
      >
        <Box
          sx={{
            width: 80,
            height: 80,
            borderRadius: 2,
            bgcolor: 'error.main',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            mx: 'auto',
            mb: 3,
          }}
        >
          <Videocam sx={{ fontSize: 40, color: 'white' }} />
        </Box>
        <Typography variant="h5" sx={{ fontWeight: 700, mb: 1 }} color="error">
          Camera Access Denied
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Please allow camera access to record video
        </Typography>
      </Box>
    );
  }

  if (hasPermission === null) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto' }}>
      {!recordedVideoUrl ? (
        <Box>
          {/* Camera Preview */}
          <Box sx={{ borderRadius: 2, overflow: 'hidden', bgcolor: 'black', mb: 3 }}>
            <video
              ref={videoRef}
              autoPlay
              muted
              style={{ width: '100%', display: 'block' }}
            />
          </Box>

          {/* Recording Controls */}
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
            {!isRecording ? (
              <Button
                variant="contained"
                size="large"
                startIcon={<Videocam />}
                onClick={startRecording}
                disabled={isAnalyzing}
                sx={{
                  py: 2,
                  px: 4,
                  fontSize: '1.1rem',
                  fontWeight: 700,
                  borderRadius: 2,
                  background: 'linear-gradient(135deg, #0071e3 0%, #0077ed 100%)',
                  boxShadow: '0 4px 16px rgba(0, 113, 227, 0.3)',
                  textTransform: 'none',
                  '&:hover': {
                    boxShadow: '0 6px 20px rgba(0, 113, 227, 0.4)',
                  },
                }}
              >
                Start Recording
              </Button>
            ) : (
              <Button
                variant="contained"
                size="large"
                color="error"
                startIcon={<Stop />}
                onClick={stopRecording}
                sx={{
                  py: 2,
                  px: 4,
                  fontSize: '1.1rem',
                  fontWeight: 700,
                  borderRadius: 2,
                  textTransform: 'none',
                  boxShadow: '0 4px 16px rgba(244, 67, 54, 0.3)',
                  '&:hover': {
                    boxShadow: '0 6px 20px rgba(244, 67, 54, 0.4)',
                  },
                }}
              >
                Stop Recording
              </Button>
            )}
          </Box>

          {isRecording && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
              <Box
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 1,
                  px: 2,
                  py: 1,
                  bgcolor: 'error.main',
                  color: 'white',
                  borderRadius: 1,
                }}
              >
                <Box
                  sx={{
                    width: 12,
                    height: 12,
                    borderRadius: '50%',
                    bgcolor: 'white',
                    animation: 'pulse 1.5s ease-in-out infinite',
                    '@keyframes pulse': {
                      '0%, 100%': { opacity: 1 },
                      '50%': { opacity: 0.3 },
                    },
                  }}
                />
                <Typography variant="body2" sx={{ fontWeight: 600 }}>
                  Recording...
                </Typography>
              </Box>
            </Box>
          )}
        </Box>
      ) : (
        <Box>
          {/* Recorded Video Preview */}
          <Box sx={{ borderRadius: 2, overflow: 'hidden', bgcolor: 'black', mb: 3 }}>
            <video
              src={recordedVideoUrl}
              controls
              style={{ width: '100%', display: 'block' }}
            />
          </Box>

          {/* Action Buttons */}
          {!isAnalyzing ? (
            <Box sx={{ display: 'flex', gap: 2 }}>
              <Button
                variant="outlined"
                size="large"
                startIcon={<Refresh />}
                onClick={handleReset}
                fullWidth
                sx={{
                  py: 2,
                  fontSize: '1.1rem',
                  fontWeight: 700,
                  borderRadius: 2,
                  borderWidth: 2,
                  textTransform: 'none',
                  '&:hover': {
                    borderWidth: 2,
                  },
                }}
              >
                Record Again
              </Button>
              <Button
                variant="contained"
                size="large"
                onClick={handleAnalyze}
                fullWidth
                sx={{
                  py: 2,
                  fontSize: '1.1rem',
                  fontWeight: 700,
                  borderRadius: 2,
                  background: 'linear-gradient(135deg, #0071e3 0%, #0077ed 100%)',
                  boxShadow: '0 4px 16px rgba(0, 113, 227, 0.3)',
                  textTransform: 'none',
                  '&:hover': {
                    boxShadow: '0 6px 20px rgba(0, 113, 227, 0.4)',
                  },
                }}
              >
                Analyze Video
              </Button>
            </Box>
          ) : (
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 2, py: 2 }}>
              <CircularProgress size={24} />
              <Typography variant="body1" color="text.secondary">
                Analyzing video...
              </Typography>
            </Box>
          )}
        </Box>
      )}
    </Box>
  );
}
