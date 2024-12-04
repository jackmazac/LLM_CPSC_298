import time
import logging
import psutil
from functools import wraps
from typing import Any, Callable, Dict

logger = logging.getLogger(__name__)

def measure_time(func: Callable) -> Callable:
    """Decorator to measure function execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        duration = end_time - start_time
        logger.debug(f"{func.__name__} took {duration:.2f} seconds")
        
        # If first arg is self and has monitor, record the metric
        if args and hasattr(args[0], 'monitor'):
            args[0].monitor.record_metric(f"{func.__name__}_duration", duration)
        
        return result
    return wrapper

class PerformanceMonitor:
    """Monitor performance metrics for the system"""
    
    def __init__(self):
        self.start_time = time.time()
        self.metrics: Dict[str, Any] = {}
        self.task_count = 0
        self.success_count = 0
        self.failure_count = 0
    
    def get_timestamp(self) -> float:
        """Get current timestamp"""
        return time.time()
    
    def get_system_metrics(self) -> Dict[str, float]:
        """Get system performance metrics"""
        process = psutil.Process()
        memory_info = process.memory_info()
        
        return {
            'cpu_percent': process.cpu_percent(),
            'memory_mb': memory_info.rss / 1024 / 1024,
            'threads': process.num_threads()
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        current_time = self.get_timestamp()
        
        self.metrics.update({
            'uptime': current_time - self.start_time,
            'timestamp': current_time,
            'total_tasks': self.task_count,
            'success_rate': (self.success_count / self.task_count * 100) if self.task_count > 0 else 0,
            'system': self.get_system_metrics()
        })
        
        return self.metrics
    
    def record_metric(self, name: str, value: Any) -> None:
        """Record a new metric"""
        self.metrics[name] = value
    
    def record_task_result(self, success: bool) -> None:
        """Record task execution result"""
        self.task_count += 1
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1