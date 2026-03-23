module.exports = {
  apps: [
    {
      name: 'deploy-Steckbrief-Manager',
      script: 'C:/APPS/Steckbrief-Manager/.venv/Scripts/python.exe',
      args: 'app.py',
      interpreter: 'none',
      cwd: 'C:/APPS/Steckbrief-Manager',
      watch: false,
      autorestart: true,
      max_restarts: 10,
      restart_delay: 5000,
      min_uptime: '10s',
      kill_timeout: 10000,
      windowsHide: true,
      treekill: true,
      env: {
        PORT: '6111',
        PYTHONUNBUFFERED: '1',
        PYTHONIOENCODING: 'utf-8',
        PYTHONUTF8: '1'
      },
      error_file: 'C:/APPS/Steckbrief-Manager/logs/pm2-error.log',
      out_file: 'C:/APPS/Steckbrief-Manager/logs/pm2-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true
    },
    {
      name: 'steckbrief-api',
      script: 'C:/APPS/Steckbrief-Manager/.venv/Scripts/python.exe',
      args: 'api_server.py',
      interpreter: 'none',
      cwd: 'C:/APPS/Steckbrief-Manager',
      watch: false,
      autorestart: true,
      max_restarts: 10,
      restart_delay: 5000,
      min_uptime: '10s',
      kill_timeout: 10000,
      windowsHide: true,
      treekill: true,
      env: {
        PYTHONUNBUFFERED: '1',
        PYTHONIOENCODING: 'utf-8',
        PYTHONUTF8: '1'
      },
      error_file: 'C:/APPS/Steckbrief-Manager/logs/api-error.log',
      out_file: 'C:/APPS/Steckbrief-Manager/logs/api-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true
    }
  ]
};
