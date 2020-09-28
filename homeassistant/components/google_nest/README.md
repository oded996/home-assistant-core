# Google Nest - Device Access

In order to use this integration, you must follow the instructions at
[Device Access: Get Started](https://developers.google.com/nest/device-access/get-started).

# Configuration

Create a configuration entry in your `configuration.yaml` file:
```
google_nest:
  project_id: "your-project-id"
  client_id: "your-client-id"
  client_secret: "your-client-secret"
```

See [Storing secrets](https://www.home-assistant.io/docs/configuration/secrets/)
for best practices on storing passwords and API tokens.

Additionally, make sure to configure your Google Nest OAuth credential with an
allowed redirect url that matches your home assistant url.
TODO: Explain this in more detail with examples.

Restart Home Assistant to load the configuration.

# Authorizing Home Assistant

To give Home Assistant access, go through *Configuration > Integrations* and add
*Google Nest Device Access*.  This will go through the OAuth approval flow
where you have to give access to Home Assistant.
TODO: Describe which options need to be enabled and which do not.

# Work Plan

This section contains a TODO list of items to complete for this integration.

  * [Done] OAuth
  * Create entities for devices
  * Modify to use pull with pubsub events
  * Allow "set" commands
