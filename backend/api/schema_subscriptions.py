# GraphQL Subscriptions Schema
# Real-time AI Chat and data streaming

import graphene
import asyncio
from graphene import ObjectType, Field, String, ID, Boolean
from django.contrib.auth.models import User
from .models import Notification, ERPNextSyncLog
from datetime import datetime
import json

# --- Subscription Types ---

class AIChatMessage(graphene.ObjectType):
    """AI Chat message type for streaming"""
    content = graphene.String()
    type = graphene.String()  # 'streaming', 'complete', 'processing', 'error'
    progress = graphene.Float()
    timestamp = graphene.DateTime()
    user_id = graphene.ID()

class OrderUpdate(graphene.ObjectType):
    """Order update notification type"""
    order_id = graphene.ID()
    status = graphene.String()
    message = graphene.String()
    timestamp = graphene.DateTime()
    user_id = graphene.ID()

class NotificationUpdate(graphene.ObjectType):
    """Real-time notification type"""
    id = graphene.ID()
    title = graphene.String()
    message = graphene.String()
    type = graphene.String()
    is_read = graphene.Boolean()
    user_id = graphene.ID()

class ERPNextSyncUpdate(graphene.ObjectType):
    """ERPNext sync status update"""
    sync_id = graphene.ID()
    status = graphene.String()
    message = graphene.String()
    records_synced = graphene.Int()
    timestamp = graphene.DateTime()
    error_message = graphene.String()

# --- Subscription Class ---

