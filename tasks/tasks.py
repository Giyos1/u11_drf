from celery import shared_task
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

@shared_task
def check_status():
    logger.info(f"✅ OK — {timezone.now()}")
    return "ok"

@shared_task
def send_daily_report():
    logger.info("📊 Hisobot yuborilmoqda...")
    return "report sent"