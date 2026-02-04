import express from 'express';
import { createConnection, Connection } from 'typeorm';
import { AuditEntry } from './models/audit-entry';
import { AuditLogService } from './services/audit-log.service';
import { TaskEventHandler } from './handlers/task-event.handler';
import { AuditQueryService } from './services/audit-query.service';
import { AuditQueryController } from './api/audit-query.controller';
import logger from './utils/logger';

const app = express();
const port = process.env.PORT || 3003;

app.use(express.json({ type: 'application/cloudevents+json' }));
app.use(express.json());

let connection: Connection;

async function initializeApp() {
  try {
    logger.info('Initializing audit service');

    // Connect to database
    connection = await createConnection({
      type: 'postgres',
      host: process.env.DB_HOST || 'localhost',
      port: parseInt(process.env.DB_PORT as string) || 5432,
      username: process.env.DB_USERNAME || 'postgres',
      password: process.env.DB_PASSWORD || 'postgres',
      database: process.env.DB_NAME || 'todo_audit',
      entities: [AuditEntry],
      synchronize: true, // In production, use migrations instead
      logging: false
    });

    logger.info('Connected to database');

    // Initialize services
    const auditLogService = new AuditLogService(connection);
    const auditQueryService = new AuditQueryService(connection);
    const taskEventHandler = new TaskEventHandler(auditLogService);
    const auditQueryController = new AuditQueryController(auditQueryService);

    // Dapr subscription endpoint
    app.get('/dapr/subscribe', (req, res) => {
      logger.info('Dapr subscription endpoint called');
      res.json([
        {
          pubsubname: 'task-pubsub',
          topic: 'task-events',
          route: '/events/task'
        }
      ]);
    });

    // Event handler endpoint for task events
    app.post('/events/task', async (req, res) => {
      try {
        const cloudEvent = req.body;
        logger.info('Received task event', { eventType: cloudEvent.type, taskId: cloudEvent.task?.id });

        // Handle all task events (created, updated, completed, deleted)
        await taskEventHandler.handle(cloudEvent);
        logger.info('Task event handled successfully', { eventType: cloudEvent.type, taskId: cloudEvent.task?.id });

        res.status(200).send('OK');
      } catch (error) {
        logger.error('Error handling task event', { error: (error as Error).message, stack: (error as Error).stack, taskId: req.body?.task?.id });
        res.status(500).send('Error');
      }
    });

    // Audit query endpoints
    app.get('/api/audits/:taskId', async (req, res) => {
      try {
        const taskId = req.params.taskId;
        logger.info('Getting audits by task ID', { taskId });

        const audits = await auditQueryController.getAuditsByTaskId(taskId);
        res.status(200).json(audits);
      } catch (error) {
        logger.error('Error getting audits by task ID', { error: (error as Error).message, stack: (error as Error).stack, taskId: req.params.taskId });
        res.status(500).send('Error retrieving audits');
      }
    });

    app.get('/api/audits', async (req, res) => {
      try {
        const userId = req.query.userId as string;
        const dateFrom = req.query.dateFrom as string;
        const dateTo = req.query.dateTo as string;
        const action = req.query.action as string;

        logger.info('Getting audits by filter', { userId, dateFrom, dateTo, action });

        const audits = await auditQueryController.getAuditsByFilter({
          userId,
          dateFrom: dateFrom ? new Date(dateFrom) : undefined,
          dateTo: dateTo ? new Date(dateTo) : undefined,
          action: action as any
        });

        res.status(200).json(audits);
      } catch (error) {
        logger.error('Error getting audits by filter', { error: (error as Error).message, stack: (error as Error).stack });
        res.status(500).send('Error retrieving audits');
      }
    });

    // Health check
    app.get('/health', (req, res) => {
      logger.info('Health check endpoint called');
      res.status(200).json({ status: 'healthy', timestamp: new Date().toISOString() });
    });

    app.listen(port, () => {
      logger.info('Audit Service started', { port });
    });
  } catch (error) {
    logger.error('Error initializing app', { error: (error as Error).message, stack: (error as Error).stack });
    process.exit(1);
  }
}

initializeApp();