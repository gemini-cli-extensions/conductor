import pytest
from conductor_core.models import Track, Plan, Task, Phase

def test_task_model():
    task = Task(description="Test Task", status="new")
    assert task.description == "Test Task"
    assert task.status == "new"

def test_phase_model():
    task = Task(description="Test Task", status="new")
    phase = Phase(name="Phase 1", tasks=[task])
    assert phase.name == "Phase 1"
    assert len(phase.tasks) == 1

def test_plan_model():
    task = Task(description="Test Task", status="new")
    phase = Phase(name="Phase 1", tasks=[task])
    plan = Plan(phases=[phase])
    assert len(plan.phases) == 1

def test_track_model():
    track = Track(track_id="test_id", description="Test Track", status="new")
    assert track.track_id == "test_id"
    assert track.status == "new"
