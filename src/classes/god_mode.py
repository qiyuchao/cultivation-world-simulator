"""
God Mode (天道模式) - 上帝视角的世界干预系统

This module provides God-like abilities to manipulate the cultivation world,
including AI-powered generation and various divine interventions.
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum

from src.classes.world import World
from src.classes.avatar import Avatar
from src.classes.event import Event
from src.classes.calendar import MonthStamp
from src.utils.llm.client import call_llm
from src.utils.llm.config import LLMMode


class GodAbility(Enum):
    """上帝能力枚举"""
    CREATE_AVATAR = "create_avatar"           # 创建角色
    DELETE_AVATAR = "delete_avatar"           # 删除角色
    MODIFY_AVATAR = "modify_avatar"           # 修改角色
    TRIGGER_EVENT = "trigger_event"           # 触发事件
    CONTROL_WEATHER = "control_weather"       # 控制天象
    GRANT_FORTUNE = "grant_fortune"           # 赐予机缘
    SEND_TRIBULATION = "send_tribulation"     # 降下天劫
    MIND_CONTROL = "mind_control"             # 心灵控制
    TIME_CONTROL = "time_control"             # 时间控制
    WORLD_RESET = "world_reset"               # 世界重置
    AI_GENERATE = "ai_generate"               # AI生成


@dataclass
class GodAction:
    """上帝行为记录"""
    ability: GodAbility
    description: str
    timestamp: MonthStamp
    target_ids: List[str]
    result: Optional[str] = None
    ai_used: bool = False


class GodMode:
    """
    上帝模式类 - 提供全能的世界干预能力
    
    作为"天道"，可以：
    1. 创造和毁灭任何生命
    2. 触发任何事件
    3. 控制天象和灵气
    4. 赐予机缘或降下天劫
    5. 调用免费AI辅助决策
    6. 直接修改世界规则
    """
    
    def __init__(self, world: World):
        self.world = world
        self.action_history: List[GodAction] = []
    
    def record_action(
        self, 
        ability: GodAbility, 
        description: str,
        target_ids: List[str] = None,
        result: str = None,
        ai_used: bool = False
    ):
        """记录上帝行为"""
        action = GodAction(
            ability=ability,
            description=description,
            timestamp=self.world.month_stamp,
            target_ids=target_ids or [],
            result=result,
            ai_used=ai_used
        )
        self.action_history.append(action)
    
    def get_action_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """获取上帝行为历史"""
        recent = self.action_history[-limit:]
        return [
            {
                "ability": action.ability.value,
                "description": action.description,
                "timestamp": str(action.timestamp),
                "target_ids": action.target_ids,
                "result": action.result,
                "ai_used": action.ai_used
            }
            for action in recent
        ]
    
    # ==================== AI能力 ====================
    
    async def ai_generate_text(
        self, 
        prompt: str,
        context: Optional[str] = None,
        use_fast_model: bool = False
    ) -> str:
        """
        使用AI生成文本
        
        Args:
            prompt: 提示词
            context: 上下文信息
            use_fast_model: 是否使用快速模型（免费）
        
        Returns:
            生成的文本
        """
        full_prompt = prompt
        if context:
            full_prompt = f"{context}\n\n{prompt}"
        
        mode = LLMMode.FAST if use_fast_model else LLMMode.NORMAL
        
        try:
            response = await call_llm(full_prompt, mode=mode)
            
            self.record_action(
                ability=GodAbility.AI_GENERATE,
                description=f"AI生成: {prompt[:50]}...",
                ai_used=True,
                result=response[:100] if response else None
            )
            
            return response
        except Exception as e:
            return f"AI生成失败: {str(e)}"
    
    async def ai_suggest_event(self, avatar: Avatar) -> str:
        """AI建议角色事件"""
        prompt = f"""
作为修仙世界的天道，为以下角色建议一个有趣的事件：

角色信息：
- 姓名：{avatar.name}
- 境界：{avatar.cultivation.realm}
- 门派：{avatar.sect.name if avatar.sect else "散修"}
- 性格：{", ".join([p.name for p in avatar.persona.personas])}

请生成一个简短的事件描述（50字以内）。
"""
        return await self.ai_generate_text(prompt, use_fast_model=True)
    
    async def ai_generate_story(
        self, 
        avatars: List[Avatar], 
        event_type: str
    ) -> str:
        """AI生成剧情"""
        avatar_info = "\n".join([
            f"- {av.name}（{av.cultivation.realm}）"
            for av in avatars[:5]  # 最多5个角色
        ])
        
        prompt = f"""
作为修仙世界的天道，为以下角色生成一个{event_type}的剧情：

涉及角色：
{avatar_info}

