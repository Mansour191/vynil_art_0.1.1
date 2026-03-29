# Django-Q Tasks for ERPNext Auto-Sync
# Automated synchronization with ERPNext using background tasks

from django_q.tasks import async_task, schedule
from django_q.models import Schedule
from django.utils import timezone
from datetime import timedelta
from api.schema_extensions_fixed import syncWithERPNext
from api.models import ERPNextSyncLog, Notification
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

def auto_sync_erpnext():
    """
    Automated ERPNext synchronization task
    Runs automatically every hour via Django-Q scheduler
    """
    try:
        logger.info("🚀 Starting automated ERPNext sync")
        
        # Check if sync is already running
        running_sync = ERPNextSyncLog.objects.filter(
            status='running',
            timestamp__gte=timezone.now() - timezone.timedelta(minutes=30)
        ).first()
        
        if running_sync:
            logger.info("⏭️ Sync already running, skipping this execution")
            return {
                'success': False,
                'message': 'Sync already running',
                'skipped': True
            }
        
        # Create sync log entry
        sync_log = ERPNextSyncLog.objects.create(
            action='auto_sync_all',
            status='running',
            message='Automated sync started',
            records_synced=0
        )
        
        # Perform sync for all data types
        sync_types = ['products', 'orders']
        total_records = 0
        errors = []
        
        for sync_type in sync_types:
            try:
                logger.info(f"🔄 Syncing {sync_type}...")
                
                result = syncWithERPNext(
                    None,  # GraphQL info context
                    sync_type=sync_type,
                    dry_run=False
                )
                
                if result.success:
                    records_synced = getattr(result, 'records_synced', 0)
                    total_records += records_synced
                    logger.info(f"✅ {sync_type} sync completed: {records_synced} records")
                else:
                    error_msg = f"{sync_type} sync failed: {result.message}"
                    errors.append(error_msg)
                    logger.error(error_msg)
                
            except Exception as e:
                error_msg = f"{sync_type} sync exception: {str(e)}"
                errors.append(error_msg)
                logger.error(error_msg)
        
        # Update sync log
        sync_log.status = 'success' if not errors else 'partial_success'
        sync_log.message = f"Automated sync completed. Total records: {total_records}"
        sync_log.records_synced = total_records
        sync_log.error_message = '; '.join(errors) if errors else None
        sync_log.save()
        
        # Send notifications to staff users
        send_sync_notification(sync_log, errors)
        
        result = {
            'success': sync_log.status != 'failed',
            'message': sync_log.message,
            'records_synced': total_records,
            'errors': errors,
            'status': sync_log.status
        }
        
        logger.info(f"🏁 Automated sync completed: {result}")
        return result
        
    except Exception as e:
        logger.error(f"❌ Automated sync failed: {str(e)}")
        
        # Update sync log if it exists
        if 'sync_log' in locals():
            sync_log.status = 'failed'
            sync_log.message = 'Automated sync failed with exception'
            sync_log.error_message = str(e)
            sync_log.save()
        
        return {
            'success': False,
            'message': f'Automated sync failed: {str(e)}',
            'status': 'failed'
        }

def send_sync_notification(sync_log, errors):
    """
    Send notification to staff users about sync status
    """
    try:
        staff_users = User.objects.filter(is_staff=True, is_active=True)
        
        # Determine notification type and message
        if sync_log.status == 'success':
            notification_type = 'success'
            title = 'ERPNext Sync Successful'
            message = f'Automated sync completed successfully. {sync_log.records_synced} records synced.'
        elif sync_log.status == 'partial_success':
            notification_type = 'warning'
            title = 'ERPNext Sync Partial Success'
            message = f'Sync completed with {len(errors)} errors. {sync_log.records_synced} records synced.'
        else:
            notification_type = 'error'
            title = 'ERPNext Sync Failed'
            message = f'Automated sync failed. Please check the system logs.'
        
        # Create notifications for all staff users
        notifications = []
        for user in staff_users:
            notification = Notification.objects.create(
                user=user,
                title=title,
                message=message,
                type=notification_type,
                data={
                    'sync_id': sync_log.id,
                    'sync_status': sync_log.status,
                    'records_synced': sync_log.records_synced,
                    'errors': errors
                }
            )
            notifications.append(notification)
        
        logger.info(f"📧 Sent sync notifications to {len(notifications)} staff users")
        
    except Exception as e:
        logger.error(f"Failed to send sync notifications: {str(e)}")

