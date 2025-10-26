import { Card, CardContent, Typography } from '@mui/material';

interface MetricsCardProps {
  label: string;
  value: string | number;
  color?: string;
}

export default function MetricsCard({ label, value, color }: MetricsCardProps) {
  return (
    <Card
      sx={{
        bgcolor: 'background.paper',
        borderLeft: 4,
        borderColor: 'primary.main',
      }}
    >
      <CardContent>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          {label}
        </Typography>
        <Typography
          variant="h4"
          sx={{
            fontWeight: 700,
            color: color || 'text.primary',
          }}
        >
          {value}
        </Typography>
      </CardContent>
    </Card>
  );
}
