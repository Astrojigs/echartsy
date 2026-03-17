"""Tests for echartsy._config global configuration."""
from __future__ import annotations

import pytest

import echartsy as ec
from echartsy._config import (
    config,
    get_adaptive,
    get_engine,
    get_overlap_warnings,
)


class TestDefaultConfig:
    def test_default_engine(self):
        assert get_engine() == "python"

    def test_adaptive_default(self):
        assert get_adaptive() == "auto"

    def test_overlap_warnings_default(self):
        assert get_overlap_warnings() is True


class TestConfigEngine:
    def test_config_jupyter(self):
        config(engine="jupyter")
        assert get_engine() == "jupyter"

    def test_config_streamlit(self):
        config(engine="streamlit")
        assert get_engine() == "streamlit"

    def test_config_python(self):
        config(engine="python")
        assert get_engine() == "python"

    def test_config_invalid_engine(self):
        with pytest.raises(ValueError, match="Unknown engine"):
            config(engine="invalid_engine")


class TestConfigAdaptive:
    def test_adaptive_dark(self):
        config(engine="python", adaptive="dark")
        assert get_adaptive() == "dark"

    def test_adaptive_light(self):
        config(engine="python", adaptive="light")
        assert get_adaptive() == "light"

    def test_adaptive_auto(self):
        config(engine="python", adaptive="auto")
        assert get_adaptive() == "auto"

    def test_adaptive_invalid(self):
        with pytest.raises(ValueError, match="Unknown adaptive mode"):
            config(engine="python", adaptive="neon")


class TestConfigOverlapWarnings:
    def test_overlap_warnings_off(self):
        config(engine="python", overlap_warnings=False)
        assert get_overlap_warnings() is False

    def test_overlap_warnings_on(self):
        config(engine="python", overlap_warnings=True)
        assert get_overlap_warnings() is True

    def test_overlap_warnings_not_changed_when_none(self):
        config(engine="python", overlap_warnings=False)
        assert get_overlap_warnings() is False
        # Calling config without overlap_warnings should not change it
        config(engine="python")
        assert get_overlap_warnings() is False


class TestConfigStateIsolation:
    def test_config_state_isolation(self):
        """Autouse fixture resets state between tests.

        If this test runs after any config mutation, the defaults should
        still be restored by the fixture.
        """
        assert get_engine() == "python"
        assert get_adaptive() == "auto"
        assert get_overlap_warnings() is True

    def test_config_mutation_is_local(self):
        """Mutate config; the next test should see defaults again."""
        config(engine="streamlit", adaptive="dark", overlap_warnings=False)
        assert get_engine() == "streamlit"
        assert get_adaptive() == "dark"
        assert get_overlap_warnings() is False

    def test_config_reverted_after_mutation(self):
        """Verify the fixture reverted the mutation from the previous test."""
        assert get_engine() == "python"
        assert get_adaptive() == "auto"
        assert get_overlap_warnings() is True
