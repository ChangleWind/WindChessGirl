# script.rpy - Ren'Py 入口脚本
# 游戏主逻辑定义在 wind_chess_renpy.rpy 中

# 主入口点 - 跳转到 wind_chess_renpy.rpy 中的 start 标签
label start:
    call wind_chess_start from _call_wind_chess_start
    return
