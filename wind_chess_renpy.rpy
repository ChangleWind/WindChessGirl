# wind_chess_renpy.rpy - 风棋少女 Ren'Py 移植完整版
# ============================================================
# 核心棋盘逻辑（纯代码实现，无需外部资源）
# 叙事性采用Ren'Py语法
# ============================================================

# -------------------- 角色声明 --------------------
# 心情系统变量（不需要在 init 中调用 renpy 函数）
init -1 python:
    _current_mood = 1
    _current_background = 1
    _current_music = 1
    _current_fengzi_tag = "fengzi_sprite"
    _current_bg_tag = "bg_image"
    _game_waiting = True  # 控制游戏循环等待
    _return = None  # 返回值
    
    # -------------------- 音量控制变量 --------------------
    # 使用 persistent 确保音量设置跨游戏会话持久化
    # 强制设置为默认值，确保不会是 None
    persistent.music_volume = 0.7
    persistent.muted = False
    persistent.music_volume_input = "70"
    
    def _apply_volume():
        """应用当前音量设置"""
        vol = persistent.music_volume if persistent.music_volume is not None else 0.7
        if persistent.muted:
            renpy.music.set_volume(0.0, channel='music')
            renpy.music.set_volume(0.0, channel='sound')
        else:
            renpy.music.set_volume(vol, channel='music')
            renpy.music.set_volume(vol, channel='sound')
        persistent.music_volume_input = str(int(vol * 100))
    
    def _save_volume(value):
        """滑块释放时保存并应用音量"""
        persistent.music_volume = value
        persistent.music_volume_input = str(int(value * 100))  # 同步输入框显示
        _apply_volume()
    
    def _on_volume_input_changed(value):
        """输入框值变化时同步滑块和屏幕变量"""
        try:
            vol = int(value)
            vol = max(0, min(100, vol))  # 限制在 0-100 范围
            persistent.music_volume = vol / 100.0
            persistent.music_volume_input = str(vol)
            renpy.set_screen_variable("volume_text", str(vol))  # 同步屏幕变量
            _apply_volume()
        except:
            pass  # 无效输入，不做处理
    
    def _apply_volume_input():
        """应用数字输入的音量值（供输入框回车确认使用）"""
        try:
            vol = int(persistent.music_volume_input)
            vol = max(0, min(100, vol))
            persistent.music_volume = vol / 100.0
            persistent.music_volume_input = str(vol)
            _apply_volume()
        except:
            persistent.music_volume_input = str(int(persistent.music_volume * 100))
    
    # 初始化时应用音量
    _apply_volume()
    
    # 心情名称映射
    MOOD_NAMES = {
        0: "隐藏", 1: "默认/日常", 2: "开心", 3: "俏皮",
        4: "害羞", 5: "惊讶", 6: "期待", 7: "得意", 8: "温柔"
    }
    
            # 情绪关键词映射
    MOOD_KEYWORDS = {
        1: ["嗯", "好的", "知道了", "原来如此", "这样啊", "好吧", "继续", "平静"],
        2: ["开心", "高兴", "好开心", "太棒了", "太好了", "哈哈", "呵呵", "嘿嘿", "嘻嘻", "happy", "joy", "fun", "喜欢", "最爱", "最喜欢", "耶", "赢", "赢了", "胜利"],
        3: ["哼", "哼~", "才不是", "讨厌", "坏人", "笨蛋", "傻瓜", "好狡猾", "哼哼", "mischief", "tease", "playful", "想", "好想"],
        4: ["害羞", "脸红", "不好意思", "不要看", "人家", "小声", "...", "诶", "啊...", "呜", "委屈", "shy", "embarrassed", "blush", "喜欢你", "心跳", "脸红"],
        5: ["诶", "咦", "什么", "怎么", "真的吗", "不会吧", "等等", "wow", "surprise", "shocked", "what", "huh", "啊？", "诶？", "咦？", "真的吗？"],
        6: ["期待", "好想", "快点", "快来", "来吧", "一定要", "绝对", "嘿嘿嘿", "excited", "eager", "hope", "期待"],
        7: ["哼哼", "哼~", "厉害吧", "不错吧", "服不服", "知道我的厉害", "最强", "proud", "得意", "victory", "won", "win", "厉害", "厉害吧", "最强"],
        8: ["温柔", "好想", "一直", "永远", "在一起", "喜欢你", "心疼", "担心", "关心", "gentle", "soft", "tender", "care", "miss", "永远", "一直"],
    }
    
    # 心情检测函数
    def _detect_mood_from_text(text):
        if not text:
            return None
        priority_moods = [8, 7, 4, 6, 3, 5, 2, 1]
        for mood in priority_moods:
            keywords = MOOD_KEYWORDS.get(mood, [])
            for keyword in keywords:
                if keyword in text:
                    return mood
        return None
    
    # 自动立绘函数（供 init python 中的 fz 函数使用）
    def _update_sprite_auto(text):
        """根据对话文本自动更新立绘"""
        target_mood = _detect_mood_from_text(text)
        if target_mood is not None:
            _current_mood = target_mood

# fengzi 角色在 init -1 python 块中定义（带立绘回调）

# -------------------- 图片声明 --------------------
# 立绘图片
image fengzi 1 = "art/crazyman/1.png"
image fengzi 2 = "art/crazyman/2.png"
image fengzi 3 = "art/crazyman/3.png"
image fengzi 4 = "art/crazyman/4.png"
image fengzi 5 = "art/crazyman/5.png"
image fengzi 6 = "art/crazyman/6.png"
image fengzi 7 = "art/crazyman/7.png"
image fengzi 8 = "art/crazyman/8.png"

# 背景图片
image bg 1 = "art/background/1.png"
image bg 2 = "art/background/2.png"
image bg 3 = "art/background/3.png"
image bg 4 = "art/background/4.png"
image bg 5 = "art/background/5.png"
image bg 6 = "art/background/6.png"
image bg 7 = "art/background/7.png"
image bg 8 = "art/background/8.png"
image bg 9 = "art/background/9.png"
image bg 10 = "art/background/10.png"
image bg 11 = "art/background/11.png"
image bg 12 = "art/background/12.png"
image bg 13 = "art/background/13.png"
image bg 14 = "art/background/14.png"
image bg 15 = "art/background/15.png"
image bg 16 = "art/background/16.png"
image bg 17 = "art/background/17.png"
image bg 18 = "art/background/18.png"
image bg 19 = "art/background/19.png"
image bg 20 = "art/background/20.png"
image bg 21 = "art/background/21.png"
image bg 22 = "art/background/22.png"



# -------------------- 棋盘位置变换 --------------------
transform board_transform:
    pos (140, 130)



