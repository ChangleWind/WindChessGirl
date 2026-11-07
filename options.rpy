# options.rpy - Ren'Py 项目配置
# ============================================================

# 基础设置
define config.name = _("风棋少女")
define config.version = "1.0.0"

# 窗口设置
define config.window_title = "风棋少女 - Wind Chess Girl"

# 存档设置
define config.save_on_mobile_background = False
define config.autosave_on_quit = True

# 调试设置
define config.developer = True

# 屏幕设置
define config.screen_width = 1280
define config.screen_height = 720

# 背景颜色
define gui.main_menu_background = "#1a1a2e"
define gui.game_menu_background = "#1a1a2e"

# 对话框设置
define gui.textbox_height = 200
define gui.text_xpos = 0.5
define gui.text_ypos = 0.8
define gui.name_xpos = 0.5
define gui.name_ypos = 0.55
define gui.dialogue_width = 1200

# 中文字体配置
init python:
    # 尝试使用系统中文字体（按优先级）
    font_list = [
        "SourceHanSerifSC-Regular.otf",    # 思源宋体
        "SourceHanSansCN-Regular.otf",    # 思源黑体（备用）
        "msyh.ttc",                      # 微软雅黑
        "simhei.ttf",                    # 黑体
        "simsun.ttc",                    # 宋体
    ]
    
    # 查找可用的中文字体
    def get_chinese_font():
        for font in font_list:
            if renpy.loadable(font):
                return font
        return None
    
    chinese_font = get_chinese_font()
    
    if chinese_font:
        gui.font = chinese_font
        style.default.font = chinese_font
    else:
        # 如果没有中文字体，使用默认字体（可能显示不正常）
        pass
    
    # 默认样式
    style.default.size = 22
    style.default.color = '#ffffff'


## This section contains information about how to build your project into
## distribution files.
init python:

    ## The name that's used for directories and archive files. For example, if
    ## this is 'mygame-1.0', the windows distribution will be in the
    ## directory 'mygame-1.0-win', in the 'mygame-1.0-win.zip' file.
    build.directory_name = "WindChessGirl-1.0"

    ## The name that's uses for executables - the program that users will run
    ## to start the game. For example, if this is 'mygame', then on Windows,
    ## users can click 'mygame.exe' to start the game.
    build.executable_name = "WindChessGirl"

    ## If True, Ren'Py will include update information into packages. This
    ## allows the updater to run.
    build.include_update = False

    ## File patterns:
    ##
    ## The following functions take file patterns. File patterns are case-
    ## insensitive, and matched against the path relative to the base
    ## directory, with and without a leading /. If multiple patterns match,
    ## the first is used.
    ##
    ##
    ## In a pattern:
    ##
    ## /
    ##     Is the directory separator.
    ## *
    ##     Matches all characters, except the directory separator.
    ## **
    ##     Matches all characters, including the directory separator.
    ##
    ## For example:
    ##
    ## *.txt
    ##     Matches txt files in the base directory.
    ## game/**.ogg
    ##     Matches ogg files in the game directory or any of its subdirectories.
    ## **.psd
    ##    Matches psd files anywhere in the project.

    ## Classify files as None to exclude them from the built distributions.

    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)

    ## To archive files, classify them as 'archive'.

    # build.classify('game/**.png', 'archive')
    # build.classify('game/**.jpg', 'archive')

    ## Files matching documentation patterns are duplicated in a mac app
    ## build, so they appear in both the app and the zip file.

    build.documentation('*.html')
    build.documentation('*.txt')
