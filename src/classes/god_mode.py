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
    
    # Life Skills (生活技能)
    MANAGE_PLANTING = "manage_planting"       # 种植管理
    MANAGE_RAISING = "manage_raising"         # 饲养管理
    UPGRADE_SKILL = "upgrade_skill"           # 技能升级
    
    # Organization System (组织系统)
    CONTROL_SECT_AI = "control_sect_ai"       # 控制宗门AI
    CREATE_SECT_MISSION = "create_sect_mission"  # 创建宗门任务
    MANAGE_FAMILY = "manage_family"           # 管理世家
    CONTROL_COURT = "control_court"           # 控制朝廷
    SET_ORG_RELATION = "set_org_relation"     # 设置组织关系
    
    # Event System (事件系统)
    TRIGGER_COMPETITION = "trigger_competition"  # 触发比武大会
    TRIGGER_SECT_COMP = "trigger_sect_comp"   # 触发宗门大比
    TRIGGER_TREASURE = "trigger_treasure"     # 触发宝物出世
    TRIGGER_DISASTER = "trigger_disaster"     # 触发自然灾害
    TRIGGER_BEAST_TIDE = "trigger_beast_tide" # 触发兽潮
    
    # Ecosystem (生态系统)
    CREATE_MAGIC_BEAST = "create_magic_beast" # 创建魔兽
    
    # Special Features (特殊功能)
    TRIGGER_POSSESSION = "trigger_possession" # 触发夺舍
    TRIGGER_REBIRTH = "trigger_rebirth"       # 触发重生
    GRANT_FATE = "grant_fate"                 # 赐予机缘因果
    PERFORM_DIVINATION = "perform_divination" # 执行占卜
    CREATE_FORMATION = "create_formation"     # 创建阵法
    SET_WORLD_SECRET = "set_world_secret"     # 设置世界秘密
    TRIGGER_APOCALYPSE = "trigger_apocalypse" # 触发灭世危机


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
    
    # ==================== 生活技能 (Life Skills) ====================
    
    def manage_avatar_skill(
        self,
        avatar_id: str,
        skill_type: str,
        action: str = "upgrade",
        value: int = 1
    ) -> bool:
        """
        管理角色生活技能
        
        Args:
            avatar_id: 角色ID
            skill_type: 技能类型 (planting, raising, forging, alchemy)
            action: 操作类型 (upgrade, set)
            value: 数值
        
        Returns:
            是否成功
        """
        avatar = self.world.avatar_manager.avatars.get(avatar_id)
        if not avatar:
            return False
        
        try:
            ability_map = {
                "planting": GodAbility.MANAGE_PLANTING,
                "raising": GodAbility.MANAGE_RAISING,
                "forging": GodAbility.UPGRADE_SKILL,
                "alchemy": GodAbility.UPGRADE_SKILL
            }
            
            # Note: Actual skill implementation would need to be in Avatar class
            # This is a placeholder for God Mode control
            
            self.record_action(
                ability=ability_map.get(skill_type, GodAbility.UPGRADE_SKILL),
                description=f"{action} {avatar.name} 的 {skill_type} 技能",
                target_ids=[avatar_id],
                result=f"设置为 {value}"
            )
            
            event_text = f"{avatar.name}的{skill_type}技能得到天道加持"
            self.world.event_manager.add_event(
                event_text,
                month_stamp=self.world.month_stamp,
                related_avatars=[avatar],
                is_major=False
            )
            
            return True
        except Exception:
            return False
    
    # ==================== 组织系统 (Organization System) ====================
    
    def create_sect_mission(
        self,
        sect_id: int,
        mission_desc: str,
        reward: Dict[str, Any] = None
    ) -> bool:
        """
        创建宗门任务
        
        Args:
            sect_id: 宗门ID
            mission_desc: 任务描述
            reward: 奖励
        
        Returns:
            是否成功
        """
        try:
            # Placeholder for sect mission system
            self.record_action(
                ability=GodAbility.CREATE_SECT_MISSION,
                description=f"为宗门 {sect_id} 创建任务: {mission_desc}",
                result="成功"
            )
            
            event_text = f"天降神谕，宗门获得新任务：{mission_desc}"
            self.world.event_manager.add_event(
                event_text,
                month_stamp=self.world.month_stamp,
                is_major=True
            )
            
            return True
        except Exception:
            return False
    
    def set_organization_relation(
        self,
        org1_id: str,
        org2_id: str,
        relation_type: str = "allied"
    ) -> bool:
        """
        设置组织间关系
        
        Args:
            org1_id: 组织1 ID
            org2_id: 组织2 ID
            relation_type: 关系类型 (allied, hostile, neutral)
        
        Returns:
            是否成功
        """
        try:
            self.record_action(
                ability=GodAbility.SET_ORG_RELATION,
                description=f"设置组织关系: {org1_id} <-> {org2_id} = {relation_type}",
                result="成功"
            )
            
            event_text = f"天意使然，两大势力关系发生变化"
            self.world.event_manager.add_event(
                event_text,
                month_stamp=self.world.month_stamp,
                is_major=True
            )
            
            return True
        except Exception:
            return False
    
    # ==================== 事件系统 (Event System) ====================
    
    def trigger_martial_competition(
        self,
        location: str = "天下第一擂台",
        participants: List[str] = None
    ) -> bool:
        """
        触发比武大会
        
        Args:
            location: 地点
            participants: 参与者ID列表
        
        Returns:
            是否成功
        """
        try:
            avatars = []
            if participants:
                for pid in participants:
                    avatar = self.world.avatar_manager.avatars.get(pid)
                    if avatar:
                        avatars.append(avatar)
            
            self.record_action(
                ability=GodAbility.TRIGGER_COMPETITION,
                description=f"触发比武大会于 {location}",
                target_ids=participants or [],
                result="成功"
            )
            
            event_text = f"{location}将举办盛大比武大会，英雄豪杰云集"
            self.world.event_manager.add_event(
                event_text,
                month_stamp=self.world.month_stamp,
                related_avatars=avatars,
                is_major=True
            )
            
            return True
        except Exception:
            return False
    
    def trigger_treasure_appearance(
        self,
        treasure_name: str,
        location: str,
        rarity: str = "legendary"
    ) -> bool:
        """
        触发宝物出世
        
        Args:
            treasure_name: 宝物名称
            location: 出现地点
            rarity: 稀有度
        
        Returns:
            是否成功
        """
        try:
            self.record_action(
                ability=GodAbility.TRIGGER_TREASURE,
                description=f"触发宝物出世: {treasure_name} 于 {location}",
                result="成功"
            )
            
            event_text = f"天地异象！{treasure_name}于{location}横空出世，引起修仙界震动"
            self.world.event_manager.add_event(
                event_text,
                month_stamp=self.world.month_stamp,
                is_major=True
            )
            
            return True
        except Exception:
            return False
    
    def trigger_natural_disaster(
        self,
        disaster_type: str = "earthquake",
        location: str = "",
        severity: int = 5
    ) -> bool:
        """
        触发自然灾害
        
        Args:
            disaster_type: 灾害类型
            location: 地点
            severity: 严重程度 (1-10)
        
        Returns:
            是否成功
        """
        try:
            self.record_action(
                ability=GodAbility.TRIGGER_DISASTER,
                description=f"触发{disaster_type}于{location}，严重程度{severity}",
                result="成功"
            )
            
            disaster_names = {
                "earthquake": "地震",
                "flood": "洪水",
                "drought": "旱灾",
                "storm": "风暴"
            }
            
            event_text = f"天降灾劫！{location}发生{disaster_names.get(disaster_type, disaster_type)}，生灵涂炭"
            self.world.event_manager.add_event(
                event_text,
                month_stamp=self.world.month_stamp,
                is_major=True
            )
            
            return True
        except Exception:
            return False
    
    def trigger_beast_tide(
        self,
        location: str,
        intensity: int = 5
    ) -> bool:
        """
        触发兽潮
        
        Args:
            location: 地点
            intensity: 强度 (1-10)
        
        Returns:
            是否成功
        """
        try:
            self.record_action(
                ability=GodAbility.TRIGGER_BEAST_TIDE,
                description=f"触发兽潮于{location}，强度{intensity}",
                result="成功"
            )
            
            event_text = f"妖兽暴动！{location}遭遇大规模兽潮袭击，危机四伏"
            self.world.event_manager.add_event(
                event_text,
                month_stamp=self.world.month_stamp,
                is_major=True
            )
            
            return True
        except Exception:
            return False
    
    # ==================== 特殊功能 (Special Features) ====================
    
    def trigger_possession(
        self,
        possessor_id: str,
        target_id: str
    ) -> bool:
        """
        触发夺舍
        
        Args:
            possessor_id: 夺舍者ID
            target_id: 被夺舍者ID
        
        Returns:
            是否成功
        """
        possessor = self.world.avatar_manager.avatars.get(possessor_id)
        target = self.world.avatar_manager.avatars.get(target_id)
        
        if not possessor or not target:
            return False
        
        try:
            self.record_action(
                ability=GodAbility.TRIGGER_POSSESSION,
                description=f"{possessor.name} 夺舍 {target.name}",
                target_ids=[possessor_id, target_id],
                result="成功"
            )
            
            event_text = f"惊天秘术！{possessor.name}施展夺舍之术，占据{target.name}肉身"
            self.world.event_manager.add_event(
                event_text,
                month_stamp=self.world.month_stamp,
                related_avatars=[possessor, target],
                is_major=True
            )
            
            return True
        except Exception:
            return False
    
    def trigger_rebirth(
        self,
        avatar_id: str,
        rebirth_type: str = "reincarnation"
    ) -> bool:
        """
        触发重生
        
        Args:
            avatar_id: 角色ID
            rebirth_type: 重生类型
        
        Returns:
            是否成功
        """
        avatar = self.world.avatar_manager.avatars.get(avatar_id)
        if not avatar:
            return False
        
        try:
            self.record_action(
                ability=GodAbility.TRIGGER_REBIRTH,
                description=f"{avatar.name} 获得重生机会 ({rebirth_type})",
                target_ids=[avatar_id],
                result="成功"
            )
            
            event_text = f"轮回奥秘！{avatar.name}逆天改命，获得重生之机"
            self.world.event_manager.add_event(
                event_text,
                month_stamp=self.world.month_stamp,
                related_avatars=[avatar],
                is_major=True
            )
            
            return True
        except Exception:
            return False
    
    async def perform_divination(
        self,
        avatar_id: str,
        question: str
    ) -> str:
        """
        执行占卜
        
        Args:
            avatar_id: 角色ID
            question: 占卜问题
        
        Returns:
            占卜结果
        """
        avatar = self.world.avatar_manager.avatars.get(avatar_id)
        if not avatar:
            return "占卜失败：未找到角色"
        
        try:
            prompt = f"""
作为修仙世界的天道，为以下角色进行占卜预言：

角色信息：
- 姓名：{avatar.name}
- 境界：{avatar.cultivation.realm}
- 问题：{question}

请生成一个神秘而富有深意的占卜预言（50字以内）。
"""
            result = await self.ai_generate_text(prompt, use_fast_model=True)
            
            self.record_action(
                ability=GodAbility.PERFORM_DIVINATION,
                description=f"为{avatar.name}占卜: {question}",
                target_ids=[avatar_id],
                result=result[:50],
                ai_used=True
            )
            
            return result
        except Exception as e:
            return f"占卜失败: {str(e)}"
    
    def set_world_secret(
        self,
        secret_name: str,
        secret_desc: str,
        reveal_condition: str = ""
    ) -> bool:
        """
        设置世界秘密
        
        Args:
            secret_name: 秘密名称
            secret_desc: 秘密描述
            reveal_condition: 揭示条件
        
        Returns:
            是否成功
        """
        try:
            self.record_action(
                ability=GodAbility.SET_WORLD_SECRET,
                description=f"设置世界秘密: {secret_name}",
                result="成功"
            )
            
            # Placeholder for world secret system
            return True
        except Exception:
            return False
    
    def trigger_apocalypse(
        self,
        apocalypse_type: str = "demon_invasion",
        severity: int = 10
    ) -> bool:
        """
        触发灭世危机
        
        Args:
            apocalypse_type: 危机类型
            severity: 严重程度
        
        Returns:
            是否成功
        """
        try:
            self.record_action(
                ability=GodAbility.TRIGGER_APOCALYPSE,
                description=f"触发灭世危机: {apocalypse_type}",
                result=f"严重程度{severity}"
            )
            
            crisis_names = {
                "demon_invasion": "魔族入侵",
                "world_collapse": "世界崩塌",
                "ancient_evil": "上古邪神复苏",
                "void_tear": "虚空裂缝"
            }
            
            event_text = f"天地大劫！{crisis_names.get(apocalypse_type, apocalypse_type)}，修仙界面临灭世危机"
            self.world.event_manager.add_event(
                event_text,
                month_stamp=self.world.month_stamp,
                is_major=True
            )
            
            return True
        except Exception:
            return False