init python:
    # -------------------- 基础导入 --------------------
    from enum import Enum
    import random
    import json
    import os
    
    # ═══════════════════════════════════════════════════════════════════
    # ★ 开发期属性冲突检查（lint 建议）：screen 语句属性冲突时立即报错
    # ═══════════════════════════════════════════════════════════════════
    config.check_conflicting_properties = True

    # ═══════════════════════════════════════════════════════════════════
    # ★ 全局禁用鼠标滚轮（回看/快进）——本游戏不是传统 galgame，
    #   滚轮在整个游戏流程中（包括对话、菜单、片尾名单）都不得产生任何作用
    # ═══════════════════════════════════════════════════════════════════
    if "mousedown_4" in config.keymap.get("rollback", []):
        config.keymap["rollback"].remove("mousedown_4")
    if "mouseup_4" in config.keymap.get("rollback", []):
        config.keymap["rollback"].remove("mouseup_4")
    if "mousedown_5" in config.keymap.get("rollforward", []):
        config.keymap["rollforward"].remove("mousedown_5")
    if "mouseup_5" in config.keymap.get("rollforward", []):
        config.keymap["rollforward"].remove("mouseup_5")
    
    # ═══════════════════════════════════════════════════════════════════
    # ★ 立绘和背景显示函数（在游戏运行时调用）
    # ═══════════════════════════════════════════════════════════════════
    
    def _show_fengzi_sprite(mood_value=None):
        """显示风子立绘（仅在背景为1时显示）"""
        global _current_mood
        # 优先级最高：背景不是1时隐藏立绘
        if _current_background != 1:
            renpy.hide(_current_fengzi_tag)
            return
        if mood_value is not None:
            _current_mood = mood_value
        if _current_mood > 0:
            sprite_name = "fengzi {}".format(_current_mood)
            # 立绘显示在右侧中部位置
            renpy.show(sprite_name, tag="fengzi_sprite", at_list=[Transform(alpha=1.0, xalign=0.9, yalign=1.0)])
        else:
            renpy.hide(_current_fengzi_tag)
    
    def _hide_fengzi():
        """隐藏风子立绘"""
        global _current_mood
        _current_mood = 0
        renpy.hide("fengzi_sprite")
    
    def _show_background(bg_value=None):
        """显示背景图片"""
        global _current_background, _current_mood
        if bg_value is not None:
            _current_background = bg_value
        if _current_background == 0:
            renpy.scene()
            renpy.show("black")
        else:
            bg_name = "bg {}".format(_current_background)
            renpy.scene()
            renpy.show(bg_name)
            # 重新显示立绘（如果需要）
            if _current_mood > 0:
                sprite_name = "fengzi {}".format(_current_mood)
                renpy.show(sprite_name, tag="fengzi_sprite", at_list=[Transform(alpha=1.0, xalign=0.9, ypos=720)])
    
    def _set_mood(mood_value):
        """设置风子的心情（同时显示立绘）"""
        global _current_mood
        _current_mood = mood_value
        _show_fengzi_sprite(mood_value)
    
    def _set_background(bg_value):
        """设置背景 - 当背景不等于1时自动隐藏风子立绘"""
        global _current_background, _current_mood
        _current_background = bg_value
        _show_background(bg_value)
        # 当背景不是一般场景时，隐藏风子立绘
        if bg_value != 1:
            _current_mood = 0
            renpy.hide("fengzi_sprite")
    
    def _set_music(music_value):
        """设置背景音乐"""
        global _current_music
        _current_music = music_value
        music_files = {
            1: "true_music/Joyful_Sprite.mp3",
            2: "true_music/Moment_of _Decision.mp3",
            3: "true_music/Eternal_Longing.mp3",
        }
        if music_value in music_files:
            renpy.music.play(music_files[music_value], loop=True, fadeout=1.0, fadein=1.0)
        elif music_value == 0:
            renpy.music.stop(fadeout=1.0)
    
    def _get_mood():
        return _current_mood
    
    def _get_background():
        return _current_background
    
    def _auto_update_sprite(text):
        """根据对话文本自动更新立绘"""
        # 优先级最高：背景不是1时隐藏立绘
        if _current_background != 1:
            renpy.hide(_current_fengzi_tag)
            return
        target_mood = _detect_mood_from_text(text)
        if target_mood is not None:
            _set_mood(target_mood)
        elif _current_mood > 0 and not renpy.showing("fengzi_sprite"):
            _show_fengzi_sprite()
    
    def _fengzi_callback(event, interact=True, **kwargs):
        """Character回调 - 在对话时自动显示风子立绘"""
        if interact and (event == "show" or event == "begin"):
            # 优先级最高：背景不是1时隐藏立绘
            if _current_background != 1:
                renpy.hide(_current_fengzi_tag)
                return
            # 获取即将显示的对话文本
            text = kwargs.get("what", "")
            # 先根据对话内容检测情绪
            target_mood = _detect_mood_from_text(text)
            if target_mood is not None:
                _set_mood(target_mood)
            else:
                _show_fengzi_sprite()
        elif event == "end":
            pass
    
    # ═══════════════════════════════════════════════════════════════════
    # ★ 风子智能对话函数 - 自动根据对话内容更新立绘
    # ═══════════════════════════════════════════════════════════════════
    def fz(text):
        """风子对话 - 自动检测情绪并更新立绘"""
        # 检测心情并更新
        _auto_update_sprite(text)
        # 显示对话
        fengzi(text)
    
    # ★ 重新定义风子角色，带自动立绘回调
    fengzi = Character("风子", color="#ff69b4", what_color="#ffb6c1", callback=_fengzi_callback)
    
    # -------------------- 枚举定义 --------------------

    # -------------------- 枚举定义 --------------------
    class WindDirection(Enum):
        HORIZONTAL = "水平风"
        VERTICAL = "垂直风"
        DIAGONAL = "旋风"
    
    class Player(Enum):
        A = "●"  # 玩家棋子
        B = "○"  # AI棋子
    
    class GameMode(Enum):
        TUTORIAL = "教程"
        PVP = "双人对战"
        PVE = "对战"
        CHAT = "聊天"

    # -------------------- 游戏阶段状态机 --------------------
    class GamePhase(Enum):
        """中央游戏状态机 - 控制棋盘与对话的交互时序"""
        PLAYER_SELECT = "玩家选子"     # 玩家选择自己的棋子
        PLAYER_MOVE = "玩家移动"       # 玩家选择目标位置移动
        AI_THINKING = "AI思考"         # AI正在思考（播放对话+延迟）
        AI_MOVING = "AI移动"           # AI执行移动
        AI_COMMENT = "AI评论"          # AI对移动发表评论
        GAME_OVER = "游戏结束"         # 游戏已结束
        IDLE = "空闲"                  # 非对局状态

    class GameStateManager:
        """中央游戏状态管理器 - 从根本上解决棋盘逻辑与GAL对话的冲突"""

        def __init__(self):
            self._phase = GamePhase.IDLE
            self._phase_data = {}  # 阶段附加数据
            self._pending_action = None  # 待执行的动作（用于screen返回）

        @property
        def phase(self):
            return self._phase

        def set_phase(self, phase, **kwargs):
            """安全地切换游戏阶段"""
            old = self._phase
            self._phase = phase
            self._phase_data = kwargs
            renpy.log("GamePhase: {} -> {} ({})".format(old.value, phase.value, kwargs))

        def get_phase_data(self, key, default=None):
            return self._phase_data.get(key, default)

        def is_player_turn(self):
            """是否是玩家的回合（棋盘应响应点击）"""
            return self._phase in (GamePhase.PLAYER_SELECT, GamePhase.PLAYER_MOVE)

        def is_ai_turn(self):
            """是否是AI的回合（棋盘应忽略点击）"""
            return self._phase in (GamePhase.AI_THINKING, GamePhase.AI_MOVING, GamePhase.AI_COMMENT)

        def is_game_over(self):
            return self._phase == GamePhase.GAME_OVER

        def is_playing(self):
            return self._phase != GamePhase.IDLE

        def start_game(self):
            """开始新游戏，进入玩家选子阶段"""
            self.set_phase(GamePhase.PLAYER_SELECT)

        def on_player_selected_piece(self):
            """玩家选中了棋子，进入移动阶段"""
            self.set_phase(GamePhase.PLAYER_MOVE)

        def on_player_moved(self, from_pos, to_pos):
            """玩家完成移动，进入AI思考阶段"""
            self.set_phase(GamePhase.AI_THINKING, from_pos=from_pos, to_pos=to_pos)

        def on_player_no_valid_move(self):
            """玩家没有合法移动（跳过）"""
            self.set_phase(GamePhase.AI_THINKING)

        def on_ai_start_thinking(self):
            """AI开始思考"""
            # phase已经在AI_THINKING了
            pass

        def on_ai_moving(self):
            """AI开始移动"""
            self.set_phase(GamePhase.AI_MOVING)

        def on_ai_moved(self, from_pos, to_pos):
            """AI完成移动，进入评论阶段"""
            self.set_phase(GamePhase.AI_COMMENT, from_pos=from_pos, to_pos=to_pos)

        def on_ai_comment_done(self):
            """AI评论结束，回到玩家选子阶段"""
            self.set_phase(GamePhase.PLAYER_SELECT)

        def on_game_over(self, winner):
            """游戏结束"""
            self.set_phase(GamePhase.GAME_OVER, winner=winner)

        def reset(self):
            """重置状态"""
            self._phase = GamePhase.IDLE
            self._phase_data = {}

    # 全局状态管理器实例
    _game_state_manager = GameStateManager()

    def get_game_state_manager():
        return _game_state_manager

    # ═══════════════════════════════════════════════════════════════════
    # ★ 核心修复：玩家移动完成回调机制
    # 用于在 ChessBoardDisplay.event() 中跳转到指定标签
    # ═══════════════════════════════════════════════════════════════════
    _player_move_jump_target = None  # 玩家移动完成后的跳转目标

    def set_player_move_jump(jump_target):
        """设置玩家移动完成后的跳转目标"""
        global _player_move_jump_target
        _player_move_jump_target = jump_target

    def on_player_move_done():
        """玩家移动完成时调用，跳转到目标标签"""
        global _player_move_jump_target, _game_waiting
        # 结束等待循环
        _game_waiting = False
        if _player_move_jump_target:
            target = _player_move_jump_target
            _player_move_jump_target = None
            renpy.jump(target)

    # -------------------- 核心棋类 --------------------
    class WindChessGame:
        """风之棋核心游戏类"""
        
        def __init__(self, board_size=9, pieces_per_player=6):
            self.board_size = board_size
            self.pieces_per_player = pieces_per_player
            self.board = [[None for _ in range(board_size)] for _ in range(board_size)]
            self.wind_direction = random.choice(list(WindDirection))
            self.current_player = Player.A
            self.game_over = False
            self.winner = None
            self.selected_piece = None
            self.valid_moves = []
            self.move_count = 0
            self.last_move = None
            self.move_made = False  # 标记玩家是否已移动
            self.wind_duration = 1
            self.max_wind_duration = 3
            self.initialize_board()
        
        def initialize_board(self):
            """初始化棋盘"""
            size = self.board_size
            pieces = self.pieces_per_player
            
            # 玩家A棋子放在顶部
            step = max(1, size // (pieces + 1))
            for i in range(pieces):
                pos = i * step + step // 2 + 1  # 向右移动一格
                if pos >= size:
                    pos = size - 1 - (i % (size // 2))
                self.board[0][pos] = Player.A
            
            # 玩家B棋子放在底部
            for i in range(pieces):
                pos = i * step + step // 2 + 1  # 向右移动一格
                if pos >= size:
                    pos = size - 1 - (i % (size // 2))
                self.board[size-1][pos] = Player.B
        
        def reset_game(self):
            """重置游戏"""
            self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
            self.wind_direction = random.choice(list(WindDirection))
            self.current_player = Player.A
            self.game_over = False
            self.winner = None
            self.selected_piece = None
            self.valid_moves = []
            self.move_count = 0
            self.last_move = None
            self.wind_duration = 1
            self.initialize_board()
        
        def change_wind(self):
            """改变风向"""
            if self.wind_duration < self.max_wind_duration and random.random() < 0.7:
                self.wind_duration += 1
            else:
                self.wind_direction = random.choice(list(WindDirection))
                self.wind_duration = 1
                return True
            return False
        
        def is_wind_eye(self, pos):
            """检查是否是风眼"""
            center = self.board_size // 2
            return pos == (center, center)
        
        def get_valid_moves(self, piece_pos):
            """获取某棋子的所有合法移动位置"""
            x, y = piece_pos
            player = self.board[y][x]
            if not player:
                return []
            
            valid_moves = []
            center = self.board_size // 2
            
            # 风眼位置可以自由移动
            if self.is_wind_eye((x, y)):
                directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
            elif self.wind_direction == WindDirection.HORIZONTAL:
                directions = [(-1,0), (1,0)]
            elif self.wind_direction == WindDirection.VERTICAL:
                directions = [(0,-1), (0,1)]
            elif self.wind_direction == WindDirection.DIAGONAL:
                directions = [(-1,-1), (-1,1), (1,-1), (1,1)]
            else:
                directions = []
            
            for dx, dy in directions:
                step = 1
                while True:
                    nx, ny = x + dx*step, y + dy*step
                    if not (0 <= nx < self.board_size and 0 <= ny < self.board_size):
                        break
                    if self.board[ny][nx] is not None:
                        break
                    valid_moves.append((nx, ny))
                    step += 1
            
            return valid_moves
        
        def get_all_valid_moves(self, player=None):
            """获取当前玩家的所有合法移动"""
            if player is None:
                player = self.current_player
            
            all_moves = []
            for y in range(self.board_size):
                for x in range(self.board_size):
                    if self.board[y][x] == player:
                        for to_pos in self.get_valid_moves((x, y)):
                            all_moves.append(((x, y), to_pos))
            return all_moves
        
        def select_piece(self, pos):
            """选择棋子"""
            x, y = pos
            if self.board[y][x] == self.current_player:
                self.selected_piece = pos
                self.valid_moves = self.get_valid_moves(pos)
                return True
            return False
        
        def deselect_piece(self):
            """取消选择"""
            self.selected_piece = None
            self.valid_moves = []
        
        def move_piece(self, from_pos, to_pos):
            """移动棋子"""
            from_x, from_y = from_pos
            to_x, to_y = to_pos
            
            if (to_x, to_y) not in self.valid_moves:
                return False
            
            self.board[to_y][to_x] = self.board[from_y][from_x]
            self.board[from_y][from_x] = None
            self.last_move = (from_pos, to_pos)
            self.move_count += 1
            self.move_made = True  # 标记玩家已移动
            
            # 检查胜利条件
            if self.check_win(self.current_player):
                self.game_over = True
                self.winner = self.current_player
                self.deselect_piece()
                return True
            
            # 切换玩家
            self.current_player = Player.B if self.current_player == Player.A else Player.A
            self.deselect_piece()
            
            return True
        
        def switch_player(self):
            """切换玩家"""
            self.current_player = Player.B if self.current_player == Player.A else Player.A
            self.deselect_piece()
        
        def check_win(self, player):
            """检查获胜条件 - 三子连线，且最多只有一颗棋子在底线上"""
            size = self.board_size
            bottom_line = 0 if player == Player.A else size - 1
            
            # 检查四个方向
            for y in range(size):
                for x in range(size - 2):
                    line = [(x+i, y) for i in range(3)]
                    if all(self.board[y][x+i] == player for i in range(3)):
                        bottom_count = sum(1 for px, py in line if py == bottom_line)
                        if bottom_count <= 1:
                            return True
            
            for x in range(size):
                for y in range(size - 2):
                    line = [(x, y+i) for i in range(3)]
                    if all(self.board[y+i][x] == player for i in range(3)):
                        bottom_count = sum(1 for px, py in line if py == bottom_line)
                        if bottom_count <= 1:
                            return True
            
            for x in range(size - 2):
                for y in range(size - 2):
                    line = [(x+i, y+i) for i in range(3)]
                    if all(self.board[y+i][x+i] == player for i in range(3)):
                        bottom_count = sum(1 for px, py in line if py == bottom_line)
                        if bottom_count <= 1:
                            return True
            
            for x in range(2, size):
                for y in range(size - 2):
                    line = [(x-i, y+i) for i in range(3)]
                    if all(self.board[y+i][x-i] == player for i in range(3)):
                        bottom_count = sum(1 for px, py in line if py == bottom_line)
                        if bottom_count <= 1:
                            return True
            
            return False
        
        def handle_click(self, pos):
            """处理棋盘点击"""
            x, y = pos
            
            # 如果已经选择了棋子，尝试移动
            if self.selected_piece is not None:
                if (x, y) in self.valid_moves:
                    self.move_piece(self.selected_piece, (x, y))
                    self.deselect_piece()
                    return True
                else:
                    self.deselect_piece()
                    if self.board[y][x] == self.current_player:
                        self.select_piece((x, y))
                    return False
            
            # 没有选择棋子，选择一个
            elif self.board[y][x] == self.current_player:
                self.select_piece((x, y))
            
            return False
        
        def has_any_valid_move(self, player=None):
            """检查是否有合法移动"""
            if player is None:
                player = self.current_player
            
            for y in range(self.board_size):
                for x in range(self.board_size):
                    if self.board[y][x] == player:
                        if self.get_valid_moves((x, y)):
                            return True
            return False
        
        # -------------------- AI 相关 --------------------
        def evaluate_position(self, pos, player):
            """评估位置价值"""
            x, y = pos
            center = self.board_size // 2
            
            score = 0
            distance = abs(x - center) + abs(y - center)
            score += (self.board_size - distance) * 2
            
            if self.is_wind_eye(pos):
                score += 50
            
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                        if self.board[ny][nx] == player:
                            score += 10
            
            return score
        
        def find_best_ai_move(self):
            """AI寻找最佳移动"""
            moves = self.get_all_valid_moves(Player.B)
            if not moves:
                return None
            
            best_moves = []
            best_score = float('-inf')
            
            for from_pos, to_pos in moves:
                score = self.evaluate_position(to_pos, Player.B)
                
                # 检查是否能获胜
                temp_board = [row[:] for row in self.board]
                temp_board[to_pos[1]][to_pos[0]] = Player.B
                temp_board[from_pos[1]][from_pos[0]] = None
                
                if self._check_win_on_board(temp_board, Player.B):
                    score += 1000
                
                # 检查是否阻止对手获胜
                if self._check_win_on_board(temp_board, Player.A):
                    score += 500
                
                # 阻挡和形成连线
                for dx, dy in [(1,0), (0,1), (1,1), (1,-1)]:
                    if self._count_line(temp_board, to_pos, dx, dy, Player.A) >= 2:
                        score += 100
                    if self._count_line(temp_board, to_pos, dx, dy, Player.B) >= 2:
                        score += 80
                
                score += random.random() * 5
                
                if score > best_score:
                    best_score = score
                    best_moves = [(from_pos, to_pos)]
                elif score == best_score:
                    best_moves.append((from_pos, to_pos))
            
            return random.choice(best_moves) if best_moves else None
        
        def _check_win_on_board(self, board, player):
            """检查某棋盘上某玩家是否获胜（三子连线且最多一颗在底线上）"""
            size = self.board_size
            bottom_line = 0 if player == Player.A else size - 1
            
            # 检查水平方向
            for y in range(size):
                for x in range(size - 2):
                    line = [(x+i, y) for i in range(3)]
                    if all(board[y][x+i] == player for i in range(3)):
                        bottom_count = sum(1 for px, py in line if py == bottom_line)
                        if bottom_count <= 1:
                            return True
            
            # 检查垂直方向
            for x in range(size):
                for y in range(size - 2):
                    line = [(x, y+i) for i in range(3)]
                    if all(board[y+i][x] == player for i in range(3)):
                        bottom_count = sum(1 for px, py in line if py == bottom_line)
                        if bottom_count <= 1:
                            return True
            
            # 检查主对角线方向
            for x in range(size - 2):
                for y in range(size - 2):
                    line = [(x+i, y+i) for i in range(3)]
                    if all(board[y+i][x+i] == player for i in range(3)):
                        bottom_count = sum(1 for px, py in line if py == bottom_line)
                        if bottom_count <= 1:
                            return True
            
            # 检查副对角线方向
            for x in range(2, size):
                for y in range(size - 2):
                    line = [(x-i, y+i) for i in range(3)]
                    if all(board[y+i][x-i] == player for i in range(3)):
                        bottom_count = sum(1 for px, py in line if py == bottom_line)
                        if bottom_count <= 1:
                            return True
            
            return False
        
        def _count_line(self, board, pos, dx, dy, player):
            """计算某方向上的连续棋子数"""
            x, y = pos
            size = self.board_size
            count = 0
            for step in [1, -1]:
                nx, ny = x + dx * step, y + dy * step
                while 0 <= nx < size and 0 <= ny < size:
                    if board[ny][nx] == player:
                        count += 1
                        nx += dx * step
                        ny += dy * step
                    else:
                        break
            return count
        
        def ai_make_move(self):
            """执行AI移动"""
            best_move = self.find_best_ai_move()
            if best_move:
                from_pos, to_pos = best_move
                # 先选择棋子并获取合法移动
                self.selected_piece = from_pos
                self.valid_moves = self.get_valid_moves(from_pos)
                # 调用 move_piece 处理移动、胜负检测、玩家切换和风向变化
                return self.move_piece(from_pos, to_pos)
            return False
        
        def get_wind_symbol(self):
            """获取风向符号"""
            if self.wind_direction == WindDirection.HORIZONTAL:
                return "←→"
            elif self.wind_direction == WindDirection.VERTICAL:
                return "↑↓"
            else:
                return "↗↙"
        
        def get_wind_color(self):
            """获取风向颜色"""
            if self.wind_direction == WindDirection.HORIZONTAL:
                return "#87ceeb"
            elif self.wind_direction == WindDirection.VERTICAL:
                return "#98fb98"
            else:
                return "#ffb6c1"

    # -------------------- 对话系统 --------------------
    class FengziDialogue:
        """风子的对话管理"""
        
        # ==================== 教程对话（原版完整移植）====================
        TUTORIAL = {
            "opening": [
                "啊，[player_name]前辈！你来啦～今天怎么这么早？",
                "诶？[player_name]前辈今天想学风之棋吗？太好了！我来教你吧！",
                "嘿嘿，能当[player_name]前辈的老师，这种机会可不多呢～"
            ],
            "experience_check": [
                "[player_name]前辈之前下过棋类游戏吗？我想知道要从哪里开始教你呢～",
            ],
            "no_exp": [
                "完全没下过吗？没关系！风之棋非常简单，我会一步步教[player_name]前辈的～",
                "放心交给风子我吧！包教包会！"
            ],
            "some_exp": [
                "下过一些简单的棋吗？那太好了！[player_name]前辈学起来会很快的～",
                "有基础的话，我们可以跳过一些基础内容呢～"
            ],
            "expert": [
                "诶？！[player_name]前辈是下棋高手吗？！那、那岂不是显得我很没用了...",
                "不、不过！风之棋可是很特别的哦！说不定[player_name]前辈也有很多不知道的地方呢～",
                "总之！请[player_name]前辈要认真听讲！不要小看我！"
            ],
            "board_intro": [
                "好啦好啦，我们开始吧！首先，让风子介绍一下棋盘～",
            ],
            "board_desc": [
                "看！这就是风之棋的棋盘！它由许多方格组成，每个位置都有坐标。",
                "横的是行，竖的是列。就像教室里的座位一样～",
                "[player_name]前辈平时坐第几排第几列呢？"
            ],
            "piece_intro": [
                "接下来是棋子～",
            ],
            "piece_desc": [
                "黑色圆点 ● 代表[player_name]前辈（玩家A），白色圆点 ○ 代表我（风子）。",
                "中间有个 ★ 标记的是风眼！这个位置超级重要哦！",
                "站在风眼上的棋子可以自由移动，想去哪儿就去哪儿！"
            ],
            "wind_demo": [
                "说到风之棋，最特别的就是【风】的规则了！",
                "风向一共有三种：水平风、垂直风、旋风！",
                "棋子必须按照风向移动哦！不能横穿风向！",
                "不过站在风眼上的棋子可以无视风向，自由移动！"
            ],
            "wind_demo_horizontal": [
                "首先是水平风！这时棋子只能左右移动～",
            ],
            "wind_demo_vertical": [
                "然后是垂直风！棋子只能上下移动～",
            ],
            "wind_demo_diagonal": [
                "最后是旋风！棋子只能斜着移动～",
            ],
            "wind_reminder": [
                "记住！棋子只能沿着风向移动！不能横穿风向哦！",
                "每次风向轮换后，要及时调整战术呢～"
            ],
            "wind_eye": [
                "对了[player_name]前辈！站在风眼（★）上的棋子可以自由移动！",
                "这是关键位置！控制风眼就等于控制了棋局的主动权！"
            ],
            "win_condition": [
                "获胜条件很简单！把自己的3个棋子连成一条直线！",
                "可以是横线、竖线，或者斜线都可以！",
                "就像井字棋一样简单，但又比井字棋有趣得多呢～"
            ],
            "move_demo": [
                "好了！现在我们来实际操作一下吧！",
                "[player_name]前辈，先选择一个你自己的棋子（●）的位置吧～",
            ],
            "move_success": [
                "很好很好！[player_name]前辈选对位置了！",
                "现在选择目标位置来移动棋子吧～"
            ],
            "move_execute": [
                "太棒了！[player_name]前辈完成第一次移动了！学得真快！"
            ],
            "move_no_valid": [
                "诶？这个位置暂时无法移动呢...",
                "没关系！换个位置试试吧～"
            ],
            "strategy_intro": [
                "[player_name]前辈，作为新手，风子有几点小技巧要告诉你～",
                "记住了这些，你就是下一个风之棋大师了！"
            ],
            "strategy_wind_eye": [
                "第一！控制风眼最重要！站在风眼上的棋子可以自由移动！",
            ],
            "strategy_wind": [
                "第二！注意风向变化！每次风向轮换后，战术要跟着调整！",
            ],
            "strategy_line": [
                "第三！时刻注意能不能把自己的三个棋子连成一条直线！",
            ],
            "strategy_block": [
                "第四！别忘了阻止对手连成一线！有时候防守比进攻更重要！",
            ],
            "strategy_mood": [
                "最后！下棋最重要的是开心，不要太在意输赢哦～",
                "能和[player_name]前辈一起下棋，风子就已经很开心了！"
            ],
            "quiz_intro": [
                "好了！理论讲完了，[player_name]前辈准备好接受考验了吗～",
                "嘻嘻，不要紧张！错了也没关系，我会一直陪着[player_name]前辈的！"
            ],
            "quiz_correct": [
                "真棒！[player_name]前辈答对了！不愧是[player_name]前辈呢～",
            ],
            "quiz_wrong": [
                "诶...这个答案不太对哦～[player_name]前辈再想想？",
                "不对不对...[player_name]前辈再试一次吧～",
                "哎呀，又错了呢...没关系，我们再来看一遍～"
            ],
            "quiz_troll_mode": [
                "哼！[player_name]前辈你该不会是故意的吧！",
                "怎么教都教不会！气死我了！",
                "你这个笨蛋[player_name]前辈！完全入戏了啊！...啊不对，我是说...",
                "咳咳！[player_name]前辈不要再逗我了！认真答题！"
            ],
            "quiz_complete": [
                "太好了[player_name]前辈！测验完成了！",
                "虽然中间有些小插曲...但是[player_name]前辈都通过了！",
                "现在[player_name]前辈已经掌握了风之棋的基本规则了！"
            ],
            "ending_setup": [
                "说起来，[player_name]前辈...我们的风棋社只有我们两个人呢。",
                "有时候会觉得很安静...但也很开心哦！",
                "能一直和[player_name]前辈一起下棋，风子就很满足了～"
            ],
            "ending_suggestion": [
                "对了[player_name]前辈！要是能再招一个人，我们就是一个正式社团了！",
                "到时候就可以举办比赛什么的了呢～",
            ],
            "ending_secret": [
                "（小声）...其实不想这样...",
                "（更小声）只想和[player_name]前辈两个人下棋...",
                "啊！没什么！[player_name]前辈什么都没听到！"
            ],
            "ending_tease": [
                "好啦好啦！教程结束！[player_name]前辈准备好和我来一盘真正的对决了吗！",
                "这次我可是不会手下留情的哦～哼哼！"
            ]
        }
        
        # ==================== 游戏内对话 ====================
        DIALOGUES = {
            "greeting": [
                "[player_name]前辈，你来啦~今天的风很舒服呢。",
                "啊，[player_name]前辈！等我很久了哦！",
                "[player_name]前辈~今天也要一起下棋吗？",
                "[player_name]前辈~今天来得比平时早呢~",
                "嘿嘿，[player_name]前辈来陪我了~",
                "等你好久啦，[player_name]前辈！"
            ],
            "game_start": [
                "哼哼，今天一定要赢过[player_name]前辈！",
                "来吧！我已经准备好了！",
                "[player_name]前辈，准备好迎接挑战了吗~",
                "今天的风向对我有利呢~",
                "来吧来吧！让我看看[player_name]前辈的实力！",
                "嘿嘿，我已经想到好策略了~"
            ],
            "my_turn": [
                "看我的！这一步可是经过深思熟虑的！",
                "风啊，回应我的呼唤吧！",
                "哼哼，有深意哦~",
                "这一步...让我想想...",
                "[player_name]前辈别催我，让我想想~",
                "风在告诉我答案呢~"
            ],
            "good_move": [
                "嘻嘻，这步棋不错吧！",
                "[player_name]前辈被我的智慧折服了吗？",
                "怎么样？是不是很意外？",
                "哼哼~这可是我的得意技！",
                "[player_name]前辈，你没想到我会这样走吧~",
                "这就是成长的力量！"
            ],
            "bad_move": [
                "哎呀...这步好像不太妙...",
                "呜...大意了...",
                "等等...让我再想想...",
                "啊...好像走错了...",
                "呜...[player_name]前辈不要笑我...",
                "我、我只是试探你而已！"
            ],
            "wind_change": [
                "风向变了呢...我的机会来了！",
                "新的风向，新的战术！",
                "风在指引我走向胜利！",
                "哦？风向变了~有趣！",
                "[player_name]前辈，跟上风的节奏吧！",
                "这阵风...会带我走向胜利吗？"
            ],
            "victory": [
                "耶！我赢了！[player_name]前辈看到了吗！",
                "胜利！这就是我的真正实力！",
                "哼哼，知道我的厉害了吧！",
                "哇哈哈哈！[player_name]前辈输了呢~",
                "[player_name]前辈，要请我吃冰淇淋哦~",
                "看到了吗！这就是我的实力！"
            ],
            "defeat": [
                "呜哇...输了...[player_name]前辈好过分...",
                "明明就差一点点的...",
                "今天的状态不太好...",
                "呜...我不服！再来！",
                "[player_name]前辈太厉害了...让我再挑战一次嘛！",
                "呜呜...我要哭了..."
            ],
            "tutorial_intro": [
                "啊，[player_name]前辈！今天让我来教你下风之棋吧！",
                "风之棋可是很有趣的游戏哦！",
                "放心交给风子我吧！包教包会！",
                "[player_name]前辈终于想学了吗~太好了！",
                "包在我身上！风子老师上线~"
            ],
            "tutorial_wind": [
                "风之棋最特别的就是【风】的规则了！",
                "风向一共有三种：水平风、垂直风、旋风！",
                "棋子必须按照风向移动哦！",
                "记住哦！棋子不能横穿风向！"
            ],
            "tutorial_wind_eye": [
                "对了[player_name]前辈！站在风眼上的棋子可以自由移动！",
                "这是关键位置！控制风眼就控制了全局！",
                "风眼就是棋盘正中央的那个位置~"
            ],
            "tutorial_win": [
                "获胜条件很简单！把自己的3个棋子连成一条直线！",
                "可以是横线、竖线，或者斜线~",
                "连成一条线就赢啦！"
            ],
            "encouragement": [
                "[player_name]前辈，让我们都发挥出全力吧！",
                "不管输赢，这都是宝贵的经历呢~",
                "能和[player_name]前辈对战，我很开心！"
            ]
        }
        
        # ==================== 28天聊天话题（原版完整移植+增加）====================
        TOPICS_28 = [
            # 第1天
            {
                "name": "初次见面",
                "category": "original",
                "day": 1,
                "conversations": [
                    {
                        "question": "[player_name]前辈...我们第一次见面的时候，你还记得吗？那时候我紧张得连话都说不利索了呢...",
                        "responses": [
                            ("当然记得，你当时自我介绍声音很小，脸红红的，特别可爱。", 5, "啊啊啊！[player_name]前辈不要说出来啦！那确实是我最紧张的一次..."),
                            ("有点记不清了，我们见过很多次了嘛。", -3, "呜...[player_name]前辈居然不记得了...明明那是我鼓起勇气第一次主动找你说话..."),
                            ("每一次见面我都记得，因为每次和你在一起都很特别。", 7, "前、[player_name]前辈！今天怎么这么会说话！我都不知道怎么回应了...")
                        ]
                    },
                    {
                        "question": "说起来，那时候我为什么要加入风棋社呢...明明我下棋也不厉害。",
                        "responses": [
                            ("是因为喜欢风棋这个游戏吧？", 4, "嗯...确实是因为喜欢游戏本身啦...不过后来发现，和[player_name]前辈一起下棋更有意思呢。"),
                            ("现在也还是不厉害哦，每次都输给我。", 5, "哼！[player_name]前辈不要得意！总有一天我会赢你的！"),
                            ("那现在为什么还留在这里呢？", 6, "那、那是因为...（小声）因为这里有[player_name]前辈在嘛，可以一起下棋。")
                        ]
                    }
                ]
            },
            # 第2天
            {
                "name": "海边学校预告",
                "category": "school",
                "day": 2,
                "conversations": [
                    {
                        "question": "[player_name]前辈[player_name]前辈！学校说要组织海边学校的活动呢！虽然是在海边进行学习，但听起来好有趣啊～[player_name]前辈会参加吗？",
                        "responses": [
                            ("当然去！可以看大海和日出，还有和大家一起的时光。", 5, "太好了！那我们明天可以一起在海边散步！听说还能捡贝壳呢～"),
                            ("有点远啊...不过有你在的话，我就去吧。", 5, "嘿嘿！[player_name]前辈最好了！放心，我会照顾好[player_name]前辈的！"),
                            ("不太感兴趣...不过如果你需要人陪的话...？", 4, "哼！[player_name]前辈明明就是想去吧！好啦好啦，那我们一起去！")
                        ]
                    },
                    {
                        "question": "啊，对了！海边学校的话，明天就要开始准备行李了！[player_name]前辈有没有什么想带的东西？",
                        "responses": [
                            ("防晒霜和帽子，大海边的太阳很毒的。", 5, "[player_name]前辈好细心！那我也带上防晒霜，我们一起不被晒黑！"),
                            ("相机！想拍下大海的风景。", 5, "好主意！那我要多拍几张照片带回来给[player_name]前辈看！"),
                            ("零食！在海边吃零食多惬意啊。", 4, "[player_name]前辈说得对！海边散步的时候配零食最棒了！")
                        ]
                    }
                ]
            },
            # 第3天
            {
                "name": "风棋的命名",
                "category": "philosophy",
                "day": 3,
                "conversations": [
                    {
                        "question": "[player_name]前辈...我在想一个问题...风棋为什么要叫'风'棋呢？明明棋子是按照风向移动的，但为什么不是'风向棋'或者'风动棋'呢？",
                        "responses": [
                            ("也许是因为下棋的时候，心要像风一样自由，不被束缚。", 6, "[player_name]前辈说得好好...心要像风一样...这样的话，不管风向怎么变，我们都能灵活应对呢！"),
                            ("我觉得是因为棋盘上的争斗要像风一样迅速、变化莫测。", 5, "有道理！风是看不见但能感受到的，就像棋盘上的形势变化一样呢！"),
                            ("这个...我也没想过，不如我们去问问老师？", 3, "也对哦...不过[player_name]前辈能和我一起想这个问题，我就很开心了～")
                        ]
                    },
                    {
                        "question": "[player_name]前辈...你说，棋子和棋手的关系是什么？棋子只能被动地移动，但棋手的思想却通过棋子表现出来...",
                        "responses": [
                            ("就像你和我的关系一样，我是棋手，你是棋子——不对，你是我的对手！", 6, "[player_name]前辈好奇怪！我是对手不是棋子啦！不过...我们下棋的时候，确实像是在对话呢..."),
                            ("棋子没有思想，但正是这种'被支配'的美感，才让棋类游戏有意思吧。", 5, "原来如此...所以我们下棋的时候，也是一种'美的创造'呢！"),
                            ("这个太哲学了...不如我们下一盘棋来思考这个问题？", 4, "哈哈！[player_name]前辈说得对！实践出真知！那我们开始吧！")
                        ]
                    }
                ]
            },
            # 第4天
            {
                "name": "兴趣爱好",
                "category": "original",
                "day": 4,
                "conversations": [
                    {
                        "question": "[player_name]前辈平时除了下棋，还喜欢做什么呢？我想多了解[player_name]前辈一点...",
                        "responses": [
                            ("喜欢看书，特别是推理小说，沉浸在解谜的世界里很有趣。", 5, "诶～推理小说！我也喜欢！可以猜凶手是谁，特别有意思！[player_name]前辈看过《金田一少年事件簿》吗？"),
                            ("喜欢看电影，特别是动画电影，画面和音乐都很美。", 5, "哇！动画电影！我也是！最近看的《你的名字》特别好看！[player_name]前辈有什么推荐的吗？"),
                            ("没什么特别的，下棋就是最大的爱好了。", 3, "这样啊...[player_name]前辈对风之棋真的是真爱呢！那我们一起加油吧！")
                        ]
                    },
                    {
                        "question": "我平时喜欢看漫画...[player_name]前辈会觉得我看漫画很幼稚吗？",
                        "responses": [
                            ("不会啊，漫画是很棒的艺术形式。", 5, "真的吗！太好了！[player_name]前辈不嫌弃最好了～"),
                            ("有点幼稚，不过没关系，开心就好。", 2, "哼...[player_name]前辈什么意思嘛..."),
                            ("你喜欢看什么类型的？我也想看看。", 6, "真、真的吗！[player_name]前辈愿意陪我一起看？那我推荐[player_name]前辈一些超好看的！")
                        ]
                    }
                ]
            },
            # 第5天
            {
                "name": "海边学校回忆",
                "category": "school",
                "day": 5,
                "conversations": [
                    {
                        "question": "[player_name]前辈～还记得上次海边学校的活动吗？我们在沙滩上捡了好多贝壳呢！我还做了一个贝壳风铃送给[player_name]前辈～",
                        "responses": [
                            ("记得！我一直把它挂在房间里呢，风吹过的时候就会叮叮当当响。", 6, "真的吗！太好了！我还以为[player_name]前辈会丢掉呢...（感动）"),
                            ("贝壳风铃还在，不过有点积灰了...（心虚）", 2, "哼！[player_name]前辈要好好珍惜！我可是花了好久的！"),
                            ("那个风铃声很好听，让我想起在海边的时光。", 6, "[player_name]前辈...我也是，每次听到那个声音，就会想起我们一起在海边的日子～")
                        ]
                    },
                    {
                        "question": "对了[player_name]前辈，海边学校的时候，有个男生问我和[player_name]前辈是什么关系呢～[player_name]前辈觉得我们是什么关系呀？",
                        "responses": [
                            ("是下棋的对手，也是朋友吧。", 5, "嗯！说得对！我们是对手，也是朋友～"),
                            ("是风棋社的社员关系呀，还能是什么？", 4, "[player_name]前辈好迟钝...算啦算啦，我们确实是在风棋社认识的嘛～"),
                            ("我觉得是特别的...（想了想）可以一起参加活动的朋友？", 6, "特别的朋友...[player_name]前辈说得我都有点害羞了呢～")
                        ]
                    }
                ]
            },
            # 第6天
            {
                "name": "胜负之道",
                "category": "philosophy",
                "day": 6,
                "conversations": [
                    {
                        "question": "[player_name]前辈...我最近在想一个问题...下棋的时候，输赢真的很重要吗？如果每次都输，那下棋还有什么意义呢？",
                        "responses": [
                            ("重要的不是输赢，而是下棋的过程，和你在一起的时间。", 7, "前、[player_name]前辈...说得好好...下棋的过程确实比结果更重要呢..."),
                            ("输了就要反省，下次赢回来，输赢当然重要！", 5, "[player_name]前辈说得对！输了不可怕，可怕的是不知道为什么输！"),
                            ("有时候输也是一种学习吧，不过我更想赢你。", 5, "哼！那我们就是永远的对手了！不过...偶尔让让我也没关系啦...")
                        ]
                    },
                    {
                        "question": "[player_name]前辈...你觉得，下棋的最终境界是什么？是计算到每一步，还是随心所欲地下棋呢？",
                        "responses": [
                            ("我觉得是'无招胜有招'，不用刻意计算，凭直觉下棋。", 6, "无招胜有招...[player_name]前辈说得好深奥！不过我觉得下棋最重要的是开心～"),
                            ("计算是基础，但最终要超越计算，达到'棋感'的境界。", 5, "棋感...我好像懂一点...就是有时候觉得这一步'应该'这么走的感觉吗？"),
                            ("我觉得是下棋的时候那种专注的感觉，和对手之间的默契。", 7, "[player_name]前辈说得好好...原来下棋还有这么多学问呢～")
                        ]
                    }
                ]
            },
            # 第7天
            {
                "name": "甜点喜好",
                "category": "original",
                "day": 7,
                "conversations": [
                    {
                        "question": "[player_name]前辈喜欢吃什么甜点呢？我最近在学做甜点...如果[player_name]前辈告诉我，说不定我可以做给[player_name]前辈吃哦！",
                        "responses": [
                            ("冰淇淋，特别是香草味的，甜甜的又不会太腻。", 5, "哇！我也是！[player_name]前辈我们口味好像！下次一起去吃冰淇淋吧！"),
                            ("草莓蛋糕！酸酸甜甜的，很好吃。", 5, "草莓蛋糕！我也喜欢！不过[player_name]前辈说初恋是什么意思...好害羞..."),
                            ("只要是甜的我都喜欢，风子同学请客的话。", 4, "哼！[player_name]前辈就想着让我请客！真是的...")
                        ]
                    },
                    {
                        "question": "啊！对了[player_name]前辈，我昨天做了一个布丁，想拿来给[player_name]前辈尝尝...但是我怕[player_name]前辈觉得不好吃。",
                        "responses": [
                            ("不管好不好吃，我都愿意尝，因为是风子同学做的。", 7, "前、[player_name]前辈！不要这样说啦！我会不好意思的！不过...我会努力做好的！"),
                            ("拿来吧，我可是很严格的哦。", 4, "呜...[player_name]前辈好严格...但是我也不会放弃的！"),
                            ("你的心意比味道更重要。", 6, "[player_name]前辈...（脸红）那、那我一定会努力做好的！")
                        ]
                    }
                ]
            },
            # 第8天
            {
                "name": "林间学校预告",
                "category": "school",
                "day": 8,
                "conversations": [
                    {
                        "question": "[player_name]前辈～这次轮到林间学校了！是在森林里进行的学习活动哦～听说要在森林里露营，还要自己生火做饭呢！[player_name]前辈会去吗？",
                        "responses": [
                            ("当然去！森林里的空气一定很清新，和城市不一样。", 5, "太好了！我听说森林里有很多小动物，说不定能看到松鼠呢！"),
                            ("露营啊...我怕虫子...但是有你在的话...算了，去吧！", 5, "[player_name]前辈别怕！到时候我帮你赶虫子！嘻嘻～"),
                            ("听起来很有趣，不过自己做饭...你能行吗？", 3, "哼！[player_name]前辈小看人！我、我虽然不太会做饭，但是可以学嘛！")
                        ]
                    },
                    {
                        "question": "对了对了！林间学校有个活动叫'森林寻宝'，就是要在森林里找隐藏的宝物！[player_name]前辈要不要和我组队呀？",
                        "responses": [
                            ("好啊，我们组队！明天一起在森林里探险！", 6, "耶！[player_name]前辈答应了！那我们要取个队名才行！就叫'风棋二人组'怎么样！"),
                            ("宝物是什么呀？该不会是虫子吧...（害怕）", 2, "哈哈哈[player_name]前辈好胆小！放心啦，是学校准备的纪念品啦～"),
                            ("和你组队的话，我会好好保护你的。", 5, "[player_name]前辈...哼，我又不是小孩子！不过...谢谢[player_name]前辈啦～")
                        ]
                    }
                ]
            },
            # 第9天
            {
                "name": "时间与棋",
                "category": "philosophy",
                "day": 9,
                "conversations": [
                    {
                        "question": "[player_name]前辈...我有时候在想，为什么古人要发明棋这种游戏呢？明明可以聊天、赏花、观月...为什么要坐在那里盯着棋盘看呢？",
                        "responses": [
                            ("也许是因为，在下棋的那一刻，时间仿佛静止了，我们可以暂时忘记世俗的烦恼。", 6, "[player_name]前辈说得好好...下棋的时候，世界好像只剩下棋盘和[player_name]前辈...好神奇的感觉..."),
                            ("因为下棋是思考的载体，通过棋局可以展现智慧和创造力。", 5, "原来如此...那我们下棋的时候，也是在进行艺术创作呢！"),
                            ("因为有你在啊，没有你的话，我才不想下棋呢。", 7, "前、[player_name]前辈！不要老是突然说这种话啦！...不过我很开心呢～")
                        ]
                    },
                    {
                        "question": "[player_name]前辈...如果我们下棋下到天黑，都忘记吃饭了怎么办？",
                        "responses": [
                            ("那我就做饭给你吃，虽然不太好吃...但保证能填饱肚子。", 6, "[player_name]前辈会做饭！那、那我下次输了也要[player_name]前辈做饭给我吃！"),
                            ("那就说明我们下棋太专注了，不过我会记得照顾你的。", 6, "[player_name]前辈...你、你对我真的很好呢...那、那我也给[player_name]前辈准备宵夜！"),
                            ("那就饿着吧，反正你的肚子会叫的。", 3, "哼！[player_name]前辈坏蛋！不过...[player_name]前辈饿了我也会心疼的...")
                        ]
                    }
                ]
            },
            # 第10天
            {
                "name": "天气话题",
                "category": "original",
                "day": 10,
                "conversations": [
                    {
                        "question": "今天天气真好呢，[player_name]前辈喜欢晴天还是雨天？晴天的话我们可以去外面走走，雨天的话...一起在窗边听雨也不错？",
                        "responses": [
                            ("晴天，阳光明媚让人心情好，可以一起去公园散步。", 5, "嗯嗯！我也是！晴天最适合散步了！[player_name]前辈想去哪个公园？"),
                            ("雨天，听着雨声很宁静，在室内下棋特别有氛围。", 5, "[player_name]前辈好浪漫！雨天确实很有意境呢～我们可以煮杯热可可一起下棋～"),
                            ("都喜欢，各有各的美。", 6, "[player_name]前辈说得对！每个天气都有它的魅力呢～")
                        ]
                    },
                    {
                        "question": "说起来...[player_name]前辈有没有想过，我们第一次见面是在什么样的天气呢？",
                        "responses": [
                            ("是个雨天，你撑着伞在走廊上，很可爱的样子。", 6, "啊！[player_name]前辈居然记得！我那时候还怕伞被风吹翻呢..."),
                            ("是个晴天，阳光照在你头发上，很耀眼。", 6, "前、[player_name]前辈...我的头发哪有阳光那么耀眼啦..."),
                            ("记不清了，但一定是很特别的一天。", 5, "嗯...对[player_name]前辈来说可能不特别，但对我来说，那一天改变了一切呢...")
                        ]
                    }
                ]
            },
            # 第11天
            {
                "name": "雪中学校预告",
                "category": "school",
                "day": 11,
                "conversations": [
                    {
                        "question": "[player_name]前辈[player_name]前辈！这次是雪中学校！去雪山上的学校哦～可以滑雪、打雪仗，还有冰雕展！听起来超好玩的！",
                        "responses": [
                            ("滑雪！我想教你，如果你在雪地里摔倒的话。", 6, "哼！我才不会摔倒呢！不过...如果[player_name]前辈想教我的话...我也不是不可以学啦..."),
                            ("打雪仗！我要和风子组队！", 5, "好！我们要打遍全班！不对，是全校！"),
                            ("冰雕展听起来不错，不过雪地里很冷，你要多穿点。", 5, "[player_name]前辈好贴心！那我穿得暖暖的，让[player_name]前辈看看我可爱的样子！")
                        ]
                    },
                    {
                        "question": "啊！对了！明天去雪中学校的时候，我们可以一起堆雪人！我要堆一个[player_name]前辈的雪人！",
                        "responses": [
                            ("那我要堆一个风子的雪人，看看谁堆得更像！", 6, "好！比赛开始！不过[player_name]前辈的雪人肯定没我的可爱！"),
                            ("堆雪人啊...我小时候堆过一个，后来化了，好伤心。", 4, "那这次我们堆一个不会化的！用冰雕的方法！这样就能一直保存了！"),
                            ("比起雪人，我更想和风子一起看雪景。", 6, "前、[player_name]前辈...（脸红）那、那我们找个好看的背景一起看雪吧...")
                        ]
                    }
                ]
            },
            # 第12天
            {
                "name": "棋如人生",
                "category": "philosophy",
                "day": 12,
                "conversations": [
                    {
                        "question": "[player_name]前辈...你说，下棋和人生有什么相似的地方呢？我觉得...下棋的时候，有时候要放弃一些棋子才能保住大局...",
                        "responses": [
                            ("就像人生，有时候要放弃一些东西，才能得到更重要的。", 6, "[player_name]前辈说得好好...那[player_name]前辈愿意为了什么而放弃什么呢？"),
                            ("不过下棋和人生不同的是，下棋可以重来，人生却不能。", 5, "是啊...所以我们要珍惜每一盘棋，每一个相遇..."),
                            ("我觉得最重要的是下棋的时候有人陪伴，不孤独。", 6, "[player_name]前辈...（感动）我也是，有[player_name]前辈陪着我下棋，很开心呢...")
                        ]
                    },
                    {
                        "question": "[player_name]前辈...我突然想到一个问题...如果人生是一盘棋，那谁是棋手，谁是棋子呢？",
                        "responses": [
                            ("我觉得我们是彼此的棋手，也是彼此的棋子，互相影响。", 6, "[player_name]前辈...说得好好...那我们就是共同创造了这一局人生棋呢..."),
                            ("也许我们自己既是棋手也是棋子吧。", 5, "有道理...我们既要思考，也要行动...这就是人生吧..."),
                            ("这个问题太深奥了，不如我们边下棋边想。", 4, "好！那我们开始吧！也许下一盘棋就能找到答案呢！")
                        ]
                    }
                ]
            },
            # 第13天
            {
                "name": "音乐喜好",
                "category": "original",
                "day": 13,
                "conversations": [
                    {
                        "question": "[player_name]前辈喜欢什么样的音乐呢？我平时喜欢听流行歌曲，特别是那些旋律好听的～",
                        "responses": [
                            ("轻音乐，让人放松，下棋的时候听特别合适。", 5, "我也是！下棋的时候听轻音乐最棒了！有推荐的吗？"),
                            ("古典音乐，优雅又有深度，像在讲述故事一样。", 5, "[player_name]前辈好有品位！古典音乐确实很棒！"),
                            ("你推荐的音乐应该都很好听。", 6, "真的吗！那我一定要给[player_name]前辈推荐几首我最爱的！")
                        ]
                    },
                    {
                        "question": "对了[player_name]前辈！学校文化祭的时候会有乐队演出哦，[player_name]前辈要和我一起去听吗？",
                        "responses": [
                            ("好啊，到时候你请我喝饮料。", 4, "哼！[player_name]前辈好狡猾！好吧好吧，我请！"),
                            ("好啊，我也想听听你喜欢的音乐。", 6, "太好了！那我一定要带[player_name]前辈去最好听的那个乐队！"),
                            ("看情况吧，如果有空的话。", 2, "这样啊...那[player_name]前辈一定要来哦！我会很期待的！")
                        ]
                    }
                ]
            },
            # 第14天
            {
                "name": "体检日",
                "category": "school",
                "day": 14,
                "conversations": [
                    {
                        "question": "[player_name]前辈...明天是学校体检日...我、我有点紧张...抽血什么的，最讨厌了...",
                        "responses": [
                            ("别怕，我陪你一起，如果你害怕的话，可以握着我的手。", 7, "前、[player_name]前辈...（小声）那我、我就放心了...不过[player_name]前辈不许笑话我！"),
                            ("体检而已嘛，又不是考试，有什么好紧张的？", 3, "[player_name]前辈不懂啦！打针很痛的！而且还要量身高体重...好羞耻..."),
                            ("我也很怕抽血...我们明天一起鼓起勇气吧！", 6, "真的吗！原来[player_name]前辈也怕！那我们互相加油！一定可以的！")
                        ]
                    },
                    {
                        "question": "说起来...体检报告上会写身高体重呢...[player_name]前辈会不会看到我的体重啊...好担心...",
                        "responses": [
                            ("不管是多少，健康就好。", 5, "[player_name]前辈说得对！健康最重要！我要好好锻炼身体！"),
                            ("比起体重，我更关心你的健康报告是否正常。", 6, "[player_name]前辈...你、你真的是很温柔的人呢...谢谢你关心我..."),
                            ("放心啦，体检是保密的，谁也看不到啦。", 4, "真的吗！太好了！那我就放心了！[player_name]前辈懂得好多啊～")
                        ]
                    }
                ]
            },
            # 第15天
            {
                "name": "风与自由",
                "category": "philosophy",
                "day": 15,
                "conversations": [
                    {
                        "question": "[player_name]前辈...你说，风是什么感觉呢？我总是觉得，风就像自由的化身，没有形状，没有边界...",
                        "responses": [
                            ("风是看不见的，但能感受到它的存在。就像有些东西，虽然看不见，但很重要。", 6, "[player_name]前辈说得好好...就像我们下棋时的默契一样，虽然看不见，但能感受到～"),
                            ("风是变化的象征，告诉我们没有什么是永恒不变的。", 5, "有道理...所以我们要学会适应变化呢～"),
                            ("风是温柔的，抚摸着脸颊；也是狂暴的，吹倒大树。我觉得这就像...人的情绪一样。", 6, "[player_name]前辈...说得好好...有时候我觉得自己就像一阵风，飘忽不定...")
                        ]
                    },
                    {
                        "question": "[player_name]前辈...那你觉得，风棋里的'风'，代表的是自由还是束缚呢？",
                        "responses": [
                            ("是规则中的自由吧，在限制中寻找最大的可能性。", 6, "原来如此...所以我们下棋的时候，要学会在规则中找到自由的走法～"),
                            ("我觉得是变化的魅力，因为风一直在变，棋局也一直在变。", 5, "说得好好！所以我们不能一成不变，要随时准备应对新的情况～"),
                            ("是命运吧...风向决定了棋子的去向，就像命运决定了我们的人生。", 6, "[player_name]前辈...这个话题有点沉重呢...不过我觉得，虽然命运决定了我们的方向，但我们可以选择怎么面对它～")
                        ]
                    }
                ]
            },
            # 第16天
            {
                "name": "未来梦想",
                "category": "original",
                "day": 16,
                "conversations": [
                    {
                        "question": "[player_name]前辈将来想成为什么样的人呢？我...我想听[player_name]前辈说说未来的事...",
                        "responses": [
                            ("想成为职业棋手，和你一起参加比赛，站在领奖台上。", 7, "前、[player_name]前辈！我们一起努力！到时候我就是[player_name]前辈的对手了！哼哼～"),
                            ("还没想好，走一步看一步吧。", 2, "这样啊...不过[player_name]前辈这么厉害，一定能找到自己的路！"),
                            ("想一直过安稳的生活，和喜欢的人在一起。", 6, "安稳的生活也很好呢...和喜欢的人在一起...[player_name]前辈说的是谁呢...")
                        ]
                    },
                    {
                        "question": "我呢...其实我的梦想是成为最强的风棋手！但是...但是如果能和[player_name]前辈一直这样下棋，也很好呢。",
                        "responses": [
                            ("那就两个梦想都实现吧，强者的同时，也能和我下棋。", 7, "[player_name]前辈说得对！我要努力变强，同时也要和[player_name]前辈一起下棋！"),
                            ("追求梦想很重要，我支持你。", 6, "谢谢[player_name]前辈！有[player_name]前辈支持我，我一定能做到的！"),
                            ("下棋不是梦想的一部分吗？", 6, "啊...[player_name]前辈说得对...下棋当然是最重要的！和[player_name]前辈下棋最重要！")
                        ]
                    }
                ]
            },
            # 第17天
            {
                "name": "考试合泊",
                "category": "school",
                "day": 17,
                "conversations": [
                    {
                        "question": "[player_name]前辈～学校要举办考试合泊呢！就是考试前大家一起在学校复习、住宿的活动～虽然听起来很累，但是可以大家一起学习！",
                        "responses": [
                            ("那我来教你数学吧，我的数学还不错。", 6, "真的吗！太好了！我的数学一直不太好...[player_name]前辈肯教我的话，我一定认真学！"),
                            ("大家一起熬夜复习...你不怕我看到你困的样子吗？", 4, "哼！我才不会困呢！不过...如果[player_name]前辈给我递杯咖啡的话...也不是不可以..."),
                            ("一起努力吧，我也想看看你认真复习的样子。", 5, "[player_name]前辈...那、那我明天一定要好好表现！让[player_name]前辈看到我努力的样子！")
                        ]
                    },
                    {
                        "question": "啊对了对了！考试合泊的话，晚上会有宵夜时间哦！听说有关东煮！我最喜欢吃关东煮里的鸡蛋和萝卜了！[player_name]前辈喜欢吃什么？",
                        "responses": [
                            ("鸡蛋和萝卜啊...和某人一样呢。那我就选年糕和鱼丸吧。", 5, "哇！我们喜欢的都很好吃！明天晚上一起去吃宵夜吧！"),
                            ("比起关东煮，我更想看你吃宵夜的样子。", 6, "前、[player_name]前辈！不要老是盯着我看啦！不过...如果你想看的话，我可以多吃一点给你看..."),
                            ("在学校露营的感觉...确实有点怪怪的，不过有宵夜就够啦！", 5, "嘻嘻！[player_name]前辈说得对！不过我觉得只要和[player_name]前辈在一起，在哪里都很好玩呢～")
                        ]
                    }
                ]
            },
            # 第18天
            {
                "name": "孤独与陪伴",
                "category": "philosophy",
                "day": 18,
                "conversations": [
                    {
                        "question": "[player_name]前辈...我有时候会想，一个人下棋是什么感觉呢？没有人说话，没有人对手...一定很孤独吧...",
                        "responses": [
                            ("所以我才来找你下棋呀，不想一个人下棋。", 7, "[player_name]前辈...（感动）我也不想一个人下棋...有[player_name]前辈在，我就开心了～"),
                            ("一个人下棋也是一种修行吧，可以静下心来思考。", 5, "说得好好...不过我还是喜欢和[player_name]前辈一起下棋的感觉～"),
                            ("孤独是人生的常态，但有你这个对手，我觉得很幸运。", 6, "[player_name]前辈...（脸红）我、我也觉得有[player_name]前辈这个对手很幸运呢～")
                        ]
                    },
                    {
                        "question": "[player_name]前辈...你觉得，棋子和棋手，谁更孤独呢？",
                        "responses": [
                            ("是棋手吧...棋子至少可以和其他棋子在一起，但棋手只能一个人做决定。", 6, "[player_name]前辈...那我觉得[player_name]前辈不是孤独的，因为有我陪着[player_name]前辈呀～"),
                            ("我觉得是棋子吧...被支配着行动，不能自主。", 5, "所以我们要珍惜每一个棋子的位置，让它们发挥最大的作用呢～"),
                            ("都不孤独吧，因为有彼此的存在。", 6, "[player_name]前辈...说得好好...就像我们下棋一样，有对手才有意义呢～")
                        ]
                    }
                ]
            },
            # 第19天
            {
                "name": "食物偏好",
                "category": "original",
                "day": 19,
                "conversations": [
                    {
                        "question": "[player_name]前辈喜欢吃什么料理？",
                        "responses": [
                            ("日式料理，清淡健康", 5, "我也是！寿司和天妇罗都很好吃！"),
                            ("中华料理，味道丰富", 4, "中华料理确实很棒！特别是小笼包！"),
                            ("西餐，特别是意大利面", 5, "意大利面！我也喜欢！奶油培根口味的最棒了！")
                        ]
                    },
                    {
                        "question": "[player_name]前辈会做饭吗？",
                        "responses": [
                            ("会一点简单的", 5, "会做饭的[player_name]前辈很厉害呢！"),
                            ("不太会做饭", 2, "没关系！我可以学做饭给[player_name]前辈吃！"),
                            ("完全不会", -1, "诶？做饭很有趣的！[player_name]前辈可以试试！")
                        ]
                    }
                ]
            },
            # 第20天
            {
                "name": "交际舞会",
                "category": "school",
                "day": 20,
                "conversations": [
                    {
                        "question": "[player_name]前辈...下个月学校有交际舞会呢...要穿正装参加，还要和同学跳舞...[player_name]前辈会参加吗？",
                        "responses": [
                            ("会啊，你穿礼服一定很好看。", 6, "前、[player_name]前辈...那、那我明天就去挑礼服！[player_name]前辈要好好期待哦！"),
                            ("跳舞啊...我是男生，和男生跳舞？", 4, "对呀！[player_name]前辈，我们是男生和男生跳舞。不过...如果[player_name]前辈想牵女孩子的手的话...我、我也可以啦...（小声）"),
                            ("不太擅长跳舞...但是如果你需要舞伴的话...？", 5, "真的吗！那我们明天开始练习吧！我、我也不想和别的女孩子跳舞...")
                        ]
                    },
                    {
                        "question": "说起来...交际舞是要男生和男生一起跳的。不过[player_name]前辈...如果可以选舞伴的话，[player_name]前辈想和谁一起跳呢？",
                        "responses": [
                            ("当然是你啊，难道还有别的选择吗？", 7, "前、[player_name]前辈！！（脸红到耳根）我、我也想和[player_name]前辈跳！...啊不对，[player_name]前辈还没回答呢！！"),
                            ("还没想好，让我再考虑考虑。", -2, "呜...[player_name]前辈好过分！...算、算了啦，反正交际舞是男生和男生跳的嘛！"),
                            ("你想和学长跳舞吗？（吃醋）", 5, "哈？学长？[player_name]前辈在说什么呀！我们是男生和男生跳舞啦！...不过[player_name]前辈吃醋的样子...嘻嘻，好可爱～")
                        ]
                    }
                ]
            },
            # 第21天
            {
                "name": "风之呼吸",
                "category": "philosophy",
                "day": 21,
                "conversations": [
                    {
                        "question": "[player_name]前辈...你说，为什么风之棋的棋盘是方形的呢？明明风是流动的，用圆形不是更合适吗？",
                        "responses": [
                            ("也许正是因为风是流动的，才需要用方正的棋盘来'框住'它，让它变得可以控制。", 6, "[player_name]前辈说得好好...就像我们的人生一样，虽然充满变化，但也要有规则来约束～"),
                            ("方形代表稳定吧，风虽然流动，但下棋的时候需要稳定的思考。", 5, "说得好好！所以下棋的时候要保持冷静，不能被风向带偏～"),
                            ("这个...我没想过，也许只是习惯吧。", 3, "哈哈[player_name]前辈好直接！不过也许你说得对，有时候不需要想太多～")
                        ]
                    },
                    {
                        "question": "[player_name]前辈...我突然想到，如果我们下棋的时候风突然停了，会怎样呢？",
                        "responses": [
                            ("那棋子就不能移动了吧，游戏就结束了。", 5, "是啊...所以我们要珍惜每一阵风，每一个下棋的机会呢～"),
                            ("风停了，但棋局还在继续，就像人生的困境中也要继续前行。", 6, "[player_name]前辈说得好好...就算遇到困难，我们也要像下棋一样，一步一步走下去～"),
                            ("那我们就创造新的风，让棋局继续下去。", 6, "说得好好！这就是风之棋的精神吧——就算风向变了，我们也要找到新的出路～")
                        ]
                    }
                ]
            },
            # 第22天
            {
                "name": "季节喜好",
                "category": "original",
                "day": 22,
                "conversations": [
                    {
                        "question": "[player_name]前辈最喜欢哪个季节呢？",
                        "responses": [
                            ("春天，樱花盛开很美", 5, "春天确实很美呢！樱花飘落的时候特别浪漫！"),
                            ("夏天，可以穿浴衣去祭典", 5, "祭典！我也喜欢！有好多好吃的和好玩的！"),
                            ("秋天，枫叶很漂亮", 5, "枫叶！红色的枫叶像火焰一样，很美呢！"),
                            ("冬天，可以看雪景", 6, "冬天确实很浪漫呢...不过要小心不要感冒了！")
                        ]
                    },
                    {
                        "question": "[player_name]前辈觉得哪个季节最适合下棋？",
                        "responses": [
                            ("春天，气候宜人", 5, "春天确实很适合呢！不冷也不热！"),
                            ("秋天，天气凉爽", 5, "秋天！我也觉得最适合下棋了！"),
                            ("冬天，室内很温暖", 4, "冬天！在温暖的房间里下棋确实很棒！"),
                            ("只要和你一起，什么季节都适合", 7, "前、[player_name]前辈！今天特别会说话呢...")
                        ]
                    }
                ]
            },
            # 第23天
            {
                "name": "感谢陪伴",
                "category": "original",
                "day": 23,
                "conversations": [
                    {
                        "question": "[player_name]前辈...谢谢你一直陪我下棋。说实话，我一开始只是想找一个对手，没想到会遇到[player_name]前辈这样温柔的人...",
                        "responses": [
                            ("我才要谢谢你，有你在，下棋变得更有意义了。", 7, "前、[player_name]前辈...我、我会一直陪着[player_name]前辈下棋的！"),
                            ("不用谢，和你在一起我也很开心。", 6, "[player_name]前辈...那我们以后也要一直在一起下棋哦！"),
                            ("风子...我也想谢谢你教会我的东西。", 6, "[player_name]前辈...（感动）那、那我们要继续一起下棋哦！")
                        ]
                    },
                    {
                        "question": "说起来...[player_name]前辈有没有后悔过和我下棋呢？毕竟我总是输...有时候会想，[player_name]前辈和更强的对手下会不会更有意思...",
                        "responses": [
                            ("从来没有，和你下棋的每一局都是独一无二的。", 7, "前、[player_name]前辈！！我会努力的！总有一天我会赢[player_name]前辈的！"),
                            ("比起赢，我更喜欢看到你认真的样子。", 7, "[player_name]前辈...你这样说...我会不好意思的...但是我会继续努力的！"),
                            ("你不需要变强，做你自己就好。", 6, "[player_name]前辈...谢谢[player_name]前辈...我会继续努力的！")
                        ]
                    }
                ]
            },
            # 第24天
            {
                "name": "回忆往事",
                "category": "original",
                "day": 24,
                "conversations": [
                    {
                        "question": "[player_name]前辈，我们第一次下棋的时候你是什么感觉？",
                        "responses": [
                            ("觉得你很可爱，但棋艺不错", 6, "诶？！前、[player_name]前辈说我可爱..."),
                            ("觉得你是个有趣的对手", 5, "有趣的对手！我会继续努力的！"),
                            ("心跳加速，不知道为什么", 7, "前、[player_name]前辈！不要说这种让人害羞的话啦！")
                        ]
                    },
                    {
                        "question": "[player_name]前辈还记得我赢你的那一次吗？",
                        "responses": [
                            ("记得，你笑得很开心", 6, "啊！[player_name]前辈记得！我确实很开心！"),
                            ("不记得了，你赢过我吗？", -3, "呜...[player_name]前辈居然不记得了..."),
                            ("记得，你当时很得意", 5, "诶嘿！因为赢了[player_name]前辈嘛！")
                        ]
                    }
                ]
            },
            # 第25天
            {
                "name": "日常习惯",
                "category": "original",
                "day": 25,
                "conversations": [
                    {
                        "question": "[player_name]前辈有什么特别的小习惯吗？",
                        "responses": [
                            ("思考的时候会摸下巴", 5, "啊！我注意到了！[player_name]前辈确实有这个习惯！"),
                            ("紧张的时候会搓手", 5, "我也注意到了！[player_name]前辈很可爱呢！"),
                            ("喜欢偷偷看你下棋的样子", 7, "诶？！前、[player_name]前辈！")
                        ]
                    },
                    {
                        "question": "[player_name]前辈平时运动吗？",
                        "responses": [
                            ("偶尔跑步，保持健康", 5, "[player_name]前辈好健康！我也要运动起来！"),
                            ("喜欢游泳，感觉很自由", 5, "游泳！我也喜欢！像鱼一样自由！"),
                            ("和你一起的话，什么运动都喜欢", 6, "前、[player_name]前辈！不要说这种让人害羞的话啦！")
                        ]
                    }
                ]
            },
            # 第26天
            {
                "name": "共同成长",
                "category": "philosophy",
                "day": 26,
                "conversations": [
                    {
                        "question": "[player_name]前辈...你觉得，这段时间以来，我们有什么变化吗？",
                        "responses": [
                            ("从陌生人变成了...可以一起下棋的朋友吧。", 6, "嗯！说得好好！我们从对手变成了朋友呢～"),
                            ("下棋的水平都提高了吧。", 5, "是啊！和[player_name]前辈下棋真的让我进步很多呢～"),
                            ("默契越来越好了，有时候不用说就知道对方在想什么。", 7, "[player_name]前辈...（脸红）我、我也这么觉得呢～")
                        ]
                    },
                    {
                        "question": "[player_name]前辈...以后我们也要一直这样下棋下去哦，这是我们的约定！",
                        "responses": [
                            ("好，这是我们的约定。", 6, "约定达成！（伸出小指）来，拉钩！"),
                            ("当然，不管发生什么，我都不会忘记和你下棋的时光。", 7, "[player_name]前辈...我、我也一样...永远都不会忘记..."),
                            ("那你要变强一点，不然每次都输给我的约定有什么意思。", 4, "哼！[player_name]前辈你等着！我一定会变强的！")
                        ]
                    }
                ]
            },
            # 第27天
            {
                "name": "小确幸",
                "category": "original",
                "day": 27,
                "conversations": [
                    {
                        "question": "[player_name]前辈...今天阳光好好啊～在窗边晒太阳好舒服～[player_name]前辈有没有什么觉得很幸福的时刻？",
                        "responses": [
                            ("和你下棋的时候，就是我最幸福的时刻。", 7, "前、[player_name]前辈！！（心跳加速）我、我也一样！和[player_name]前辈下棋是最幸福的事！"),
                            ("吃好吃的东西的时候，比如冰淇淋和蛋糕。", 4, "冰淇淋和蛋糕！我也喜欢！下次我们一起去吃吧！"),
                            ("看着窗外的云发呆，什么都不想的时候。", 4, "[player_name]前辈也有这样的时候啊～我以为[player_name]前辈一直在想棋谱呢～")
                        ]
                    },
                    {
                        "question": "[player_name]前辈[player_name]前辈～我发现了！我们在活动室里，可以看到窗外的樱花树哦！等春天来了，一定很漂亮！",
                        "responses": [
                            ("到时候我们可以在窗边边看樱花边下棋。", 6, "好！这就是我们的约定！春天的时候一起赏樱下棋！"),
                            ("那我期待那一天。（看着窗外的树）", 5, "[player_name]前辈...我也好期待春天快点来呢～"),
                            ("春天快点来吧。", 5, "[player_name]前辈...我也是呢～")
                        ]
                    }
                ]
            },
            # 第28天
            {
                "name": "最后的约定",
                "category": "original",
                "day": 28,
                "conversations": [
                    {
                        "question": "[player_name]前辈...和你在一起的这些天，我学到了很多...不只是下棋，还有...怎么和人相处。",
                        "responses": [
                            ("我也学到了很多，谢谢你，风子。", 6, "[player_name]前辈...（感动）谢谢[player_name]前辈...谢谢[player_name]前辈出现在我的生命里..."),
                            ("这些天也是我最珍贵的回忆。", 6, "[player_name]前辈...我会把这份记忆永远珍藏在心底的..."),
                            ("以后也要继续一起下棋哦。", 6, "嗯！这是我们的约定！")
                        ]
                    },
                    {
                        "question": "[player_name]前辈...我们的故事还会继续吧？",
                        "responses": [
                            ("当然，这只是开始。", 6, "[player_name]前辈...（幸福地笑）我等[player_name]前辈这句话好久了...那我们继续写我们的故事吧！"),
                            ("会的，直到永远。", 7, "永远...[player_name]前辈...我、我也想和[player_name]前辈一直这样下去..."),
                            ("嗯，这是我们的开始。", 6, "[player_name]前辈...（紧紧握着[player_name]前辈的手）那、那我会一直陪着[player_name]前辈...一直一直...")
                        ]
                    }
                ]
            }
        ]
        
        # ==================== 游戏内对话（补充）====================
        DIALOGUES.update({
            "almost_win": [
                "哼哼...看起来我要赢了呢~",
                "[player_name]前辈，你的棋子好像被包围了呢~",
                "嘿嘿，这局我很有信心哦！"
            ],
            "almost_lose": [
                "呜...形势不太妙...",
                "啊...[player_name]前辈好厉害...",
                "等等...让我想想办法..."
            ],
            "critical_move": [
                "这一步...是关键！",
                "我要认真下了！",
                "看招！"
            ]
        })
        
        @classmethod
        def get(cls, key):
            # 先从 DIALOGUES 查找
            dialogues = cls.DIALOGUES.get(key, [])
            if not dialogues:
                # 再从 TUTORIAL 查找
                dialogues = cls.TUTORIAL.get(key, [])
            text = random.choice(dialogues) if dialogues else ""
            # ★ 在 Python 层直接替换姓名占位符（嵌套插值不会被 Ren'Py 二次解析）
            return text.replace("[player_name]", str(player_name))
        
        @classmethod
        def get_all(cls, key):
            # 先从 DIALOGUES 查找
            dialogues = cls.DIALOGUES.get(key, [])
            if not dialogues:
                # 再从 TUTORIAL 查找
                dialogues = cls.TUTORIAL.get(key, [])
            return dialogues
        
        @classmethod
        def get_index(cls, key, index=0):
            dialogues = cls.DIALOGUES.get(key, [])
            if dialogues and 0 <= index < len(dialogues):
                return dialogues[index]
            return cls.get(key)

        @classmethod
        def _pname_all(cls, data):
            """递归替换对话数据中所有 [player_name] 占位符。
            玩家姓名未设置时替换为空串，避免出现 [player_name] 字面。"""
            name = str(player_name) if player_name else ""
            if isinstance(data, str):
                return data.replace("[player_name]", name)
            if isinstance(data, dict):
                return {k: cls._pname_all(v) for k, v in data.items()}
            if isinstance(data, list):
                return [cls._pname_all(v) for v in data]
            if isinstance(data, tuple):
                return tuple(cls._pname_all(v) for v in data)
            return data

    # -------------------- 存档管理 --------------------
    class AchievementManager:
        """存档管理器"""
        
        SAVE_FILE = "wind_chess_save.json"
        
        def __init__(self):
            self.data = self._load_data()
        
        def _load_data(self):
            default_data = {
                "total_games": 0,
                "total_wins": 0,
                "total_losses": 0,
                "chat_days": 0,
                "current_chat_topic": 0,
                "tutorial_completed": False,
                "wind_mood": 1,  # 心情值
                "total_mood_points": 0,  # 累计心情点数
                "season_triggered": {
                    "spring": False, 
                    "summer": False, 
                    "autumn": False, 
                    "winter": False
                },
                "special_endings": {
                    "sulking": False,
                    "confession": False
                },
                "games_after_sulking": 0,
                "games_after_seasons": 0,
                "critical_game_found": False,
                "chat_completed": False  # 28天聊天是否完成
            }
            
            try:
                if os.path.exists(self.SAVE_FILE):
                    with open(self.SAVE_FILE, 'r', encoding='utf-8') as f:
                        loaded = json.load(f)
                        for key, value in default_data.items():
                            if key not in loaded:
                                loaded[key] = value
                        return loaded
            except:
                pass
            
            return default_data
        
        def save(self):
            """保存数据到文件"""
            try:
                # 确保目录存在
                save_dir = os.path.dirname(self.SAVE_FILE)
                if save_dir and not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                with open(self.SAVE_FILE, 'w', encoding='utf-8') as f:
                    json.dump(self.data, f, ensure_ascii=False, indent=2)
                renpy.log("游戏数据已保存")
            except Exception as e:
                renpy.log("保存数据失败: " + str(e))
        
        @property
        def ending_state(self):
            """结局状态：0=未触发任何特殊结局，1=已触发赌气结局，2=已触发告白结局"""
            se = self.data["special_endings"]
            if se["confession"]:
                return 2
            if se["sulking"]:
                return 1
            return 0

        def record_game(self, won, is_critical=False):
            """记录一局结果，并返回本局应触发的特殊结局（无则 None）。

            ending_state：0=无特殊结局，1=赌气，2=告白（告白最高优先、触发后永久禁止赌气）
            规则：
            - 关键局（state==0 时）：赢 → 赌气(1)；输 → 告白(2)
            - 赌气状态(1)：玩家可继续下棋，从第 6 盘起输 → 告白(2)
            """
            self.data["total_games"] += 1
            if won:
                self.data["total_wins"] += 1
            else:
                self.data["total_losses"] += 1

            state = self.ending_state
            ending = None

            if is_critical and state == 0:
                # 关键局：赢 → 赌气结局；输 → 告白结局
                ending = "sulking" if won else "confession"
            elif state == 1 and not won and self.data["games_after_sulking"] >= 5:
                # 赌气后已下满 5 盘，从第 6 盘起再输 → 告白（判定先于计数）
                ending = "confession"

            # 赌气后游戏计数（无论输赢都要计数）
            if state == 1:
                self.data["games_after_sulking"] += 1

            self.save()
            return ending
        
        def check_critical_game(self):
            """检查本盘是否是关键棋（在进入对局时调用一次）。

            规则：
            1. 28 天聊天已全部完成；
            2. 总游戏次数 >= 10；
            3. 从未触发过关键棋（一次性事件）。
            三者同时满足 → 本盘是关键棋。
            """
            # 已经触发过关键棋，不再触发
            if self.data["critical_game_found"]:
                return False

            # 未完成全部聊天内容
            if not self._all_chat_completed():
                return False

            # 聊天完成后，游戏次数达到 10 盘，下一盘（含补触发）就是关键棋
            if self.data["total_games"] >= 10:
                self.data["critical_game_found"] = True
                self.save()
                return True

            return False
        
        def _all_chat_completed(self):
            """检查是否完成了和风子聊天的全部内容"""
            return self.data.get("chat_completed", False)
        
        def trigger_special_ending(self, ending_type):
            """触发特殊结局
            
            注意：告白结局具有最高优先级，一旦触发永久禁止赌气结局
            """
            if ending_type == "sulking":
                # 只有告白结局未触发才能触发赌气结局
                if not self.data["special_endings"]["confession"]:
                    self.data["special_endings"]["sulking"] = True
                    self.data["games_after_sulking"] = 0
            elif ending_type == "confession":
                # 告白结局触发后，永久禁止赌气结局
                self.data["special_endings"]["confession"] = True
                self.data["special_endings"]["sulking"] = False
            
            # 注意：critical_game_found 不重置——关键局全局只有一次
            self.save()
        
        def record_chat_day(self):
            """记录聊天天数"""
            self.data["chat_days"] += 1
            
            # 检查是否完成28天聊天
            if self.data["chat_days"] >= 28:
                self.data["chat_completed"] = True
            
            # 检查季节事件触发
            if self.data["chat_days"] % 7 == 0:
                seasons = self.data["season_triggered"]
                season_map = {
                    7: "spring",
                    14: "summer",
                    21: "autumn",
                    28: "winter"
                }
                if self.data["chat_days"] in season_map:
                    season = season_map[self.data["chat_days"]]
                    if not seasons[season]:
                        seasons[season] = True
                        self.save()
                        return season
            
            self.save()
            return None
        
        def add_mood_points(self, points):
            """添加心情点数"""
            self.data["total_mood_points"] += points
            # 根据累计点数调整心情
            if self.data["total_mood_points"] >= 50:
                self.data["wind_mood"] = 8  # 温柔
            elif self.data["total_mood_points"] >= 35:
                self.data["wind_mood"] = 7  # 得意
            elif self.data["total_mood_points"] >= 20:
                self.data["wind_mood"] = 6  # 期待
            elif self.data["total_mood_points"] >= 5:
                self.data["wind_mood"] = 5  # 惊讶
            elif self.data["total_mood_points"] >= -5:
                self.data["wind_mood"] = 4  # 害羞
            elif self.data["total_mood_points"] >= -15:
                self.data["wind_mood"] = 3  # 俏皮
            else:
                self.data["wind_mood"] = 2  # 开心
            self.save()
        
        def get_wind_mood(self):
            """获取当前心情"""
            return self.data.get("wind_mood", 1)
        
        def get_current_topic(self):
            """获取当前话题索引"""
            return self.data.get("current_chat_topic", 0)
        
        def advance_topic(self):
            """进入下一个话题"""
            self.data["current_chat_topic"] += 1
            self.save()
        
        def can_chat_more(self):
            """检查是否还能继续聊天"""
            return self.data["current_chat_topic"] < 28 and not self.data.get("chat_completed", False)
        
        def is_chat_completed(self):
            """检查聊天是否已完成"""
            return self.data.get("chat_completed", False)
        
        def complete_tutorial(self):
            self.data["tutorial_completed"] = True
            self.save()
        
        def has_completed_tutorial(self):
            return self.data.get("tutorial_completed", False)
        
        def reset_all(self):
            """重置所有数据"""
            self.data = {
                "total_games": 0,
                "total_wins": 0,
                "total_losses": 0,
                "chat_days": 0,
                "current_chat_topic": 0,
                "tutorial_completed": False,
                "wind_mood": 1,
                "total_mood_points": 0,
                "season_triggered": {
                    "spring": False, 
                    "summer": False, 
                    "autumn": False, 
                    "winter": False
                },
                "special_endings": {
                    "sulking": False,
                    "confession": False
                },
                "games_after_sulking": 0,
                "games_after_seasons": 0,
                "critical_game_found": False,
                "chat_completed": False
            }
            self.save()
            renpy.log("游戏数据已重置完成")
    
    # 全局实例
    _achievement_manager = AchievementManager()
    
    def get_achievement_manager():
        return _achievement_manager

    # -------------------- Canvas 棋盘绘制 --------------------
    hover_cell = None
    
    def screen_to_board(sx, sy, board_x, board_y, cell_size, board_size):
        """屏幕坐标转棋盘坐标"""
        bx = int((sx - board_x) / cell_size)
        by = int((sy - board_y) / cell_size)
        if 0 <= bx < board_size and 0 <= by < board_size:
            return (bx, by)
        return None
    
    def init_game():
        """初始化游戏"""
        global hover_cell
        hover_cell = None

    # -------------------- 自定义 Displayable --------------------
    class ChessBoardDisplay(renpy.Displayable):
        """棋盘显示组件"""
        
        def __init__(self, game, board_x=0, board_y=0, cell_size=50, **kwargs):
            super(ChessBoardDisplay, self).__init__(**kwargs)
            self.game = game
            self.board_x = board_x
            self.board_y = board_y
            self.cell_size = cell_size
            self.board_size = game.board_size
            self.board_total = self.board_size * self.cell_size
            
            # 颜色定义
            self.grid_color = "#4a4a6a"
            self.wind_eye_color = "#ffd700"
            self.valid_move_color = "#66ff6688"
            self.selected_color = "#64b5f6"
            self.player_a_color = "#2196F3"
            self.player_b_color = "#f44336"
            self.last_move_color = "#aaaaaa"
            self.background_color = "#1a1a2e"
        
        def render(self, width, height, st, at):
            render = renpy.Render(self.board_total, self.board_total)
            
            # 绘制背景
            render.canvas().rect(
                self.background_color,
                (0, 0, self.board_total, self.board_total)
            )
            
            # 绘制网格
            canvas = render.canvas()
            for i in range(self.board_size + 1):
                canvas.rect(
                    self.grid_color,
                    (0, i * self.cell_size, self.board_total, 1)
                )
                canvas.rect(
                    self.grid_color,
                    (i * self.cell_size, 0, 1, self.board_total)
                )
            
            # 绘制风眼标记 (X)
            center = self.board_size // 2
            cx = center * self.cell_size + self.cell_size // 2
            cy = center * self.cell_size + self.cell_size // 2
            canvas.line(self.wind_eye_color, (cx - 10, cy - 10), (cx + 10, cy + 10), 2)
            canvas.line(self.wind_eye_color, (cx + 10, cy - 10), (cx - 10, cy + 10), 2)
            
            # 绘制有效移动高亮
            for move in self.game.valid_moves:
                mx = move[0] * self.cell_size + 5
                my = move[1] * self.cell_size + 5
                canvas.rect(
                    self.valid_move_color,
                    (mx, my, self.cell_size - 10, self.cell_size - 10)
                )
            
            # 绘制最后移动的轨迹
            if self.game.last_move:
                fx, fy = self.game.last_move[0]
                tx, ty = self.game.last_move[1]
                fx_pos = fx * self.cell_size + self.cell_size // 2
                fy_pos = fy * self.cell_size + self.cell_size // 2
                tx_pos = tx * self.cell_size + self.cell_size // 2
                ty_pos = ty * self.cell_size + self.cell_size // 2
                canvas.line(self.last_move_color, (fx_pos, fy_pos), (tx_pos, ty_pos), 3)
            
            # 绘制棋子
            for y in range(self.board_size):
                for x in range(self.board_size):
                    if self.game.board[y][x] is not None:
                        px = x * self.cell_size + self.cell_size // 2
                        py = y * self.cell_size + self.cell_size // 2
                        is_selected = (x, y) == self.game.selected_piece if self.game.selected_piece else False
                        
                        if self.game.board[y][x] == Player.A:
                            piece_color = self.selected_color if is_selected else self.player_a_color
                        else:
                            piece_color = "#ef5350" if is_selected else self.player_b_color
                        
                        radius = 18
                        canvas.circle(
                            "#ffffff" if is_selected else "#333333",
                            (px, py), radius + 3, 0
                        )
                        canvas.circle(piece_color, (px, py), radius, 0)
            
            return render
        
        def event(self, ev, x, y, st):
            global hover_cell

            # 获取状态管理器
            gsm = get_game_state_manager()

            # 更新悬停信息（仅玩家回合时）
            if gsm.is_player_turn():
                if 0 <= x < self.board_total and 0 <= y < self.board_total:
                    hover_cell = screen_to_board(x, y, 0, 0, self.cell_size, self.board_size)
                else:
                    hover_cell = None
            else:
                hover_cell = None

            # 只处理鼠标点击事件，且仅在玩家回合时响应
            import pygame
            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                # ★ 核心修复：只有状态机允许时才处理棋盘点击
                if not gsm.is_player_turn():
                    # 非玩家回合，吞掉事件防止穿透到棋盘逻辑
                    return None

                pos = screen_to_board(x, y, 0, 0, self.cell_size, self.board_size)
                if not pos:
                    return None

                if gsm.phase == GamePhase.PLAYER_SELECT:
                    # 玩家选择棋子阶段（PVP 和 PVE 通用，根据 current_player 判断）
                    if self.game.board[pos[1]][pos[0]] == self.game.current_player:
                        self.game.select_piece(pos)
                        gsm.on_player_selected_piece()
                    renpy.restart_interaction()

                elif gsm.phase == GamePhase.PLAYER_MOVE:
                    # 玩家移动棋子阶段
                    if self.game.selected_piece and pos in self.game.valid_moves:
                        from_pos = self.game.selected_piece
                        if self.game.move_piece(self.game.selected_piece, pos):
                            # ★ 核心修复：移动成功后调用回调，跳转到主循环
                            gsm.on_player_moved(from_pos, pos)
                            renpy.restart_interaction()
                            on_player_move_done()  # 触发 jump 跳转
                            return None
                    else:
                        # 点击了无效位置
                        self.game.deselect_piece()
                        # 检查是否点击了另一个自己的棋子（PVP/PVE 通用）
                        if self.game.board[pos[1]][pos[0]] == self.game.current_player:
                            self.game.select_piece(pos)
                            gsm.set_phase(GamePhase.PLAYER_MOVE)
                        else:
                            gsm.set_phase(GamePhase.PLAYER_SELECT)
                    renpy.restart_interaction()

            return None

# ============================================================
# Screen 定义
# ============================================================

# -------------------- 主菜单 --------------------
screen main_menu():
    modal True
    tag menu
    
    # 拦截滚轮事件，防止意外触发
    key "mousedown_4" action NullAction()
    key "mousedown_5" action NullAction()
    key "mouseup_4" action NullAction()
    key "mouseup_5" action NullAction()
    
    frame:
        xalign 0.5
        yalign 0.5
        background "#1a1a2e"
        padding (60, 50)
        
        vbox:
            xalign 0.5
            spacing 30
            
            text "{b}{size=+10}风棋少女{/size}{/b}":
                size 48
                color "#ffd700"
                xalign 0.5
            
            null height 20
            
            textbutton _("{b}开始游戏{/b}"):
                xalign 0.5
                action Return("pve")
                text_size 28
                text_color "#ffffff"
                text_hover_color "#ffd700"
            
            textbutton _("{b}新手教程{/b}"):
                xalign 0.5
                action Return("tutorial")
                text_size 24
                text_color "#ffffff"
                text_hover_color "#ffd700"
            
            textbutton _("{b}双人对战{/b}"):
                xalign 0.5
                action Return("pvp")
                text_size 24
                text_color "#ffffff"
                text_hover_color "#ffd700"
            
            textbutton _("{b}与风子聊天{/b}"):
                xalign 0.5
                action Return("chat")
                text_size 24
                text_color "#ffffff"
                text_hover_color "#ffd700"
            
            textbutton _("{b}游戏设置{/b}"):
                xalign 0.5
                action Return("settings")
                text_size 24
                text_color "#aaaaaa"
                text_hover_color "#ffd700"

# -------------------- 游戏棋盘屏幕 --------------------
screen game_screen(game, mode="pve"):
    # modal 必须是非动态的，设为 False
    # 点击控制由 ChessBoardDisplay.event() 内部根据状态机处理
    modal False
    tag game_screen
    
    # 获取状态管理器（用于显示信息）
    $ gsm = get_game_state_manager()

    # 顶部信息栏
    frame:
        xpos 0.5
        ypos 0.0
        xanchor 0.5
        yanchor 0.0
        background "#333355"
        padding (30, 10)

        text "{b}风棋少女{/b}" size 28 color "#ffd700"

    # 风向信息
    frame:
        xpos 0.5
        ypos 0.0
        xanchor 0.5
        yanchor 0.0
        yoffset 45
        background "#222244"
        padding (20, 8)

        $ wind_text = game.wind_direction.value if game.wind_direction else "无风"
        text "风向：[wind_text] [game.get_wind_symbol()]" size 20 color game.get_wind_color()

    # 回合信息 - 根据状态机显示
    frame:
        xpos 0.5
        ypos 0.0
        xanchor 0.5
        yanchor 0.0
        yoffset 90
        background "#333355"
        padding (30, 10)

        if gsm.is_game_over():
            if mode == "pvp":
                if game.winner == Player.A:
                    text "{b}玩家A（●）获胜！{/b}" size 24 color "#4CAF50"
                else:
                    text "{b}玩家B（○）获胜！{/b}" size 24 color "#4CAF50"
            else:
                if game.winner == Player.A:
                    text "{b}玩家获胜！{/b}" size 24 color "#4CAF50"
                else:
                    text "{b}风子获胜！{/b}" size 24 color "#f44336"
        elif mode == "pvp":
            if game.current_player == Player.A:
                text "玩家A（●）的回合 - 请选择棋子" size 22 color "#2196F3"
            else:
                text "玩家B（○）的回合 - 请选择棋子" size 22 color "#FF9800"
        elif gsm.phase == GamePhase.PLAYER_SELECT:
            text "[player_name]前辈的回合 - 请选择棋子（●）" size 22 color "#2196F3"
        elif gsm.phase == GamePhase.PLAYER_MOVE:
            if mode == "pvp":
                if game.current_player == Player.A:
                    text "玩家A（●）的回合 - 请选择目标位置" size 22 color "#4CAF50"
                else:
                    text "玩家B（○）的回合 - 请选择目标位置" size 22 color "#4CAF50"
            else:
                text "[player_name]前辈的回合 - 请选择目标位置" size 22 color "#4CAF50"
        elif gsm.phase == GamePhase.AI_THINKING:
            text "风子正在思考..." size 22 color "#ff69b4"
        elif gsm.phase == GamePhase.AI_MOVING:
            text "风子落子中..." size 22 color "#ff69b4"
        elif gsm.phase == GamePhase.AI_COMMENT:
            text "风子有话要说..." size 22 color "#ff69b4"
        else:
            text "等待中..." size 22 color "#888888"

    # 棋盘显示区域
    $ cell_size = 50
    add ChessBoardDisplay(game, cell_size=cell_size) at board_transform

    # 鼠标悬停提示 - 仅在玩家回合
    if gsm.is_player_turn() and hover_cell:
        $ hx, hy = hover_cell
        frame:
            xpos 0.98
            ypos 0.5
            xanchor 1.0
            background "#333355"
            padding (10, 5)

            if 0 <= hx < game.board_size and 0 <= hy < game.board_size:
                if game.board[hy][hx] == Player.A:
                    text "点击选择棋子" size 16 color "#2196F3"
                elif (hx, hy) in game.valid_moves:
                    text "点击移动到这里" size 16 color "#4CAF50"
                else:
                    text "等待选择..." size 16 color "#888888"

    # AI回合提示（带动画效果）
    if gsm.is_ai_turn() and not gsm.is_game_over():
        frame:
            xpos 0.5
            ypos 0.85
            xanchor 0.5
            background "#333355"
            padding (20, 10)

            if gsm.phase == GamePhase.AI_THINKING:
                text "风子正在思考..." size 18 color "#ff69b4"
            elif gsm.phase == GamePhase.AI_MOVING:
                text "风子落子了！" size 18 color "#ff69b4"
            elif gsm.phase == GamePhase.AI_COMMENT:
                text "风子在说些什么..." size 18 color "#ff69b4"

    # 底部按钮
    frame:
        xpos 0.5
        ypos 0.92
        xanchor 0.5
        background "#333355"
        padding (20, 10)

        hbox:
            spacing 30

            textbutton _("{b}返回菜单{/b}"):
                action Return("menu")
                text_size 20
                text_color "#ffffff"

            if gsm.is_game_over():
                textbutton _("{b}再来一局{/b}"):
                    action Return("restart")
                    text_size 20
                    text_color "#ffffff"

# -------------------- 片尾字幕（一个屏幕、一条连续动画） --------------------
# "写在制作人员名单之前" + "制作人员名单" 作为一个整体，
# 先空白 1 秒，然后整块内容从屏幕最底部向上连续滚动，署名停在屏幕底部。
# 总时长 1 + 70 = 71 秒，点击/空格/回车可跳过。
transform credits_roll_transform:
    xalign 0.5
    yanchor 0.0 ypos 1.0
    pause 1.0
    linear 70.0 yanchor 1.0 ypos 1.0

screen credits_combined_screen():
    modal True
    layer "master"
    
    # 隐藏话语框
    $ renpy.hide_screen("say")
    
    # 黑色背景
    add "#000000"
    
    # 滚动的字幕内容（一个 vbox，两段内容连续排布）
    vbox:
        at credits_roll_transform
        xalign 0.5
        spacing 30
        
        # ==================== 第一部分：写在制作人员名单之前 ====================
        text "写在制作人员名单之前" size 48 color "#ffffff" xalign 0.5 bold True
        
        null height 80
        
        # 开发内容（首行缩进两字符，长文本自动换行）
        text "　　DeepSeek 完成了本游戏的核心概念开发、剧本和剧情工作、游戏逻辑程序文件开发、提示词撰写和统筹协调工作。" size 28 xalign 0.5 color "#ffffff" xmaximum 1000
        text "　　Suno AI 完成了本游戏的音乐工作。" size 28 xalign 0.5 color "#ffffff"
        text "　　CodeBuddy 完成了剩下的程序工作。" size 28 xalign 0.5 color "#ffffff"
        text "　　吐司 完成了美术工作。" size 28 xalign 0.5 color "#ffffff"
        
        null height 40
        
        # 个人贡献（首行缩进两字符，长文本自动换行）
        text "　　我个人负责作为电子信使，把AI们的指令传来传去，担任游戏试玩员，并且在大面上把控一些方向。" size 24 xalign 0.5 color "#ffffff" xmaximum 1000
        text "　　没有其他人类直接参与本游戏的开发工作。" size 24 xalign 0.5 color "#ffffff"
        
        null height 100
        
        # 感谢（首行缩进两字符，长文本自动换行）
        text "　　感谢所有AI工程师们，是他们不断扩展了人类凭一张纸和一支铅笔可以到达的边界。" size 26 xalign 0.5 color "#ffffff" italic True xmaximum 1000
        text "　　也感谢所有玩到这里的玩家，包括你。" size 26 xalign 0.5 color "#ffffff" italic True
        
        null height 150
        
        # 署名（右对齐，字号统一）
        text "常乐风" size 28 xalign 1.0 color "#ffffff"
        text "2026年4月19日" size 28 xalign 1.0 color "#ffffff"
        text "中华人民共和国，北京" size 28 xalign 1.0 color "#ffffff"
        
        # ==================== 两部分之间的分隔 ====================
        null height 300
        
        # ==================== 第二部分：制作人员名单 ====================
        text "制作人员名单" size 48 color "#ffffff" xalign 0.5 bold True
        
        null height 60
        
        # 制作人员
        text "制作人：常乐风" size 26 xalign 0.5 color "#ffffff"
        text "编剧：常乐风" size 26 xalign 0.5 color "#ffffff"
        text "音乐：常乐风" size 26 xalign 0.5 color "#ffffff"
        text "作曲：常乐风" size 26 xalign 0.5 color "#ffffff"
        text "原画：常乐风" size 26 xalign 0.5 color "#ffffff"
        text "角色设计：常乐风" size 26 xalign 0.5 color "#ffffff"
        text "CG：常乐风" size 26 xalign 0.5 color "#ffffff"
        text "动画原画：常乐风" size 26 xalign 0.5 color "#ffffff"
        
        null height 60
        
        # 歌曲信息
        text "歌曲《欢跃的精灵》" size 24 xalign 0.5 color "#ffffff" bold True
        text "编曲：常乐风，作曲：常乐风" size 22 xalign 0.5 color "#ffffff"
        text "钢片琴：常乐风，长笛：常乐风，尼龙弦吉他：常乐风" size 20 xalign 0.5 color "#ffffff"
        
        null height 30
        
        text "歌曲《抉择时刻》" size 24 xalign 0.5 color "#ffffff" bold True
        text "编曲：常乐风，作曲：常乐风" size 22 xalign 0.5 color "#ffffff"
        text "低音提琴：常乐风，小号：常乐风，定音鼓：常乐风" size 20 xalign 0.5 color "#ffffff"
        
        null height 30
        
        text "歌曲《绵延的思念》" size 24 xalign 0.5 color "#ffffff" bold True
        text "编曲：常乐风，作曲：常乐风" size 22 xalign 0.5 color "#ffffff"
        text "钢琴：常乐风，小提琴：常乐风，三角铁：常乐风" size 20 xalign 0.5 color "#ffffff"
        
        # 末尾空白，让最后内容滚到屏幕上方
        null height 400
    
    # 禁用鼠标滚轮与翻页键（全局已禁用，这里双保险）
    key "mousedown_4" action NullAction()
    key "mousedown_5" action NullAction()
    key "mouseup_4" action NullAction()
    key "mouseup_5" action NullAction()
    key "K_PAGEUP" action NullAction()
    key "K_PAGEDOWN" action NullAction()
    key "rollback" action NullAction()
    key "rollforward" action NullAction()

# -------------------- 制作人员名单标签 --------------------
label show_credits:
    # 片尾字幕 = 一个屏幕、一条连续动画（1 秒空白 + 70 秒滚动）。
    # 点击/空格/回车会提前打断 renpy.pause，实现跳过。
    python:
        renpy.block_rollback()
        renpy.hide_screen("say")
        renpy.show_screen("credits_combined_screen")
        
        # 等待整条动画播完（71 秒）+ 6 秒定格，然后回到结局菜单
        renpy.pause(77.0)
        
        renpy.hide_screen("credits_combined_screen")
        renpy.restart_interaction()
    return

# -------------------- 设置屏幕 --------------------
screen settings_screen():
    modal True
    tag settings
    
    frame:
        xalign 0.5
        yalign 0.5
        background "#1a1a2e"
        padding (50, 40)
        
        vbox:
            xalign 0.5
            spacing 30
            
            text "{b}游戏设置{/b}":
                size 36
                color "#ffd700"
                xalign 0.5
            
            null height 20
            
            # -------------------- 音量控制 --------------------
            frame:
                background "#333355"
                padding (30, 20)
                xalign 0.5
                
                vbox:
                    xalign 0.5
                    spacing 15
                    
                    text "音量设置" size 24 color "#ffd700"
                    
                    hbox:
                        xalign 0.5
                        spacing 10
                        
                        # 静音按钮
                        if persistent.muted:
                            textbutton _("{b}🔇{/b}"):
                                action [SetField(persistent, "muted", False), Function(_apply_volume)]
                                text_size 28
                                text_color "#888888"
                        else:
                            textbutton _("{b}🔊{/b}"):
                                action [SetField(persistent, "muted", True), Function(_apply_volume)]
                                text_size 28
                                text_color "#ffd700"
                        
                        # 音量滑块
                        bar:
                            value FieldValue(persistent, "music_volume", range=1.0, step=0.01)
                            xmaximum 200
                            ysize 30
                            thumb "#ffd700"
                            thumb_shadow "#000000"
                            left_gutter 0
                            right_gutter 0
                            changed _save_volume
                        
                        # 音量百分比显示
                        text " [int(persistent.music_volume * 100)]%" size 18 color "#ffffff" xpos 5
                    
                    # 快捷音量按钮
                    hbox:
                        xalign 0.5
                        spacing 10
                        
                        textbutton _("静音"):
                            action ToggleVariable("persistent.muted"), Function(_apply_volume)
                            text_size 14
                            text_color "#aaaaaa"
                            text_hover_color "#ffd700"
                            text_selected_color "#ffd700"
                        
                        textbutton _("{b}25%{/b}"):
                            action [SetVariable("persistent.music_volume", 0.25), Function(_save_volume, 0.25)]
                            text_size 14
                            text_color "#aaaaaa"
                            text_hover_color "#ffd700"
                        
                        textbutton _("{b}50%{/b}"):
                            action [SetVariable("persistent.music_volume", 0.5), Function(_save_volume, 0.5)]
                            text_size 14
                            text_color "#aaaaaa"
                            text_hover_color "#ffd700"
                        
                        textbutton _("{b}75%{/b}"):
                            action [SetVariable("persistent.music_volume", 0.75), Function(_save_volume, 0.75)]
                            text_size 14
                            text_color "#aaaaaa"
                            text_hover_color "#ffd700"
                        
                        textbutton _("{b}100%{/b}"):
                            action [SetVariable("persistent.music_volume", 1.0), Function(_save_volume, 1.0)]
                            text_size 14
                            text_color "#aaaaaa"
                            text_hover_color "#ffd700"
            
            null height 20
            
            textbutton _("{b}姓名设置{/b}"):
                xalign 0.5
                action Return("name")
                text_size 16
                text_color "#666688"
                text_hover_color "#ffd700"
            
            null height 10
            
            textbutton _("{b}重置游戏数据{/b}"):
                xalign 0.5
                action Return("reset")
                text_size 20
                text_color "#f44336"
            
            textbutton _("{b}返回主菜单{/b}"):
                xalign 0.5
                action Return("menu")
                text_size 24
                text_color "#ffffff"
                text_hover_color "#ffd700"

# -------------------- 姓名输入屏幕（输入 crb 可进入检修入口） --------------------
screen crb_input_screen():
    modal True
    zorder 100
    
    default name_text = ""
    
    key "K_ESCAPE" action Return(None)
    
    frame:
        xalign 0.5
        yalign 0.5
        background "#1a1a2e"
        padding (50, 40)
        
        vbox:
            xalign 0.5
            spacing 25
            
            text "{b}姓名设置{/b}":
                size 30
                color "#ffd700"
                xalign 0.5
            
            text "请输入你希望风子对你的称呼：":
                size 20
                color "#ffffff"
                xalign 0.5
            
            frame:
                xalign 0.5
                xminimum 320
                yminimum 60
                background "#0d0d1f"
                padding (20, 10)
                
                input:
                    value ScreenVariableInputValue("name_text")
                    length 20
                    xalign 0.5
                    yalign 0.5
                    size 28
                    color "#ffffff"
                    text_align 0.5
            
            text "输入完成后点击「确认」提交，Esc 取消":
                size 14
                color "#8888aa"
                xalign 0.5
            
            hbox:
                xalign 0.5
                spacing 40
                
                textbutton _("确认"):
                    action Return(name_text.strip().lower())
                    text_size 22
                    text_color "#ffd700"
                    text_hover_color "#ffffff"
                
                textbutton _("取消"):
                    action Return(None)
                    text_size 22
                    text_color "#aaaaaa"
                    text_hover_color "#ffd700"

# -------------------- crb 检修入口的特殊结局选择 --------------------
# 提示文字放在屏幕上部 25% 处，与下方选项拉开距离，避免重叠
screen crb_menu_screen():
    modal True
    zorder 100
    
    key "K_ESCAPE" action Return("cancel")
    
    vbox:
        xalign 0.5
        ypos 0.2
        spacing 50
        
        text "检修权限已通过，请选择要触发的特殊结局：":
            size 28
            color "#ffd700"
            xalign 0.5
        
        vbox:
            xalign 0.5
            spacing 20
            
            textbutton _("赌气结局"):
                action Return("sulking")
                text_size 24
                text_color "#ffffff"
                text_hover_color "#ffd700"
                xalign 0.5
            
            textbutton _("告白结局"):
                action Return("confession")
                text_size 24
                text_color "#ffffff"
                text_hover_color "#ffd700"
                xalign 0.5
            
            textbutton _("取消"):
                action Return("cancel")
                text_size 24
                text_color "#aaaaaa"
                text_hover_color "#ffd700"
                xalign 0.5

# ============================================================
# Ren'Py 标签和叙事逻辑
# ============================================================

# 玩家姓名（在"姓名设置"中设置，空字符串则保持"[player_name]前辈"称呼）
default player_name = ""

label wind_chess_start:
    $ init_game()
    $ game_mode = None
    $ current_game = None
    
    scene black
    
    # ★ 设置一般时间音乐
    $ _set_music(1)
    
    centered "{b}{size=+10}风棋少女{/size}{/b}"
    
    pause 1.5
    
    jump main_menu_label

label main_menu_label:
    # ★ 设置一般时间音乐和背景（返回主菜单时）
    $ _set_music(1)
    $ _set_background(1)
    $ _set_mood(1)  # 默认心情立绘
    
    show screen main_menu
    
    $ _return = ui.interact()
    
    if _return == "pve":
        jump pve_game
    elif _return == "tutorial":
        jump tutorial_game
    elif _return == "pvp":
        jump pvp_game
    elif _return == "chat":
        jump chat_game
    elif _return == "settings":
        jump settings_label
    else:
        jump main_menu_label

label settings_label:
    call screen settings_screen
    
    if _return == "reset":
        $ get_achievement_manager().reset_all()
        $ renpy.restart_interaction()  # 刷新屏幕显示
        centered "{b}{size=+4}游戏数据已重置{/size}{/b}" with dissolve
        $ renpy.pause(1.2)
        jump settings_label  # 重新显示设置页面让用户确认
    elif _return == "menu":
        jump main_menu_label
    elif _return == "name":
        # ★ 姓名设置（输入 crb 可进入代码审查委员会检修入口）
        hide screen settings_screen
        hide screen main_menu
        scene black with fade
        
        show text "{b}{size=+4}姓名设置{/size}{/b}" at truecenter with dissolve
        $ renpy.pause(0.8)
        hide text with dissolve
        
        call screen crb_input_screen
        $ name_input = _return
        
        if name_input == "crb":
            call screen crb_menu_screen
            if _return == "sulking":
                jump sulking_ending
            elif _return == "confession":
                jump confession_ending
            else:
                jump settings_label
        elif name_input is None or name_input is True:
            # Esc 默认 dismiss 行为可能返回 True，一律视为取消
            jump settings_label
        elif name_input == "rickroll":
            # 彩蛋：用系统浏览器打开 B 站视频
            $ renpy.run(OpenURL("https://www.bilibili.com/video/BV1GJ411x7h7/"))
            jump settings_label
        else:
            $ player_name = name_input
            if player_name == "":
                centered "{color=#aaaaaa}未输入内容，风子依然称呼你为「[player_name]前辈」{/color}" with dissolve
            else:
                centered "{color=#ffd700}已设置！风子会称呼你为「[player_name]前辈」{/color}" with dissolve
            $ renpy.pause(1.2)
            jump settings_label

# -------------------- PVE 对战 --------------------
label pve_game:
    # 先隐藏主菜单屏幕
    hide screen main_menu
    hide screen say
    
    scene #1a1a2e with fade
    
    # ★ 设置紧张刺激的下棋音乐
    $ _set_music(2)
    $ _set_background(1)  # 下棋背景
    $ _set_mood(2)  # 下棋时显示立绘（开心心情）

    $ am = get_achievement_manager()

    # 检查特殊结局状态
    if am.data["special_endings"]["confession"]:
        jump confession_mode_game
    elif am.data["special_endings"]["sulking"]:
        jump sulking_mode_game

    fengzi "[FengziDialogue.get('greeting')]"
    fengzi "[FengziDialogue.get('game_start')]"

    $ current_game = WindChessGame()
    $ game_mode = "pve"
    $ wind_changed_this_turn = False
    $ is_critical_game = am.check_critical_game()
    $ gsm = get_game_state_manager()
    $ gsm.start_game()
    
    # ★ 设置玩家移动完成后的跳转目标
    $ set_player_move_jump("player_turn_done")

    jump pve_loop

# ★ 玩家回合入口
label pve_loop:
    $ gsm = get_game_state_manager()

    if current_game.game_over or gsm.is_game_over():
        jump pve_end

    # ========== 玩家回合 ==========
    if gsm.phase == GamePhase.PLAYER_SELECT or gsm.phase == GamePhase.PLAYER_MOVE:
        # ★ 重新设置玩家移动完成后的跳转目标（每次进入玩家回合都要设置）
        $ set_player_move_jump("player_turn_done")
        
        # ★ 使用 show screen + 循环等待替代 call screen
        # 棋盘组件会在玩家移动完成后跳转到 player_turn_done
        show screen game_screen(current_game, "pve")
        
        # ★ 关键修复：使用全局标志控制循环，而不是依赖 _return
        $ _game_waiting = True
        while _game_waiting:
            $ result = renpy.ui.interact(suppress_overlay=True, suppress_underlay=True)
            # _return 可能在点击按钮时设置，或通过棋盘跳转时改变 _game_waiting
            if isinstance(result, str):
                if result == "menu":
                    $ _game_waiting = False
                    $ _return = "menu"
                elif result == "restart":
                    $ _game_waiting = False
                    $ _return = "restart"
        
        # 隐藏 screen
        hide screen game_screen
        
        # 处理返回按钮
        if _return == "menu":
            $ gsm.reset()
            $ _return = None
            $ _game_waiting = True
            jump main_menu_label
        elif _return == "restart":
            $ gsm.reset()
            $ _return = None
            $ _game_waiting = True
            jump pve_game
        
        jump pve_loop

    # ========== AI回合 ==========
    elif gsm.is_ai_turn():
        jump ai_turn

    else:
        # 未知状态，重置
        $ gsm.set_phase(GamePhase.PLAYER_SELECT)
        jump pve_loop

# ★ 玩家移动完成后的处理（由棋盘组件通过 jump 跳转）
label player_turn_done:
    $ gsm = get_game_state_manager()
    
    # 隐藏棋盘 screen
    hide screen game_screen
    
    # 检查是否游戏结束
    if current_game.game_over:
        $ gsm.on_game_over(current_game.winner)
        jump pve_end

    # 玩家移动完成 → 进入AI思考阶段
    $ gsm.on_player_moved(None, None)
    jump ai_turn

label ai_turn:
    $ gsm = get_game_state_manager()
    $ cell_size = 50

    # --- 阶段1：AI思考（播放风子对话）---
    if gsm.phase == GamePhase.AI_THINKING:
        # 先隐藏交互式棋盘，显示静态棋盘（AI回合不接收点击）
        hide screen game_screen
        show expression ChessBoardDisplay(current_game, cell_size=cell_size) as cb at board_transform

        # ★ AI先说话
        $ _set_mood(3)  # 俏皮
        fengzi "[FengziDialogue.get('my_turn')]"

        # 短暂延迟模拟"思考"
        $ renpy.pause(0.5)

        # --- 阶段2：AI执行移动 ---
        $ gsm.on_ai_moving()

        $ ai_result = current_game.ai_make_move()

        # 刷新棋盘显示AI移动后的状态
        show expression ChessBoardDisplay(current_game, cell_size=cell_size) as cb at board_transform
        $ renpy.restart_interaction()

        if current_game.game_over:
            $ gsm.on_game_over(current_game.winner)
            jump pve_end

        # --- 阶段3：AI评论 ---
        $ gsm.on_ai_moved(None, None)

        # ★ AI移动后再说话（根据好棋/坏棋改变立绘）
        $ good_move = random.random() > 0.3
        if good_move:
            $ _set_mood(7)  # 得意
            fengzi "[FengziDialogue.get('good_move')]"
        else:
            $ _set_mood(5)  # 惊讶
            fengzi "[FengziDialogue.get('bad_move')]"

        # 一个回合结束（玩家+AI各下一步），决定是否改变风向
        if current_game.move_count % 2 == 0:
            $ wind_changed = current_game.change_wind()
            if wind_changed:
                $ _set_mood(6)  # 期待
                fengzi "[FengziDialogue.get('wind_change')]"
            # 风向改变后刷新棋盘
            show expression ChessBoardDisplay(current_game, cell_size=cell_size) as cb at board_transform

        # ★ 关键修复：不再调用 switch_player()
        # move_piece 内部已经切换了 current_player（从B→A）
        # 之前这里多调用了一次导致玩家被跳过

        # AI评论结束，回到玩家选子阶段
        $ gsm.on_ai_comment_done()
        hide expression cb

        jump pve_loop

    else:
        # 不在AI思考阶段，回到主循环
        jump pve_loop

label pve_end:
    $ gsm = get_game_state_manager()
    $ am = get_achievement_manager()
    
    # ★ 修改：保持棋盘显示，让玩家看到最终局面
    # 清理可能存在的棋盘显示
    hide screen game_screen
    hide expression cb
    # 显示静态棋盘让玩家欣赏最终局面
    show expression ChessBoardDisplay(current_game, cell_size=50) as final_board at board_transform
    
    # 显示"胜负已分"的提示
    show text "{b}{size=+4}【胜负已分】{/size}{/b}" at truecenter with dissolve
    $ renpy.pause(0.8)
    
    # 隐藏胜负提示，准备显示风子反应
    hide text with dissolve
    
    # 短暂暂停让玩家记住最终局面
    $ renpy.pause(1.0)

    if current_game.winner == Player.A:
        # 玩家赢了（风子输了）
        $ ending_result = am.record_game(True, is_critical_game)
        $ _set_mood(4)  # 害羞/委屈
        fengzi "[FengziDialogue.get('defeat')]"

        # 重置状态机
        $ gsm.reset()

        # 统一结局判定（见 record_game）：关键棋胜利 → 赌气结局
        if ending_result == "sulking":
            jump sulking_ending
        elif ending_result == "confession":
            jump confession_ending

        menu:
            "再来一局！":
                hide expression final_board
                jump pve_game
            "返回主菜单":
                hide expression final_board
                jump main_menu_label
    else:
        # 玩家输了（风子赢了）
        $ ending_result = am.record_game(False, is_critical_game)
        $ _set_mood(7)  # 得意
        fengzi "[FengziDialogue.get('victory')]"

        # 重置状态机
        $ gsm.reset()

        # 统一结局判定（见 record_game）：输关键棋 / 赌气后满5盘再输 → 告白结局
        if ending_result == "confession":
            jump confession_ending
        elif ending_result == "sulking":
            jump sulking_ending

        menu:
            "再来一局！":
                hide expression final_board
                jump pve_game
            "返回主菜单":
                hide expression final_board
                jump main_menu_label

# -------------------- 新手教程 --------------------
label tutorial_game:
    # 先隐藏主菜单屏幕
    hide screen main_menu
    hide screen say
    
    scene black with fade
    
    # ★ 设置紧张刺激的下棋音乐
    $ _set_music(2)
    $ _set_background(1)  # 教程背景
    $ _set_mood(3)  # 俏皮心情
    
    fengzi "[FengziDialogue.get('tutorial_intro')]"
    
    centered "{b}{size=+5}【风之棋教程】{/size}{/b}"
    
    fengzi "风之棋是一种非常有趣的棋类游戏~"
    fengzi "让我来教[player_name]前辈怎么玩吧！"
    
    centered "{b}{size=+5}一、棋盘介绍{/size}{/b}"
    
    fengzi "棋盘由9×9的格子组成~"
    fengzi "每个位置都可以放棋子"
    fengzi "中央有一个特殊的位置——风眼，用X标记"
    fengzi "站在风眼上的棋子可以自由移动！"
    
    centered "{b}{size=+5}二、风向规则{/size}{/b}"
    
    fengzi "[FengziDialogue.get('tutorial_wind')]"
    
    centered "风向说明："
    fengzi "水平风 ←→ ：棋子只能左右移动"
    fengzi "垂直风 ↑↓ ：棋子只能上下移动"
    fengzi "旋风 ↗↙ ：棋子只能斜向移动"
    
    fengzi "记住哦！棋子不能横穿风向！"
    
    centered "{b}{size=+5}三、风眼特权{/size}{/b}"
    
    fengzi "[FengziDialogue.get('tutorial_wind_eye')]"
    
    centered "{b}{size=+5}四、获胜条件{/size}{/b}"
    
    fengzi "[FengziDialogue.get('tutorial_win')]"
    fengzi "可以是横线、竖线，或者斜线~"
    
    centered "{b}{size=+5}五、操作说明{/size}{/b}"
    
    fengzi "点击你的棋子（蓝色●）选中它"
    fengzi "绿色的格子表示可以移动的位置"
    fengzi "再次点击目标位置即可移动"
    
    fengzi "好啦！教程结束，开始练习吧！"
    fengzi "我会陪着[player_name]前辈一起下的~"
    
    $ current_game = WindChessGame()
    $ game_mode = "tutorial"
    $ gsm = get_game_state_manager()
    $ gsm.start_game()
    
    # ★ 设置玩家移动完成后的跳转目标
    $ set_player_move_jump("tutorial_player_done")

    jump tutorial_loop

# ★ 教程模式：玩家回合
label tutorial_loop:
    $ gsm = get_game_state_manager()

    if gsm.phase == GamePhase.PLAYER_SELECT or gsm.phase == GamePhase.PLAYER_MOVE:
        # ★ 重新设置玩家移动完成后的跳转目标
        $ set_player_move_jump("tutorial_player_done")
        
        show screen game_screen(current_game, "tutorial")
        
        # ★ 使用全局标志控制循环
        $ _game_waiting = True
        while _game_waiting:
            $ result = renpy.ui.interact(suppress_overlay=True, suppress_underlay=True)
            if isinstance(result, str):
                if result == "menu":
                    $ _game_waiting = False
                    $ _return = "menu"
                elif result == "restart":
                    $ _game_waiting = False
                    $ _return = "restart"
        
        # 隐藏 screen
        hide screen game_screen
        
        # 处理返回按钮
        if _return == "menu":
            $ gsm.reset()
            $ _return = None
            $ _game_waiting = True
            jump main_menu_label
        elif _return == "restart":
            $ gsm.reset()
            $ _return = None
            $ _game_waiting = True
            jump tutorial_game
        
        jump tutorial_loop

    jump tutorial_loop

# ★ 教程模式：玩家移动完成后的处理
label tutorial_player_done:
    $ gsm = get_game_state_manager()
    
    # 隐藏棋盘 screen
    hide screen game_screen
    
    if current_game.game_over:
        if current_game.winner == Player.A:
            $ am = get_achievement_manager()
            $ am.complete_tutorial()
            $ gsm.reset()
            centered "{b}恭喜获胜！{/b}"
            fengzi "[player_name]前辈太厉害了！"
            fengzi "教程全部完成啦~"
            fengzi "以后也要经常来找我下棋哦~"
        else:
            $ gsm.reset()
            centered "{b}风子获胜了...{/b}"
            fengzi "哼哼~[player_name]前辈还要多练习呢~"
            fengzi "没关系！再来一局吧！"

        menu:
            "再来一局":
                jump tutorial_game
            "返回主菜单":
                jump main_menu_label

    # ★ 教程模式：AI自动行动
    # move_piece 内部已经切换了 current_player
    if current_game.current_player == Player.B:
        $ cell_size = 50
        
        # 显示静态棋盘
        show expression ChessBoardDisplay(current_game, cell_size=cell_size) as cb at board_transform
        
        # AI说话
        fengzi "[FengziDialogue.get('my_turn')]"
        $ renpy.pause(0.3)
        
        # AI移动
        $ current_game.ai_make_move()
        $ current_game.change_wind()
        
        # 刷新棋盘
        show expression ChessBoardDisplay(current_game, cell_size=cell_size) as cb at board_transform
        $ renpy.restart_interaction()
        
        # AI评论
        fengzi "[FengziDialogue.get('good_move')]"
        
        hide expression cb
        
        if current_game.game_over:
            jump tutorial_player_done
        
        # 重置状态机到玩家选子
        $ gsm.set_phase(GamePhase.PLAYER_SELECT)
        
        jump tutorial_loop

# -------------------- 双人对战 --------------------
label pvp_game:
    # 先隐藏主菜单屏幕
    hide screen main_menu
    hide screen say
    
    scene black with fade
    
    # ★ 设置紧张刺激的下棋音乐
    $ _set_music(2)
    $ _set_background(1)  # 下棋背景
    $ _hide_fengzi()  # PVP 不显示立绘
    
    centered "{b}{size=+5}双人对战{/size}{/b}"
    
    centered "玩家A（●）先手"
    centered "玩家B（○）后手"
    
    $ current_game = WindChessGame()
    $ game_mode = "pvp"
    $ gsm = get_game_state_manager()
    $ gsm.start_game()
    
    # 设置玩家移动完成后的跳转目标
    $ set_player_move_jump("pvp_player_done")

    jump pvp_loop

label pvp_loop:
    $ gsm = get_game_state_manager()

    if gsm.phase == GamePhase.PLAYER_SELECT or gsm.phase == GamePhase.PLAYER_MOVE:
        # ★ 重新设置玩家移动完成后的跳转目标
        $ set_player_move_jump("pvp_player_done")
        
        show screen game_screen(current_game, "pvp")
        
        # ★ 使用全局标志控制循环
        $ _game_waiting = True
        while _game_waiting:
            $ result = renpy.ui.interact(suppress_overlay=True, suppress_underlay=True)
            if isinstance(result, str):
                if result == "menu":
                    $ _game_waiting = False
                    $ _return = "menu"
                elif result == "restart":
                    $ _game_waiting = False
                    $ _return = "restart"
        
        # 隐藏 screen
        hide screen game_screen
        
        # 处理返回按钮
        if _return == "menu":
            $ gsm.reset()
            $ _return = None
            $ _game_waiting = True
            jump main_menu_label
        elif _return == "restart":
            $ gsm.reset()
            $ _return = None
            $ _game_waiting = True
            jump pvp_game
        
        jump pvp_loop
    
    # 安全回退：如果状态异常（不应发生），返回游戏循环
    jump pvp_loop

# PVP 模式：玩家移动完成
label pvp_player_done:
    $ gsm = get_game_state_manager()
    
    hide screen game_screen
    
    if current_game.game_over:
        $ gsm.reset()
        if current_game.winner == Player.A:
            centered "{b}玩家A（●）获胜！{/b}"
        else:
            centered "{b}玩家B（○）获胜！{/b}"

        menu:
            "再来一局":
                jump pvp_game
            "返回主菜单":
                jump main_menu_label

    # 切换玩家
    $ current_game.switch_player()
    $ current_game.change_wind()
    # 重置状态机到玩家选子阶段
    $ gsm.set_phase(GamePhase.PLAYER_SELECT)
    
    jump pvp_loop


# -------------------- 与风子聊天（28天话题系统）--------------------
label chat_game:
    # 先隐藏主菜单屏幕
    hide screen main_menu
    hide screen say
    
    scene black with fade
    
    # ★ 设置一般时间音乐和聊天背景
    $ _set_music(1)
    $ _set_background(1)  # 聊天背景
    $ _set_mood(2)  # 开心心情
    
    $ am = get_achievement_manager()
    $ progress = am.data
    
    # 检查特殊结局后的对话
    if progress["special_endings"]["confession"]:
        # 告白结局后的对话
        fengzi "[player_name]前辈...你又来陪我了呢~"
        fengzi "（害羞地笑）能和[player_name]前辈在一起，我很幸福哦~"
        jump chat_after_confession
    elif progress["special_endings"]["sulking"]:
        # 赌气结局后的对话
        fengzi "...哼"
        fengzi "（偷瞄[player_name]前辈）...[player_name]前辈又来找我了呢"
        fengzi "（小声）...其实我没有真的生气啦..."
        jump chat_after_sulking
    elif progress["chat_completed"]:
        # 28天聊天完成后的对话
        fengzi "[player_name]前辈~我们聊了好多好多呢~"
        fengzi "（幸福地笑）和[player_name]前辈在一起的每一天，我都记得哦~"
        jump chat_menu_completed
    else:
        # 进入28天聊天系统
        jump chat_28_days

# 28天聊天主入口
label chat_28_days:
    $ am = get_achievement_manager()
    $ topic_index = am.get_current_topic()
    $ topics = FengziDialogue._pname_all(FengziDialogue.TOPICS_28)
    $ current_topic = topics[topic_index]
    $ am.data["chat_days"] = topic_index + 1  # 更新天数
    
    centered "{b}{size=+5}{color=#000000}第 [topic_index + 1] 天{/color}{/size}{/b}"
    centered "{b}[current_topic['name']]{/b}"
    
    fengzi "[FengziDialogue.get('greeting')]"
    
    jump chat_topic_conversation

# 话题对话循环
label chat_topic_conversation:
    $ am = get_achievement_manager()
    $ topic_index = am.get_current_topic()
    $ topics = FengziDialogue._pname_all(FengziDialogue.TOPICS_28)
    
    # 检查是否还有话题
    if topic_index >= 28:
        jump chat_all_completed
    
    $ current_topic = topics[topic_index]
    $ conversations = current_topic["conversations"]
    
    # 显示话题中的对话
    $ conv_index = 0

label chat_conv_loop:
    $ am = get_achievement_manager()
    $ topic_index = am.get_current_topic()
    $ topics = FengziDialogue._pname_all(FengziDialogue.TOPICS_28)
    $ current_topic = topics[topic_index]
    $ conversations = current_topic["conversations"]
    
    if conv_index >= len(conversations):
        # 本话题结束
        jump chat_topic_end
    
    $ conv = conversations[conv_index]

    $ _set_mood(2)  # 日常
    fengzi "[conv['question']]"

    # 直接使用对话选项，不再构建中间变量
    menu:
        "[conv['responses'][0][0]]":
            $ am.add_mood_points(conv['responses'][0][1])
            $ _set_mood(am.get_wind_mood())
            fengzi "[conv['responses'][0][2]]"
            $ conv_index += 1
            jump chat_conv_loop
        "[conv['responses'][1][0]]":
            $ am.add_mood_points(conv['responses'][1][1])
            $ _set_mood(am.get_wind_mood())
            fengzi "[conv['responses'][1][2]]"
            $ conv_index += 1
            jump chat_conv_loop
        "[conv['responses'][2][0]]":
            $ am.add_mood_points(conv['responses'][2][1])
            $ _set_mood(am.get_wind_mood())
            fengzi "[conv['responses'][2][2]]"
            $ conv_index += 1
            jump chat_conv_loop

label chat_topic_end:
    $ am = get_achievement_manager()
    $ am.advance_topic()
    $ season = am.record_chat_day()
    
    if season:
        jump season_event
    
    fengzi "和[player_name]前辈聊天真开心呢~"
    jump chat_28_days

# 28天全部完成
label chat_all_completed:
    $ am = get_achievement_manager()
    $ am.data["chat_completed"] = True
    $ am.save()
    
    fengzi "[player_name]前辈...谢谢你陪我聊了这么久~"
    fengzi "这28天的回忆，我会一直珍藏在心里的~"
    fengzi "（伸出手）[player_name]前辈，以后也要一直陪着我哦~"
    
    jump chat_menu_completed

# 聊天完成后的菜单
label chat_menu_completed:
    menu:
        "和风子下棋":
            jump pve_game
        "返回主菜单":
            jump main_menu_label

label chat_after_confession:
    menu:
        "今天也陪陪你":
            fengzi "真的吗！太好了~"
            fengzi "（开心地拉着[player_name]前辈的袖子）"
            return
        "想和你下棋":
            fengzi "好呀~和[player_name]前辈下棋最开心了~"
            jump pve_game
        "我该回去了":
            fengzi "...嗯，[player_name]前辈下次再来哦"
            fengzi "（小声）...我会想你的..."
            jump main_menu_label

label chat_after_sulking:
    menu:
        "对不起啦，别生气了":
            fengzi "哼...谁生气了！"
            fengzi "（转过脸去）...我才没有生气呢..."
            fengzi "...好吧，看在[player_name]前辈这么诚恳的份上"
            fengzi "（小声）...我就原谅你吧..."
            fengzi "（抬起头笑了）那[player_name]前辈陪我下棋吧！"
            jump pve_game
        "今天来下棋吧":
            fengzi "...哼，看在棋的份上"
            fengzi "我就和[player_name]前辈下一盘！"
            jump pve_game
        "我先走了":
            fengzi "...随便你"
            fengzi "（小声）...下次一定要来哦..."
            jump main_menu_label

# 兼容旧的聊天标签（重定向到28天系统）
label chat_daily:
    $ am = get_achievement_manager()
    $ topic_index = am.get_current_topic()
    $ topics = FengziDialogue._pname_all(FengziDialogue.TOPICS_28)
    $ current_topic = topics[topic_index]
    
    fengzi "今天啊~[current_topic['conversations'][0]['question']]"
    
    menu:
        "[current_topic['conversations'][0]['responses'][0][0]]":
            $ am.add_mood_points(current_topic['conversations'][0]['responses'][0][1])
            fengzi "[current_topic['conversations'][0]['responses'][0][2]]"
        "[current_topic['conversations'][0]['responses'][1][0]]":
            $ am.add_mood_points(current_topic['conversations'][0]['responses'][1][1])
            fengzi "[current_topic['conversations'][0]['responses'][1][2]]"
        "[current_topic['conversations'][0]['responses'][2][0]]":
            $ am.add_mood_points(current_topic['conversations'][0]['responses'][2][1])
            fengzi "[current_topic['conversations'][0]['responses'][2][2]]"
    
    $ season = am.record_chat_day()
    if season:
        jump season_event
    
    fengzi "和[player_name]前辈聊天真开心~"
    return

label chat_weather:
    $ am = get_achievement_manager()
    $ topic_index = am.get_current_topic()
    $ topics = FengziDialogue._pname_all(FengziDialogue.TOPICS_28)
    $ current_topic = topics[topic_index]
    
    fengzi "天气吗？我喜欢晴天呢~"
    fengzi "阳光明媚的日子最适合下棋了！"
    fengzi "[player_name]前辈呢？喜欢什么天气？"
    
    menu:
        "晴天":
            fengzi "真的吗！我们喜好一样呢~"
            fengzi "以后晴天一起出去散步吧~"
        "雨天":
            fengzi "雨天也不错~听着雨声下棋很有氛围呢"
            fengzi "下次雨天来找我吧~"
        "雪天":
            fengzi "雪天很浪漫呢~和[player_name]前辈一起看雪一定很美好~"
            fengzi "（脸红）我、我是说一起看雪而已啦..."
    
    $ season = am.record_chat_day()
    if season:
        jump season_event
    
    return

label chat_hobby:
    fengzi "爱好啊~我喜欢看漫画呢！"
    fengzi "还有弹吉他、收集贝壳~"
    fengzi "[player_name]前辈呢？平时喜欢做什么？"
    
    menu:
        "下棋":
            fengzi "哈哈哈~[player_name]前辈和我一样呢！"
            fengzi "看来我们是命中注定的对手呢~"
        "看书":
            fengzi "看书啊~[player_name]前辈是学霸吗？好厉害！"
            fengzi "下次借我看看呗~"
        "玩游戏":
            fengzi "玩游戏！我也喜欢！我们一起玩吧~"
            fengzi "不过下棋的话我可是不会输的哦~"
    
    $ season = am.record_chat_day()
    if season:
        jump season_event
    
    return

label chat_dream:
    fengzi "梦想啊..."
    fengzi "我的梦想是成为最强的风棋手！"
    fengzi "然后...和[player_name]前辈一直一起下棋~"
    
    fengzi "（小声）[player_name]前辈会不会觉得我很奇怪..."
    
    menu:
        "一点也不奇怪":
            fengzi "真的吗！[player_name]前辈...谢谢你！"
            fengzi "（开心地笑）我会努力的！"
            fengzi "为了能和[player_name]前辈一直下棋~"
        "确实有点奇怪":
            fengzi "哼！[player_name]前辈真过分！"
            fengzi "明明是[player_name]前辈的问题！"
            fengzi "（鼓起脸颊）我要生气了..."
            fengzi "（忍不住笑了）开玩笑啦~"
    
    $ season = am.record_chat_day()
    if season:
        jump season_event
    
    return

label chat_chess:
    fengzi "下棋啊~"
    fengzi "[player_name]前辈觉得风之棋最有趣的地方是什么呢？"
    
    menu:
        "风的变化":
            fengzi "对对对！风向的变化让每局棋都不一样呢~"
            fengzi "这就是风之棋的魅力所在！"
        "和[player_name]前辈下棋":
            fengzi "（脸红）前、[player_name]前辈..."
            fengzi "能和[player_name]前辈一起下棋，我也很开心呢~"
        "思考的过程":
            fengzi "[player_name]前辈说得对！思考每一步棋的过程很有趣~"
            fengzi "特别是想出妙招的时候，特别有成就感！"
    
    $ season = am.record_chat_day()
    if season:
        jump season_event
    
    return

label season_event:
    if season == "spring":
        centered "{b}{size=+5}【春日赏樱】{/size}{/b}" with dissolve
        $ _set_background(2)
        $ _set_music(3)
        fengzi "[player_name]前辈！快看！樱花开了呢~"
        $ _set_background(3)
        $ renpy.pause(10.0)
        fengzi "粉色的花瓣随风飘落，好浪漫啊~"
        $ _set_background(4)
        $ renpy.pause(10.0)
        fengzi "能和[player_name]前辈一起看樱花，我觉得很幸福哦~"
        $ _set_background(5)
        $ renpy.pause(10.0)
        fengzi "（伸出手接住飘落的花瓣）"
        fengzi "[player_name]前辈，我们要一直这样在一起呢~"
    elif season == "summer":
        centered "{b}{size=+5}【夏日祭典】{/size}{/b}" with dissolve
        $ _set_background(6)
        $ _set_music(3)
        fengzi "[player_name]前辈！今天有夏日祭典呢~"
        $ _set_background(7)
        $ renpy.pause(10.0)
        fengzi "好多小摊子啊！有棉花糖、刨冰、还有捞金鱼！"
        $ _set_background(8)
        $ renpy.pause(10.0)
        fengzi "（开心地拉着[player_name]前辈的手）"
        fengzi "那我们一起去看烟火吧！"
        $ _set_background(9)
        $ renpy.pause(10.0)
        fengzi "（看着烟火）好美啊...能和[player_name]前辈一起看，真好..."
    elif season == "autumn":
        centered "{b}{size=+5}【秋季露营】{/size}{/b}" with dissolve
        $ _set_background(10)
        $ _set_music(3)
        fengzi "[player_name]前辈~森林里的空气好清新啊~"
        $ _set_background(11)
        $ renpy.pause(10.0)
        fengzi "秋天的枫叶红红的，好漂亮~"
        $ _set_background(12)
        $ renpy.pause(10.0)
        fengzi "（把一片枫叶递给[player_name]前辈）送给你~"
        $ _set_background(13)
        $ renpy.pause(10.0)
        fengzi "记得我们一起在森林里露营的时光吗？"
        fengzi "那是我最美好的回忆之一呢~"
    elif season == "winter":
        centered "{b}{size=+5}【冬季滑雪】{/size}{/b}" with dissolve
        $ _set_background(14)
        $ _set_music(3)
        fengzi "[player_name]前辈！下雪了呢~好漂亮啊！"
        $ _set_background(15)
        $ renpy.pause(10.0)
        fengzi "白雪覆盖了整个世界，就像童话一样~"
        $ _set_background(16)
        $ renpy.pause(10.0)
        fengzi "（张开双臂接住雪花）"
        $ _set_background(17)
        $ renpy.pause(10.0)
        fengzi "啊...有点冷..."
        fengzi "（靠近[player_name]前辈）[player_name]前辈...借我一点温暖吧~"
    
    centered "【季节事件完成】"
    return

# -------------------- 特殊结局 --------------------
label sulking_ending:
    scene black with fade
    
    # ★ 设置相关音乐和背景
    $ _set_music(3)
    $ _set_background(18)  # 赌气结局背景1
    
    $ am = get_achievement_manager()
    $ am.trigger_special_ending("sulking")
    
    centered "{b}{size=+10}特殊结局{/size}{/b}"
    centered "{b}风子的赌气{/b}"
    
    pause 1.0
    
    $ _set_background(19)  # 赌气结局背景2
    fengzi "哼！讨厌的[player_name]前辈！"
    fengzi "每次都赢我..."
    fengzi "我...我再也不理你了！"
    
    fengzi "（转身离开，但走得很慢）"
    
    fengzi "...哼！"
    
    $ _set_background(20)  # 赌气结局背景3：夜晚的街道
    centered "{b}当晚，回家的路上{/b}"
    
    fengzi "（独自走在夜晚的街道上，踢着路边的小石子）"
    fengzi "哼...哼什么啊...明明...明明是我自己想多下一盘的..."
    
    fengzi "（抬头看了看夜空，路灯把影子拉得好长）"
    fengzi "...[player_name]前辈现在在做什么呢..."
    fengzi "（小声）...我又没说真的不理你了..."
    
    fengzi "（忽然停下脚步，攥紧了拳头）"
    fengzi "对、对了！明天一定要赢回来！"
    fengzi "...（小声）不是因为想见你哦！只是...只是想赢棋而已！"
    
    # ★ 在对话框中显示最后的对话
    fengzi "..."
    fengzi "（加快脚步，走出几步又忍不住回头望了一眼来时的路）"
    fengzi "（微笑）...明天见，[player_name]前辈。"
    
    # ★ 隐藏对话框，屏幕变黑，显示白色文字
    $ renpy.hide_screen("say")
    scene black with fade
    
    pause 0.5
    
    centered "{b}{size=+5}结局：还有明天{/size}{/b}"
    
    pause 1.5
    
    centered "{color=#ffffff}只为博君一笑，不必照单全收{/color}"
    
    pause 1.0
    
    centered "{color=#ffffff}感谢您游玩本游戏{/color}"
    
    pause 1.5
    
    menu:
        "再来一局":
            jump pve_game
        "返回主菜单":
            jump main_menu_label

label confession_ending:
    scene black with fade
    
    # ★ 设置浪漫音乐和告白背景
    $ _set_music(3)
    $ _set_background(21)  # 告白结局背景1
    
    $ am = get_achievement_manager()
    $ am.trigger_special_ending("confession")
    
    centered "{b}{size=+10}特殊结局{/size}{/b}"
    centered "{b}风子的告白{/b}"
    
    pause 1.0
    
    $ _set_background(22)  # 告白结局背景2
    
    centered "{b}风棋社，黄昏{/b}"
    
    fengzi "[player_name]前辈..."
    fengzi "其实我一直想告诉你..."
    
    fengzi "虽然我总是输给[player_name]前辈"
    fengzi "但我真的很开心..."
    
    fengzi "[player_name]前辈...我..."
    fengzi "我喜欢你！"
    
    fengzi "从第一次和[player_name]前辈下棋开始"
    fengzi "我就一直喜欢着[player_name]前辈..."
    
    fengzi "我知道我很笨，总是输"
    fengzi "但是..."
    fengzi "和[player_name]前辈在一起的时间"
    fengzi "是我最开心的时候..."
    
    # ★ 隐藏对话框，屏幕变黑，显示白色文字
    $ renpy.hide_screen("say")
    scene black with fade
    
    pause 0.5
    
    centered "{b}{size=+5}结局：输了游戏，赢了人生{/size}{/b}"
    
    pause 1.5
    
    centered "{color=#ffffff}只为博君一笑，不必照单全收{/color}"
    
    pause 1.0
    
    centered "{color=#ffffff}感谢您游玩本游戏{/color}"
    
    pause 1.5
    
    # 显示制作人员名单
    call show_credits from _call_show_credits
    
    menu:
        "返回主菜单":
            jump main_menu_label

# -------------------- 赌气/告白模式游戏 --------------------
label sulking_mode_game:
    scene black with fade

    # ★ 设置相关音乐和背景
    $ _set_music(2)
    $ _set_background(1)  # 下棋背景
    $ _set_mood(3)  # 俏皮/赌气心情

    fengzi "...哼"
    fengzi "（不情愿地抬起头）[player_name]前辈来了啊..."
    fengzi "...来下棋的吗？"

    $ current_game = WindChessGame()
    $ game_mode = "pve"
    $ wind_changed_this_turn = False
    $ is_critical_game = False
    $ gsm = get_game_state_manager()
    $ gsm.start_game()

    jump pve_loop

label confession_mode_game:
    scene black with fade

    # ★ 设置浪漫音乐和背景
    $ _set_music(1)
    $ _set_background(1)  # 下棋背景
    $ _set_mood(8)  # 温柔心情

    fengzi "[player_name]前辈~你来啦~"
    fengzi "（害羞地笑）能和你下棋，真好~"

    $ current_game = WindChessGame()
    $ game_mode = "pve"
    $ wind_changed_this_turn = False
    $ is_critical_game = False
    $ gsm = get_game_state_manager()
    $ gsm.start_game()

    jump pve_loop
