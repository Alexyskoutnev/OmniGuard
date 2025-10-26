import { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  Button,
  Alert,
  AlertTitle,
  AppBar,
  Toolbar,
  Tabs,
  Tab,
  Paper,
} from '@mui/material';
import { Refresh, Error as ErrorIcon, CloudUpload, Videocam } from '@mui/icons-material';
import VideoUpload from './components/VideoUpload';
import VideoRecorder from './components/VideoRecorder';
import AgentFlowGraph from './components/AgentFlowGraph';
import { AnalysisResponse } from './types';

const API_URL = 'http://localhost:8000';

function App() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState(0);

  const handleVideoUpload = async (file: File) => {
    setIsAnalyzing(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_URL}/api/analyze`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Analysis failed: ${response.statusText}`);
      }

      const data: AnalysisResponse = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error occurred');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: '#fafafa' }}>
      {/* Header */}
      <AppBar
        position="static"
        elevation={0}
        sx={{
          bgcolor: 'white',
          borderBottom: 1,
          borderColor: 'divider',
        }}
      >
        <Container maxWidth="xl">
          <Toolbar sx={{ py: 2, px: 0 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, flexGrow: 1 }}>
              <Box
                sx={{
                  width: 44,
                  height: 44,
                  borderRadius: 2,
                  background: 'linear-gradient(135deg, #0071e3 0%, #0077ed 100%)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  boxShadow: '0 4px 12px rgba(0, 113, 227, 0.25)',
                }}
              >
                <Videocam sx={{ color: 'white', fontSize: 28 }} />
              </Box>
              <Box>
                <Typography variant="h6" sx={{ fontWeight: 700, color: 'text.primary' }}>
                  Construction Safety AI
                </Typography>
                <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                  Real-time safety monitoring powered by AI
                </Typography>
              </Box>
            </Box>

            {result && (
              <Button
                startIcon={<Refresh />}
                onClick={handleReset}
                sx={{
                  textTransform: 'none',
                  fontWeight: 600,
                  borderRadius: 2,
                }}
                variant="outlined"
              >
                New Analysis
              </Button>
            )}
          </Toolbar>
        </Container>
      </AppBar>

      <Container maxWidth="xl" sx={{ py: 8 }}>
        {/* Hero Section */}
        {!result && (
          <Box sx={{ textAlign: 'center', mb: 8, maxWidth: 800, mx: 'auto' }}>
            <Typography
              variant="h3"
              sx={{
                fontWeight: 800,
                mb: 2,
                background: 'linear-gradient(135deg, #0071e3 0%, #0077ed 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                letterSpacing: '-0.02em',
              }}
            >
              AI-Powered Safety Analysis
            </Typography>
            <Typography
              variant="h6"
              sx={{
                color: 'text.secondary',
                fontWeight: 400,
                lineHeight: 1.6,
                mb: 1,
              }}
            >
              Upload or record construction site videos for instant AI safety analysis
            </Typography>
            <Typography variant="body2" sx={{ color: 'text.secondary' }}>
              Detect hazards, analyze risks, and get actionable insights in real-time
            </Typography>
          </Box>
        )}

        {/* Error Display */}
        {error && (
          <Alert
            severity="error"
            icon={<ErrorIcon />}
            sx={{
              mb: 4,
              borderRadius: 2,
              border: 1,
              borderColor: 'error.light',
            }}
            onClose={() => setError(null)}
          >
            <AlertTitle sx={{ fontWeight: 600 }}>Error</AlertTitle>
            {error}
          </Alert>
        )}

        {/* Video Input Section */}
        <Box sx={{ mb: 6 }}>
          <Paper
            elevation={0}
            sx={{
              border: 1,
              borderColor: 'divider',
              overflow: 'hidden',
              borderRadius: 3,
              bgcolor: 'white',
              boxShadow: '0 4px 24px rgba(0,0,0,0.06)',
            }}
          >
            <Tabs
              value={activeTab}
              onChange={(_, newValue) => setActiveTab(newValue)}
              sx={{
                borderBottom: 1,
                borderColor: 'divider',
                bgcolor: 'white',
                '& .MuiTab-root': {
                  py: 2.5,
                  minHeight: 'auto',
                },
                '& .Mui-selected': {
                  color: 'primary.main',
                },
              }}
              TabIndicatorProps={{
                sx: {
                  height: 3,
                  borderRadius: '3px 3px 0 0',
                  background: 'linear-gradient(135deg, #0071e3 0%, #0077ed 100%)',
                },
              }}
            >
              <Tab
                icon={<CloudUpload />}
                label="Upload Video"
                iconPosition="start"
                sx={{
                  textTransform: 'none',
                  fontWeight: 600,
                  fontSize: '1rem',
                }}
              />
              <Tab
                icon={<Videocam />}
                label="Record Video"
                iconPosition="start"
                sx={{
                  textTransform: 'none',
                  fontWeight: 600,
                  fontSize: '1rem',
                }}
              />
            </Tabs>

            <Box sx={{ p: 6 }}>
              {activeTab === 0 && (
                <VideoUpload onUpload={handleVideoUpload} isAnalyzing={isAnalyzing} />
              )}
              {activeTab === 1 && (
                <VideoRecorder onUpload={handleVideoUpload} isAnalyzing={isAnalyzing} />
              )}
            </Box>
          </Paper>
        </Box>

        {/* Results Section */}
        {result && (
          <Box>
            <Typography
              variant="h4"
              sx={{
                fontWeight: 700,
                mb: 1,
                color: 'text.primary',
              }}
            >
              Analysis Results
            </Typography>
            <Typography variant="body1" sx={{ color: 'text.secondary', mb: 4 }}>
              AI agent workflow and safety findings
            </Typography>
            <AgentFlowGraph traces={result.trace} />
          </Box>
        )}
      </Container>

    </Box>
  );
}

export default App;
