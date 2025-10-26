import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  palette: {
    primary: {
      main: '#0071e3',
      dark: '#0077ed',
    },
    secondary: {
      main: '#1d1d1f',
    },
    error: {
      main: '#dc2626',
    },
    warning: {
      main: '#ea580c',
    },
    success: {
      main: '#65a30d',
    },
    background: {
      default: '#ffffff',
      paper: '#f5f5f7',
    },
    text: {
      primary: '#1d1d1f',
      secondary: '#86868b',
    },
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      'Helvetica',
      'Arial',
      'sans-serif',
    ].join(','),
    h1: {
      fontSize: '2.5rem',
      fontWeight: 600,
      letterSpacing: '-0.02em',
      color: '#1d1d1f',
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
      letterSpacing: '-0.01em',
      color: '#1d1d1f',
    },
    h3: {
      fontSize: '1.5rem',
      fontWeight: 600,
      color: '#1d1d1f',
    },
    subtitle1: {
      fontSize: '1.2rem',
      fontWeight: 400,
      color: '#86868b',
    },
    body1: {
      fontSize: '1rem',
      color: '#1d1d1f',
    },
    body2: {
      fontSize: '0.875rem',
      color: '#86868b',
    },
  },
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 500,
          fontSize: '1rem',
          padding: '12px 32px',
          borderRadius: '12px',
        },
        contained: {
          boxShadow: 'none',
          '&:hover': {
            boxShadow: 'none',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: 'none',
          border: '1px solid #e5e7eb',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          boxShadow: 'none',
          border: '1px solid #e5e7eb',
        },
      },
    },
    MuiAccordion: {
      styleOverrides: {
        root: {
          boxShadow: 'none',
          border: '1px solid #e5e7eb',
          '&:before': {
            display: 'none',
          },
        },
      },
    },
  },
});
