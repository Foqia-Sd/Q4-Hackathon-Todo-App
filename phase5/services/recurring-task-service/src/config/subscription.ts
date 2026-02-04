// Dapr subscription configuration for recurring-task-service
// This would typically be configured via the /dapr/subscribe endpoint

export interface DaprSubscription {
  pubsubname: string;
  topic: string;
  route: string;
}

export interface SubscriptionConfig {
  subscriptions: DaprSubscription[];
}

// This configuration is typically handled by the Dapr sidecar via the /dapr/subscribe endpoint
// The actual subscription happens in the main index.ts file
export const subscriptionConfig: SubscriptionConfig = {
  subscriptions: [
    {
      pubsubname: 'task-pubsub',
      topic: 'task-events',
      route: '/events/task'
    }
  ]
};