import express from 'express';
import { DaprServer, DaprClient } from '@dapr/dapr';
import { RecurrenceService } from './services/recurrence.service';
import { TaskCreatorService } from './services/task-creator.service';
import { TaskCompletedHandler } from './handlers/task-completed.handler';
import logger from './utils/logger';

// Define interfaces for type safety
interface TaskData {
  taskId: string;
  userId: string;
  action: string;
  task: {
    id: string;
    title: string;
    description?: string;
    recurrence_rule?: string;
    due_date?: string;
    priority?: string;
    status: string;
    user_id: string;
    created_at: string;
    updated_at: string;
  };
}

const app = express();
app.use(express.json({ type: 'application/cloudevents+json' }));
app.use(express.json());

const daprPort = process.env.DAPR_HTTP_PORT || '3500';
const serverHost = '0.0.0.0';
const serverPort = process.env.SERVER_PORT || '3001';

// Initialize services
const recurrenceService = new RecurrenceService();
const taskCreatorService = new TaskCreatorService(process.env.CHAT_API_URL || 'http://chat-api:8000');
const taskCompletedHandler = new TaskCompletedHandler(recurrenceService, taskCreatorService);

// Create Dapr Server
const server = new DaprServer({
  serverHost,
  serverPort: parseInt(serverPort as string),
  clientOptions: {
    daprHost: 'localhost',
    daprPort: parseInt(daprPort as string),
  },
});

// Define Dapr subscription for task events
const subscribeHandler = async () => {
  return [
    {
      pubsubname: 'task-pubsub',
      topic: 'task-events',
      route: '/events/task'
    }
  ];
};

// Event handler for task events
const handleTaskEvent = async (data: any) => {
  logger.info('Received task event', { eventType: data.type, taskId: data.task?.id });

  try {
    // Only handle TaskCompleted events
    if (data.type === 'com.todo.task.completed') {
      logger.info('Processing task completion event', { taskId: data.task?.id });
      await taskCompletedHandler.handle(data);
      logger.info('Successfully processed task completion event', { taskId: data.task?.id });
    }

    return { status: 'SUCCESS' };
  } catch (error) {
    logger.error('Error handling task event', { error: (error as Error).message, stack: (error as Error).stack, taskId: data.task?.id });
    return { status: 'ERROR', message: (error as Error).message };
  }
};

// Start the server
server.start().then(async () => {
  logger.info(`Dapr server started`, { host: serverHost, port: serverPort });

  // Subscribe to task events
  await server.pubsub.subscribe('task-pubsub', 'task-events', handleTaskEvent);
  logger.info('Subscribed to task events', { pubsubName: 'task-pubsub', topic: 'task-events' });

  // Set up the subscription endpoint for Dapr to discover
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

  // Health check endpoint
  app.get('/health', (req, res) => {
    logger.info('Health check endpoint called');
    res.status(200).json({ status: 'healthy', timestamp: new Date().toISOString() });
  });

  // Additional endpoint for direct HTTP calls (fallback)
  app.post('/events/task', async (req, res) => {
    try {
      const cloudEvent = req.body;
      logger.info('Direct HTTP event received', { eventType: cloudEvent.type, taskId: cloudEvent.task?.id });

      if (cloudEvent.type === 'com.todo.task.completed') {
        logger.info('Processing task completion via direct HTTP call', { taskId: cloudEvent.task?.id });
        await taskCompletedHandler.handle(cloudEvent);
      }

      res.status(200).send({ status: 'SUCCESS' });
    } catch (error) {
      logger.error('Error handling direct task event', { error: (error as Error).message, stack: (error as Error).stack });
      res.status(500).send({ status: 'ERROR', message: (error as Error).message });
    }
  });

  app.listen(parseInt(serverPort as string), () => {
    logger.info(`Recurring Task Service HTTP server listening`, { port: serverPort });
  });
}).catch((err) => {
  logger.error('Error starting server', { error: (err as Error).message, stack: (err as Error).stack });
});