def setup_auto_sync_scheduler():
    """
    Setup Django-Q scheduler for automatic ERPNext sync
    This function should be called during app initialization
    """
    try:
        # Check if scheduler already exists
        existing_schedule = Schedule.objects.filter(
            name='erpnext_auto_sync'
        ).first()
        
        if existing_schedule:
            logger.info("📅 ERPNext auto-sync scheduler already exists")
            return existing_schedule
        
        # Create new scheduler
        schedule_obj = schedule(
            'api.tasks.auto_sync_erpnext',
            name='erpnext_auto_sync',
            schedule_type=Schedule.HOURS,
            repeats=-1,  # Repeat forever
            next_run=timezone.now() + timedelta(hours=1),  # Start in 1 hour
        )
        
        logger.info("📅 ERPNext auto-sync scheduler created successfully")
        return schedule_obj
        
    except Exception as e:
        logger.error(f"Failed to setup auto-sync scheduler: {str(e)}")
        return None

def manual_sync_task(sync_type='all', dry_run=False):
    """
    Manual sync task that can be called from anywhere
    """
    try:
        logger.info(f"🔄 Starting manual sync task: {sync_type}")
        
        # Create sync log
        sync_log = ERPNextSyncLog.objects.create(
            action=f'manual_task_sync_{sync_type}',
            status='running',
            message=f'Manual task sync started for {sync_type}',
            records_synced=0
        )
        
        # Perform sync
        result = syncWithERPNext(None, sync_type=sync_type, dry_run=dry_run)
        
        # Update sync log
        sync_log.status = 'success' if result.success else 'failed'
        sync_log.message = result.message
        sync_log.records_synced = getattr(result, 'records_synced', 0)
        sync_log.error_message = getattr(result, 'error_message', None)
        sync_log.save()
        
        logger.info(f"✅ Manual sync task completed: {result}")
        return result
        
    except Exception as e:
        logger.error(f"❌ Manual sync task failed: {str(e)}")
        
        if 'sync_log' in locals():
            sync_log.status = 'failed'
            sync_log.message = 'Manual task sync failed with exception'
            sync_log.error_message = str(e)
            sync_log.save()
        
        return {
            'success': False,
            'message': f'Manual sync task failed: {str(e)}',
            'status': 'failed'
        }

def get_sync_status():
    """
    Get current sync status and statistics
    """
    try:
        latest_sync = ERPNextSyncLog.objects.first()
        
        if not latest_sync:
            return {
                'status': 'never_synced',
                'message': 'No sync history found',
                'last_sync': None,
                'total_records': 0
            }
        
        # Get sync statistics
        total_syncs = ERPNextSyncLog.objects.count()
        successful_syncs = ERPNextSyncLog.objects.filter(status='success').count()
        failed_syncs = ERPNextSyncLog.objects.filter(status='failed').count()
        
        return {
            'status': latest_sync.status,
            'message': latest_sync.message,
            'last_sync': latest_sync.timestamp,
            'records_synced': latest_sync.records_synced,
            'error_message': latest_sync.error_message,
            'statistics': {
                'total_syncs': total_syncs,
                'successful_syncs': successful_syncs,
                'failed_syncs': failed_syncs,
                'success_rate': (successful_syncs / total_syncs * 100) if total_syncs > 0 else 0
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get sync status: {str(e)}")
        return {
            'status': 'error',
            'message': f'Failed to get sync status: {str(e)}',
            'last_sync': None,
            'total_records': 0
        }

# Initialize scheduler when module is imported
def initialize_scheduler():
    """Initialize the auto-sync scheduler"""
    try:
        setup_auto_sync_scheduler()
        logger.info("🚀 ERPNext auto-sync scheduler initialized")
    except Exception as e:
        logger.error(f"Failed to initialize scheduler: {str(e)}")

# Auto-initialize when module is imported
initialize_scheduler()
