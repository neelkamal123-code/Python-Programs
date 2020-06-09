import cx_Freeze
executables = [cx_Freeze.Executable("xoduku.py")]

cx_Freeze.setup(
    name = "Space Welcomes You",
    options = {"build_exe":{"packages":["pygame"],
    "include_files":["chicken.png","end_screen.png","enemy_bullets.png"
    ,"enemyship.png","explosion.wav","heroship.png","laser.wav",
    "level_1.jpg","level_2.jpg","level_3.jpg","player_bullets.png",
    "pubg.png","welcome_screen.png","welcome.mp3","XOD.png",]}},

    executables = executables

)