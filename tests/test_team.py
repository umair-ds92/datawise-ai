"""
Tests for Team Orchestration
"""

import pytest
from config.openai_model_client import get_model_client
from config.docker_utils import getDockerCommandLineExecutor
from team.analyzer_gpt import (
    create_basic_team,
    create_visualization_team,
    create_statistics_team,
)
from team.selector import create_smart_selector
from team.termination_conditions import create_standard_termination
from team.handoffs import create_handoff_pattern


class TestTeamCreation:
    """Test team creation functions"""
    
    def test_basic_team_creation(self):
        """Test creating basic two-agent team"""
        model_client = get_model_client()
        docker = getDockerCommandLineExecutor()
        
        team = create_basic_team(docker, model_client)
        
        assert team is not None
        assert len(team._participants) == 2
        assert hasattr(team, '_termination_condition')
    
    def test_visualization_team_creation(self):
        """Test creating visualization-focused team"""
        model_client = get_model_client()
        docker = getDockerCommandLineExecutor()
        
        team = create_visualization_team(docker, model_client)
        
        assert team is not None
        assert len(team._participants) == 3
    
    def test_statistics_team_creation(self):
        """Test creating statistics-focused team"""
        model_client = get_model_client()
        docker = getDockerCommandLineExecutor()
        
        team = create_statistics_team(docker, model_client)
        
        assert team is not None
        assert len(team._participants) == 3


class TestSelectors:
    """Test agent selector strategies"""
    
    def test_keyword_selector(self):
        """Test keyword-based selector creation"""
        selector = create_smart_selector('keyword')
        
        assert selector is not None
        assert hasattr(selector, 'select_by_keywords')
    
    def test_round_robin_selector(self):
        """Test round-robin selector creation"""
        selector = create_smart_selector('round_robin')
        
        assert selector is not None
        assert hasattr(selector, 'get_next_agent')
    
    def test_priority_selector(self):
        """Test priority-based selector creation"""
        selector = create_smart_selector('priority')
        
        assert selector is not None
        assert hasattr(selector, 'get_next_agent_name')


class TestTerminationConditions:
    """Test termination conditions"""
    
    def test_standard_termination(self):
        """Test standard termination condition"""
        termination = create_standard_termination()
        
        assert termination is not None
    
    def test_standard_termination_with_custom_rounds(self):
        """Test standard termination with custom max rounds"""
        termination = create_standard_termination(max_rounds=20)
        
        assert termination is not None


class TestHandoffPatterns:
    """Test handoff pattern creation"""
    
    def test_simple_pattern(self):
        """Test simple workflow pattern"""
        pattern = create_handoff_pattern('simple')
        
        assert isinstance(pattern, list)
        assert len(pattern) == 2
        assert 'Data_Analyzer' in pattern
        assert 'Code_Executor' in pattern
    
    def test_visualization_pattern(self):
        """Test visualization workflow pattern"""
        pattern = create_handoff_pattern('visualization')
        
        assert isinstance(pattern, list)
        assert len(pattern) == 3
        assert 'Visualization_Specialist' in pattern
    
    def test_statistical_pattern(self):
        """Test statistical workflow pattern"""
        pattern = create_handoff_pattern('statistical')
        
        assert isinstance(pattern, list)
        assert 'Statistics_Analyst' in pattern
    
    def test_comprehensive_pattern(self):
        """Test comprehensive workflow pattern"""
        pattern = create_handoff_pattern('comprehensive')
        
        assert isinstance(pattern, list)
        assert len(pattern) == 4


if __name__ == "__main__":
    """Run tests directly"""
    print("🧪 Testing Team Orchestration...")
    
    try:
        test_team = TestTeamCreation()
        test_team.test_basic_team_creation()
        print("✅ Basic team creation works")
        
        test_team.test_visualization_team_creation()
        print("✅ Visualization team creation works")
        
        test_team.test_statistics_team_creation()
        print("✅ Statistics team creation works")
        
        test_selectors = TestSelectors()
        test_selectors.test_keyword_selector()
        test_selectors.test_round_robin_selector()
        test_selectors.test_priority_selector()
        print("✅ All selectors work")
        
        test_termination = TestTerminationConditions()
        test_termination.test_standard_termination()
        print("✅ Termination conditions work")
        
        test_handoffs = TestHandoffPatterns()
        test_handoffs.test_simple_pattern()
        test_handoffs.test_visualization_pattern()
        test_handoffs.test_statistical_pattern()
        test_handoffs.test_comprehensive_pattern()
        print("✅ All handoff patterns work")
        
        print("\n✅ All team orchestration tests passed!")
        print("\nTo run with pytest: pytest tests/test_team.py -v")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)