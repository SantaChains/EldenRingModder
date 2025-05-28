# Elden Ring ModEngine2 TOML Configurator
一个用于自动生成 Elden Ring 游戏 ModEngine2 配置文件的 Python 工具。该工具会扫描当前目录，识别 DLL 文件和 Mod 文件夹，并生成符合 ModEngine2 规范的*config_eldenring.toml*配置文件。

# 使用方法
解压并将脚本放置在MOD根目录（与 modengine2_launcher.exee 同级）
确保已安装 Python 3.8 或更高版本
运行程序: EldenRingModder.exe
脚本会自动生成或**覆盖**config_eldenring.toml文件
启动 ModEngine2 加载游戏
>[modengine]
debug = false
external_dlls = [ 
    "dinput8.dll",
    "dsound.dll",
    其他DLL文件...
]
[extension.mod_loader]
enabled = true
loose_params = false
mods = [
    { enabled = true, name = "MyMod1", path = "mods\\MyMod1" },
    { enabled = true, name = "MyMod2", path = "mods\\MyMod2" },
    # 其他Mod...
]
[extension.scylla_hide]
enabled = false

# 功能限制
1. 路径处理
脚本使用双反斜杠\\作为路径分隔符，适用于 Windows 环境
生成的是相对于脚本位置的相对路径，移动脚本可能导致路径失效
2. Mod 识别算法
依赖预定义的文件夹和文件列表，可能无法识别所有类型的 Mod
嵌套过深的 Mod 结构可能无法被正确检测
如需扩展识别规则，可修改is_mod_folder函数
3. 配置文件覆盖
每次运行都会覆盖现有config_eldenring.toml文件
建议在运行前备份重要的自定义配置
4. 兼容性
仅在 Windows 环境下测试过
可能与特殊命名的 DLL 或 Mod 文件夹存在冲突

# 使用此工具时请注意：
工具按 "原样" 提供，作者不对任何游戏问题、数据丢失或其他损失负责
使用前请确保备份游戏文件和现有配置
如遇 Mod 加载问题，请检查生成的配置文件是否正确

# 贡献与改进
欢迎对本工具提出改进建议或提交 Pull Request。您可以：
扩展 Mod 识别规则
添加配置文件备份功能
优化目录扫描性能
改进错误处理机制
如需帮助或遇到问题，请在项目仓库提交 Issue。
