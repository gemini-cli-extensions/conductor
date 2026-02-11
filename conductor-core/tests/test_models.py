from conductor_core.models import Phase, Plan, Task, TaskStatus, Track, TrackStatus


def test_task_model():
    task = Task(description="Test Task", status=TaskStatus.PENDING)
    assert task.description == "Test Task"
    assert task.status == TaskStatus.PENDING


def test_phase_model():
    task = Task(description="Test Task", status=TaskStatus.PENDING)
    phase = Phase(name="Phase 1", tasks=[task])
    assert phase.name == "Phase 1"
    assert len(phase.tasks) == 1


def test_plan_model():
    task = Task(description="Test Task", status=TaskStatus.PENDING)
    phase = Phase(name="Phase 1", tasks=[task])
    plan = Plan(phases=[phase])
    assert len(plan.phases) == 1


def test_track_model():
    track = Track(track_id="test_id", description="Test Track", status=TrackStatus.NEW)
    assert track.track_id == "test_id"
    assert track.status == TrackStatus.NEW
