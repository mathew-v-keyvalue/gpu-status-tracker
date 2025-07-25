# GPU Tracker Slack Bot 🚀

> A modern Slack bot to manage and monitor GPU resources in your team. Built with Python, Flask, and Slack's Block Kit for a rich, professional interface with comprehensive monitoring and management features.

This bot allows team members to check GPU availability, claim GPUs for specific tasks, release them when done, and get real-time performance snapshots - all within Slack's native interface.

---

## ✨ Key Features

### 📊 **Comprehensive Monitoring**

- **Allocation Dashboard**: Visual status of all GPUs with user assignments
- **Real-time Performance**: Live `nvidia-smi` data with temperature, utilization, and memory
- **Usage Analytics**: Track claim duration and usage patterns
- **Smart Status Indicators**: Color-coded health status (🔥 High Load, ⚡ Active, 💤 Idle)

### 🛠️ **Advanced Management**

- **Flexible Duration**: Reserve GPUs from 30 minutes to 12 hours
- **Purpose Tracking**: Document what each GPU is being used for
- **Auto-expiry Warnings**: Notifications when claims are about to expire
- **Multi-user Support**: Handles concurrent users safely

### 💎 **Modern UI/UX**

- **Rich Block Kit Interface**: Professional cards and layouts
- **Mobile Optimized**: Works seamlessly on mobile Slack apps
- **Accessibility**: High contrast images and clear visual hierarchy
- **Consistent Branding**: Professional appearance across all interactions

---

## 🎮 Demo & Usage

### **GPU Status Dashboard (`/gpu`)**

```
🎯 GPU Allocation Dashboard
📅 Updated: 2:30 PM IST, July 25 | Total GPUs: 4

✅ GPU 0
Status: Available for use

🔴 GPU 1 - In Use
👤 User: john.doe
📝 Purpose: Training ResNet model
⏰ Until: ~4:30 PM IST
⏳ 2h 15m remaining

💡 Use `/gpu claim <id> <purpose> [duration]` to reserve a GPU
```

### **Claiming a GPU**

```
Command: /gpu claim 0 training model 2h
Response:
🎉 GPU 0 Successfully Claimed!

👤 User: john.doe
📝 Purpose: training model
⏰ Duration: 2h
🕒 Release Time: ~4:30 PM IST

💡 Remember to use `/gpu release 0` when you're done!
```

### **Real-time Performance (`/gpu realtime`)**

```
🚀 GPU Real-Time Status Dashboard
📅 Last updated: 2:30 PM IST, July 25

⚡ GPU 0: NVIDIA RTX 4090
Status: Active

🌡️ Temperature: 72°C    ⚡ GPU Utilization: 85%
💾 Memory Usage: 18.2GB  📊 Memory %: 76.3%

🔄 Active Processes (2)
• python (PID: 12345) - 8192MiB
• jupyter (PID: 12346) - 2048MiB
```

---

## 🚀 Quick Start

### **Prerequisites**

