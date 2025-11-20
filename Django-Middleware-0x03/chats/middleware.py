from datetime import datetime
import logging
import asyncio
from asgiref.sync import sync_to_async
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.utils.timezone import now
from collections import defaultdict
import time


# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("requests.log"),
        logging.StreamHandler()
    ]
)

# Store for tracking message counts by IP
message_count_tracker = defaultdict(
    lambda: {'count': 0, 'reset_time': time.time()})


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware that logs each user's requests including timestamp, user, and path.
    """

    def __init__(self, get_response):
        """
        Initialize the middleware with the get_response callable.

        Args:
            get_response (callable): The next middleware or view to be called.
        """
        self.get_response = get_response
        super().__init__(get_response)

    def __init__(self, get_response):
        self.get_response = get_response
        self._is_coroutine = asyncio.iscoroutinefunction(get_response)
        super().__init__(get_response)

    async def __call__(self, request):
        """Process incoming request and log info in an async-safe way."""

        def _get_username(r):
            user = getattr(r, 'user', None)
            try:
                return user.username if user and getattr(user, 'is_authenticated', False) else 'Anonymous'
            except Exception:
                return 'Anonymous'

        # Extract username in a thread to avoid synchronous DB access in the event loop
        username = await sync_to_async(_get_username, thread_sensitive=True)(request)
        path = request.path

        logger.info(f"Request received - User: {username}, Path: {path}")

        # Call the next middleware or view, keeping sync/async compatibility
        if self._is_coroutine:
            response = await self.get_response(request)
        else:
            response = await sync_to_async(self.get_response, thread_sensitive=True)(request)

        return response


class RestrictAccessByTimeMiddleware(MiddlewareMixin):
    """Middleware to restrict chat access outside 9AM-6PM"""

    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)

    def __call__(self, request):
        if '/api/conversations/' in request.path or '/api/messages/' in request.path:
            current_hour = now().hour
            if current_hour < 9 or current_hour >= 18:
                return JsonResponse(
                    {'error': 'Chat access is restricted to 9AM-6PM'}, status=403
                )

        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware(MiddlewareMixin):
    """Middleware to rate-limit messages per IP address (5 messages per minute)"""

    def __init__(self, get_response):
        self.get_response = get_response
        self.message_limit = 5
        self.time_window = 60  # seconds
        super().__init__(get_response)

    def __call__(self, request):
        if request.method == 'POST' and '/api/messages/' in request.path:
            client_ip = self.get_client_ip(request)
            current_time = time.time()

            tracker_entry = message_count_tracker[client_ip]

            # Reset count if time window has passed
            if current_time - tracker_entry['reset_time'] > self.time_window:
                tracker_entry['count'] = 0
                tracker_entry['reset_time'] = current_time

            # Check if limit exceeded
            if tracker_entry['count'] >= self.message_limit:
                return JsonResponse(
                    {'error': 'Message limit exceeded. Max 5 messages per minute.'},
                    status=429
                )

            # Increment message count
            tracker_entry['count'] += 1

        response = self.get_response(request)
        return response

    @staticmethod
    def get_client_ip(request):
        """Extract client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolePermissionMiddleware(MiddlewareMixin):
    """Middleware to enforce role-based permissions (admin/moderator only for certain endpoints)"""

    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)

    def __call__(self, request):
        protected_paths = ['/api/user/', '/api/admin/']

        if any(path in request.path for path in protected_paths):
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'Authentication required.'}, status=401)

            # Check if user has admin or moderator role
            user_role = getattr(request.user, 'role', None)
            if user_role not in ['admin', 'moderator']:
                return JsonResponse(
                    {'error': 'Only admin or moderator users can access this endpoint'},
                    status=403
                )

        response = self.get_response(request)
        return response
