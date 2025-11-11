import logging
import sys
import gzip
import shutil
from pathlib import Path
from logging.handlers import RotatingFileHandler
import structlog
from pythonjsonlogger import jsonlogger
import hashlib

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

# ------------------------------------------------------------
# 🔹 Custom RotatingFileHandler with Compression & Hashing
# ------------------------------------------------------------
class CompressedRotatingFileHandler(RotatingFileHandler):
    """
    Extends RotatingFileHandler to compress rotated logs into .gz
    and maintain an integrity hash for comparison.
    """

    def doRollover(self):
        super().doRollover()  # Rotate the file first

        # Compress old logs
        for old_log in LOG_DIR.glob("app.log.*"):
            if not old_log.suffix == ".gz" and old_log.is_file():
                compressed_path = old_log.with_suffix(old_log.suffix + ".gz")
                with open(old_log, "rb") as f_in, gzip.open(compressed_path, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
                old_log.unlink()  # delete uncompressed file
                create_log_hash(compressed_path)


def create_log_hash(file_path: Path):
    """Generate SHA256 hash for a file and store in a .hash file."""
    hash_file = file_path.with_suffix(file_path.suffix + ".hash")
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha.update(chunk)
    hash_file.write_text(sha.hexdigest())


def compare_log_files(file1: Path, file2: Path) -> bool:
    """Compare two log files by their SHA256 hash."""
    def get_hash(file):
        sha = hashlib.sha256()
        with open(file, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha.update(chunk)
        return sha.hexdigest()
    return get_hash(file1) == get_hash(file2)


# ------------------------------------------------------------
# 1️⃣ Configure standard logging handlers
# ------------------------------------------------------------
log_level = logging.INFO

# Custom rotating handler (10 MB max, 5 backups)
file_handler = CompressedRotatingFileHandler(LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5)
console_handler = logging.StreamHandler(sys.stdout)

# JSON formatter for structured logs
json_formatter = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(name)s %(funcName)s %(lineno)d %(message)s"
)
file_handler.setFormatter(json_formatter)

# Readable console logs
console_formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
console_handler.setFormatter(console_formatter)

logging.basicConfig(
    level=log_level,
    handlers=[file_handler, console_handler],
)

# ------------------------------------------------------------
# 2️⃣ Configure Structlog (structured, contextual logs)
# ------------------------------------------------------------
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.make_filtering_bound_logger(log_level),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger("invoai")
logger.info("✅ Structlog-based logger initialized with compression and hash checking.")
