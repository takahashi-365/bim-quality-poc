from scripts.run_pipeline import BASE_DIR, PIPELINE_STEPS, display_path


def test_pipeline_has_expected_number_of_steps() -> None:
    assert len(PIPELINE_STEPS) == 7


def test_all_pipeline_scripts_exist() -> None:
    missing_scripts = [
        step.script for step in PIPELINE_STEPS if not step.script.is_file()
    ]
    assert missing_scripts == []


def test_all_expected_outputs_are_inside_repository() -> None:
    for step in PIPELINE_STEPS:
        for output in step.expected_outputs:
            assert output.is_relative_to(BASE_DIR)


def test_pipeline_step_names_are_unique() -> None:
    names = [step.name for step in PIPELINE_STEPS]
    assert len(names) == len(set(names))


def test_display_path_returns_repository_relative_path() -> None:
    sample_path = BASE_DIR / "src" / "check_bim_quality.py"
    assert display_path(sample_path) == "src/check_bim_quality.py"


def test_pipeline_scripts_are_python_files() -> None:
    assert all(step.script.suffix == ".py" for step in PIPELINE_STEPS)


def test_pipeline_expected_outputs_are_defined() -> None:
    assert all(step.expected_outputs for step in PIPELINE_STEPS)
