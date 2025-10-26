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
  const [error, setError] = useState<string | null>(null);

  const videoRef = useRef<HTMLVideoElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const streamRef = useRef<MediaStream | null>(null);

  // Request camera access
  useEffect(() => {
    let mounted = true;

    const requestCamera = async () => {
      try {
        const mediaStream = await navigator.mediaDevices.getUserMedia({
          video: { width: 1280, height: 720 },
          audio: true,
        });

        if (!mounted) {
          mediaStream.getTracks().forEach(track => track.stop());
          return;
        }

        streamRef.current = mediaStream;
        setHasPermission(true);

        if (videoRef.current) {
          videoRef.current.srcObject = mediaStream;
        }
      } catch (err) {
        console.error('Error accessing camera:', err);
        if (mounted) {
          setHasPermission(false);
          setError(err instanceof Error ? err.message : 'Camera access denied');
        }
      }
    };

    requestCamera();

    // Cleanup
    return () => {
      mounted = false;
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
        streamRef.current = null;
      }
    };
  }, []);

  const getSupportedMimeType = () => {
    const types = [
      'video/webm;codecs=vp9,opus',
      'video/webm;codecs=vp8,opus',
      'video/webm',
      'video/mp4',
    ];

    for (const type of types) {
      if (MediaRecorder.isTypeSupported(type)) {
        return type;
      }
    }
    return '';
  };

  const startRecording = () => {
    if (!streamRef.current) {
      setError('Camera stream not available');
      return;
    }

    try {
      chunksRef.current = [];
      const mimeType = getSupportedMimeType();

      if (!mimeType) {
        setError('No supported video format found');
        return;
      }

      const mediaRecorder = new MediaRecorder(streamRef.current, {
        mimeType: mimeType,
      });

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: mimeType });
        const url = URL.createObjectURL(blob);
        setRecordedVideoUrl(url);
      };

      mediaRecorder.onerror = (event) => {
        console.error('MediaRecorder error:', event);
        setError('Recording failed');
        setIsRecording(false);
      };

      mediaRecorderRef.current = mediaRecorder;
      mediaRecorder.start(100); // Capture data every 100ms
      setIsRecording(true);
      setError(null);
    } catch (err) {
      console.error('Error starting recording:', err);
      setError(err instanceof Error ? err.message : 'Failed to start recording');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      try {
        mediaRecorderRef.current.stop();
        setIsRecording(false);
      } catch (err) {
        console.error('Error stopping recording:', err);
        setError('Failed to stop recording');
      }
    }
  };

  const handleAnalyze = () => {
    if (recordedVideoUrl && chunksRef.current.length > 0) {
      const mimeType = getSupportedMimeType();
      const extension = mimeType.includes('webm') ? 'webm' : 'mp4';
      const blob = new Blob(chunksRef.current, { type: mimeType });
      const file = new File([blob], `recorded_${Date.now()}.${extension}`, {
        type: mimeType,
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
        <Typography variant="body1" color="text.secondary" sx={{ mb: 1 }}>
          Please allow camera access to record video
        </Typography>
        {error && (
          <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 2 }}>
            Error: {error}
          </Typography>
        )}
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
          {/* Error Display */}
          {error && (
            <Box
              sx={{
                p: 2,
                mb: 3,
                bgcolor: 'rgba(244, 67, 54, 0.1)',
                border: 1,
                borderColor: 'error.main',
                borderRadius: 2,
                textAlign: 'center',
              }}
            >
              <Typography variant="body2" color="error">
                {error}
              </Typography>
            </Box>
          )}

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
