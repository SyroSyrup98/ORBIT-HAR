# ORBIT-HAR

**Onboard Recognition & Behavioural Intelligence for Tasks**

An onboard AI-assisted experiment monitoring system designed for
Human Activity Recognition (HAR) during space-based experiments.

## Problem

In space missions, communication delays and restricted bandwidth can
make continuous ground-based supervision of astronauts impractical.

ORBIT-HAR aims to provide a local AI assistant that can:

- Monitor astronaut activities through onboard camera feeds
- Detect relevant objects and human interactions
- Recognize activities involved in a predefined experiment
- Validate whether experiment steps are performed in the correct order
- Detect skipped or out-of-sequence actions
- Provide real-time guidance and deviation alerts
- Maintain lightweight timestamped experiment logs
- Operate locally without requiring continuous cloud connectivity

## Objective

The goal is to build a working proof-of-concept of an onboard
experiment-execution assistant.

The initial prototype will focus on:

> Camera → Human Activity Recognition → Object/Interaction Detection
> → Experiment State Validation → Guidance/Alert → Logging

## Current Scope

The initial prototype will use:

- One fixed camera
- One predefined experiment
- A limited set of activities
- A limited set of experiment objects
- Local AI inference
- A local web-based monitoring interface

The system will be designed so that additional experiments,
activities, objects, and models can be added later.

## System Architecture

```text
                    ┌──────────────┐
                    │    Camera    │
                    └──────┬───────┘
                           │
                           ▼
                ┌────────────────────┐
                │     Perception     │
                │                    │
                │ Object Detection  │
                │ Pose / Hand       │
                │ Detection         │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Activity &         │
                │ Interaction       │
                │ Recognition       │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Experiment State  │
                │     Machine       │
                └─────────┬──────────┘
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
          Guidance     Alerts       Logging
              │           │           │
              └───────────┼───────────┘
                          ▼
                ┌────────────────────┐
                │   ORBIT-HAR UI     │
                │   Mission Console  │
                └────────────────────┘