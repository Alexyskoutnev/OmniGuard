export interface ToolCall {
  tool_name: string;
  arguments: Record<string, any>;
  result: string;
  duration_ms: number;
  timestamp: string;
  success: boolean;
  error: string | null;
}

export interface AgentTrace {
  agent_name: string;
  start_time: string;
  end_time: string;
  duration_ms: number;
  iterations: number;
  handoff_to: string | null;
  final_output: string | null;
  tool_calls: ToolCall[];
}

export interface Predictions {
  probability: number;
  incident_type: string;
  confidence: number;
}

export interface EventData {
  video_id: string;
  safety_status: 'SAFE' | 'LOW' | 'MEDIUM' | 'HIGH' | 'EXTREME';
  scene_description: string;
  predictions: Predictions;
  safety_response: string;
}

export interface AnalysisResponse {
  status: string;
  video_id: string;
  event: EventData;
  agent_output: string;
  trace: AgentTrace[];
}