请生成一个生动的剧情片段（200字以内）。
"""
        return await self.ai_generate_text(prompt, use_fast_model=False)
    
    # ==================== 角色控制 ====================
    
    def modify_avatar_attribute(
        self,
        avatar_id: str,
        attribute: str,
        value: Any
    ) -> bool:
        """
        修改角色属性
        
        Args:
            avatar_id: 角色ID
            attribute: 属性名（如 "cultivation.level", "hp.current"）
            value: 新值
        
        Returns:
            是否成功
        """
        avatar = self.world.avatar_manager.avatars.get(avatar_id)
        if not avatar:
            return False
        
        try:
            # 支持嵌套属性访问
            parts = attribute.split('.')
            obj = avatar
            for part in parts[:-1]:
                obj = getattr(obj, part)
            setattr(obj, parts[-1], value)
            
            self.record_action(
                ability=GodAbility.MODIFY_AVATAR,
                description=f"修改 {avatar.name} 的 {attribute} 为 {value}",
                target_ids=[avatar_id],
                result="成功"
            )
            return True
        except Exception as e:
            self.record_action(
                ability=GodAbility.MODIFY_AVATAR,
                description=f"修改 {avatar.name} 的 {attribute} 失败",
                target_ids=[avatar_id],
                result=f"失败: {str(e)}"
            )
            return False
    
    def grant_fortune(
        self,
        avatar_id: str,
        fortune_type: str,
        value: int
    ) -> bool:
        """
        赐予机缘
        
        Args:
            avatar_id: 角色ID
            fortune_type: 机缘类型（exp, magic_stone, item等）
            value: 数值
        
        Returns:
            是否成功
        """
        avatar = self.world.avatar_manager.avatars.get(avatar_id)
        if not avatar:
            return False
        
        try:
            if fortune_type == "exp":
                avatar.cultivation.exp += value
            elif fortune_type == "magic_stone":
                avatar.magic_stone.add(value)
            elif fortune_type == "hp":
                avatar.hp.heal(value)
            
            self.record_action(
                ability=GodAbility.GRANT_FORTUNE,
                description=f"赐予 {avatar.name} {fortune_type} {value}",
                target_ids=[avatar_id],
                result="成功"
            )
            
            # 创建世界事件
            event_text = f"天道垂怜，{avatar.name}获得了神秘的恩赐"
            self.world.event_manager.add_event(
                event_text,
                month_stamp=self.world.month_stamp,
                related_avatars=[avatar],
                is_major=True
            )
            
            return True
        except Exception as e:
            return False
    
    def send_tribulation(
        self,
        avatar_id: str,
        difficulty: int = 1
    ) -> bool:
        """
        降下天劫
        
        Args:
            avatar_id: 角色ID
            difficulty: 难度等级（1-10）
        
        Returns:
            是否成功
        """
        avatar = self.world.avatar_manager.avatars.get(avatar_id)
        if not avatar:
            return False
        
        try:
            # 减少HP作为天劫伤害
            damage = avatar.hp.max * difficulty * 0.1
            avatar.hp.damage(int(damage))
            
            self.record_action(
                ability=GodAbility.SEND_TRIBULATION,
                description=f"对 {avatar.name} 降下 {difficulty}级天劫",
                target_ids=[avatar_id],
                result=f"造成{int(damage)}点伤害"
            )
            
            # 创建世界事件
            event_text = f"天降异象，{avatar.name}遭受天劫考验"
            self.world.event_manager.add_event(
                event_text,
                month_stamp=self.world.month_stamp,
                related_avatars=[avatar],
                is_major=True
            )
            
            return True
        except Exception as e:
            return False
    
    # ==================== 世界控制 ====================
    
    def trigger_world_event(
        self,
        event_text: str,
        related_avatar_ids: List[str] = None,
        is_major: bool = True
    ) -> bool:
        """
        触发世界事件
        
        Args:
            event_text: 事件描述
            related_avatar_ids: 相关角色ID列表
            is_major: 是否为重大事件
        
        Returns:
            是否成功
        """
        try:
            related_avatars = []
            if related_avatar_ids:
                for aid in related_avatar_ids:
                    avatar = self.world.avatar_manager.avatars.get(aid)
                    if avatar:
                        related_avatars.append(avatar)
            
            self.world.event_manager.add_event(
                event_text,
                month_stamp=self.world.month_stamp,
                related_avatars=related_avatars,
                is_major=is_major
            )
            
            self.record_action(
                ability=GodAbility.TRIGGER_EVENT,
                description=f"触发事件: {event_text}",
                target_ids=related_avatar_ids or [],
                result="成功"
            )
            
            return True
        except Exception as e:
            return False
    
    def adjust_world_qi(self, tile_id: str, delta: float) -> bool:
        """
        调整地块灵气
        
        Args:
            tile_id: 地块ID
            delta: 灵气变化量
        
        Returns:
            是否成功
        """
        try:
            tile = self.world.map.tiles.get(tile_id)
            if not tile:
                return False
            
            tile.qi = max(0, tile.qi + delta)
            
            self.record_action(
                ability=GodAbility.CONTROL_WEATHER,
                description=f"调整地块灵气 {delta:+.1f}",
                result="成功"
            )
            
            return True
        except Exception:
            return False
