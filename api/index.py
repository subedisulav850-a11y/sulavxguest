"""
Vercel Serverless Handler for Garena Guest Generator API
"""
import json
import asyncio
import sys
import os
from flask import Flask, request, jsonify

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from app.py
try:
    from app import (
        ACTIVATION_CONFIGS,
        create_acc_for_api,
        REGION_IP_RANGES
    )
except ImportError as e:
    # Fallback if app.py is not found
    ACTIVATION_CONFIGS = {}
    REGION_IP_RANGES = {}

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    """Root endpoint - API information"""
    return jsonify({
        "status": "online",
        "service": "Garena Guest Generator API with IP/Proxy Rotation & Auto Activation",
        "version": "2.0.0",
        "supported_regions": list(ACTIVATION_CONFIGS.keys()) if ACTIVATION_CONFIGS else [],
        "endpoints": {
            "/": "This info page",
            "/g": "Generate accounts: /g?name={name}&region={region}&count={count}&activate={true/false}"
        },
        "example": "/g?name=Vaibhav&region=IND&count=5&activate=true",
        "docs": "https://github.com/yourusername/garena-generator"
    })

@app.route('/g', methods=['GET'])
def generate_accounts():
    """
    Generate Garena guest accounts
    Query Parameters:
        - name: Name prefix (default: Sulav)
        - region: Region code (IND, BD, PK, ID, TH, VN, ME, BR, TW, EU, CIS, NA, SAC)
        - count: Number of accounts to generate (1-50)
        - activate: Auto activate accounts (true/false)
    """
    # Parse parameters
    name_prefix = request.args.get('name', 'Sulav')
    region = request.args.get('region', 'IND').upper()
    auto_activate = request.args.get('activate', 'true').lower() == 'true'
    
    try:
        count = int(request.args.get('count', '1'))
    except ValueError:
        count = 1
    
    # Validate and limit count
    count = max(1, min(count, 50))
    is_ghost = (region == "GHOST")
    actual_region = "BR" if is_ghost else region
    
    # Validate region
    if actual_region not in ACTIVATION_CONFIGS:
        return jsonify({
            "status": "error",
            "message": f"Region '{actual_region}' not supported. Supported: {list(ACTIVATION_CONFIGS.keys())}"
        }), 400
    
    try:
        # Run async generation
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        results = loop.run_until_complete(
            generate_accounts_async(actual_region, name_prefix, count, is_ghost, auto_activate)
        )
        loop.close()
        
        response_data = {
            "status": "success" if results else "failed",
            "requested_count": count,
            "generated_count": len(results),
            "auto_activation": auto_activate,
            "region": actual_region,
            "accounts": results,
            "timestamp": asyncio.get_event_loop().time() if hasattr(asyncio, 'get_event_loop') else None
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "region": actual_region
        }), 500

async def generate_accounts_async(region, name_prefix, count, is_ghost, auto_activate):
    """Generate multiple accounts with concurrency control"""
    import aiohttp
    
    semaphore = asyncio.Semaphore(10)
    results = []
    
    connector = aiohttp.TCPConnector(limit=0, force_close=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for _ in range(count):
            tasks.append(create_acc_for_api(
                session, region, name_prefix, is_ghost, semaphore, auto_activate
            ))
        
        completed = await asyncio.gather(*tasks, return_exceptions=True)
        
        for account_data in completed:
            if isinstance(account_data, Exception):
                continue
            if account_data and account_data.get('account_id') != "N/A":
                results.append(account_data)
    
    return results

@app.route('/regions', methods=['GET'])
def list_regions():
    """List all supported regions"""
    return jsonify({
        "supported_regions": list(ACTIVATION_CONFIGS.keys()),
        "total": len(ACTIVATION_CONFIGS),
        "ip_ranges": REGION_IP_RANGES
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        "status": "healthy",
        "service": "garena-generator",
        "regions_available": len(ACTIVATION_CONFIGS),
        "version": "2.0.0"
    })

# Vercel serverless handler
def handler(event, context):
    """Vercel serverless entry point"""
    return app(event, context)

# Local development server
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)