# Only use this on the GPU server with VLLM installed
LOG=./vllm-nemotron-$(date +%Y%m%d-%H%M%S).log

env TRANSFORMERS_NO_TORCHVISION=1 \
nohup uv run vllm serve nvidia/NVIDIA-Nemotron-Nano-9B-v2 \
  --trust-remote-code \
  --mamba_ssm_cache_dtype float32 \
  --enable-auto-tool-choice \
  --tool-parser-plugin "$(pwd)/NVIDIA-Nemotron-Nano-9B-v2/nemotron_toolcall_parser_no_streaming.py" \
  --tool-call-parser "nemotron_json" \
  --host 0.0.0.0 --port 8000 \
  > "$LOG" 2>&1 &
echo "PID: $!  LOG: $LOG"
