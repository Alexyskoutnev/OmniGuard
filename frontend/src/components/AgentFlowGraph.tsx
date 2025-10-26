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
  Grow,
} from '@mui/material';
import {
  ExpandMore,
  CheckCircle,
  Cancel,
  PlayArrow,
  DoneAll,
} from '@mui/icons-material';
import { AgentTrace, ToolCall } from '../types';

interface AgentFlowGraphProps {
  traces: AgentTrace[];
}

export default function AgentFlowGraph({ traces }: AgentFlowGraphProps) {
  const [visibleAgents, setVisibleAgents] = useState<number>(0);
  const [showCompletion, setShowCompletion] = useState(false);

  useEffect(() => {
    // Stagger agent appearance
    traces.forEach((_, index) => {
      setTimeout(() => {
        setVisibleAgents((prev) => prev + 1);
      }, index * 400);
    });

    // Show completion after all agents
    setTimeout(() => {
      setShowCompletion(true);
    }, traces.length * 400 + 500);
  }, [traces]);

  return (
    <Box sx={{ position: 'relative', py: 4 }}>
      {/* Flow Container */}
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0, position: 'relative' }}>
        {traces.map((trace, index) => (
          <Box key={index}>
            <Fade in={index < visibleAgents} timeout={600}>
              <Box>
                <AgentFlowNode
                  trace={trace}
                  index={index}
                  isVisible={index < visibleAgents}
                  hasNext={index < traces.length - 1}
                />
              </Box>
            </Fade>
          </Box>
        ))}
      </Box>

      {/* Completion Badge */}
      {showCompletion && (
        <Grow in={showCompletion} timeout={1000}>
          <Paper
            elevation={0}
            sx={{
              mt: 4,
              p: 4,
              textAlign: 'center',
              bgcolor: 'success.50',
              border: 2,
              borderColor: 'success.main',
              borderStyle: 'dashed',
              position: 'relative',
              overflow: 'hidden',
              '&::before': {
                content: '""',
                position: 'absolute',
                top: 0,
                left: '-100%',
                width: '100%',
                height: '100%',
                background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent)',
                animation: 'shimmer 2s infinite',
              },
              '@keyframes shimmer': {
                '0%': { left: '-100%' },
                '100%': { left: '100%' },
              },
            }}
          >
            <DoneAll sx={{ fontSize: 48, color: 'success.main', mb: 2 }} />
            <Typography variant="h5" sx={{ fontWeight: 600, color: 'success.dark' }}>
              Analysis Complete
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              {traces.length} agent{traces.length !== 1 ? 's' : ''} executed •{' '}
              {traces.reduce((acc, t) => acc + t.tool_calls.length, 0)} tool calls •{' '}
              {traces.reduce((acc, t) => acc + (t.duration_ms || 0), 0).toFixed(0)}ms total
            </Typography>
          </Paper>
        </Grow>
      )}
    </Box>
  );
}

