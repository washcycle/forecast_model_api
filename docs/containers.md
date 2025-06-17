# Best Practices for Python Containers

- Multistage builds to reduce container size.

| Environment Variable      | Purpose                                                                              |
| ------------------------- | ------------------------------------------------------------------------------------ |
| `PYTHONUNBUFFERED`        | Sends output to stdout immediately to the terminal, useful for logging and debugging |
| `PYTHONDONTWRITEBYTECODE` | Prevents python from writing .pyc files, saves disk space                            |

