# Django Management Command for Manual ERPNext Sync
# Usage: python manage.py run_sync [--type products|orders|all] [--dry-run]

from django.core.management.base import BaseCommand
from django.utils import timezone
from api.schema_extensions_fixed import syncWithERPNext
from api.models import ERPNextSyncLog
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Run ERPNext synchronization manually'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            choices=['products', 'orders', 'all'],
            default='all',
            help='Type of sync to run (products, orders, or all)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run sync in dry-run mode (no actual changes)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force sync even if recent sync exists'
        )
    
    def handle(self, *args, **options):
        sync_type = options['type']
        dry_run = options['dry_run']
        force = options['force']
        
        self.stdout.write(
            self.style.SUCCESS(
                f'🚀 Starting ERPNext sync (type: {sync_type}, dry-run: {dry_run})'
            )
        )
        
        try:
            # Check if recent sync exists (unless forced)
            if not force:
                recent_sync = ERPNextSyncLog.objects.filter(
                    status='success',
                    timestamp__gte=timezone.now() - timezone.timedelta(hours=1)
                ).first()
                
                if recent_sync:
                    self.stdout.write(
                        self.style.WARNING(
                            f'⚠️ Recent sync found at {recent_sync.timestamp}. Use --force to override.'
                        )
                    )
                    return
            
            # Create sync log entry
            sync_log = ERPNextSyncLog.objects.create(
                action=f'manual_sync_{sync_type}',
                status='running',
                message=f'Manual sync started for {sync_type}',
                records_synced=0
            )
            
            # Perform sync
            result = syncWithERPNext(
                None,  # GraphQL info context (not needed for manual sync)
                sync_type=sync_type,
                dry_run=dry_run
            )
            
            # Update sync log
            sync_log.status = 'success' if result.success else 'failed'
            sync_log.message = result.message
            sync_log.records_synced = getattr(result, 'records_synced', 0)
            sync_log.error_message = getattr(result, 'error_message', None)
            sync_log.save()
            
            if result.success:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Sync completed successfully. Records synced: {sync_log.records_synced}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f'❌ Sync failed: {result.message}'
                    )
                )
                if sync_log.error_message:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Error details: {sync_log.error_message}'
                        )
                    )
        
        except Exception as e:
            logger.error(f"Manual sync failed: {str(e)}")
            self.stdout.write(
                self.style.ERROR(
                    f'❌ Sync failed with exception: {str(e)}'
                )
            )
            
            # Update sync log with error
            if 'sync_log' in locals():
                sync_log.status = 'failed'
                sync_log.message = 'Manual sync failed with exception'
                sync_log.error_message = str(e)
                sync_log.save()
