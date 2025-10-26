import { useState } from 'react';
import {
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Box,
  Typography,
  Chip,
  Grid,
  Paper,
  Alert,
} from '@mui/material';
import {
  ExpandMore,
  CheckCircle,
  Cancel,
  ArrowForward,
  Code,
} from '@mui/icons-material';
import { AgentTrace, ToolCall } from '../types';

interface AgentTraceTreeProps {
  traces: AgentTrace[];
}

export default function AgentTraceTree({ traces }: AgentTraceTreeProps) {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
      {traces.map((trace, idx) => (
        <AgentNode key={idx} trace={trace} />
      ))}
    </Box>
  );
}

function AgentNode({ trace }: { trace: AgentTrace }) {
  const [expanded, setExpanded] = useState(true);

  const formatTime = (isoTime: string) => {
    return new Date(isoTime).toLocaleTimeString('en-US', {
      hour12: false,
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    });
  };

  return (
    <Accordion expanded={expanded} onChange={() => setExpanded(!expanded)}>
      <AccordionSummary expandIcon={<ExpandMore />}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, width: '100%' }}>
          <Code color="primary" />
          <Typography variant="h6" sx={{ fontWeight: 600 }}>
            {trace.agent_name}
          </Typography>
          <Chip
            label={`${trace.duration_ms.toFixed(0)}ms`}
            size="small"
            sx={{ ml: 'auto', mr: 2 }}
          />
        </Box>
      </AccordionSummary>
      <AccordionDetails>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
          {/* Metadata */}
          <Grid container spacing={2}>
            <Grid item xs={4}>
              <Typography variant="body2" color="text.secondary">
                Start:{' '}
                <Typography component="span" sx={{ fontFamily: 'monospace' }}>
                  {formatTime(trace.start_time)}
                </Typography>
              </Typography>
            </Grid>
            <Grid item xs={4}>
              <Typography variant="body2" color="text.secondary">
                Iterations:{' '}
                <Typography component="span" sx={{ fontFamily: 'monospace' }}>
                  {trace.iterations}
                </Typography>
              </Typography>
            </Grid>
            <Grid item xs={4}>
              <Typography variant="body2" color="text.secondary">
                Duration:{' '}
                <Typography component="span" sx={{ fontFamily: 'monospace' }}>
                  {trace.duration_ms.toFixed(0)}ms
                </Typography>
              </Typography>
            </Grid>
          </Grid>

          {/* Tool Calls */}
          {trace.tool_calls.length > 0 && (
            <Box>
              <Typography variant="subtitle1" sx={{ mb: 2, fontWeight: 600 }}>
                Tool Executions
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                {trace.tool_calls.map((toolCall, idx) => (
                  <ToolCallNode key={idx} toolCall={toolCall} />
                ))}
              </Box>
            </Box>
          )}

          {/* Handoff */}
          {trace.handoff_to && (
            <Alert
              icon={<ArrowForward />}
              severity="info"
              sx={{ bgcolor: 'primary.50' }}
            >
              Handed off to: <strong>{trace.handoff_to}</strong>
            </Alert>
          )}

          {/* Final Output */}
          {trace.final_output && (
            <Accordion>
              <AccordionSummary expandIcon={<ExpandMore />}>
                <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                  Final Output
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Typography variant="body2" color="text.secondary">
                  {trace.final_output}
                </Typography>
              </AccordionDetails>
            </Accordion>
          )}
        </Box>
      </AccordionDetails>
    </Accordion>
  );
}

function ToolCallNode({ toolCall }: { toolCall: ToolCall }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <Paper
      sx={{
        border: 1,
        borderColor: 'divider',
        overflow: 'hidden',
      }}
    >
      <Box
        sx={{
          p: 2,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          cursor: 'pointer',
          '&:hover': {
            bgcolor: 'background.paper',
          },
        }}
        onClick={() => setExpanded(!expanded)}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          {toolCall.success ? (
            <CheckCircle sx={{ fontSize: 20, color: 'success.main' }} />
          ) : (
            <Cancel sx={{ fontSize: 20, color: 'error.main' }} />
          )}
          <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
            {toolCall.tool_name}
          </Typography>
          <Chip
            label={`${toolCall.duration_ms.toFixed(1)}ms`}
            size="small"
            variant="outlined"
          />
        </Box>
        <ExpandMore
          sx={{
            transform: expanded ? 'rotate(180deg)' : 'rotate(0deg)',
            transition: '0.3s',
          }}
        />
      </Box>

      {expanded && (
        <Box sx={{ px: 2, pb: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          {/* Input */}
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMore />}>
              <Typography variant="body2" sx={{ fontWeight: 600 }}>
                📥 Input
              </Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Paper
                sx={{
                  p: 2,
                  bgcolor: 'background.paper',
                  overflow: 'auto',
                }}
              >
                <pre style={{ margin: 0, fontSize: '0.75rem' }}>
                  {JSON.stringify(toolCall.arguments, null, 2)}
                </pre>
              </Paper>
            </AccordionDetails>
          </Accordion>

          {/* Output */}
          <Accordion defaultExpanded>
            <AccordionSummary expandIcon={<ExpandMore />}>
              <Typography variant="body2" sx={{ fontWeight: 600 }}>
                📤 Output
              </Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Paper
                sx={{
                  p: 2,
                  bgcolor: 'background.paper',
                  overflow: 'auto',
                }}
              >
                <Typography
                  variant="body2"
                  sx={{
                    fontFamily: 'monospace',
                    whiteSpace: 'pre-wrap',
                    color: toolCall.error ? 'error.main' : 'text.secondary',
                  }}
                >
                  {toolCall.error ||
                    (toolCall.result.length > 500
                      ? toolCall.result.substring(0, 500) + '...'
                      : toolCall.result)}
                </Typography>
              </Paper>
            </AccordionDetails>
          </Accordion>
        </Box>
      )}
    </Paper>
  );
}
