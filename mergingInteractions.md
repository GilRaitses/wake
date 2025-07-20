When you return to work with your teammate, your immediate steps can flow cleanly if you treat this like a merge pipeline with specific responsibilities and clear targets. Here's a walkthrough of what needs to happen, both technically and conceptually:

First, for your teammate:

Ask her to commit and push all her latest work on the mapping framework to her feature branch. If she’s using Cursor, that’s just saving her local changes, staging, committing with a clear message, and then pushing. She can push directly to her feature branch (`map-feature`, `feature/maps`, or whatever naming convention you're using).

Once that’s done, she should open a **pull request (PR)** to merge her feature branch into the main branch. This PR lets you review, comment on, and approve the changes before they get folded into your deployment stream. Think of it as a "proposal to integrate code" rather than a merge action itself. You’ll be the one to review and approve it.

After you approve and merge the PR into `main`, you trigger your deployment flow. If your Firebase app auto-deploys from `main`, you’re good. If not, you’ll have to run your build/deploy commands to push the updated app bundle (now including the mapping framework) to Firebase Hosting.

Now for the agent side:

Your agent needs to become aware of the map configuration objects—these might be stored in Firebase (like Firestore collections per user or per session) or dynamically generated from BigQuery forecasts. So define a clean interface for the agent to read or receive map configuration data. This can be a function like:

`getMapConfig(timeRange, placeIds) → {geoJSON, mapOptions, overlays, UIStates}`

Then, you let the agent formulate its response using a structure like this:

1. **Forecast Overview:** A text-based summary drawn from historical data, current probabilities, and environmental context.
2. **Interactive Timeline:** A UI module that references temporal slices (like “next 4 hours” in 15-min intervals), each linked to a visual forecast representation.
3. **Configurable Map:** Auto-centered on location(s) with predictive overlays and toggleable controls (species layer, risk factor, wave conditions, etc).
4. **Plan/Export Options:** Buttons or gestures to save this config to the user’s trip journal, add notes or images (from camera roll), or export/share it.

You’re building an interaction style where the agent doesn’t just respond in words—it **constructs a data-object-guided interface fragment**. So the theory behind the user experience is not just conversational AI, but **agent-driven spatial planning**. The model is being tasked with generating scaffolding for decision-making, not just content.

To move forward now:

When you return:

* Ask her to push her map changes and create a pull request.
* Merge it into `main` once you’ve reviewed it.
* Deploy your Firebase app if you’re not using CI/CD.
* Refactor your agent’s code to include map configuration reading and UI scaffold building.
* Define JSON-like schemas for forecast payloads, timeline objects, and saved events.

And zooming out—your system will be best served by aligning map interactivity with the agent’s latent knowledge over both **spatial correlations** and **temporal coherence**. This gives your forecasting system a scaffolding logic: map features are canvases, and the forecasts paint behavior over them. Responses become dynamic experiences. Let me know if you want that scaffolding logic represented visually or structured as a schema.


For the agentic feature

Your Gemma3 agent must output a JSON object that exactly matches the schema shown below. It must include a forecastOverview string that summarizes orca sighting probabilities and context. It must include timeSeries as an array of entries each containing timestamp probability and summary. It must include mapConfig as an object defining center with lat and lng zoomLevel as an integer and overlays as an array of geoData layers. It must include actions as an array of objects each containing type label and optional payload. Use this schema exactly so the frontend can render the interface automatically

```json
{
  "type": "object",
  "properties": {
    "forecastOverview": { "type": "string" },
    "timeSeries": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "timestamp": { "type": "string", "format": "date-time" },
          "probability": { "type": "number" },
          "summary": { "type": "string" }
        },
        "required": ["timestamp", "probability", "summary"]
      }
    },
    "mapConfig": {
      "type": "object",
      "properties": {
        "center": {
          "type": "object",
          "properties": {
            "lat": { "type": "number" },
            "lng": { "type": "number" }
          },
          "required": ["lat", "lng"]
        },
        "zoomLevel": { "type": "integer" },
        "overlays": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "type": { "type": "string" },
              "data": { "type": "object" }
            },
            "required": ["type", "data"]
          }
        }
      },
      "required": ["center", "zoomLevel", "overlays"]
    },
    "actions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "type": { "type": "string" },
          "label": { "type": "string" },
          "payload": { "type": ["object", "null"] }
        },
        "required": ["type", "label"]
      }
    }
  },
  "required": ["forecastOverview", "timeSeries", "mapConfig", "actions"]
}
```

For the map feature team

Implement a module that follows our data pipeline and adheres to the schema shown below. Raw sightings arrive in Firestore under the sightings collection. A BigQuery ml job consumes that data and writes forecastRecords to Firestore under forecastConfigs. When code merges into main the build system runs npm run build then firebase deploy to update hosting. The module must read forecastConfigs and produce mapConfig objects that match the schema. It must also include pipeline metadata in each object with dataSources array transformations array and a deployment object naming triggerBranch buildCommand and deployCommand. Following this schema ensures that forecasts appear on the map automatically after each deployment

```json
{
  "type": "object",
  "properties": {
    "mapConfig": {
      "type": "object",
      "properties": {
        "center": { "type": "object" },
        "zoomLevel": { "type": "integer" },
        "overlays": { "type": "array" }
      },
      "required": ["center", "zoomLevel", "overlays"]
    },
    "pipeline": {
      "type": "object",
      "properties": {
        "dataSources": { "type": "array", "items": { "type": "string" } },
        "transformations": { "type": "array", "items": { "type": "string" } },
        "deployment": {
          "type": "object",
          "properties": {
            "triggerBranch": { "type": "string" },
            "buildCommand": { "type": "string" },
            "deployCommand": { "type": "string" }
          },
          "required": ["triggerBranch", "buildCommand", "deployCommand"]
        }
      },
      "required": ["dataSources", "transformations", "deployment"]
    }
  },
  "required": ["mapConfig", "pipeline"]
}
```
