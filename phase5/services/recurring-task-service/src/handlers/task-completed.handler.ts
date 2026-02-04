import { RecurrenceService } from '../services/recurrence.service';
import { TaskCreatorService } from '../services/task-creator.service';

export class TaskCompletedHandler {
  private recurrenceService: RecurrenceService;
  private taskCreatorService: TaskCreatorService;

  constructor(
    recurrenceService: RecurrenceService,
    taskCreatorService: TaskCreatorService
  ) {
    this.recurrenceService = recurrenceService;
    this.taskCreatorService = taskCreatorService;
  }

  /**
   * Handles the TaskCompleted event and creates the next occurrence if applicable
   * @param cloudEvent CloudEvent containing the task completion data
   */
  async handle(cloudEvent: any): Promise<void> {
    console.log('Handling TaskCompleted event:', cloudEvent);

    try {
      const eventData = cloudEvent.data;

      // Extract task data from the event
      const task = eventData.task;
      const userId = eventData.userId;

      // Check if the task has a recurrence rule
      if (!task.recurrence_rule) {
        console.log(`Task ${task.id} does not have a recurrence rule, skipping`);
        return;
      }

      // Validate the recurrence rule
      if (!this.recurrenceService.validateRecurrenceRule(task.recurrence_rule)) {
        console.error(`Invalid recurrence rule for task ${task.id}: ${task.recurrence_rule}`);
        return;
      }

      // Calculate the next occurrence date
      const lastOccurrence = task.completed_at ? new Date(task.completed_at) : new Date(task.updated_at);
      const nextOccurrenceDate = this.recurrenceService.calculateNextOccurrence(
        task.recurrence_rule,
        lastOccurrence
      );

      if (!nextOccurrenceDate) {
        console.log(`No further occurrences for task ${task.id}, recurrence rule exhausted`);
        return;
      }

      console.log(`Calculated next occurrence for task ${task.id} on ${nextOccurrenceDate}`);

      // Create the next occurrence of the task
      const nextTask = this.recurrenceService.createNextTaskFromRecurrence(task, nextOccurrenceDate);

      // Create the new task via the Chat API
      const createdTask = await this.taskCreatorService.createTask(nextTask, userId);

      if (createdTask) {
        console.log(`Successfully created next occurrence of task ${task.id} as new task ${createdTask.id}`);
      } else {
        console.error(`Failed to create next occurrence of task ${task.id}`);
      }
    } catch (error) {
      console.error('Error in TaskCompletedHandler.handle():', error);
      throw error; // Re-throw to be caught by the main event handler
    }
  }
}