class Subscription(ObjectType):
    """GraphQL Subscriptions for real-time updates"""
    
    # AI Chat Subscription - Streaming responses
    ai_chat_stream = graphene.Field(
        AIChatMessage,
        message=graphene.String(required=True),
        context=graphene.String(),
        description="Stream AI chat responses in real-time"
    )
    
    # Order Updates Subscription
    order_updates = graphene.Field(
        OrderUpdate,
        order_id=graphene.ID(required=True),
        description="Subscribe to order status updates"
    )
    
    # Notifications Subscription
    notifications = graphene.Field(
        NotificationUpdate,
        user_id=graphene.ID(),
        description="Subscribe to real-time notifications"
    )
    
    # ERPNext Sync Status Subscription
    erpnext_sync_status = graphene.Field(
        ERPNextSyncUpdate,
        description="Subscribe to ERPNext sync status updates"
    )

    # --- Subscription Resolvers ---
    
    async def resolve_ai_chat_stream(self, info, message, context=None):
        """
        Stream AI chat responses in real-time
        This resolver simulates streaming responses like ChatGPT
        """
        try:
            user = info.context.user
            if not user.is_authenticated:
                raise Exception("Authentication required for AI chat")
            
            # Validate input
            if not message or not message.strip():
                raise Exception("Message cannot be empty")
            
            # Send processing indicator
            yield AIChatMessage(
                content="AI is thinking...",
                type="processing",
                progress=0,
                timestamp=datetime.now(),
                user_id=str(user.id)
            )
            
            # Simulate AI processing delay
            await asyncio.sleep(1)
            
            # Mock AI response (replace with actual AI integration)
            full_response = f"AI Response: I understand you're asking about '{message}'. Let me help you with that..."
            
            # Stream response character by character for typing effect
            current_response = ""
            chars_per_chunk = 5  # Send 5 characters at a time for smoother streaming
            
            for i in range(0, len(full_response), chars_per_chunk):
                chunk = full_response[i:i + chars_per_chunk]
                current_response += chunk
                progress = (i + chars_per_chunk) / len(full_response) * 100
                
                yield AIChatMessage(
                    content=current_response,
                    type="streaming",
                    progress=min(progress, 100),
                    timestamp=datetime.now(),
                    user_id=str(user.id)
                )
                
                # Small delay for realistic typing effect
                await asyncio.sleep(0.1)
            
            # Send final complete message
            yield AIChatMessage(
                content=full_response,
                type="complete",
                progress=100,
                timestamp=datetime.now(),
                user_id=str(user.id)
            )
            
        except Exception as e:
            # Send error message
            yield AIChatMessage(
                content=f"Error: {str(e)}",
                type="error",
                progress=0,
                timestamp=datetime.now(),
                user_id=str(user.id) if user.is_authenticated else "anonymous"
            )
    
    async def resolve_order_updates(self, info, order_id):
        """
        Subscribe to order status updates
        """
        try:
            user = info.context.user
            if not user.is_authenticated:
                raise Exception("Authentication required")
            
            # Validate order access (user can only see their own orders unless staff)
            # This would involve database queries to verify access
            
            # Initial status
            yield OrderUpdate(
                order_id=order_id,
                status="subscribed",
                message="Subscribed to order updates",
                timestamp=datetime.now(),
                user_id=str(user.id)
            )
            
            # This would typically listen to database changes or message queue
            # For demo purposes, we'll simulate updates
            for i in range(3):
                await asyncio.sleep(5)  # Wait for updates
                yield OrderUpdate(
                    order_id=order_id,
                    status="processing",
                    message=f"Order update {i+1}: Processing your order...",
                    timestamp=datetime.now(),
                    user_id=str(user.id)
                )
            
            # Final status
            yield OrderUpdate(
                order_id=order_id,
                status="completed",
                message="Order processing completed",
                timestamp=datetime.now(),
                user_id=str(user.id)
            )
            
        except Exception as e:
            yield OrderUpdate(
                order_id=order_id,
                status="error",
                message=f"Error: {str(e)}",
                timestamp=datetime.now(),
                user_id=str(user.id) if user.is_authenticated else "anonymous"
            )
    
    async def resolve_notifications(self, info, user_id=None):
        """
        Subscribe to real-time notifications
        """
        try:
            user = info.context.user
            if not user.is_authenticated:
                raise Exception("Authentication required")
            
            target_user_id = user_id or str(user.id)
            
            # Get existing notifications
            existing_notifications = Notification.objects.filter(
                user_id=target_user_id,
                is_read=False
            ).order_by('-created_at')[:5]
            
            for notification in existing_notifications:
                yield NotificationUpdate(
                    id=str(notification.id),
                    title=notification.title,
                    message=notification.message,
                    type=notification.type,
                    is_read=notification.is_read,
                    user_id=target_user_id
                )
            
            # Listen for new notifications (this would typically use Django Signals)
            # For demo purposes, we'll simulate new notifications
            while True:
                await asyncio.sleep(10)  # Check for new notifications every 10 seconds
                
                # Check for new notifications
                new_notifications = Notification.objects.filter(
                    user_id=target_user_id,
                    is_read=False,
                    created_at__gt=datetime.now() - timedelta(seconds=10)
                )
                
                for notification in new_notifications:
                    yield NotificationUpdate(
                        id=str(notification.id),
                        title=notification.title,
                        message=notification.message,
                        type=notification.type,
                        is_read=notification.is_read,
                        user_id=target_user_id
                    )
                
        except Exception as e:
            yield NotificationUpdate(
                id="error",
                title="Subscription Error",
                message=f"Error: {str(e)}",
                type="error",
                is_read=False,
                user_id=str(user.id) if user.is_authenticated else "anonymous"
            )
    
    async def resolve_erpnext_sync_status(self, info):
        """
        Subscribe to ERPNext sync status updates
        """
        try:
            user = info.context.user
            if not user.is_authenticated or not user.is_staff:
                raise Exception("Staff access required for sync status")
            
            # Get latest sync log
            latest_sync = ERPNextSyncLog.objects.first()
            
            if latest_sync:
                yield ERPNextSyncUpdate(
                    sync_id=str(latest_sync.id),
                    status=latest_sync.status,
                    message=latest_sync.message,
                    records_synced=latest_sync.records_synced,
                    timestamp=latest_sync.timestamp,
                    error_message=latest_sync.error_message
                )
            else:
                yield ERPNextSyncUpdate(
                    sync_id="none",
                    status="no_sync",
                    message="No sync history found",
                    records_synced=0,
                    timestamp=datetime.now(),
                    error_message=None
                )
            
            # Listen for new sync updates (this would typically use Django Signals)
            # For demo purposes, we'll check periodically
            last_sync_id = latest_sync.id if latest_sync else None
            
            while True:
                await asyncio.sleep(30)  # Check for sync updates every 30 seconds
                
                latest_sync = ERPNextSyncLog.objects.first()
                if latest_sync and latest_sync.id != last_sync_id:
                    yield ERPNextSyncUpdate(
                        sync_id=str(latest_sync.id),
                        status=latest_sync.status,
                        message=latest_sync.message,
                        records_synced=latest_sync.records_synced,
                        timestamp=latest_sync.timestamp,
                        error_message=latest_sync.error_message
                    )
                    last_sync_id = latest_sync.id
                
        except Exception as e:
            yield ERPNextSyncUpdate(
                sync_id="error",
                status="error",
                message=f"Error: {str(e)}",
                records_synced=0,
                timestamp=datetime.now(),
                error_message=str(e)
            )

# --- Enhanced Schema with Subscriptions ---

from .schema_extensions_fixed import ExtendedQuery as ERPNextQuery, ExtendedMutation as ERPNextMutation

class EnhancedQuery(ERPNextQuery, ObjectType):
    """Enhanced Query with subscription support"""
    pass

class EnhancedMutation(ERPNextMutation, ObjectType):
    """Enhanced Mutation with subscription support"""
    pass

class EnhancedSubscription(Subscription, ObjectType):
    """Enhanced Subscription with all real-time features"""
    pass

print("🚀 GraphQL Subscriptions configured for AI Chat and real-time updates")
