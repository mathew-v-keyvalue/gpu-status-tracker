"""Handler for real-time GPU performance monitoring."""
import subprocess
import logging
from datetime import datetime
from typing import List, Dict, Any
from config import INDIA_TZ
from utils.slack_blocks import create_error_block

logger = logging.getLogger(__name__)


def handle_realtime_status(args: List[str], user_id: str, user_name: str) -> List[Dict[str, Any]]:
    """
    Handle real-time GPU status command using nvidia-smi.
    
    Args:
        args: Command arguments (unused)
        user_id: Slack user ID
        user_name: Slack user name
        
    Returns:
        List of Slack block elements for the response
    """
    try:
        # Query GPU information
        gpu_query = "index,name,temperature.gpu,utilization.gpu,memory.used,memory.total,uuid"
        gpu_cmd = [
            "nvidia-smi",
            f"--query-gpu={gpu_query}",
            "--format=csv,noheader,nounits"
        ]
        
        gpu_result = subprocess.run(
            gpu_cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=10  # 10 second timeout
        )
        
        if not gpu_result.stdout.strip():
            logger.warning("nvidia-smi returned empty output")
            return create_error_block(
                "No GPU Data",
                "No GPU information was returned. Please check your NVIDIA drivers."
            )
        
        gpus = [line.split(", ") for line in gpu_result.stdout.strip().split('\n') if line.strip()]

        # Query process information
        process_query = "gpu_uuid,pid,process_name,used_gpu_memory"
        process_cmd = [
            "nvidia-smi",
            f"--query-compute-apps={process_query}",
            "--format=csv,noheader,nounits"
        ]
        
        processes_by_gpu = {}
        try:
            process_result = subprocess.run(
                process_cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
            
            if process_result.stdout.strip():
                for line in process_result.stdout.strip().split('\n'):
                    if line.strip():
                        parts = line.split(", ")
                        if len(parts) >= 4:
                            uuid, pid, name, mem = parts[0], parts[1], parts[2], parts[3]
                            if uuid not in processes_by_gpu:
                                processes_by_gpu[uuid] = []
                            processes_by_gpu[uuid].append({
                                "pid": pid.strip(),
                                "name": name.strip(),
                                "mem": mem.strip()
                            })
        except subprocess.CalledProcessError:
            # No processes running is not an error
            logger.debug("No GPU processes found or query failed")
        except Exception as e:
            logger.warning(f"Error querying GPU processes: {e}")

        current_time = datetime.now(INDIA_TZ).strftime('%I:%M %p IST, %B %d')
        blocks = [
            {"type": "header", "text": {"type": "plain_text", "text": "🚀 GPU Real-Time Status Dashboard"}},
            {"type": "context", "elements": [{"type": "mrkdwn", "text": f"📅 Last updated: {current_time}"}]}
        ]

        if not gpus:
            return blocks + [
                {"type": "section", "text": {"type": "mrkdwn", "text": "⚠️ *No NVIDIA GPUs detected*"}}
            ]

        for gpu_data in gpus:
            if len(gpu_data) < 7:
                logger.warning(f"Invalid GPU data format: {gpu_data}")
                continue
                
            index, name, temp, util, mem_used, mem_total, uuid = (
                gpu_data[0].strip(),
                gpu_data[1].strip(),
                gpu_data[2].strip(),
                gpu_data[3].strip(),
                gpu_data[4].strip(),
                gpu_data[5].strip(),
                gpu_data[6].strip()
            )
            
            # Calculate memory percentage
            try:
                mem_used_float = float(mem_used)
                mem_total_float = float(mem_total)
                mem_percent = (mem_used_float / mem_total_float * 100) if mem_total_float > 0 else 0
                mem_percent_str = f"{mem_percent:.1f}%"
            except (ValueError, ZeroDivisionError):
                mem_percent_str = "N/A"
            
            # Determine status emoji
            try:
                util_int = int(util)
                temp_int = int(temp)
                if util_int > 80 or temp_int > 80:
                    status_emoji = "🔥"
                    status_text = "High Load"
                elif util_int > 0:
                    status_emoji = "⚡"
                    status_text = "Active"
                else:
                    status_emoji = "💤"
                    status_text = "Idle"
            except ValueError:
                status_emoji = "⚡"
                status_text = "Active"
            
            blocks.extend([
                {"type": "divider"},
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{status_emoji} *GPU {index}: {name}*\nStatus: {status_text}"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"🌡️ *Temperature:*\n{temp}°C"},
                        {"type": "mrkdwn", "text": f"⚡ *GPU Utilization:*\n{util}%"},
                        {"type": "mrkdwn", "text": f"💾 *Memory Usage:*\n{mem_used}MiB / {mem_total}MiB"},
                        {"type": "mrkdwn", "text": f"📊 *Memory %:*\n{mem_percent_str}"}
                    ]
                }
            ])
            
            process_list = processes_by_gpu.get(uuid)
            if process_list:
                process_text = "\n".join([
                    f"• `{p['name']}` (PID: {p['pid']}) - {p['mem']}MiB"
                    for p in process_list
                ])
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"🔄 *Active Processes ({len(process_list)}):*\n{process_text}"
                    }
                })
            else:
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "🔄 *Active Processes:*\nNo processes running"
                    }
                })
        
        return blocks
        
    except FileNotFoundError:
        logger.error("nvidia-smi command not found")
        return create_error_block(
            "NVIDIA Driver Error",
            "The `nvidia-smi` command was not found. Please ensure NVIDIA drivers are installed."
        )
    except subprocess.TimeoutExpired:
        logger.error("nvidia-smi command timed out")
        return create_error_block(
            "Timeout Error",
            "The GPU query timed out. Please try again later."
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"nvidia-smi command failed: {e.stderr}")
        return create_error_block(
            "NVIDIA Driver Error",
            f"The `nvidia-smi` command failed to execute.\n*Error:* {e.stderr[:200] if e.stderr else 'Unknown error'}"
        )
    except Exception as e:
        logger.error(f"Unexpected error in realtime handler: {e}")
        return create_error_block(
            "Unexpected Error",
            f"An unexpected error occurred: {str(e)}"
        )