function AgentFlowNode({
  trace,
  index,
  isVisible,
  hasNext,
}: {
  trace: AgentTrace;
  index: number;
  isVisible: boolean;
  hasNext: boolean;
}) {
  const [expanded, setExpanded] = useState(false);

  return (
    <Box sx={{ position: 'relative' }}>
      {/* Connecting Line to Next Agent */}
      {hasNext && (
        <Box
          sx={{
            position: 'absolute',
            left: '50%',
            bottom: -32,
            width: 2,
            height: 32,
            bgcolor: 'primary.main',
            transform: 'translateX(-50%)',
            opacity: isVisible ? 1 : 0,
            transition: 'opacity 0.6s',
            zIndex: 0,
            '&::after': {
              content: '""',
              position: 'absolute',
              bottom: -6,
              left: '50%',
              transform: 'translateX(-50%)',
              width: 0,
              height: 0,
              borderLeft: '6px solid transparent',
              borderRight: '6px solid transparent',
              borderTop: '8px solid',
              borderTopColor: 'primary.main',
            },
          }}
        />
      )}

      <Paper
        elevation={expanded ? 8 : 2}
        sx={{
          position: 'relative',
          overflow: 'hidden',
          border: 2,
          borderColor: expanded ? 'primary.main' : 'divider',
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          '&:hover': {
            borderColor: 'primary.main',
            transform: 'translateY(-2px)',
            boxShadow: 4,
          },
        }}
      >
        {/* Agent Header */}
        <Box
          onClick={() => setExpanded(!expanded)}
          sx={{
            p: 3,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: 2,
            bgcolor: expanded ? 'primary.50' : 'transparent',
            transition: 'background-color 0.3s',
          }}
        >
          {/* Step Number */}
          <Box
            sx={{
              width: 40,
              height: 40,
              borderRadius: '50%',
              bgcolor: 'primary.main',
              color: 'white',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: 700,
              fontSize: '1.1rem',
              flexShrink: 0,
            }}
          >
            {index + 1}
          </Box>

          {/* Agent Info */}
          <Box sx={{ flexGrow: 1 }}>
            <Typography variant="h6" sx={{ fontWeight: 600, mb: 0.5 }}>
              {trace.agent_name}
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, alignItems: 'center', flexWrap: 'wrap' }}>
              <Chip
                icon={<PlayArrow sx={{ fontSize: 16 }} />}
                label={`${trace.tool_calls.length} tools`}
                size="small"
                variant="outlined"
              />
              <Chip
                label={`${trace.duration_ms.toFixed(0)}ms`}
                size="small"
                color="primary"
                variant="filled"
              />
              {trace.handoff_to && (
                <Chip
                  label={`→ ${trace.handoff_to}`}
                  size="small"
                  color="secondary"
                  variant="outlined"
                />
              )}
            </Box>
          </Box>

          {/* Expand Icon */}
          <ExpandMore
            sx={{
              transform: expanded ? 'rotate(180deg)' : 'rotate(0deg)',
              transition: 'transform 0.3s',
              color: 'primary.main',
            }}
          />
        </Box>

        {/* Tool Calls */}
        {expanded && (
          <Box sx={{ px: 3, pb: 3 }}>
            <Box
              sx={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
                gap: 2,
                mt: 2,
              }}
            >
              {trace.tool_calls.map((toolCall, idx) => (
                <Grow key={idx} in={expanded} timeout={300 + idx * 100}>
                  <Box>
                    <ToolCallCard toolCall={toolCall} />
                  </Box>
                </Grow>
              ))}
            </Box>
          </Box>
        )}
      </Paper>
    </Box>
  );
}

function ToolCallCard({ toolCall }: { toolCall: ToolCall }) {
  const [showDetails, setShowDetails] = useState(false);

  return (
    <Paper
      elevation={0}
      sx={{
        border: 1,
        borderColor: toolCall.success ? 'success.main' : 'error.main',
        bgcolor: toolCall.success ? 'success.50' : 'error.50',
        p: 2,
        height: '100%',
        transition: 'all 0.2s',
        cursor: 'pointer',
        '&:hover': {
          transform: 'translateY(-2px)',
          boxShadow: 2,
        },
      }}
      onClick={() => setShowDetails(!showDetails)}
    >
      <Box sx={{ display: 'flex', alignItems: 'start', gap: 1.5, mb: 1.5 }}>
        {toolCall.success ? (
          <CheckCircle sx={{ fontSize: 20, color: 'success.main', mt: 0.3 }} />
        ) : (
          <Cancel sx={{ fontSize: 20, color: 'error.main', mt: 0.3 }} />
        )}
        <Box sx={{ flexGrow: 1 }}>
          <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 0.5 }}>
            {toolCall.tool_name}
          </Typography>
          <Chip label={`${toolCall.duration_ms.toFixed(1)}ms`} size="small" />
        </Box>
      </Box>

      {showDetails && (
        <Accordion
          disableGutters
          elevation={0}
          sx={{
            bgcolor: 'transparent',
            '&:before': { display: 'none' },
          }}
        >
          <AccordionSummary expandIcon={<ExpandMore />} sx={{ px: 0, minHeight: 0 }}>
            <Typography variant="caption" sx={{ fontWeight: 600 }}>
              View Details
            </Typography>
          </AccordionSummary>
          <AccordionDetails sx={{ px: 0, pt: 0 }}>
            <Typography variant="caption" display="block" sx={{ mb: 1, fontWeight: 600 }}>
              Input:
            </Typography>
            <Paper
              sx={{
                p: 1,
                bgcolor: 'background.paper',
                mb: 2,
                maxHeight: 120,
                overflow: 'auto',
              }}
            >
              <pre style={{ margin: 0, fontSize: '0.7rem' }}>
                {JSON.stringify(toolCall.arguments, null, 2)}
              </pre>
            </Paper>
            <Typography variant="caption" display="block" sx={{ mb: 1, fontWeight: 600 }}>
              Output:
            </Typography>
            <Paper
              sx={{
                p: 1,
                bgcolor: 'background.paper',
                maxHeight: 120,
                overflow: 'auto',
              }}
            >
              <Typography variant="caption" sx={{ whiteSpace: 'pre-wrap' }}>
                {toolCall.error ||
                  (toolCall.result.length > 300
                    ? toolCall.result.substring(0, 300) + '...'
                    : toolCall.result)}
              </Typography>
            </Paper>
          </AccordionDetails>
        </Accordion>
      )}
    </Paper>
  );
}
