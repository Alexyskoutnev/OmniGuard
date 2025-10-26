import { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Fade,
  Divider,
} from '@mui/material';
import {
  ExpandMore,
  CheckCircle,
  Cancel,
  ArrowDownward,
} from '@mui/icons-material';
import { AgentTrace, ToolCall } from '../types';

interface AgentFlowGraphProps {
  traces: AgentTrace[];
}

export default function AgentFlowGraph({ traces }: AgentFlowGraphProps) {
  const [visibleAgents, setVisibleAgents] = useState<number>(0);

  useEffect(() => {
    traces.forEach((_, index) => {
      setTimeout(() => {
        setVisibleAgents((prev) => prev + 1);
      }, index * 300);
    });
  }, [traces]);

  return (
    <Box sx={{ py: 2 }}>
      {traces.map((trace, index) => (
        <Box key={index}>
          <Fade in={index < visibleAgents} timeout={500}>
            <Box>
              <AgentFlowNode trace={trace} index={index} />
            </Box>
          </Fade>

          {index < traces.length - 1 && (
            <Box
              sx={{
                display: 'flex',
                justifyContent: 'center',
                py: 2,
              }}
            >
              <ArrowDownward sx={{ color: 'primary.main', fontSize: 32 }} />
            </Box>
          )}
        </Box>
      ))}

      {/* Summary */}
      <Fade in={visibleAgents === traces.length} timeout={800}>
        <Paper
          sx={{
            mt: 3,
            p: 3,
            textAlign: 'center',
            bgcolor: 'success.50',
            border: 1,
            borderColor: 'success.main',
          }}
        >
          <CheckCircle sx={{ fontSize: 40, color: 'success.main', mb: 1 }} />
          <Typography variant="h6" sx={{ fontWeight: 600, color: 'success.dark', mb: 1 }}>
            Analysis Complete
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {traces.length} agents • {traces.reduce((acc, t) => acc + t.tool_calls.length, 0)} tool calls • {traces.reduce((acc, t) => acc + (t.duration_ms || 0), 0).toFixed(0)}ms
          </Typography>
        </Paper>
      </Fade>
    </Box>
  );
}

function AgentFlowNode({ trace, index }: { trace: AgentTrace; index: number }) {
  const [expanded, setExpanded] = useState(true);

  return (
    <Paper
      elevation={0}
      sx={{
        border: 1,
        borderColor: 'divider',
        overflow: 'hidden',
        bgcolor: 'white',
      }}
    >
      {/* Header */}
      <Box
        onClick={() => setExpanded(!expanded)}
        sx={{
          p: 3,
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          gap: 2,
          bgcolor: 'white',
          transition: 'background-color 0.2s',
          '&:hover': {
            bgcolor: 'rgba(0, 113, 227, 0.02)',
          },
        }}
      >
        {/* Step Number */}
        <Box
          sx={{
            width: 36,
            height: 36,
            borderRadius: '50%',
            bgcolor: 'primary.main',
            color: 'white',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontWeight: 700,
            fontSize: '1rem',
            flexShrink: 0,
          }}
        >
          {index + 1}
        </Box>

        {/* Agent Name */}
        <Box sx={{ flexGrow: 1 }}>
          <Typography variant="h6" sx={{ fontWeight: 600, mb: 0.5 }}>
            {trace.agent_name}
          </Typography>
          <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
            <Chip label={`${trace.tool_calls.length} tools`} size="small" />
            <Chip label={`${trace.duration_ms.toFixed(0)}ms`} size="small" color="primary" />
            {trace.handoff_to && (
              <Chip label={`→ ${trace.handoff_to}`} size="small" variant="outlined" />
            )}
          </Box>
        </Box>

        <ExpandMore
          sx={{
            transform: expanded ? 'rotate(180deg)' : 'rotate(0deg)',
            transition: 'transform 0.3s',
          }}
        />
      </Box>

      {/* Tool Calls */}
      {expanded && trace.tool_calls.length > 0 && (
        <Box sx={{ p: 3, pt: 0 }}>
          <Divider sx={{ mb: 3 }} />
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            {trace.tool_calls.map((toolCall, idx) => (
              <ToolCallCard key={idx} toolCall={toolCall} />
            ))}
          </Box>
        </Box>
      )}
    </Paper>
  );
}

