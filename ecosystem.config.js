module.exports = {
  apps: [{
    name: 'prayer-time-app',
    script: 'main.py',
    interpreter: process.env.PYTHON_INTERPRETER || '/home/pi/prayer-time-d/venv/bin/python3',
    cwd: process.env.APP_DIR || '/home/pi/prayer-time-d',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production',
      PYTHONPATH: process.env.APP_DIR || '/home/pi/prayer-time-d'
    },
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    log_file: './logs/combined.log',
    time: true
  }]
};
