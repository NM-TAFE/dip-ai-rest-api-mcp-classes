1.  Request Schema

```json
{
  "id": "01kh05ckzngeq3sr8sxmykfafx",
  "name": "Qui quis dolor.",
  "description": "Maxime corporis est mollitia qui eligendi consectetur. Nostrum occaecati distinctio hic est.",
  "status": "in_progress",
  "due_date": "2026-02-09",
  "created": {
    "human": "59 minutes ago",
    "string": "2026-02-09T02:58:44+00:00"
  },
  "assigned_to": "01k9nrmg4f9ncqkx02zzvea3km"
}
```

2. Response schema

```json
{
  [
    {
      "id": "01kh05ckzngeq3sr8sxmykfafx",
      "name": "Qui quis dolor.",
      "description": "Maxime corporis est mollitia qui eligendi consectetur. Nostrum occaecati distinctio hic est.",
      "status": "in_progress",
      "due_date": null,
      "created": {
        "human": "59 minutes ago",
        "string": "2026-02-09T02:58:44+00:00"
      },
      "project": {
        "id": "01kh05ckzf2spw59q6cefchmbh",
        "name": "Updated Project Testing October",
        "description": "Sample",
        "created": {
          "human": "59 minutes ago",
          "string": "2026-02-09T02:58:44+00:00"
        }
      },
      "assigned_to": null
    }
  ]
}
```

3. Error schema - comes with a 422 Status Code

```json
{
  "message": "The selected assigned to is invalid.",
  "errors": {
    "assigned_to": ["The selected assigned to is invalid."]
  }
}
```
