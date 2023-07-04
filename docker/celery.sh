#!/bin/bash
celery -A app.tasks.celery_app:celery worker -l INFO

