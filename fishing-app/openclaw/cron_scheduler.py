"""Cron Scheduler - 定时任务调度器"""
import logging
from typing import Dict, Any, List
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

from openclaw.report_agent import ReportAgent

logger = logging.getLogger(__name__)


class CronScheduler:
    """定时任务调度器
    
    管理所有定时任务的调度和执行
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize cron scheduler
        
        Args:
            config: OpenClaw configuration
        """
        self.config = config
        self.scheduler = BackgroundScheduler()
        self.report_agent = ReportAgent(config)
        
        # Get timezone
        timezone_str = config.get('environment', {}).get('timezone', 'Asia/Shanghai')
        self.timezone = pytz.timezone(timezone_str)
        
        logger.info(f"Cron scheduler initialized with timezone: {timezone_str}")
    
    def start(self):
        """Start scheduler"""
        logger.info("Starting cron scheduler...")
        
        # Register all cron jobs
        cron_jobs = self.config.get('cron_jobs', [])
        
        for job_config in cron_jobs:
            if not job_config.get('enabled', True):
                logger.info(f"Skipping disabled job: {job_config.get('name')}")
                continue
            
            self._register_job(job_config)
        
        # Start scheduler
        self.scheduler.start()
        logger.info(f"Cron scheduler started with {len(self.scheduler.get_jobs())} jobs")
    
    def stop(self):
        """Stop scheduler"""
        logger.info("Stopping cron scheduler...")
        self.scheduler.shutdown()
        logger.info("Cron scheduler stopped")
    
    def _register_job(self, job_config: Dict[str, Any]):
        """Register a cron job
        
        Args:
            job_config: Job configuration
        """
        name = job_config.get('name')
        display_name = job_config.get('display_name', name)
        schedule = job_config.get('schedule')
        agent = job_config.get('agent')
        config = job_config.get('config', {})
        
        logger.info(f"Registering job: {display_name} ({schedule})")
        
        # Create trigger
        trigger = CronTrigger.from_crontab(schedule, timezone=self.timezone)
        
        # Determine job function
        if agent == 'report-agent':
            report_type = config.get('report_type', 'daily')
            if report_type == 'daily':
                func = self._run_daily_report
            elif report_type == 'weekly':
                func = self._run_weekly_report
            else:
                logger.warning(f"Unknown report type: {report_type}")
                return
        elif agent == 'backup-agent':
            func = self._run_backup
        else:
            logger.warning(f"Unknown agent: {agent}")
            return
        
        # Add job to scheduler
        self.scheduler.add_job(
            func,
            trigger=trigger,
            id=name,
            name=display_name,
            kwargs={'config': config}
        )
        
        logger.info(f"Job registered: {display_name}")
    
    def _run_daily_report(self, config: Dict[str, Any]):
        """Run daily report job
        
        Args:
            config: Job configuration
        """
        logger.info("Running daily report job...")
        
        try:
            report = self.report_agent.generate_daily_report()
            logger.info(f"Daily report completed: {report.get('date')}")
        except Exception as e:
            logger.error(f"Daily report failed: {e}", exc_info=True)
    
    def _run_weekly_report(self, config: Dict[str, Any]):
        """Run weekly report job
        
        Args:
            config: Job configuration
        """
        logger.info("Running weekly report job...")
        
        try:
            report = self.report_agent.generate_weekly_report()
            logger.info(f"Weekly report completed: {report.get('start_date')} ~ {report.get('end_date')}")
        except Exception as e:
            logger.error(f"Weekly report failed: {e}", exc_info=True)
    
    def _run_backup(self, config: Dict[str, Any]):
        """Run backup job
        
        Args:
            config: Job configuration
        """
        logger.info("Running backup job...")
        
        # TODO: Implement backup logic
        logger.info("Backup completed (placeholder)")
    
    def list_jobs(self) -> List[Dict[str, Any]]:
        """List all scheduled jobs
        
        Returns:
            List of job information
        """
        jobs = []
        
        for job in self.scheduler.get_jobs():
            next_run = job.next_run_time
            
            jobs.append({
                'id': job.id,
                'name': job.name,
                'next_run': next_run.isoformat() if next_run else None,
                'trigger': str(job.trigger)
            })
        
        return jobs
    
    def trigger_job(self, job_id: str):
        """Manually trigger a job
        
        Args:
            job_id: Job ID
        """
        logger.info(f"Manually triggering job: {job_id}")
        
        job = self.scheduler.get_job(job_id)
        if job is None:
            raise ValueError(f"Job not found: {job_id}")
        
        job.modify(next_run_time=datetime.now(self.timezone))
        logger.info(f"Job triggered: {job_id}")
