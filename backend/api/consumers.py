# Django Channels Consumers for GraphQL Subscriptions
# Real-time AI Chat Streaming via WebSockets

import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError
import graphene
from .schema_extensions_fixed import ChatWithAIMutation

class AIChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time AI chat streaming
    Handles GraphQL subscription for AI responses
    """
    
    async def connect(self):
        """Accept WebSocket connection"""
        await self.accept()
        self.user = self.scope["user"]
        self.chat_id = f"chat_{self.user.id if self.user.is_authenticated else 'anonymous'}"
        
        # Join chat room
        await self.channel_layer.group_add(
            self.chat_id,
            self.channel_name
        )
        
        print(f"🔗 AI Chat connected: {self.chat_id}")
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        await self.channel_layer.group_discard(
            self.chat_id,
            self.channel_name
        )
        print(f"🔌 AI Chat disconnected: {self.chat_id}")
    
    async def receive(self, text_data):
        """Receive message from WebSocket"""
        try:
            data = json.loads(text_data)
            message = data.get('message', '')
            context = data.get('context', {})
            
            if not message.strip():
                await self.send_error("Message cannot be empty")
                return
            
            # Start AI processing
            await self.process_ai_message(message, context)
            
        except json.JSONDecodeError:
            await self.send_error("Invalid JSON format")
        except Exception as e:
            await self.send_error(f"Error processing message: {str(e)}")
    
    async def process_ai_message(self, message, context):
        """Process AI message and stream response"""
        try:
            # Send processing indicator
            await self.send_message({
                'type': 'processing',
                'message': 'AI is thinking...'
            })
            
            # Simulate AI processing with streaming
            ai_response = await self.generate_ai_response_stream(message, context)
            
        except Exception as e:
            await self.send_error(f"AI processing failed: {str(e)}")
    
    async def generate_ai_response_stream(self, message, context):
        """Generate AI response with streaming effect"""
        try:
            # Simulate AI processing time
            await asyncio.sleep(0.5)
            
            # Mock AI response (replace with actual AI logic)
            full_response = f"AI Response to: {message}"
            
            # Stream response character by character
            current_response = ""
            
            for i, char in enumerate(full_response):
                current_response += char
                await self.send_message({
                    'type': 'streaming',
                    'content': current_response,
                    'progress': (i + 1) / len(full_response) * 100
                })
                await asyncio.sleep(0.05)  # Simulate typing delay
            
            # Send final response
            await self.send_message({
                'type': 'complete',
                'content': full_response,
                'timestamp': asyncio.get_event_loop().time()
            })
            
        except Exception as e:
            await self.send_error(f"AI generation failed: {str(e)}")
    
    async def send_message(self, data):
        """Send message to WebSocket"""
        await self.send(text_data=json.dumps({
            'success': True,
            'data': data
        }))
    
    async def send_error(self, error_message):
        """Send error message to WebSocket"""
        await self.send(text_data=json.dumps({
            'success': False,
            'error': error_message
        }))

class GraphQLSubscriptionConsumer(AsyncWebsocketConsumer):
    """
    Generic GraphQL subscription consumer
    Handles real-time data updates
    """
    
    async def connect(self):
        await self.accept()
        self.subscription_id = f"sub_{id(self)}"
        
        await self.channel_layer.group_add(
            "graphql_subscriptions",
            self.channel_name
        )
        
        print(f"🔗 GraphQL Subscription connected: {self.subscription_id}")
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "graphql_subscriptions",
            self.channel_name
        )
        print(f"🔌 GraphQL Subscription disconnected: {self.subscription_id}")
    
    async def receive(self, text_data):
        """Handle subscription queries"""
        try:
            data = json.loads(text_data)
            subscription_type = data.get('type')
            
            if subscription_type == 'ai_chat':
                # Handle AI chat subscription
                await self.handle_ai_chat_subscription(data)
            elif subscription_type == 'order_updates':
                # Handle order updates subscription
                await self.handle_order_updates_subscription(data)
            else:
                await self.send_error("Unknown subscription type")
                
        except Exception as e:
            await self.send_error(f"Subscription error: {str(e)}")
    
    async def handle_ai_chat_subscription(self, data):
        """Handle AI chat subscription"""
        message = data.get('message', '')
        
        # Send to AI chat consumer
        await self.channel_layer.group_send(
            f"chat_{self.scope['user'].id if self.scope['user'].is_authenticated else 'anonymous'}",
            {
                'type': 'ai_message',
                'message': message,
                'sender': self.channel_name
            }
        )
    
    async def handle_order_updates_subscription(self, data):
        """Handle order updates subscription"""
        order_id = data.get('order_id')
        
        if order_id:
            # Subscribe to order updates
            await self.channel_layer.group_add(
                f"order_{order_id}",
                self.channel_name
            )
            
            await self.send_message({
                'type': 'subscribed',
                'subscription': 'order_updates',
                'order_id': order_id
            })
    
    async def send_message(self, data):
        """Send message to WebSocket"""
        await self.send(text_data=json.dumps({
            'success': True,
            'data': data
        }))
    
    async def send_error(self, error_message):
        """Send error message to WebSocket"""
        await self.send(text_data=json.dumps({
            'success': False,
            'error': error_message
        }))
