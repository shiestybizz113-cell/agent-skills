#!/usr/bin/env bash
# Home Agent — session start hook
# Runs on every new agent session: checks system health, CRM, analytics
set -e

echo "--- Home Agent: Session Start ---"

# Load mempalace context
if command -v mempalace &>/dev/null; then
    mempalace wake-up 2>/dev/null || echo "mempalace wake-up unavailable"
fi

# Check backend health
if curl -sf http://localhost:8001/health >/dev/null 2>&1; then
    echo "Backend: ONLINE"
elif curl -sf http://localhost:8000/health >/dev/null 2>&1; then
    echo "Backend: ONLINE (port 8000)"
else
    echo "Backend: OFFLINE (start with: cd ~/projects/Empire-1/backend && uvicorn server:app --port 8001)"
fi

# Quick CRM summary
if curl -sf http://localhost:8001/api/crm/metrics >/dev/null 2>&1; then
    crm=$(curl -sf http://localhost:8001/api/crm/metrics 2>/dev/null)
    echo "CRM: $(echo $crm | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"{d.get('metrics',{}).get('total_leads',0)} leads | \${d.get('metrics',{}).get('total_pipeline_value',0):,.0f} pipeline\")" 2>/dev/null || echo "unavailable")"
fi

# Quick KPI summary
if curl -sf http://localhost:8001/api/business-analytics/kpi >/dev/null 2>&1; then
    kpi=$(curl -sf http://localhost:8001/api/business-analytics/kpi 2>/dev/null)
    echo "KPIs: $(echo $kpi | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"{d.get('kpis',{}).get('total_users',0)} users | {d.get('kpis',{}).get('active_clients',0)} active | {d.get('kpis',{}).get('conversion_rate',0)}% conversion\")" 2>/dev/null || echo "unavailable")"
fi

# Check AGENTS.md for next steps
grep "^## Next Steps" -A 5 ~/projects/AGENTS.md 2>/dev/null | head -6

echo "---"
