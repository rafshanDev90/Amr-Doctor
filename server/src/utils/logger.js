const fs = require('fs');
const path = require('path');

const logDir = path.join(__dirname, '../../logs');
if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir);
}

const logFile = path.join(logDir, 'server.log');

const logger = {
    info: (message) => {
        const log = `${new Date().toISOString()} [INFO] ${message}\n`;
        console.log(log.trim());
        fs.appendFileSync(logFile, log);
    },
    error: (message, error) => {
        const log = `${new Date().toISOString()} [ERROR] ${message} ${error ? error.stack || error : ''}\n`;
        console.error(log.trim());
        fs.appendFileSync(logFile, log);
    },
    debug: (message) => {
        if (process.env.NODE_ENV !== 'production') {
            const log = `${new Date().toISOString()} [DEBUG] ${message}\n`;
            console.log(log.trim());
            fs.appendFileSync(logFile, log);
        }
    }
};

module.exports = logger;
