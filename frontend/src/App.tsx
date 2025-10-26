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
import MetricsCard from './components/MetricsCard';
import AgentTraceTree from './components/AgentTraceTree';
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

  const getSeverityColor = (status: string) => {
    const colors: Record<string, string> = {
      SAFE: '#65a30d',
      LOW: '#65a30d',
      MEDIUM: '#d97706',
      HIGH: '#ea580c',
      EXTREME: '#dc2626',
    };
    return colors[status] || '#1d1d1f';
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
          <Box sx={{ flexGrow: 1 }}>
            <Typography variant="h1" sx={{ fontSize: '2rem', mb: 0.5 }}>
              Construction Safety Agent System
            </Typography>
            <Typography variant="subtitle1">
              AI-powered real-time safety monitoring
            </Typography>
          </Box>
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

        {/* Upload Section */}
        {!result && <VideoUpload onUpload={handleVideoUpload} isAnalyzing={isAnalyzing} />}

        {/* Results Section */}
        {result && (
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            {/* Metrics Grid */}
            <Box>
              <Typography variant="h2" sx={{ mb: 3 }}>
                Analysis Results
              </Typography>
              <Grid container spacing={3}>
                <Grid item xs={12} sm={6} md={3}>
                  <MetricsCard
                    label="Safety Status"
                    value={result.event.safety_status}
                    color={getSeverityColor(result.event.safety_status)}
                  />
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <MetricsCard
                    label="Risk Probability"
                    value={`${(result.event.predictions.probability * 100).toFixed(0)}%`}
                    color="#dc2626"
                  />
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <MetricsCard
                    label="Incident Type"
                    value={result.event.predictions.incident_type}
                  />
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <MetricsCard label="Video ID" value={result.video_id} />
                </Grid>
              </Grid>
            </Box>

            {/* Two Column Layout */}
            <Grid container spacing={4}>
              {/* Left Column */}
              <Grid item xs={12} lg={6}>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                  <Box>
                    <Typography variant="h3" sx={{ mb: 2 }}>
                      Scene Analysis
                    </Typography>
                    <Typography variant="body1" color="text.secondary" sx={{ lineHeight: 1.8 }}>
                      {result.event.scene_description}
                    </Typography>
                  </Box>

                  <Box>
                    <Typography variant="h3" sx={{ mb: 2 }}>
                      Safety Response
                    </Typography>
                    <Alert severity="info">
                      <Typography variant="body2" sx={{ lineHeight: 1.8 }}>
                        {result.event.safety_response}
                      </Typography>
                    </Alert>
                  </Box>
                </Box>
              </Grid>

              {/* Right Column */}
              <Grid item xs={12} lg={6}>
                <Typography variant="h3" sx={{ mb: 2 }}>
                  Agent Analysis
                </Typography>
                <Alert severity="success">
                  <Typography variant="body2" sx={{ lineHeight: 1.8 }}>
                    {result.agent_output}
                  </Typography>
                </Alert>
              </Grid>
            </Grid>

            {/* Agent Trace Section */}
            <Box>
              <Typography variant="h2" sx={{ mb: 3 }}>
                Agent Execution Trace
              </Typography>
              <AgentTraceTree traces={result.trace} />
            </Box>

            {/* Download Buttons */}
            <Grid container spacing={3}>
              <Grid item xs={12} md={4}>
                <Button
                  variant="contained"
                  fullWidth
                  size="large"
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
                  variant="contained"
                  fullWidth
                  size="large"
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
                  variant="contained"
                  fullWidth
                  size="large"
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
        <Container>
          <Typography variant="body2" color="text.secondary" align="center">
            Powered by Gemini 2.5 Pro Vision • NVIDIA Nemotron • Custom Agent Framework
          </Typography>
        </Container>
      </Box>
    </Box>
  );
}

export default App;
