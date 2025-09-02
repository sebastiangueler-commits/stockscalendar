[33mcommit da5da1cb840fff78e8da006349bd5589b0b0722b[m[33m ([m[1;36mHEAD[m[33m -> [m[1;32mmain[m[33m, [m[1;31morigin/main[m[33m, [m[1;31morigin/HEAD[m[33m)[m
Author: sebastiangueler-commits <sebastiangueler@gmail.com>
Date:   Wed Aug 27 17:17:41 2025 -0300

    Develop a full-stack financial analysis app (#1)
    
    * Initialize Financial Calendars App backend with FastAPI, auth, and ML features
    
    Co-authored-by: sebigueler <sebigueler@gmail.com>
    
    * Add role-based access control to calendar and search endpoints
    
    Co-authored-by: sebigueler <sebigueler@gmail.com>
    
    * Enhance symbol management, auth, and fundamentals with dynamic symbol fetching
    
    Co-authored-by: sebigueler <sebigueler@gmail.com>
    
    * Enhance Stripe integration, add bootstrap limits, and improve scheduler
    
    Co-authored-by: sebigueler <sebigueler@gmail.com>
    
    ---------
    
    Co-authored-by: Cursor Agent <cursoragent@cursor.com>
    Co-authored-by: sebigueler <sebigueler@gmail.com>

.env.example
README.md
__pycache__/main.cpython-313.pyc
backend/__pycache__/config.cpython-313.pyc
backend/__pycache__/database.cpython-313.pyc
backend/__pycache__/models.cpython-313.pyc
backend/__pycache__/schemas.cpython-313.pyc
backend/auth/__init__.py
backend/auth/__pycache__/__init__.cpython-313.pyc
backend/auth/__pycache__/security.cpython-313.pyc
backend/auth/security.py
backend/config.py
backend/database.py
backend/models.py
backend/routers/__init__.py
backend/routers/__pycache__/__init__.cpython-313.pyc
backend/routers/__pycache__/auth.cpython-313.pyc
backend/routers/admin.py
backend/routers/auth.py
backend/routers/calendars.py
backend/routers/ops.py
backend/routers/search.py
backend/routers/signals.py
backend/routers/stripe.py
backend/schemas.py
backend/services/__init__.py
backend/services/bootstrap.py
backend/services/fundamentals.py
backend/services/market_data.py
backend/services/ml.py
backend/services/scheduler.py
backend/services/symbols.py
backend/static/.gitkeep
backend/templates/.gitkeep
calendar_fundamental.json
calendar_historical.json
main.py
requirements.txt