- Python 3.9+
- NVIDIA GPU with drivers installed
- Slack workspace with admin access
- [ngrok](https://ngrok.com/download) for local development

### **1. Installation**

```bash
git clone <your-repository-url>
cd gpu-tracker-bot
pip install flask zoneinfo
```

### **2. Configure GPU Count**

```python
# In the code, update this line:
TOTAL_GPUS = 2  # Change to your actual GPU count
```

### **3. Create Slack App**

#### **A. Basic Setup**

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click "Create New App" → "From scratch"
3. Name: "GPU Tracker Bot"
4. Choose your workspace

#### **B. Configure Slash Command**

```
Features → Slash Commands → Create New Command

Command: /gpu
Short Description: Manage and monitor GPU resources
Usage Hint: [status|realtime|claim|release|help]
Request URL: https://your-ngrok-url.ngrok.io/
```

#### **C. Set OAuth Permissions**

```
Features → OAuth & Permissions → Scopes

Bot Token Scopes:
- commands
- chat:write
```

#### **D. Install to Workspace**

```
Settings → Install App → Install to Workspace
```

### **4. Run the Bot**

#### **Terminal 1: Start ngrok**

```bash
ngrok http 5000
# Copy the https:// URL (e.g., https://abc123.ngrok.io)
```

#### **Terminal 2: Run the bot**

```bash
python your_bot_file.py
# Bot runs on http://localhost:5000
```

### **5. Update Slack URLs**

Paste your ngrok URL into:

- Slash Command Request URL: `https://abc123.ngrok.io/`

---

## 📖 Command Reference

### **Slash Commands**

| Command                                | Description                 | Example                    |
| -------------------------------------- | --------------------------- | -------------------------- |
| `/gpu` or `/gpu status`                | Show allocation dashboard   | `/gpu`                     |
| `/gpu realtime`                        | Live performance monitoring | `/gpu realtime`            |
| `/gpu claim <id> <purpose> [duration]` | Reserve a GPU               | `/gpu claim 0 training 2h` |
| `/gpu release <id>`                    | Release your GPU            | `/gpu release 0`           |
| `/gpu help`                            | Show help guide             | `/gpu help`                |

### **Duration Formats**

- `30m` = 30 minutes
- `1h` = 1 hour
- `2h` = 2 hours
- `4h` = 4 hours
- `8h` = 8 hours
- `12h` = 12 hours

---

## 🏗️ Architecture

### **Core Components**

```
├── GPU Tracker Bot (your_bot_file.py)
│   ├── Flask Routes
│   │   └── /               # Slash commands
│   ├── Command Handlers
│   │   ├── handle_status()      # Dashboard display
│   │   ├── handle_realtime()    # Performance monitoring
│   │   ├── handle_claim()       # GPU reservation
│   │   ├── handle_release()     # GPU release
│   │   └── handle_help()        # Help documentation
│   └── Utilities
│       ├── Status management (JSON file)
│       ├── Time parsing & formatting
│       └── Block Kit UI builders
```

### **Data Flow**

1. **User Command**: User types slash command in Slack
2. **Route Handling**: Flask processes the request
3. **Business Logic**: Handler functions process the action
4. **GPU Operations**: Status updates or nvidia-smi queries
5. **UI Generation**: Block Kit elements created
6. **Response**: Rich interface sent back to Slack

### **State Management**

```json
{
  "0": { "status": "available" },
  "1": {
    "status": "in_use",
    "user_id": "U123456",
    "user_name": "john.doe",
    "purpose": "Training ResNet model",
    "claim_time": "2025-07-25T14:30:00",
    "release_time": "2025-07-25T16:30:00"
  }
}
```

---

## 🛠️ Development

### **Local Development**

```bash
# Run with debug mode
python your_bot_file.py
# Flask runs with debug=True for auto-reload

# Test endpoints
curl -X POST http://localhost:5000/ -d "text=status&user_id=U123&user_name=test"
```

### **Adding New Features**

#### **New Command Handler**

```python
def handle_new_command(args, user_id, user_name):
    """Handle new command logic."""
    return create_success_block("Success", "New feature works!")

# Add to main route handler
elif action == "newcommand":
    response_blocks = handle_new_command(args, user_id, user_name)
```

#### **New Interactive Element**

```python
def create_new_block():
    """Create a new Block Kit element for display."""
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*New Feature*\nDescription of the new functionality"
            }
        }
    ]
```

### **Testing**

```bash
# Test nvidia-smi integration
nvidia-smi --query-gpu=index,name --format=csv,noheader

# Test JSON file operations
python -c "import json; print(json.load(open('gpu_status.json')))"

# Test time parsing
python -c "from datetime import timedelta; print(timedelta(hours=2))"
```

---

## 🔧 Configuration

### **Environment Variables**

```bash
# Optional: Set custom configuration
export GPU_STATUS_FILE="custom_gpu_status.json"
export TOTAL_GPUS=4
export TIMEZONE="Asia/Kolkata"
```

### **Customization Options**

```python
# Modify these constants in the code:
TOTAL_GPUS = 4              # Your GPU count
STATUS_FILE = 'gpu_status.json'  # Status storage file
INDIA_TZ = ZoneInfo("Asia/Kolkata")  # Your timezone

# Add new duration options:
duration_options = [
    {"text": {"type": "plain_text", "text": "6 hours"}, "value": "6h"},
    {"text": {"type": "plain_text", "text": "24 hours"}, "value": "24h"}
]
```

---

## 🚨 Troubleshooting

### **Common Issues**

#### **"nvidia-smi not found"**

```bash
# Check NVIDIA driver installation
nvidia-smi
# If not found, install NVIDIA drivers for your system
```

#### **"Command not recognized"**

```bash
# Check if the slash command is properly configured in Slack
# Verify the command starts with the exact text: /gpu
```

#### **"Bot not responding"**

- Verify ngrok URL is updated in Slack app settings
- Check Flask server is running on port 5000
- Ensure OAuth permissions include required scopes

### **Debug Mode**

```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Add debug prints for troubleshooting
print(f"Received command: {command_text}")
print(f"User: {user_name} ({user_id})")
```

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### **Development Setup**

```bash
git clone <repository-url>
cd gpu-tracker-bot
pip install -r requirements.txt
python -m pytest tests/  # Run tests
```

### **Contribution Guidelines**

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Add** tests for new functionality
4. **Commit** changes (`git commit -m 'Add amazing feature'`)
5. **Push** to branch (`git push origin feature/amazing-feature`)
6. **Open** a Pull Request

### **Code Style**

- Follow PEP 8 Python style guide
- Use descriptive function and variable names
- Add docstrings to all functions
- Include type hints where appropriate

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Slack Block Kit**: For the amazing interactive UI components
- **NVIDIA**: For the comprehensive nvidia-smi tool
- **Flask**: For the lightweight and flexible web framework
- **Community**: For feedback and feature requests

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Documentation**: [Wiki](https://github.com/your-repo/wiki)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)

---

_Built with ❤️ for GPU-sharing teams everywhere_
