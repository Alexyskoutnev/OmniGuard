import { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  Button,
  Grid,
  Alert,
  AlertTitle,
  AppBar,
  Toolbar,
} from '@mui/material';
import { Refresh, Error as ErrorIcon } from '@mui/icons-material';
import VideoUpload from './components/VideoUpload';
import AgentFlowGraph from './components/AgentFlowGraph';
import { AnalysisResponse } from './types';

const API_URL = 'http://localhost:8000';

function App() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

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
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
      {/* Header */}
      <AppBar
        position="static"
        elevation={0}
        sx={{
          bgcolor: 'background.default',
          borderBottom: 1,
          borderColor: 'divider',
        }}
      >
        <Toolbar sx={{ py: 2 }}>

          {result && (
            <Button
              startIcon={<Refresh />}
              onClick={handleReset}
              sx={{ textTransform: 'none' }}
            >
              Reset
            </Button>
          )}
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ py: 6 }}>
        {/* Error Display */}
        {error && (
          <Alert
            severity="error"
            icon={<ErrorIcon />}
            sx={{ mb: 4 }}
            onClose={() => setError(null)}
          >
            <AlertTitle>Error</AlertTitle>
            {error}
          </Alert>
        )}

        {/* Upload Section - Always visible */}
        <VideoUpload onUpload={handleVideoUpload} isAnalyzing={isAnalyzing} />

        {/* Results Section */}
        {result && (
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 4, mt: 4 }}>
            {/* Agent Flow Graph */}
            <Box>
              <AgentFlowGraph traces={result.trace} />
            </Box>

            {/* Download Buttons */}
            <Grid container spacing={3}>
              <Grid item xs={12} md={4}>
                <Button
                  variant="outlined"
                  fullWidth
                  onClick={() => {
                    const blob = new Blob([JSON.stringify(result.event, null, 2)], {
                      type: 'application/json',
                    });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `event_${result.video_id}.json`;
                    a.click();
                  }}
                >
                  Download Event Data
                </Button>
              </Grid>
              <Grid item xs={12} md={4}>
                <Button
                  variant="outlined"
                  fullWidth
                  onClick={() => {
                    const blob = new Blob([result.agent_output], {
                      type: 'text/plain',
                    });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `report_${result.video_id}.txt`;
                    a.click();
                  }}
                >
                  Download Report
                </Button>
              </Grid>
              <Grid item xs={12} md={4}>
                <Button
                  variant="outlined"
                  fullWidth
                  onClick={() => {
                    const blob = new Blob([JSON.stringify(result.trace, null, 2)], {
                      type: 'application/json',
                    });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `trace_${result.video_id}.json`;
                    a.click();
                  }}
                >
                  Download Trace
                </Button>
              </Grid>
            </Grid>
          </Box>
        )}
      </Container>

      {/* Footer */}
      <Box
        component="footer"
        sx={{
          borderTop: 1,
          borderColor: 'divider',
          py: 4,
          mt: 8,
        }}
      >
      </Box>
    </Box>
  );
}

export default App;
