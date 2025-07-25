from .claim_handler import handle_claim
from .release_handler import handle_release
from .status_handler import handle_status
from .realtime_handler import handle_realtime_status
from .help_handler import handle_help

command_handlers = {
    "claim": handle_claim,
    "release": handle_release,
    "status": handle_status,
    "realtime": handle_realtime_status,
    "help": handle_help
}