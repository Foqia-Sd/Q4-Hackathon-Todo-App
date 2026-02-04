import express from 'express';
import cron from 'node-cron';
import { ReminderService } from './services/reminder.service';
import { ReminderStateService } from './services/reminder-state.service';
import { NotificationDeliveryService } from './services/notification-delivery.service';
import { TaskCreatedHandler } from './handlers/task-created.handler';
import { TaskUpdatedHandler } from './handlers/task-updated.handler';
import { CronTriggerHandler } from './handlers/cron-trigger.handler';
import logger from './utils/logger';

const app = express();
const port = process.env.PORT || 3002;

app.use(express.json({ type: 'application/cloudevents+json' }));
app.use(express.json());

// Initialize services
const reminderStateService = new ReminderStateService(process.env.DAPR_STATE_STORE || 'statestore');
const reminderService = new ReminderService(reminderStateService);
const notificationDeliveryService = new NotificationDeliveryService();
const taskCreatedHandler = new TaskCreatedHandler(reminderService);
const taskUpdatedHandler = new TaskUpdatedHandler(reminderService);
const cronTriggerHandler = new CronTriggerHandler(reminderService, notificationDeliveryService);

// Set up cron job to check for reminders every minute
cron.schedule('* * * * *', async () => {
  logger.info('Checking for due reminders');
  try {
    await cronTriggerHandler.handle();
    logger.info('Reminder check completed successfully');
  } catch (error) {
    logger.error('Error checking for due reminders', { error: (error as Error).message, stack: (error as Error).stack });
  }
});

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

    if (cloudEvent.type === 'com.todo.task.created') {
      logger.info('Processing task creation event', { taskId: cloudEvent.task?.id });
      await taskCreatedHandler.handle(cloudEvent);
    } else if (cloudEvent.type === 'com.todo.task.updated') {
      logger.info('Processing task update event', { taskId: cloudEvent.task?.id });
      await taskUpdatedHandler.handle(cloudEvent);
    }

    res.status(200).send('OK');
  } catch (error) {
    logger.error('Error handling task event', { error: (error as Error).message, stack: (error as Error).stack });
    res.status(500).send('Error');
  }
});

// Cron trigger endpoint (called by Dapr cron binding)
app.post('/check-reminders', async (req, res) => {
  try {
    logger.info('Cron trigger received');
    await cronTriggerHandler.handle();
    res.status(200).send({ status: 'SUCCESS' });
  } catch (error) {
    logger.error('Error in cron trigger', { error: (error as Error).message, stack: (error as Error).stack });
    res.status(500).send({ status: 'ERROR', message: (error as Error).message });
  }
});

// Health check
app.get('/health', (req, res) => {
  logger.info('Health check endpoint called');
  res.status(200).json({ status: 'healthy', timestamp: new Date().toISOString() });
});

app.listen(port, () => {
  logger.info('Notification Service started', { port });
});