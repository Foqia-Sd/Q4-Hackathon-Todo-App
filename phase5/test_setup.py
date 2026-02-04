"""
Test script to validate the Phase 5 Event-Driven Microservices setup
"""

import os
import sys
from pathlib import Path

def test_services_exist():
    """Test that all required services exist"""
    services_dir = Path("services")

    required_services = [
        "chat-api",
        "recurring-task-service",
        "notification-service",
        "audit-service"
    ]

    print("Testing service directories exist...")
    for service in required_services:
        service_path = services_dir / service
        if service_path.exists():
            print(f"[PASS] {service} directory exists")
        else:
            print(f"[FAIL] {service} directory missing")
            return False

    return True

def test_recurring_task_service():
    """Test recurring-task-service structure"""
    service_dir = Path("services/recurring-task-service")

    required_files = [
        "package.json",
        "tsconfig.json",
        "src/index.ts",
        "src/services/recurrence.service.ts",
        "src/services/task-creator.service.ts",
        "src/handlers/task-completed.handler.ts",
        "Dockerfile"
    ]

    print("\nTesting recurring-task-service structure...")
    for file in required_files:
        file_path = service_dir / file
        if file_path.exists():
            print(f"[PASS] {file} exists")
        else:
            print(f"[FAIL] {file} missing")
            return False

    return True

def test_notification_service():
    """Test notification-service structure"""
    service_dir = Path("services/notification-service")

    required_files = [
        "package.json",
        "tsconfig.json",
        "src/index.ts",
        "src/services/reminder.service.ts",
        "src/services/reminder-state.service.ts",
        "src/services/notification-delivery.service.ts",
        "src/handlers/task-created.handler.ts",
        "src/handlers/task-updated.handler.ts",
        "src/handlers/cron-trigger.handler.ts",
        "Dockerfile"
    ]

    print("\nTesting notification-service structure...")
    for file in required_files:
        file_path = service_dir / file
        if file_path.exists():
            print(f"[PASS] {file} exists")
        else:
            print(f"[FAIL] {file} missing")
            return False

    return True

def test_audit_service():
    """Test audit-service structure"""
    service_dir = Path("services/audit-service")

    required_files = [
        "package.json",
        "tsconfig.json",
        "src/index.ts",
        "src/models/audit-entry.ts",
        "src/services/audit-log.service.ts",
        "src/services/audit-query.service.ts",
        "src/handlers/task-event.handler.ts",
        "src/api/audit-query.controller.ts",
        "Dockerfile"
    ]

    print("\nTesting audit-service structure...")
    for file in required_files:
        file_path = service_dir / file
        if file_path.exists():
            print(f"[PASS] {file} exists")
        else:
            print(f"[FAIL] {file} missing")
            return False

    return True

def test_helm_charts():
    """Test Helm chart structure"""
    helm_dir = Path("helm/todo-chatbot")

    required_charts = [
        "charts/recurring-task-service",
        "charts/notification-service",
        "charts/audit-service"
    ]

    print("\nTesting Helm chart structure...")
    for chart in required_charts:
        chart_dir = helm_dir / chart
        if chart_dir.exists():
            print(f"[PASS] {chart} exists")
        else:
            print(f"[FAIL] {chart} missing")
            return False

    # Check umbrella chart
    if (helm_dir / "Chart.yaml").exists():
        print("[PASS] Umbrella Chart.yaml exists")
    else:
        print("[FAIL] Umbrella Chart.yaml missing")
        return False

    if (helm_dir / "values.yaml").exists():
        print("[PASS] Umbrella values.yaml exists")
    else:
        print("[FAIL] Umbrella values.yaml missing")
        return False

    return True

def test_database_migrations():
    """Test database migration files exist"""
    migration_dir = Path("services/chat-api/alembic/versions")

    print("\nTesting database migrations...")
    migration_files = list(migration_dir.glob("*.py"))
    if migration_files:
        print(f"[PASS] Found {len(migration_files)} migration files:")
        for f in migration_files:
            print(f"  - {f.name}")
        return True
    else:
        print("[FAIL] No migration files found")
        return False

def main():
    print("Phase 5 Event-Driven Microservices Setup Validation")
    print("=" * 55)

    tests = [
        test_services_exist,
        test_recurring_task_service,
        test_notification_service,
        test_audit_service,
        test_helm_charts,
        test_database_migrations
    ]

    all_passed = True
    for test in tests:
        if not test():
            all_passed = False

    print(f"\n{'='*55}")
    if all_passed:
        print("[PASS] All tests passed! Phase 5 setup is complete.")
    else:
        print("[FAIL] Some tests failed. Please check the output above.")

    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)