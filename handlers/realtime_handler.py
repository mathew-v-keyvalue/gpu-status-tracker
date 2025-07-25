import subprocess
from datetime import datetime
from config import INDIA_TZ
from utils.slack_blocks import create_error_block

def handle_realtime_status(args, user_id, user_name): # Add args to match signature
    try:
        gpu_query = "index,name,temperature.gpu,utilization.gpu,memory.used,memory.total,uuid"
        gpu_result = subprocess.run(f"nvidia-smi --query-gpu={gpu_query} --format=csv,noheader,nounits".split(), capture_output=True, text=True, check=True)
        gpus = [line.split(", ") for line in gpu_result.stdout.strip().split('\n')]

        process_query = "gpu_uuid,pid,process_name,used_gpu_memory"
        process_result = subprocess.run(f"nvidia-smi --query-compute-apps={process_query} --format=csv,noheader,nounits".split(), capture_output=True, text=True, check=True)
        
        processes_by_gpu = {}
        if process_result.stdout.strip():
            for line in process_result.stdout.strip().split('\n'):
                uuid, pid, name, mem = line.split(", ")
                if uuid not in processes_by_gpu: processes_by_gpu[uuid] = []
                processes_by_gpu[uuid].append({"pid": pid, "name": name, "mem": mem})

        current_time = datetime.now(INDIA_TZ).strftime('%I:%M %p IST, %B %d')
        blocks = [{"type": "header", "text": {"type": "plain_text", "text": "🚀 GPU Real-Time Status"}},
                  {"type": "context", "elements": [{"type": "mrkdwn", "text": f"📅 Last updated: {current_time}"}]}]

        if not gpus or not gpus[0]:
            return blocks + [{"type": "section", "text": {"type": "mrkdwn", "text": "⚠️ *No NVIDIA GPUs detected*"}}]

        for index, name, temp, util, mem_used, mem_total, uuid in gpus:
            blocks.extend([
                {"type": "divider"},
                {"type": "section", "text": {"type": "mrkdwn", "text": f"💻 *GPU {index}: {name}*"}},
                {"type": "section", "fields": [{"type": "mrkdwn", "text": f"🌡️ *Temp:*\n{temp}°C"}, {"type": "mrkdwn", "text": f"⚡ *Util:*\n{util}%"}, {"type": "mrkdwn", "text": f"💾 *Memory:*\n{mem_used}MiB / {mem_total}MiB"}]}
            ])
            process_list = processes_by_gpu.get(uuid)
            if process_list:
                process_text = "\n".join([f"• `{p['name']}` (PID: {p['pid']}) - *{p['mem']}MiB*" for p in process_list])
                blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": f"🔄 *Active Processes:*\n{process_text}"}})
        return blocks
    except (FileNotFoundError, subprocess.CalledProcessError):
        return create_error_block("NVIDIA Driver Error", "The `nvidia-smi` command was not found or failed to execute.")