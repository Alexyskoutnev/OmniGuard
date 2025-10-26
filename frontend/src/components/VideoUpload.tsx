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
            p: 10,
            textAlign: 'center',
            cursor: 'pointer',
            border: '3px dashed',
            borderColor: 'divider',
            borderRadius: 3,
            bgcolor: '#fafafa',
            display: 'block',
            transition: 'all 0.3s ease',
            '&:hover': {
              borderColor: 'primary.main',
              bgcolor: 'rgba(0, 113, 227, 0.02)',
              transform: 'translateY(-2px)',
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
              width: 96,
              height: 96,
              borderRadius: 3,
              background: 'linear-gradient(135deg, #0071e3 0%, #0077ed 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              mx: 'auto',
              mb: 3,
              boxShadow: '0 8px 24px rgba(0, 113, 227, 0.25)',
            }}
          >
            <CloudUpload sx={{ fontSize: 48, color: 'white' }} />
          </Box>
          <Typography variant="h5" gutterBottom sx={{ fontWeight: 700, mb: 1 }}>
            Drop your video here
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 0.5 }}>
            or click to browse
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.875rem' }}>
            Supports MP4, MOV, AVI • Max 50MB
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
