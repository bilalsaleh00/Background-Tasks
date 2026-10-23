import time
import uuid

from fastapi import APIRouter, BackgroundTasks, HTTPException


router = APIRouter()

report_store: dict[str, dict] = {}
notification_log: list[dict] = []


def generate_report(
    report_id: str,
    report_type: str,
    rows: int
) -> None:
    report_store[report_id]["status"] = "processing"

    time.sleep(2)

    report_store[report_id]["status"] = "complete"
    report_store[report_id]["result"] = {
        "report_type": report_type,
        "rows_processed": rows
    }


def send_notification(
    recipient: str,
    message: str
) -> None:
    time.sleep(1)

    notification_log.append({
        "recipient": recipient,
        "message": message
    })


@router.post("/")
def create_report(
    background_tasks: BackgroundTasks,
    report_type: str = "sales",
    rows: int = 100
):
    report_id = str(uuid.uuid4())

    report_store[report_id] = {
        "status": "pending"
    }

    background_tasks.add_task(
        generate_report,
        report_id,
        report_type,
        rows
    )

    return {
        "report_id": report_id,
        "status": "pending"
    }


@router.get("/notifications/log")
def get_notification_log():
    return {
        "notifications": notification_log
    }


@router.post("/notifications")
def create_notification(
    background_tasks: BackgroundTasks,
    recipient: str = "user@example.com",
    message: str = "Hello!"
):
    background_tasks.add_task(
        send_notification,
        recipient,
        message
    )

    return {
        "status": "queued",
        "recipient": recipient
    }


@router.get("/{report_id}")
def get_report_status(report_id: str):
    if report_id not in report_store:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    return report_store[report_id]