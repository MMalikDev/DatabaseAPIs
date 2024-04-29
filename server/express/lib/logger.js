import expressWinston from "express-winston";
import winston from "winston";

const { combine, timestamp, printf, prettyPrint } = winston.format;

function customLogger(opts) {
  return (req, res, next) => {
    console.log(req.method, req.originalUrl);
    next();
  };
}

const customFormat = printf(({ level, message }) => `[${level}]: ${message}`);

const logger = expressWinston.logger({
  transports: [new winston.transports.Console()],
  format: combine(customFormat),
  msg: "{{res.statusCode}} {{req.method}} {{req.url}}\t| {{res.responseTime}}ms",
  level: "info",
  meta: false,
});

const errorLogger = expressWinston.errorLogger({
  transports: [new winston.transports.Console()],
  format: combine(timestamp({ format: "MMM-DD-YYYY HH:mm:ss" }), prettyPrint()),
  msg: "{{res.statusCode}} {{req.method}}  {{req.url}}",
  level: "error",
  meta: false,
});

export { customLogger, errorLogger, logger };
