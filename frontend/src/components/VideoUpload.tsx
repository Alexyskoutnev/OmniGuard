import { useState } from 'react';
import {
  Box,
  Button,
  Typography,
  Paper,
  CircularProgress,
} from '@mui/material';
import { CloudUpload, VideoFile } from '@mui/icons-material';

interface VideoUploadProps {
  onUpload: (file: File) => void;
  isAnalyzing: boolean;
}

export default function VideoUpload({ onUpload, isAnalyzing }: VideoUploadProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  const handleUpload = () => {
    if (selectedFile) {
      onUpload(selectedFile);
    }
  };

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto' }}>
      {!selectedFile ? (
        <Box
          component="label"
          sx={{
            p: 8,
            textAlign: 'center',
            cursor: 'pointer',
            border: '2px dashed',
            borderColor: 'divider',
            borderRadius: 2,
            bgcolor: 'white',
            display: 'block',
            transition: 'border-color 0.3s',
            '&:hover': {
              borderColor: 'primary.main',
            },
          }}
        >
          <input
            type="file"
            accept="video/*"
            onChange={handleFileSelect}
            style={{ display: 'none' }}
            disabled={isAnalyzing}
          />
          <Box
            sx={{
              width: 80,
              height: 80,
              borderRadius: '50%',
              bgcolor: 'background.paper',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              mx: 'auto',
              mb: 3,
            }}
          >
            <CloudUpload sx={{ fontSize: 40, color: 'primary.main' }} />
          </Box>
          <Typography variant="h6" gutterBottom sx={{ fontWeight: 500 }}>
            Choose a video file
          </Typography>
          <Typography variant="body2" color="text.secondary">
            MP4, MOV, or AVI up to 50MB
          </Typography>
        </Box>
      ) : (
        <Box>
          {previewUrl && (
            <Box sx={{ borderRadius: 2, overflow: 'hidden', bgcolor: 'black', mb: 3 }}>
              <video
                src={previewUrl}
                controls
                style={{ width: '100%', display: 'block' }}
              />
            </Box>
          )}

          {!isAnalyzing && (
            <Button
              variant="contained"
              onClick={handleUpload}
              fullWidth
              size="large"
            >
              Analyze Video
            </Button>
          )}

          {isAnalyzing && (
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
