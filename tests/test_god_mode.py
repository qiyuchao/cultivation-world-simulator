"""
Tests for God Mode functionality
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.classes.god_mode import GodMode, GodAbility
from src.classes.world import World
from src.classes.avatar import Avatar


@pytest.fixture
def mock_world():
    """Create a mock world for testing"""
    world = Mock(spec=World)
    world.month_stamp = Mock()
    world.month_stamp.__str__ = Mock(return_value="Year 100, Month 1")
    world.avatar_manager = Mock()
    world.avatar_manager.avatars = {}
    world.event_manager = Mock()
    world.map = Mock()
    world.map.tiles = {}
    return world


@pytest.fixture
def mock_avatar():
    """Create a mock avatar for testing"""
    avatar = Mock(spec=Avatar)
    avatar.id = "test_avatar_1"
    avatar.name = "测试修士"
    avatar.cultivation = Mock()
    avatar.cultivation.realm = "筑基期"
    avatar.cultivation.exp = 1000
    avatar.sect = Mock()
    avatar.sect.name = "测试宗门"
    avatar.persona = Mock()
    avatar.persona.personas = []
    avatar.hp = Mock()
    avatar.hp.max = 1000
    avatar.hp.current = 1000
    avatar.hp.damage = Mock()
    avatar.hp.heal = Mock()
    avatar.magic_stone = Mock()
    avatar.magic_stone.add = Mock()
    return avatar


def test_god_mode_initialization(mock_world):
    """Test God Mode initialization"""
    god_mode = GodMode(mock_world)
    
    assert god_mode.world == mock_world
    assert god_mode.action_history == []


def test_record_action(mock_world):
    """Test recording God actions"""
    god_mode = GodMode(mock_world)
    
    god_mode.record_action(
        ability=GodAbility.GRANT_FORTUNE,
        description="Test action",
        target_ids=["avatar1"],
        result="Success",
        ai_used=False
    )
    
    assert len(god_mode.action_history) == 1
    action = god_mode.action_history[0]
    assert action.ability == GodAbility.GRANT_FORTUNE
    assert action.description == "Test action"
    assert action.target_ids == ["avatar1"]
    assert action.result == "Success"
    assert action.ai_used == False


def test_get_action_history(mock_world):
    """Test retrieving action history"""
    god_mode = GodMode(mock_world)
    
    # Add multiple actions
    for i in range(5):
        god_mode.record_action(
            ability=GodAbility.TRIGGER_EVENT,
            description=f"Action {i}",
            target_ids=[],
            result="Success"
        )
    
    history = god_mode.get_action_history(limit=3)
    assert len(history) == 3
    # Should return the most recent 3 actions
    assert history[0]["description"] == "Action 2"
    assert history[1]["description"] == "Action 3"
    assert history[2]["description"] == "Action 4"


def test_modify_avatar_attribute(mock_world, mock_avatar):
    """Test modifying avatar attributes"""
    god_mode = GodMode(mock_world)
    mock_world.avatar_manager.avatars = {"test_avatar_1": mock_avatar}
    
    # Test simple attribute modification
    result = god_mode.modify_avatar_attribute(
        "test_avatar_1",
        "name",
        "新名字"
    )
    
    assert result == True
    assert mock_avatar.name == "新名字"
    assert len(god_mode.action_history) == 1


def test_modify_avatar_nested_attribute(mock_world, mock_avatar):
    """Test modifying nested avatar attributes"""
    god_mode = GodMode(mock_world)
    mock_world.avatar_manager.avatars = {"test_avatar_1": mock_avatar}
    
    # Test nested attribute modification
    result = god_mode.modify_avatar_attribute(
        "test_avatar_1",
        "cultivation.exp",
        5000
    )
    
    assert result == True
    assert mock_avatar.cultivation.exp == 5000


def test_grant_fortune_exp(mock_world, mock_avatar):
    """Test granting EXP fortune"""
    god_mode = GodMode(mock_world)
    mock_world.avatar_manager.avatars = {"test_avatar_1": mock_avatar}
    mock_avatar.cultivation.exp = 1000
    
    result = god_mode.grant_fortune(
        "test_avatar_1",
        "exp",
        500
    )
    
    assert result == True
    assert mock_avatar.cultivation.exp == 1500
    assert mock_world.event_manager.add_event.called


def test_grant_fortune_magic_stone(mock_world, mock_avatar):
    """Test granting magic stone fortune"""
    god_mode = GodMode(mock_world)
    mock_world.avatar_manager.avatars = {"test_avatar_1": mock_avatar}
    
    result = god_mode.grant_fortune(
        "test_avatar_1",
        "magic_stone",
        1000
    )
    
    assert result == True
    assert mock_avatar.magic_stone.add.called
    assert mock_avatar.magic_stone.add.call_args[0][0] == 1000


def test_send_tribulation(mock_world, mock_avatar):
    """Test sending tribulation"""
    god_mode = GodMode(mock_world)
    mock_world.avatar_manager.avatars = {"test_avatar_1": mock_avatar}
    mock_avatar.hp.max = 1000
    
    result = god_mode.send_tribulation(
        "test_avatar_1",
        difficulty=5
    )
    
    assert result == True
    assert mock_avatar.hp.damage.called
    # Damage should be max_hp * difficulty * 0.1 = 1000 * 5 * 0.1 = 500
    assert mock_avatar.hp.damage.call_args[0][0] == 500
    assert mock_world.event_manager.add_event.called


def test_trigger_world_event(mock_world, mock_avatar):
    """Test triggering world events"""
    god_mode = GodMode(mock_world)
    mock_world.avatar_manager.avatars = {"test_avatar_1": mock_avatar}
    
    result = god_mode.trigger_world_event(
        "天降异象",
        related_avatar_ids=["test_avatar_1"],
        is_major=True
    )
    
    assert result == True
    assert mock_world.event_manager.add_event.called
    call_args = mock_world.event_manager.add_event.call_args
    assert call_args[0][0] == "天降异象"
    assert call_args[1]["is_major"] == True


def test_adjust_world_qi(mock_world):
    """Test adjusting world qi"""
    god_mode = GodMode(mock_world)
    
    # Create a mock tile
    mock_tile = Mock()
    mock_tile.qi = 100
    mock_world.map.tiles = {"tile1": mock_tile}
    
    result = god_mode.adjust_world_qi("tile1", 50)
    
    assert result == True
    assert mock_tile.qi == 150


def test_adjust_world_qi_negative(mock_world):
    """Test adjusting world qi with negative value"""
    god_mode = GodMode(mock_world)
    
    # Create a mock tile
    mock_tile = Mock()
    mock_tile.qi = 100
    mock_world.map.tiles = {"tile1": mock_tile}
    
    result = god_mode.adjust_world_qi("tile1", -150)
    
    assert result == True
    # Qi should not go below 0
    assert mock_tile.qi == 0


@pytest.mark.asyncio
async def test_ai_generate_text():
    """Test AI text generation"""
    mock_world = Mock()
    mock_world.month_stamp = Mock()
    
    god_mode = GodMode(mock_world)
    
    with patch('src.classes.god_mode.call_llm', new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = "Generated text"
        
        result = await god_mode.ai_generate_text(
            "Generate something",
            context="Context info",
            use_fast_model=True
        )
        
        assert result == "Generated text"
        assert mock_llm.called
        assert len(god_mode.action_history) == 1
        assert god_mode.action_history[0].ai_used == True


@pytest.mark.asyncio
async def test_ai_suggest_event(mock_avatar):
    """Test AI suggesting events"""
    mock_world = Mock()
    mock_world.month_stamp = Mock()
    
    god_mode = GodMode(mock_world)
    
    with patch('src.classes.god_mode.call_llm', new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = "Suggested event"
        
        result = await god_mode.ai_suggest_event(mock_avatar)
        
        assert result == "Suggested event"
        assert mock_llm.called


def test_invalid_avatar_id(mock_world):
    """Test operations with invalid avatar ID"""
    god_mode = GodMode(mock_world)
    
    # Test with non-existent avatar
    result = god_mode.grant_fortune("invalid_id", "exp", 100)
    assert result == False
    
    result = god_mode.send_tribulation("invalid_id", 5)
    assert result == False
    
    result = god_mode.modify_avatar_attribute("invalid_id", "name", "Test")
    assert result == False