function ToolCallCard({ toolCall }: { toolCall: ToolCall }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <Paper
      elevation={0}
      sx={{
        border: 1,
        borderColor: toolCall.success ? 'success.main' : 'error.main',
        overflow: 'hidden',
      }}
    >
      {/* Tool Header */}
      <Box
        sx={{
          p: 2,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          bgcolor: toolCall.success ? 'success.50' : 'error.50',
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
          {toolCall.success ? (
            <CheckCircle sx={{ fontSize: 20, color: 'success.main' }} />
          ) : (
            <Cancel sx={{ fontSize: 20, color: 'error.main' }} />
          )}
          <Box>
            <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
              {toolCall.tool_name}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              {toolCall.duration_ms.toFixed(1)}ms
            </Typography>
          </Box>
        </Box>
      </Box>

      {/* Expandable Details */}
      <Accordion
        expanded={expanded}
        onChange={() => setExpanded(!expanded)}
        disableGutters
        elevation={0}
        sx={{
          '&:before': { display: 'none' },
          bgcolor: 'transparent',
        }}
      >
        <AccordionSummary
          expandIcon={<ExpandMore />}
          sx={{
            px: 2,
            py: 1,
            minHeight: 'auto',
            '&.Mui-expanded': {
              minHeight: 'auto',
            },
            '& .MuiAccordionSummary-content': {
              margin: '8px 0',
            },
          }}
        >
          <Typography variant="body2" sx={{ fontWeight: 500 }}>
            View Details
          </Typography>
        </AccordionSummary>
        <AccordionDetails sx={{ p: 2, pt: 0 }}>
          {/* Input */}
          <Box sx={{ mb: 2 }}>
            <Typography
              variant="caption"
              sx={{
                fontWeight: 600,
                textTransform: 'uppercase',
                color: 'text.secondary',
                mb: 1,
                display: 'block',
              }}
            >
              Input
            </Typography>
            <Paper
              elevation={0}
              sx={{
                p: 2,
                bgcolor: 'rgba(0, 0, 0, 0.02)',
                border: 1,
                borderColor: 'divider',
                maxHeight: 200,
                overflow: 'auto',
              }}
            >
              <pre
                style={{
                  margin: 0,
                  fontSize: '0.75rem',
                  fontFamily: 'Monaco, monospace',
                  whiteSpace: 'pre-wrap',
                  wordBreak: 'break-word',
                }}
              >
                {JSON.stringify(toolCall.arguments, null, 2)}
              </pre>
            </Paper>
          </Box>

          {/* Output */}
          <Box>
            <Typography
              variant="caption"
              sx={{
                fontWeight: 600,
                textTransform: 'uppercase',
                color: 'text.secondary',
                mb: 1,
                display: 'block',
              }}
            >
              Output
            </Typography>
            <Paper
              elevation={0}
              sx={{
                p: 2,
                bgcolor: 'rgba(0, 0, 0, 0.02)',
                border: 1,
                borderColor: 'divider',
                maxHeight: 200,
                overflow: 'auto',
              }}
            >
              {toolCall.error ? (
                <Typography
                  variant="body2"
                  sx={{
                    color: 'error.main',
                    fontFamily: 'Monaco, monospace',
                    fontSize: '0.75rem',
                    whiteSpace: 'pre-wrap',
                  }}
                >
                  {toolCall.error}
                </Typography>
              ) : (
                <Typography
                  variant="body2"
                  sx={{
                    fontFamily: 'Monaco, monospace',
                    fontSize: '0.75rem',
                    whiteSpace: 'pre-wrap',
                    wordBreak: 'break-word',
                  }}
                >
                  {toolCall.result}
                </Typography>
              )}
            </Paper>
          </Box>
        </AccordionDetails>
      </Accordion>
    </Paper>
  );
}
