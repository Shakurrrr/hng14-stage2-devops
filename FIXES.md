File: api/main.py  
Line: 7  
Issue: Redis host hardcoded as localhost  
Impact: Will fail in containerized environment  
Fix: Replace with environment variable REDIS_HOST