import pytest
from conductor_core.models import Track, Plan, Task, Phase, TaskStatus, TrackStatus

def test_task_model():
    task = Task(description="Test Task", status=TaskStatus.NEW)
    assert task.description == "Test Task"
    assert task.status == TaskStatus.NEW

def test_phase_model():
    task = Task(description="Test Task", status=TaskStatus.NEW)
    phase = Phase(name="Phase 1", tasks=[task])
    assert phase.name == "Phase 1"
    assert len(phase.tasks) == 1

def test_plan_model():
    task = Task(description="Test Task", status=TaskStatus.NEW)
    phase = Phase(name="Phase 1", tasks=[task])
    plan = Plan(phases=[phase])
    assert len(plan.phases) == 1

def test_track_model():
    track = Track(track_id="test_id", description="Test Track", status=TrackStatus.NEW)
    assert track.track_id == "test_id"
    assert track.status == TrackStatus.NEW
