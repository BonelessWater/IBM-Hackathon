from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging

logger = logging.getLogger(__name__)

class PlaygroundConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'playground'

    def ready(self):
        self.start_scheduler()

    def start_scheduler(self):
        from .tasks import log_emails_task  # Import your task function here

        scheduler = BackgroundScheduler()
        
        # Add a job to run every 5 minutes
        scheduler.add_job(
            log_emails_task,
            trigger=CronTrigger(hour='*/5'),  # Every 5 minutes
            id='log_emails_task',
            replace_existing=True,
            max_instances=1
        )

        scheduler.start()
        logger.debug("Scheduler started for log_emails_task.")
