# Prometheus Custom Service Discovery

Trigo’s solution includes proprietary sensors based on embedded microcontrollers running bare-metal software under tight resource limits (low CPU, low memory). Those devices cannot run modern tooling such as Docker or Consul agents, but they do expose an HTTP server with a dedicated metrics endpoint.

Store operators can change which sensors participate, so the active inventory updates frequently.

In this exercise, you will implement a custom service discovery mechanism for [Prometheus](https://prometheus.io/) so that Prometheus keeps monitoring the correct set of sensors as configuration changes.

# Exercise

The [inventory service](./inventory_server/) exposes an HTTP endpoint that returns the list of hosts for the currently active sensors.

For example:

```
curl -XGET http://localhost:1337/inventory
```

returns the hostnames to monitor:

```
[
    "sensor_1",
    "sensor_2",
    "sensor_12",
    ...
]
```

# Requirements

## Goals

* **Service discovery:** Implement custom Prometheus service discovery that queries the inventory endpoint and produces target groups for those sensors.
* **Runtime stack:** Provide a minimal Docker Compose file *or* Helm chart that runs the full stack, with Prometheus listening on HTTP **TCP 9090** and configured to scrape the sensor targets via your discovery.

Note that the hosts provided by the inventory are dummy, and that's fine if your Prometheus isn't able to connect to them. The goal is just to add them as targets.

## Quality

* Keep the solution clear and maintainable, follow sensible best practices, and prefer current stable versions of dependencies where practical.

## Constraints

* Do not modify the inventory service code.
* Complete the exercise within **two hours** (maximum).

## Submission

* Fork this repository, push your solution, open a pull request to our repository, and send us a link.

## Tools, references, and questions

* You may use any language, framework, library, or code snippets you find helpful.
* You may use any source of information, including AI tools. Please note that we can identify submissions generated with AI, and in such cases, stricter evaluation criteria may be applied.
* If anything is unclear, ask us — we are happy to help.

Solution README by Yuval Graiber:
# Prometheus Custom Service Discovery

## Overview
This project implements a custom service discovery mechanism for Prometheus, designed to monitor a dynamic set of proprietary sensors. Since these sensors are resource-constrained and cannot run modern agents, this solution uses an **adapter-based** approach.

## Architecture
The system consists of three main components:
1. **Inventory Server**: A mock service that provides the current list of active sensors via an HTTP API.
2. **Discovery Adapter**: A Python-based microservice that periodically fetches the inventory and updates a shared JSON file.
3. **Prometheus**: Configured with `file_sd_configs` to watch the shared JSON file and scrape the sensors dynamically.

## Setup & Deployment
To deploy the entire monitoring stack, use Docker Compose:

Bash:
docker-compose up -d --build

The adapter polls the inventory_server every 30 seconds
It formats the sensor list into the Prometheus-compatible JSON structure:
[
  {
    "targets": ["sensor_0:80", "sensor_1:80", "..."]
  }
]
The file is mapped via a Docker volume to the Prometheus container, enabling real-time service discovery updates without restarting Prometheus.

Monitoring
You can access the Prometheus dashboard at: http://localhost:9090
Navigate to Status > Targets to view the dynamically discovered sensors.
Note: As these sensors are simulated, they will appear as DOWN in the dashboard, which confirms the discovery mechanism is successfully reaching them.