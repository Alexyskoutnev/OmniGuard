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
    <Box sx={{ maxWidth: 800, mx: 'auto' }}>
      <Paper
        elevation={0}
        sx={{
          p: 8,
          textAlign: 'center',
          cursor: 'pointer',
          border: '2px dashed',
          borderColor: selectedFile ? 'primary.main' : 'divider',
          bgcolor: 'white',
          transition: 'all 0.3s',
          '&:hover': {
            borderColor: 'primary.main',
            bgcolor: 'rgba(0, 113, 227, 0.02)',
          },
        }}
        component="label"
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
            bgcolor: 'rgba(0, 113, 227, 0.08)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            mx: 'auto',
            mb: 3,
          }}
        >
          {selectedFile ? (
            <VideoFile sx={{ fontSize: 40, color: 'primary.main' }} />
          ) : (
            <CloudUpload sx={{ fontSize: 40, color: 'primary.main' }} />
          )}
        </Box>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 500 }}>
          {selectedFile ? selectedFile.name : 'Choose a video file'}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          MP4, MOV, or AVI up to 50MB
        </Typography>
      </Paper>

      {previewUrl && (
        <Box sx={{ mt: 4, borderRadius: 2, overflow: 'hidden', bgcolor: 'black' }}>
          <video
            src={previewUrl}
            controls
            style={{ width: '100%', display: 'block' }}
          />
        </Box>
      )}

      {selectedFile && (
        <Button
          variant="contained"
          onClick={handleUpload}
          disabled={isAnalyzing}
          fullWidth
          size="large"
          sx={{ mt: 4 }}
          startIcon={isAnalyzing ? <CircularProgress size={20} color="inherit" /> : null}
        >
          {isAnalyzing ? 'Analyzing...' : 'Analyze Video'}
        </Button>
      )}
    </Box>
  );
}
