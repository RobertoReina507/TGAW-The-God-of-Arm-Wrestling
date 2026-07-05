"""
FuerzitasPrototype.py
UPBGE 0.50 / Blender 5.x - Python Component - v9.3 standalone audio path fix from v9.2

Attach this component to an Empty named GameManager.

Starter scene object names:
    GameManager
    Needle
    GreenZone_Weak_00...GreenZone_Weak_89
    GreenZone_Medium_00...GreenZone_Medium_89
    GreenZone_Strong_00...GreenZone_Strong_89
    PhaseArc_Spawn_00...PhaseArc_Spawn_179
    PhaseArc_Plan_00...PhaseArc_Plan_179
    PhaseArc_Reveal_00...PhaseArc_Reveal_179
    Pip_Player_01_Empty / Weak / Medium / Strong
    Pip_Enemy_01_Empty / Weak / Medium / Strong

Legacy fallback object names still supported:
    GreenZone
    UI_PlayerSeq, UI_EnemySeq, UI_Status, UI_Level, UI_Force, UI_Balance

Controls:
    SPACE  -> Player 1 hit
    ENTER  -> Player 2 hit in LOCAL_2P mode
    ESC    -> Pause / back
    Mouse  -> Menu buttons
    Arrows -> Navigate menus
    ENTER  -> Select menu option
    R      -> Restart current match during gameplay
    N      -> Force next level for testing during gameplay
    M      -> Toggle 1P_VS_AI / LOCAL_2P for testing during gameplay
"""

import random
import os
import sys
from math import radians
from collections import OrderedDict

import bge
from mathutils import Euler


LEVELS = [
    {
        "name": "Nivel 1 - Bar de barrio",
        "opponent": "El Flaco",
        "needle_speed": 115.0,
        "green_size": 72.0,
        "zone_move_interval": 3.00,
        "zone_move_min": 18.0,
        "zone_move_max": 50.0,
        "ai_accuracy": 0.45,
        "ai_interval": 1.85,
        "ai_force3_chance": 0.08,
    },
    {
        "name": "Nivel 2 - Gimnasio viejo",
        "opponent": "La Roca",
        "needle_speed": 135.0,
        "green_size": 66.0,
        "zone_move_interval": 2.80,
        "zone_move_min": 22.0,
        "zone_move_max": 58.0,
        "ai_accuracy": 0.50,
        "ai_interval": 1.75,
        "ai_force3_chance": 0.11,
    },
    {
        "name": "Nivel 3 - Feria nocturna",
        "opponent": "Doña Garra",
        "needle_speed": 155.0,
        "green_size": 60.0,
        "zone_move_interval": 2.60,
        "zone_move_min": 26.0,
        "zone_move_max": 66.0,
        "ai_accuracy": 0.55,
        "ai_interval": 1.62,
        "ai_force3_chance": 0.14,
    },
    {
        "name": "Nivel 4 - Azotea industrial",
        "opponent": "Turbo Brazo",
        "needle_speed": 172.0,
        "green_size": 56.0,
        "zone_move_interval": 2.42,
        "zone_move_min": 30.0,
        "zone_move_max": 74.0,
        "ai_accuracy": 0.59,
        "ai_interval": 1.52,
        "ai_force3_chance": 0.17,
    },
    {
        "name": "Nivel 5 - Campeón local",
        "opponent": "El Titán",
        "needle_speed": 188.0,
        "green_size": 52.0,
        "zone_move_interval": 2.24,
        "zone_move_min": 34.0,
        "zone_move_max": 82.0,
        "ai_accuracy": 0.63,
        "ai_interval": 1.43,
        "ai_force3_chance": 0.20,
    },
    {
        "name": "Nivel 6 - Muelle nocturno",
        "opponent": "Mazo",
        "needle_speed": 202.0,
        "green_size": 49.0,
        "zone_move_interval": 2.08,
        "zone_move_min": 38.0,
        "zone_move_max": 88.0,
        "ai_accuracy": 0.66,
        "ai_interval": 1.36,
        "ai_force3_chance": 0.23,
    },
    {
        "name": "Nivel 7 - Taller clandestino",
        "opponent": "Chispa",
        "needle_speed": 216.0,
        "green_size": 46.0,
        "zone_move_interval": 1.94,
        "zone_move_min": 42.0,
        "zone_move_max": 94.0,
        "ai_accuracy": 0.69,
        "ai_interval": 1.30,
        "ai_force3_chance": 0.26,
    },
    {
        "name": "Nivel 8 - Ring de madera",
        "opponent": "La Muralla",
        "needle_speed": 228.0,
        "green_size": 43.0,
        "zone_move_interval": 1.82,
        "zone_move_min": 46.0,
        "zone_move_max": 100.0,
        "ai_accuracy": 0.72,
        "ai_interval": 1.24,
        "ai_force3_chance": 0.29,
    },
    {
        "name": "Nivel 9 - Club subterráneo",
        "opponent": "Nudillo",
        "needle_speed": 240.0,
        "green_size": 40.0,
        "zone_move_interval": 1.70,
        "zone_move_min": 50.0,
        "zone_move_max": 106.0,
        "ai_accuracy": 0.75,
        "ai_interval": 1.19,
        "ai_force3_chance": 0.32,
    },
    {
        "name": "Nivel 10 - Final del bar",
        "opponent": "Brazo de Hierro",
        "needle_speed": 252.0,
        "green_size": 38.0,
        "zone_move_interval": 1.60,
        "zone_move_min": 54.0,
        "zone_move_max": 112.0,
        "ai_accuracy": 0.78,
        "ai_interval": 1.14,
        "ai_force3_chance": 0.35,
    },
    {
        "name": "Nivel 11 - Circuito élite",
        "opponent": "La Bestia",
        "needle_speed": 262.0,
        "green_size": 36.0,
        "zone_move_interval": 1.52,
        "zone_move_min": 58.0,
        "zone_move_max": 118.0,
        "ai_accuracy": 0.80,
        "ai_interval": 1.10,
        "ai_force3_chance": 0.38,
    },
    {
        "name": "Nivel 12 - Mesa del campeón",
        "opponent": "El Imparable",
        "needle_speed": 272.0,
        "green_size": 34.0,
        "zone_move_interval": 1.44,
        "zone_move_min": 62.0,
        "zone_move_max": 124.0,
        "ai_accuracy": 0.82,
        "ai_interval": 1.06,
        "ai_force3_chance": 0.41,
    },
    {
        "name": "Nivel 13 - Reto internacional",
        "opponent": "Omega Grip",
        "needle_speed": 282.0,
        "green_size": 32.0,
        "zone_move_interval": 1.37,
        "zone_move_min": 66.0,
        "zone_move_max": 130.0,
        "ai_accuracy": 0.85,
        "ai_interval": 1.02,
        "ai_force3_chance": 0.44,
    },
    {
        "name": "Nivel 14 - Última ronda",
        "opponent": "El Coloso",
        "needle_speed": 292.0,
        "green_size": 30.0,
        "zone_move_interval": 1.31,
        "zone_move_min": 70.0,
        "zone_move_max": 136.0,
        "ai_accuracy": 0.88,
        "ai_interval": 0.98,
        "ai_force3_chance": 0.47,
    },
    {
        "name": "Nivel 15 - Gran final",
        "opponent": "The God of Arm Wrestling",
        "needle_speed": 302.0,
        "green_size": 28.0,
        "zone_move_interval": 1.25,
        "zone_move_min": 74.0,
        "zone_move_max": 142.0,
        "ai_accuracy": 0.90,
        "ai_interval": 0.94,
        "ai_force3_chance": 0.50,
    },
]


class FuerzitasPrototype(bge.types.KX_PythonComponent):
    args = OrderedDict([
        ("Mode", "1P_VS_AI"),           # Valid values: 1P_VS_AI, LOCAL_2P
        ("Start Level", 1),
        ("Start At Menu", True),
        ("Menu Enabled", True),
        ("Local Level", 1),
        ("Target Hits", 5),              # For the Outlast-like sequence, keep this at 5.
        ("Balance Win", 6),
        ("Auto Advance", True),
        ("Round End Delay", 2.0),
        ("Visual Rotation Sign", -1.0),  # Change to 1.0 if needle/zone rotate visually inverted.
        ("Guide Angle Offset", 0.0),     # Rotates green/yellow/orange logic and visuals together.

        # v5 target scheduling. Logical angles increase with the needle. With
        # Visual Rotation Sign = -1, these defaults place green mostly on the
        # lower-left side, yellow above/right, and orange near the right side,
        # matching the supplied design diagram.
        ("Spawn Arc Start", 20.0),
        ("Spawn Arc End", 210.0),
        ("Plan Arc Start", 220.0),
        ("Plan Arc End", 290.0),
        ("Reveal Arc Start", 292.0),
        ("Reveal Arc End", 350.0),
        ("Show Phase Guide", True),
        ("Clean HUD", True),
        ("Show Debug Hint", False),
        ("Arm Balance Angle", 24.0),
        ("Arm Hit Pulse Angle", 7.0),
        ("Arm Pulse Time", 0.22),
        ("Show Level Intro", True),
        ("Level Intro Time", 1.25),
        ("Show Result Summary", True),
        ("Result Screen Time", 2.40),
        ("Force Toast Time", 0.82),

        # v9 quality polish: keeps gameplay rules intact but improves feel.
        ("Input Buffer Time", 0.07),      # Small pre-window grace for human input.
        ("Transition Time", 0.28),        # Short fade between menu/game states.
        ("Pushbar Smooth", 13.0),         # Higher = faster push bar response.
        ("Arm Smooth", 11.0),             # Higher = faster arm visual response.
        ("Impact Flash Time", 0.16),
        ("Camera Shake Strength", 0.006),
        ("AI Humanization", True),

        # Menu / input.
        ("Mouse Origin Top", True),
        ("Mouse Y Inverted", False),
        ("Use Custom Cursor", False),
        ("Disable Esc Exit Key", True),
        ("Fullscreen On Start", True),

        # Audio. Put final files in //assets/audio/ with the names used by SOUND_FILES.
        ("Master Volume", 0.80),
        ("Music Volume", 0.42),
        ("SFX Volume", 0.90),
        ("Mute Audio", False),
        ("Audio Assets Path", "//assets/audio"),

        ("Debug Prints", False),
    ])

    FORCE_NAMES = {
        0: "Empty",
        1: "Weak",
        2: "Medium",
        3: "Strong",
    }

    FORCE_COLORS = {
        0: (0.58, 0.60, 0.62, 1.0),   # empty ring / neutral gray
        1: (0.98, 0.96, 0.86, 1.0),   # weak: warm white
        2: (1.00, 0.74, 0.06, 1.0),   # medium: yellow / amber
        3: (1.00, 0.18, 0.08, 1.0),   # strong: red-orange
    }

    MENU_SCREENS = ("MAIN_MENU", "MODE_SELECT", "LOCAL_LEVEL_SELECT", "SETTINGS", "EXIT_CONFIRM", "PAUSED")

    # Button rectangles use normalized screen coordinates with origin at top-left.
    # If your mouse clicks are vertically inverted in UPBGE, change the component
    # property "Mouse Origin Top" to False.
    BUTTONS = {
        # v8 coordinates match the modelled UI, not the old centered prototype boxes.
        "MAIN_MENU": [
            ("start", "MENU_Main_Btn_Start", "MENU_Main_Txt_Start", "Jugar", 0.240, 0.405, 0.335, 0.115),
            ("settings_main", "MENU_Main_Btn_Settings", "MENU_Main_Txt_Settings", "Opciones", 0.240, 0.550, 0.335, 0.105),
            ("exit_main", "MENU_Main_Btn_Exit", "MENU_Main_Txt_Exit", "Salir del juego", 0.240, 0.695, 0.335, 0.105),
        ],
        "MODE_SELECT": [
            ("mode_ai", "MENU_Mode_Btn_AI", "MENU_Mode_Txt_AI", "Contra IA", 0.500, 0.435, 0.430, 0.102),
            ("mode_local", "MENU_Mode_Btn_Local", "MENU_Mode_Txt_Local", "2 jugadores local", 0.500, 0.555, 0.430, 0.102),
            ("back_main", "MENU_Mode_Btn_Back", "MENU_Mode_Txt_Back", "Volver", 0.500, 0.705, 0.300, 0.086),
        ],
        "LOCAL_LEVEL_SELECT": [
            ("local_level_prev", "MENU_Local_Btn_Prev", "MENU_Local_Txt_Prev", "<", 0.390, 0.535, 0.080, 0.085),
            ("local_level_next", "MENU_Local_Btn_Next", "MENU_Local_Txt_Next", ">", 0.610, 0.535, 0.080, 0.085),
            ("local_level_start", "MENU_Local_Btn_Start", "MENU_Local_Txt_Start", "Iniciar duelo", 0.500, 0.655, 0.360, 0.092),
            ("back_mode", "MENU_Local_Btn_Back", "MENU_Local_Txt_Back", "Volver", 0.500, 0.780, 0.280, 0.080),
        ],
        "SETTINGS": [
            ("player_sleeve_prev", "MENU_Settings_Btn_PlayerColorPrev", "MENU_Settings_Txt_PlayerColorPrev", "<", 0.625, 0.365, 0.052, 0.065),
            ("player_sleeve_next", "MENU_Settings_Btn_PlayerColorNext", "MENU_Settings_Txt_PlayerColorNext", ">", 0.820, 0.365, 0.052, 0.065),
            ("enemy_sleeve_prev", "MENU_Settings_Btn_EnemyColorPrev", "MENU_Settings_Txt_EnemyColorPrev", "<", 0.625, 0.505, 0.052, 0.065),
            ("enemy_sleeve_next", "MENU_Settings_Btn_EnemyColorNext", "MENU_Settings_Txt_EnemyColorNext", ">", 0.820, 0.505, 0.052, 0.065),
            ("volume_down", "MENU_Settings_Btn_VolMinus", "MENU_Settings_Txt_VolMinus", "<", 0.625, 0.635, 0.052, 0.065),
            ("volume_up", "MENU_Settings_Btn_VolPlus", "MENU_Settings_Txt_VolPlus", ">", 0.820, 0.635, 0.052, 0.065),
            ("exit_settings", "MENU_Settings_Btn_Exit", "MENU_Settings_Txt_Exit", "Salir del juego", 0.500, 0.795, 0.595, 0.105),
        ],
        "EXIT_CONFIRM": [
            ("confirm_exit_yes", "MENU_Exit_Btn_Yes", "MENU_Exit_Txt_Yes", "Sí", 0.430, 0.610, 0.145, 0.086),
            ("confirm_exit_no", "MENU_Exit_Btn_No", "MENU_Exit_Txt_No", "No", 0.570, 0.610, 0.145, 0.086),
        ],
        "PAUSED": [
            ("resume", "MENU_Pause_Btn_Resume", "MENU_Pause_Txt_Resume", "Continuar", 0.500, 0.365, 0.350, 0.092),
            ("settings_pause", "MENU_Pause_Btn_Settings", "MENU_Pause_Txt_Settings", "Opciones", 0.500, 0.485, 0.350, 0.092),
            ("main_from_pause", "MENU_Pause_Btn_Main", "MENU_Pause_Txt_Main", "Menú principal", 0.500, 0.605, 0.350, 0.092),
            ("exit_pause", "MENU_Pause_Btn_Exit", "MENU_Pause_Txt_Exit", "Salir del juego", 0.500, 0.725, 0.350, 0.092),
        ],
    }

    DANGER_ACTIONS = {"exit_main", "exit_pause", "exit_settings", "confirm_exit_yes"}

    SLEEVE_PALETTE = [
        ("Azul noche", (0.08, 0.10, 0.16, 1.0)),
        ("Rojo vino", (0.42, 0.05, 0.06, 1.0)),
        ("Verde botella", (0.05, 0.26, 0.15, 1.0)),
        ("Mostaza", (0.78, 0.50, 0.08, 1.0)),
        ("Morado neón", (0.32, 0.10, 0.45, 1.0)),
        ("Gris acero", (0.34, 0.38, 0.44, 1.0)),
    ]

    SOUND_FILES = {
        "music_main": ("music_main.ogg", "music_main.wav", "music_main.mp3", "music_main.flac", "music_main.aac"),
        "hit_weak": ("hit_weak.wav", "hit_weak.ogg", "hit_weak.mp3", "hit_weak.flac"),
        "hit_medium": ("hit_medium.wav", "hit_medium.ogg", "hit_medium.mp3", "hit_medium.flac"),
        "hit_strong": ("hit_strong.wav", "hit_strong.ogg", "hit_strong.mp3", "hit_strong.flac"),
        "miss": ("miss.wav", "miss.ogg", "miss.mp3", "miss.flac"),
        "ui_click": ("ui_click.wav", "ui_click.ogg", "ui_click.mp3", "ui_click.flac"),
        "ui_start": ("ui_start.wav", "ui_start.ogg", "ui_start.mp3", "ui_start.flac"),
        "ui_back": ("ui_back.wav", "ui_back.ogg", "ui_back.mp3", "ui_back.flac"),
        "ui_exit": ("ui_exit.wav", "ui_exit.ogg", "ui_exit.mp3", "ui_exit.flac"),
        "ui_confirm": ("ui_confirm.wav", "ui_confirm.ogg", "ui_confirm.mp3", "ui_confirm.flac"),
    }

    def start(self, args):
        self.scene = bge.logic.getCurrentScene()

        self.fullscreen_on_start = bool(args.get("Fullscreen On Start", True))

        if self.fullscreen_on_start:
            try:
                bge.render.setFullScreen(True)
            except Exception as exc:
                print("[TGAW] No se pudo activar pantalla completa:", exc)

        self.mode = str(args.get("Mode", "1P_VS_AI")).strip().upper()
        if self.mode not in ("1P_VS_AI", "LOCAL_2P"):
            self.mode = "1P_VS_AI"

        self.level_index = max(0, min(len(LEVELS) - 1, int(args.get("Start Level", 1)) - 1))
        self.local_level_index = max(0, min(len(LEVELS) - 1, int(args.get("Local Level", 1)) - 1))
        self.start_at_menu = bool(args.get("Start At Menu", True))
        self.menu_enabled = bool(args.get("Menu Enabled", True))
        self.target_hits = max(1, int(args.get("Target Hits", 5)))
        self.balance_win = 6  # TGAW v8.7: fixed win condition requested by design: advantage +6
        self.auto_advance = bool(args.get("Auto Advance", True))
        self.round_end_delay = float(args.get("Round End Delay", 2.0))
        self.visual_rotation_sign = float(args.get("Visual Rotation Sign", -1.0))
        self.guide_angle_offset = float(args.get("Guide Angle Offset", 0.0)) % 360.0
        self.spawn_arc_start = float(args.get("Spawn Arc Start", 20.0)) % 360.0
        self.spawn_arc_end = float(args.get("Spawn Arc End", 210.0)) % 360.0
        self.plan_arc_start = float(args.get("Plan Arc Start", 220.0)) % 360.0
        self.plan_arc_end = float(args.get("Plan Arc End", 290.0)) % 360.0
        self.reveal_arc_start = float(args.get("Reveal Arc Start", 292.0)) % 360.0
        self.reveal_arc_end = float(args.get("Reveal Arc End", 350.0)) % 360.0
        self.show_phase_guide = bool(args.get("Show Phase Guide", True))
        self.clean_hud = bool(args.get("Clean HUD", True))
        self.show_debug_hint = bool(args.get("Show Debug Hint", False))
        self.arm_balance_angle = float(args.get("Arm Balance Angle", 24.0))
        self.arm_hit_pulse_angle = float(args.get("Arm Hit Pulse Angle", 7.0))
        self.arm_pulse_time = max(0.05, float(args.get("Arm Pulse Time", 0.22)))
        self.show_level_intro = bool(args.get("Show Level Intro", True))
        self.level_intro_time = max(0.0, float(args.get("Level Intro Time", 1.25)))
        self.show_result_summary = bool(args.get("Show Result Summary", True))
        self.result_screen_time = max(0.8, float(args.get("Result Screen Time", 2.40)))
        self.force_toast_time = max(0.35, float(args.get("Force Toast Time", 0.82)))
        self.input_buffer_time = self._clamp(float(args.get("Input Buffer Time", 0.07)), 0.0, 0.12)
        self.transition_time = self._clamp(float(args.get("Transition Time", 0.28)), 0.0, 0.75)
        self.pushbar_smooth = max(1.0, float(args.get("Pushbar Smooth", 13.0)))
        self.arm_smooth = max(1.0, float(args.get("Arm Smooth", 11.0)))
        self.impact_flash_time = self._clamp(float(args.get("Impact Flash Time", 0.16)), 0.0, 0.55)
        self.camera_shake_strength = self._clamp(float(args.get("Camera Shake Strength", 0.006)), 0.0, 0.025)
        self.ai_humanization = bool(args.get("AI Humanization", True))
        # v8.9: Roberto's UPBGE build reports bge.logic.mouse.position with a top-left Y origin.
        # Using inversion here made the custom cursor move upside-down. Keep it off by default.
        self.mouse_origin_top = bool(args.get("Mouse Origin Top", True))
        self.mouse_y_inverted = bool(args.get("Mouse Y Inverted", False))
        self.use_custom_cursor = bool(args.get("Use Custom Cursor", False))
        self.disable_esc_exit_key = bool(args.get("Disable Esc Exit Key", True))
        self.master_volume = self._clamp(float(args.get("Master Volume", 0.80)), 0.0, 1.0)
        self.music_volume = self._clamp(float(args.get("Music Volume", 0.42)), 0.0, 1.0)
        self.sfx_volume = self._clamp(float(args.get("SFX Volume", 0.90)), 0.0, 1.0)
        self.mute_audio = bool(args.get("Mute Audio", False))
        self.audio_assets_path = str(args.get("Audio Assets Path", "//assets/audio"))
        self.debug_prints = bool(args.get("Debug Prints", False))

        if self.disable_esc_exit_key:
            try:
                bge.logic.setExitKey(0)
            except Exception:
                pass

        # Runtime object references.
        self.needle = self._obj("Needle")
        self.green_zone = self._obj("GreenZone")  # Legacy single-color wedge fallback.
        self.arm_player = self._obj("Arm_Player")
        self.arm_enemy = self._obj("Arm_Enemy")
        self.arm_player_sleeve = self._obj("Arm_Player_Sleeve")
        self.arm_enemy_sleeve = self._obj("Arm_Enemy_Sleeve")
        if not self.arm_player_sleeve:
            self.arm_player_sleeve = self._find_child_suffix(self.arm_player, "Sleeve")
        if not self.arm_enemy_sleeve:
            self.arm_enemy_sleeve = self._find_child_suffix(self.arm_enemy, "Sleeve")
        self.player_sleeve_color_index = 0
        self.enemy_sleeve_color_index = 1

        # New segmented force-zone objects: white / yellow / red.
        self.max_zone_ticks = 90
        self.zone_ticks = {
            1: self._collect_numbered("GreenZone_Weak", self.max_zone_ticks),
            2: self._collect_numbered("GreenZone_Medium", self.max_zone_ticks),
            3: self._collect_numbered("GreenZone_Strong", self.max_zone_ticks),
        }
        self.use_segmented_zone = any(self.zone_ticks[force] for force in (1, 2, 3))
        if self.use_segmented_zone and self.green_zone:
            self.set_visible(self.green_zone, False)

        # v4.2 static guide arcs: green = possible target spawn region,
        # yellow = planning sector, orange = reveal/reaction sector.
        self.max_phase_ticks = 180
        self.phase_ticks = {
            "SPAWN": self._collect_numbered("PhaseArc_Spawn", self.max_phase_ticks),
            "PLAN": self._collect_numbered("PhaseArc_Plan", self.max_phase_ticks),
            "REVEAL": self._collect_numbered("PhaseArc_Reveal", self.max_phase_ticks),
        }

        # UI text references. These can be missing during early tests.
        self.ui_player = self._obj("UI_PlayerSeq")
        self.ui_enemy = self._obj("UI_EnemySeq")
        self.ui_status = self._obj("UI_Status")
        self.ui_level = self._obj("UI_Level")
        self.ui_force = self._obj("UI_Force")
        self.ui_balance = self._obj("UI_Balance")
        self.ui_hint = self._obj("UI_Hint")
        self.ui_player_label = self._obj("UI_PlayerLabel")
        self.ui_enemy_label = self._obj("UI_EnemyLabel")
        self.ui_intro_panel = self._obj("UI_Intro_Panel")
        self.ui_intro_title = self._obj("UI_Intro_Title")
        self.ui_intro_subtitle = self._obj("UI_Intro_Subtitle")
        self.ui_intro_hint = self._obj("UI_Intro_Hint")
        self.ui_result_panel = self._obj("UI_Result_Panel")
        self.ui_result_title = self._obj("UI_Result_Title")
        self.ui_result_stats = self._obj("UI_Result_Stats")
        self.ui_result_hint = self._obj("UI_Result_Hint")
        self.ui_fade_overlay = self._obj("UI_FadeOverlay")
        self.ui_impact_flash = self._obj("UI_ImpactFlash")
        self.game_camera = self._obj("Camera_FirstPersonPrototype")
        try:
            if not self.game_camera:
                self.game_camera = self.scene.active_camera
        except Exception:
            pass
        self.camera_base_local_position = self.game_camera.localPosition.copy() if self.game_camera else None

        # Optional polished balance bar objects created by upgrade_scene_v4.py.
        self.balance_bar_player = self._obj("UI_BalanceBar_Player")
        self.balance_bar_enemy = self._obj("UI_BalanceBar_Enemy")
        self.pushbar_bg = self._obj("UI_PushBar_BG")
        self.pushbar_player = self._obj("UI_PushBar_Player")
        self.pushbar_enemy = self._obj("UI_PushBar_Enemy")
        self.pushbar_marker = self._obj("UI_PushBar_Marker")
        self.pushbar_base = self._read_pushbar_base()

        # Preserve low-poly arm starting rotations. The runtime balance animation is applied on top.
        self.arm_player_base_orientation = self.arm_player.localOrientation.copy() if self.arm_player else None
        self.arm_enemy_base_orientation = self.arm_enemy.localOrientation.copy() if self.arm_enemy else None

        # New accumulator pip references. Each slot has an Empty/Weak/Medium/Strong object.
        self.pips = {
            "PLAYER": self._collect_pips("Pip_Player"),
            "ENEMY": self._collect_pips("Pip_Enemy"),
        }
        # v5.1 preferred accumulator layout: one fill object per slot, recolored at runtime.
        # This avoids the old stacked-disc issue where every slot could look red if visibility
        # did not update reliably in a given UPBGE build.
        self.simple_pips = {
            "PLAYER": self._collect_simple_pips("Pip_Player"),
            "ENEMY": self._collect_simple_pips("Pip_Enemy"),
        }
        self.use_simple_pip_ui = bool(self.simple_pips["PLAYER"] or self.simple_pips["ENEMY"])
        self.use_pip_ui = self.use_simple_pip_ui or bool(self.pips["PLAYER"] or self.pips["ENEMY"])

        # Menu/settings runtime state.
        self.screen = "MAIN_MENU" if (self.menu_enabled and self.start_at_menu) else "PLAYING"
        self.settings_return_screen = "MAIN_MENU"
        self.exit_return_screen = "MAIN_MENU"
        self.menu_selected_index = 0
        self.menu_hover_action = None

        self.menu_objects = self._collect_menu_objects()
        self.hud_objects = self._collect_hud_objects()
        self.menu_cursor = self._obj("MENU_Cursor")
        self.menu_cursor_norm = (0.5, 0.5)
        self.mouse_origin_top_active = self.mouse_origin_top

        # Audio runtime state. Everything is optional; missing files only disable sound.
        self.audio_device = None
        self.music_handle = None
        self.sound_cache = {}
        self.sfx_handles = []
        self.init_audio()

        self.last_time = bge.logic.getFrameTime()
        self.force_message_timer = 0.0
        self.arm_pulse_timer = 0.0
        self.arm_pulse_side = None
        self.arm_pulse_force = 0

        # v9 runtime smoothing/feedback state. These are visual only; they do not
        # change the scoring rules of v8.9.
        self.frame_dt = 0.0
        self.visual_balance = 0.0
        self.visual_arm_balance = 0.0
        self.player_input_buffer_timer = 0.0
        self.enemy_input_buffer_timer = 0.0
        self.screen_transition_timer = 0.0
        self.screen_transition_duration = max(0.001, self.transition_time)
        self.impact_flash_timer = 0.0
        self.impact_flash_color = (1.0, 1.0, 1.0, 0.0)
        self.camera_shake_timer = 0.0
        self.camera_shake_power = 0.0

        self.load_level(self.level_index)
        self.restart_match(keep_level=True)
        self.apply_sleeve_colors()
        self.start_music()
        self.update_screen_visibility(force=True)
        self.update_mouse_visibility()
        self.update_music_volume()

    # ---------- Core loop ----------

    def update(self):
        dt = self._dt()
        self.frame_dt = dt
        self._cleanup_sfx_handles()
        self.handle_global_keys()

        if self.screen == "PLAYING":
            self.handle_debug_keys()
            if self.state == "LEVEL_INTRO":
                self.level_intro_timer -= dt
                if self.level_intro_timer <= 0.0:
                    self.begin_level_play()
            elif self.state == "PLAYING":
                self.update_dial(dt)
                self.update_zone_scheduler(dt)
                self.update_timing_window(dt)
                self.update_input_buffers(dt)
                self.handle_player_inputs()
                if self.mode == "1P_VS_AI":
                    self.update_ai_window(dt)
            elif self.state == "ROUND_END":
                self.round_end_timer -= dt
                if self.round_end_timer <= 0.0 and self.auto_advance:
                    self.after_round_end()
        elif self.screen in self.MENU_SCREENS:
            self.handle_menu_inputs()

        if self.force_message_timer > 0.0 and self.screen == "PLAYING":
            self.force_message_timer -= dt
            if self.force_message_timer <= 0.0:
                self.set_text(self.ui_force, "")

        if self.arm_pulse_timer > 0.0:
            self.arm_pulse_timer = max(0.0, self.arm_pulse_timer - dt)

        if self.screen_transition_timer > 0.0:
            self.screen_transition_timer = max(0.0, self.screen_transition_timer - dt)
        if self.impact_flash_timer > 0.0:
            self.impact_flash_timer = max(0.0, self.impact_flash_timer - dt)
        if self.camera_shake_timer > 0.0:
            self.camera_shake_timer = max(0.0, self.camera_shake_timer - dt)

        self.update_visuals()
        if self.screen == "PLAYING" and self.state == "PLAYING":
            self.check_round_winner()
        self.update_ui()
        self.update_menu_ui()
        self.update_screen_visibility()
        self.update_music_volume()

    def _dt(self):
        # Prefer deltaTime() when available. Keep a fallback for compatibility.
        try:
            dt = float(bge.logic.deltaTime())
        except Exception:
            now = float(bge.logic.getFrameTime())
            dt = now - self.last_time
            self.last_time = now

        # Avoid huge jumps if the game window stalls.
        if dt < 0.0:
            return 0.0
        return min(dt, 0.05)

    # ---------- Setup / level ----------

    def _obj(self, name):
        obj = self.scene.objects.get(name)
        if obj:
            return obj
        # Blender may keep .001 suffixes if a previous upgrade left duplicates.
        # Prefer exact names, but fall back to the first object with the requested base name.
        try:
            for candidate in self._iter_scene_objects():
                if candidate.name == name or candidate.name.startswith(name + "."):
                    return candidate
        except Exception:
            pass
        return None

    def _find_child_suffix(self, parent, suffix):
        if not parent:
            return None
        try:
            for child in parent.children:
                if child.name.endswith(suffix) or child.name.endswith("_" + suffix):
                    return child
        except Exception:
            pass
        return None

    def _collect_numbered(self, prefix, count):
        objects = []
        for i in range(count):
            obj = self._obj("%s_%02d" % (prefix, i))
            if obj:
                objects.append(obj)
        return objects

    def _collect_pips(self, prefix):
        slots = []
        for slot in range(1, self.target_hits + 1):
            slot_data = {}
            for force, variant in self.FORCE_NAMES.items():
                name = "%s_%02d_%s" % (prefix, slot, variant)
                obj = self._obj(name)
                if obj:
                    slot_data[force] = obj
            if slot_data:
                slots.append(slot_data)
        return slots

    def _collect_simple_pips(self, prefix):
        slots = []
        for slot in range(1, self.target_hits + 1):
            ring = self._obj("%s_%02d_Ring" % (prefix, slot))
            fill = self._obj("%s_%02d_Fill" % (prefix, slot))
            if ring or fill:
                slots.append({"ring": ring, "fill": fill})
        return slots

    def _read_pushbar_base(self):
        """Store camera-local geometry for the v8.7 push bar.

        The bar is updated by changing width and center position. This avoids
        the previous visual error where two full bars were rendered on top of
        each other.
        """
        bg = self._obj("UI_PushBar_BG")
        if not bg:
            return None
        try:
            pos = bg.localPosition.copy()
        except Exception:
            try:
                pos = bg.position.copy()
            except Exception:
                return None
        width = 0.36
        try:
            # Prefer mesh bounding box in local coordinates.
            xs = []
            for mesh in bg.meshes:
                for vertex in mesh.getVertexArrayLength(0) and range(mesh.getVertexArrayLength(0)) or []:
                    try:
                        xs.append(mesh.getVertex(0, vertex).XYZ.x)
                    except Exception:
                        pass
            if xs:
                width = max(xs) - min(xs)
        except Exception:
            pass
        # Fallback property set by the repair script is optional.
        try:
            width = float(bg.get("push_width", width))
        except Exception:
            pass
        return {"center_x": float(pos.x), "center_y": float(pos.y), "center_z": float(pos.z), "width": max(0.05, width)}

    def load_level(self, index):
        # TGAW v7.1: IA campaign ends at level 15. No infinite roguelike scaling.
        index = max(0, min(len(LEVELS) - 1, int(index)))
        config = dict(LEVELS[index])
        config["display_level"] = index + 1
        config["is_roguelike"] = False

        self.level_index = index
        self.level = config

        self.needle_speed = config["needle_speed"]
        self.green_size = config["green_size"]
        self.zone_move_interval = config["zone_move_interval"]
        self.zone_move_min = config["zone_move_min"]
        self.zone_move_max = config["zone_move_max"]
        self.ai_accuracy = config["ai_accuracy"]
        self.ai_interval = config["ai_interval"]
        self.ai_force3_chance = config["ai_force3_chance"]

        if self.debug_prints:
            print("[TGAW v9] Loaded", config["name"], "Opponent:", config["opponent"])

    def restart_match(self, keep_level=True):
        if not keep_level:
            self.load_level(0)

        self.state = "LEVEL_INTRO" if self.show_level_intro and self.level_intro_time > 0.0 else "PLAYING"
        self.level_intro_timer = self.level_intro_time
        self.round_winner = None
        self.round_end_timer = 0.0
        self.player_force_total = 0
        self.enemy_force_total = 0
        self.player_misses = 0
        self.enemy_misses = 0
        self.player_force_counts = {1: 0, 2: 0, 3: 0}
        self.enemy_force_counts = {1: 0, 2: 0, 3: 0}

        # v5.1: first pass starts inside the yellow planning sector. A target is
        # planned immediately, then revealed once the needle reaches the orange sector.
        plan_start, plan_end = self.effective_arc(self.plan_arc_start, self.plan_arc_end)
        reveal_start, reveal_end = self.effective_arc(self.reveal_arc_start, self.reveal_arc_end)
        self.needle_angle = self.initial_needle_angle_in_plan_sector(plan_start, plan_end)
        self.green_start_angle = 0.0
        self.zone_timer = 0.0

        # v4.2+ target lifecycle. The target is not visible at match start;
        # it is planned in the yellow sector and revealed in the orange sector.
        self.target_planned = False
        self.target_visible = False
        self.in_plan_sector = self.angle_in_arc(self.needle_angle, plan_start, plan_end)
        self.in_reveal_sector = self.angle_in_arc(self.needle_angle, reveal_start, reveal_end)
        if self.in_plan_sector:
            self.plan_next_target()

        # Consecutive sequences. A miss clears the full sequence, Outlast-style.
        self.player_sequence = []
        self.enemy_sequence = []
        self.player_hits = 0
        self.enemy_hits = 0
        self.player_last_force = 0
        self.enemy_last_force = 0
        self.balance = 0
        self.visual_balance = 0.0
        self.visual_arm_balance = 0.0
        self.player_input_buffer_timer = 0.0
        self.enemy_input_buffer_timer = 0.0

        # Outlast-like timing window state. Each pass through the active zone is one objective.
        self.is_in_timing_window = False
        self.player_pressed_this_window = False
        self.enemy_pressed_this_window = False
        self.ai_window_elapsed = 0.0
        self.ai_press_delay = None
        self.ai_planned_force = 0

        self.set_text(self.ui_force, "")
        self.force_message_timer = 0.0

    def begin_level_play(self):
        if self.state != "LEVEL_INTRO":
            return
        self.state = "PLAYING"
        self.set_text(self.ui_force, "")
        self.force_message_timer = 0.0

    # ---------- Dial ----------

    def update_dial(self, dt):
        self.needle_angle = (self.needle_angle + self.needle_speed * dt) % 360.0

    def update_zone_scheduler(self, dt):
        """v4.2 target lifecycle.

        The target no longer moves in an anti-clockwise pattern. Each lap works
        like this:
            yellow sector -> choose a random target inside the green spawn arc
            orange sector -> reveal the target early enough for reaction
            green spawn arc -> player must hit the shown target
        """
        plan_start, plan_end = self.effective_arc(self.plan_arc_start, self.plan_arc_end)
        reveal_start, reveal_end = self.effective_arc(self.reveal_arc_start, self.reveal_arc_end)
        currently_in_plan = self.angle_in_arc(self.needle_angle, plan_start, plan_end)
        currently_in_reveal = self.angle_in_arc(self.needle_angle, reveal_start, reveal_end)

        if currently_in_plan and not self.in_plan_sector:
            self.plan_next_target()

        if currently_in_reveal and not self.in_reveal_sector:
            if not self.target_planned:
                self.plan_next_target()
            self.reveal_target()

        self.in_plan_sector = currently_in_plan
        self.in_reveal_sector = currently_in_reveal

    def angle_in_arc(self, angle, start, end):
        angle = angle % 360.0
        start = start % 360.0
        end = end % 360.0
        if start <= end:
            return start <= angle <= end
        return angle >= start or angle <= end

    def effective_arc(self, start, end):
        return ((start + self.guide_angle_offset) % 360.0, (end + self.guide_angle_offset) % 360.0)

    def arc_length(self, start, end):
        length = (end - start) % 360.0
        return 360.0 if length == 0.0 else length

    def sample_target_start_angle(self):
        spawn_start, spawn_end = self.effective_arc(self.spawn_arc_start, self.spawn_arc_end)
        spawn_length = self.arc_length(spawn_start, spawn_end)
        available = max(1.0, spawn_length - self.green_size)
        return (spawn_start + random.uniform(0.0, available)) % 360.0

    def initial_needle_angle_in_plan_sector(self, plan_start, plan_end):
        plan_length = self.arc_length(plan_start, plan_end)
        # Start a little inside yellow, not on the exact border. That gives the game
        # one clean first pass: yellow plans -> orange reveals -> green objective.
        offset = min(max(3.0, plan_length * 0.18), max(3.0, plan_length - 2.0))
        return (plan_start + offset) % 360.0

    def plan_next_target(self):
        self.green_start_angle = self.sample_target_start_angle()
        self.target_planned = True
        self.target_visible = False
        if self.debug_prints:
            print("[Fuerzitas] New target planned at %.1f deg" % self.green_start_angle)

    def reveal_target(self):
        if not self.target_planned:
            self.plan_next_target()
        self.target_visible = True
        if self.debug_prints:
            print("[Fuerzitas] Target revealed")

    def hide_target_after_window(self):
        self.target_visible = False
        self.target_planned = False

    def move_zone_left(self):
        # Legacy method kept for compatibility with older saved components.
        # v4.2 uses plan_next_target() instead of a predictable drifting zone.
        self.plan_next_target()

    def check_hit_force(self):
        """
        Returns:
            0 = miss
            1 = valid hit, weak   -> first third of zone
            2 = valid hit, medium -> second third of zone
            3 = valid hit, strong -> final third of zone

        The valid zone extends clockwise from green_start_angle to green_start_angle + green_size.
        Force 3 is near the end, matching the timing pressure of Outlast's arm-wrestling minigame.
        """
        if not self.target_visible:
            return 0

        relative = (self.needle_angle - self.green_start_angle) % 360.0
        if relative > self.green_size:
            return 0

        third = self.green_size / 3.0
        if relative < third:
            return 1
        if relative < third * 2.0:
            return 2
        return 3

    def update_timing_window(self, dt):
        """Tracks the active objective window.

        A player must press once before the needle leaves the valid zone. If the
        player presses outside the zone or lets the window close without pressing,
        the full consecutive sequence is cleared.
        """
        currently_in_window = self.check_hit_force() > 0

        if currently_in_window and not self.is_in_timing_window:
            self.on_timing_window_enter()

        if currently_in_window:
            self.ai_window_elapsed += dt

        if not currently_in_window and self.is_in_timing_window:
            self.on_timing_window_exit()

        self.is_in_timing_window = currently_in_window

    def on_timing_window_enter(self):
        self.player_pressed_this_window = False
        self.enemy_pressed_this_window = False
        self.ai_window_elapsed = 0.0
        self.ai_press_delay = None
        self.ai_planned_force = 0

        if self.mode == "1P_VS_AI":
            # Estimate how long this pass through the target lasts. Schedule one IA attempt inside it.
            window_duration = max(0.05, self.green_size / max(1.0, self.needle_speed))
            self.ai_press_delay = random.uniform(window_duration * 0.18, window_duration * 0.86)
            self.ai_planned_force = self.plan_ai_force()

    def on_timing_window_exit(self):
        if self.state != "PLAYING":
            return

        if not self.player_pressed_this_window:
            self.apply_timeout_miss("PLAYER")

        if self.mode == "LOCAL_2P":
            if not self.enemy_pressed_this_window:
                self.apply_timeout_miss("ENEMY")
        elif self.mode == "1P_VS_AI":
            if not self.enemy_pressed_this_window:
                self.apply_timeout_miss("AI")

        self.hide_target_after_window()

    def mark_pressed_this_window(self, side):
        if side == "PLAYER":
            self.player_pressed_this_window = True
        else:
            self.enemy_pressed_this_window = True

    def already_pressed_this_window(self, side):
        if side == "PLAYER":
            return self.player_pressed_this_window
        return self.enemy_pressed_this_window

    def apply_timeout_miss(self, side):
        # Missing by omission also clears the full sequence.
        if side == "PLAYER":
            self.player_sequence[:] = []
            self.player_hits = 0
            self.player_last_force = 0
            self.player_misses += 1
        else:
            self.enemy_sequence[:] = []
            self.enemy_hits = 0
            self.enemy_last_force = 0
            self.enemy_misses += 1

        self.show_force_message(side, 0, reset=True, timeout=True)
        self.trigger_feedback(side, 0, miss=True)
        self.trigger_arm_pulse("ENEMY" if side == "PLAYER" else "PLAYER", 1)
        if self.is_human_controlled_side(side):
            self.play_sfx("miss")

    # ---------- Input ----------

    def handle_player_inputs(self):
        keyboard = bge.logic.keyboard.inputs

        if keyboard[bge.events.SPACEKEY].activated:
            self.player_attempt("PLAYER")

        enter_pressed = keyboard[bge.events.ENTERKEY].activated or keyboard[bge.events.PADENTER].activated
        if self.mode == "LOCAL_2P" and enter_pressed:
            self.player_attempt("ENEMY")

    def update_input_buffers(self, dt):
        """Consume a tiny pre-window input buffer for human players.

        This does not make the target easier by a large margin; it only prevents
        the common frustration of pressing a few frames before the active window
        while the objective is already visible. Presses far outside the window
        still count as misses, preserving the intended tension.
        """
        if self.player_input_buffer_timer > 0.0:
            self.player_input_buffer_timer = max(0.0, self.player_input_buffer_timer - dt)
            if self.is_in_timing_window and not self.already_pressed_this_window("PLAYER"):
                force = self.check_hit_force()
                if force > 0:
                    self.player_input_buffer_timer = 0.0
                    self.mark_pressed_this_window("PLAYER")
                    self.apply_attempt("PLAYER", force)

        if self.mode == "LOCAL_2P" and self.enemy_input_buffer_timer > 0.0:
            self.enemy_input_buffer_timer = max(0.0, self.enemy_input_buffer_timer - dt)
            if self.is_in_timing_window and not self.already_pressed_this_window("ENEMY"):
                force = self.check_hit_force()
                if force > 0:
                    self.enemy_input_buffer_timer = 0.0
                    self.mark_pressed_this_window("ENEMY")
                    self.apply_attempt("ENEMY", force)

    def can_buffer_pre_window_hit(self):
        if self.input_buffer_time <= 0.0 or not self.target_visible:
            return False
        # Seconds until the needle reaches the beginning of the active target.
        degrees_to_start = (self.green_start_angle - self.needle_angle) % 360.0
        if degrees_to_start <= 0.0001:
            return False
        seconds_to_start = degrees_to_start / max(1.0, self.needle_speed)
        return 0.0 < seconds_to_start <= self.input_buffer_time

    def handle_debug_keys(self):
        keyboard = bge.logic.keyboard.inputs

        #if keyboard[bge.events.RKEY].activated:
        #    self.restart_match(keep_level=True)

        #if keyboard[bge.events.NKEY].activated:
        #    self.load_level(self.level_index + 1)
        #    self.restart_match(keep_level=True)

        #if keyboard[bge.events.MKEY].activated:
        #    self.mode = "LOCAL_2P" if self.mode == "1P_VS_AI" else "1P_VS_AI"
        #    self.restart_match(keep_level=True)

    # ---------- Attempts / match result ----------

    def player_attempt(self, side):
        # Ignore button mashing after a valid attempt in the same objective window.
        if self.is_in_timing_window and self.already_pressed_this_window(side):
            return

        force = self.check_hit_force()
        if force > 0 and self.is_in_timing_window:
            self.mark_pressed_this_window(side)
            self.apply_attempt(side, force)
            return

        # v9: allow a very small buffer only immediately before the target starts.
        # This improves feel without turning early/late presses into valid hits.
        if self.can_buffer_pre_window_hit():
            if side == "PLAYER":
                self.player_input_buffer_timer = self.input_buffer_time
            elif side == "ENEMY" and self.mode == "LOCAL_2P":
                self.enemy_input_buffer_timer = self.input_buffer_time
            return

        self.apply_attempt(side, force)

    def plan_ai_force(self):
        # The IA plays one objective window at a time. v9 adds slight human-like
        # variation so it no longer feels like a fixed probability machine.
        accuracy = float(self.ai_accuracy)
        force3_chance = float(self.ai_force3_chance)
        if self.ai_humanization:
            # If IA is losing, it takes a little more risk; if it is winning,
            # it becomes slightly less perfect. Values stay clamped for fairness.
            pressure = self._clamp(float(self.balance) / float(max(1, self.balance_win)), -1.0, 1.0)
            accuracy += pressure * 0.035
            force3_chance += pressure * 0.055
            accuracy += random.uniform(-0.045, 0.035)
            # Occasional human hesitation even in late levels.
            if random.random() < 0.035:
                return 0
        accuracy = self._clamp(accuracy, 0.25, 0.92)
        force3_chance = self._clamp(force3_chance, 0.05, 0.58)

        if random.random() > accuracy:
            return 0

        r = random.random()
        if r < force3_chance:
            return 3
        if r < 0.60:
            return 2
        return 1

    def update_ai_window(self, dt):
        if not self.is_in_timing_window:
            return
        if self.enemy_pressed_this_window:
            return
        if self.ai_press_delay is None:
            return

        if self.ai_window_elapsed >= self.ai_press_delay:
            self.mark_pressed_this_window("AI")
            self.apply_attempt("AI", self.ai_planned_force)

    def apply_attempt(self, side, force):
        is_player = side == "PLAYER"
        sequence = self.player_sequence if is_player else self.enemy_sequence

        if is_player:
            self.player_last_force = force
        else:
            self.enemy_last_force = force

        if force <= 0:
            # Important gameplay change: missing resets the consecutive sequence.
            sequence[:] = []
            if is_player:
                self.player_hits = 0
                self.player_misses += 1
            else:
                self.enemy_hits = 0
                self.enemy_misses += 1
            self.show_force_message(side, 0, reset=True)
            self.trigger_feedback(side, 0, miss=True)
            self.trigger_arm_pulse("ENEMY" if is_player else "PLAYER", 1)
            if self.is_human_controlled_side(side):
                self.play_sfx("miss")
            return

        if self.is_human_controlled_side(side):
            self.play_force_sound(force)

        self.trigger_feedback(side, force, miss=False)
        self.trigger_arm_pulse(side, force)

        sequence.append(force)
        if len(sequence) > self.target_hits:
            del sequence[0:len(sequence) - self.target_hits]

        if is_player:
            self.player_hits = len(self.player_sequence)
            self.player_force_total += force
            self.player_force_counts[force] = self.player_force_counts.get(force, 0) + 1
            self.balance += force
        else:
            self.enemy_hits = len(self.enemy_sequence)
            self.enemy_force_total += force
            self.enemy_force_counts[force] = self.enemy_force_counts.get(force, 0) + 1
            self.balance -= force

        self.show_force_message(side, force)
        self.check_round_winner()

    # The old timer-based IA was replaced by objective-window IA in v4.

    def check_round_winner(self):
        """Victory is decided only by force advantage.

        The five discs remain as an Outlast-style consecutive-hit history, but
        completing them is no longer a direct win condition. Weak/medium/strong
        hits matter through the score difference: +1, +2, +3.
        """
        if self.balance >= self.balance_win:
            self.end_round("PLAYER")
        elif self.balance <= -self.balance_win:
            self.end_round("ENEMY")

    def end_round(self, winner):
        if self.state != "PLAYING":
            return
        self.state = "ROUND_END"
        self.round_winner = winner
        self.round_end_timer = self.result_screen_time if self.show_result_summary else self.round_end_delay

        if self.debug_prints:
            print("[TGAW v9] Round winner:", winner)

    def after_round_end(self):
        if self.mode == "1P_VS_AI" and self.round_winner == "PLAYER":
            next_level = self.level_index + 1
            if next_level < len(LEVELS):
                self.load_level(next_level)
                self.restart_match(keep_level=True)
            else:
                # Campaign finished after level 15. Return to main menu after the result screen.
                self.set_screen("MAIN_MENU", play_sound="ui_confirm")
        else:
            # In local mode the selected level repeats forever until players leave.
            self.restart_match(keep_level=True)


    # ---------- Menus / pause ----------

    def handle_global_keys(self):
        keyboard = bge.logic.keyboard.inputs
        if keyboard[bge.events.ESCKEY].activated:
            if self.screen == "PLAYING":
                self.pause_game()
            elif self.screen == "PAUSED":
                self.resume_game()
            elif self.screen == "MODE_SELECT":
                self.set_screen("MAIN_MENU", play_sound="ui_back")
            elif self.screen == "LOCAL_LEVEL_SELECT":
                self.set_screen("MODE_SELECT", play_sound="ui_back")
            elif self.screen == "SETTINGS":
                self.set_screen(self.settings_return_screen, play_sound="ui_back")
            elif self.screen == "EXIT_CONFIRM":
                self.set_screen(self.exit_return_screen, play_sound="ui_back")

    def handle_menu_inputs(self):
        buttons = self.current_buttons()
        if not buttons:
            return

        keyboard = bge.logic.keyboard.inputs
        if keyboard[bge.events.DOWNARROWKEY].activated or keyboard[bge.events.SKEY].activated:
            self.menu_selected_index = (self.menu_selected_index + 1) % len(buttons)
            self.play_sfx("ui_click")
        elif keyboard[bge.events.UPARROWKEY].activated or keyboard[bge.events.WKEY].activated:
            self.menu_selected_index = (self.menu_selected_index - 1) % len(buttons)
            self.play_sfx("ui_click")

        enter_pressed = keyboard[bge.events.ENTERKEY].activated or keyboard[bge.events.PADENTER].activated
        space_pressed = keyboard[bge.events.SPACEKEY].activated
        if enter_pressed or space_pressed:
            self.activate_button(buttons[self.menu_selected_index][0])
            return

        self.menu_hover_action = self.hit_test_menu_button()
        if self.menu_hover_action:
            for idx, btn in enumerate(buttons):
                if btn[0] == self.menu_hover_action:
                    self.menu_selected_index = idx
                    break

        mouse = bge.logic.mouse.inputs
        if mouse[bge.events.LEFTMOUSE].activated:
            action = self.menu_hover_action
            if action:
                for idx, btn in enumerate(buttons):
                    if btn[0] == action:
                        self.menu_selected_index = idx
                        break
                self.activate_button(action)

    def current_buttons(self):
        return list(self.BUTTONS.get(self.screen, []))

    def hit_test_menu_button(self):
        """Return the button under the mouse using the same coordinate space as the UI.

        v8.9 calibration:
        The prior build forced screen_y = 1 - mouse_y. On the tested project that
        inverted vertical motion and made hover feel inconsistent. The default is now
        screen_y = mouse_y, with an optional GameManager property "Mouse Y Inverted"
        for machines/builds that report the opposite origin.
        """
        try:
            mx, my = bge.logic.mouse.position
        except Exception:
            return None

        sx = self._clamp(float(mx), 0.0, 1.0)
        raw_y = self._clamp(float(my), 0.0, 1.0)

        # v8.9 calibration:
        # In Roberto's UPBGE test build the Y coordinate already behaves like
        # the authored UI rectangles: 0.0 at top, 1.0 at bottom. Therefore
        # the default must NOT invert Y. If a different machine reports the
        # opposite, set the GameManager property "Mouse Y Inverted" to True.
        sy = (1.0 - raw_y) if self.mouse_y_inverted else raw_y

        self.menu_cursor_norm = (sx, sy)
        self.mouse_origin_top_active = not self.mouse_y_inverted

        best_action = None
        best_score = 999.0
        for action, obj_name, txt_name, label, cx, cy, w, h in self.current_buttons():
            half_w = w * 0.5
            half_h = h * 0.5
            dx = abs(sx - cx)
            dy = abs(sy - cy)
            if dx <= half_w and dy <= half_h:
                # If two hit boxes slightly overlap, prefer the one whose center is closest.
                score = (dx / max(half_w, 0.0001)) + (dy / max(half_h, 0.0001))
                if score < best_score:
                    best_score = score
                    best_action = action
        return best_action

    def activate_button(self, action):
        if action in ("start",):
            self.set_screen("MODE_SELECT", play_sound="ui_start")
        elif action == "settings_main":
            self.settings_return_screen = "MAIN_MENU"
            self.set_screen("SETTINGS", play_sound="ui_click")
        elif action == "settings_pause":
            self.settings_return_screen = "PAUSED"
            self.set_screen("SETTINGS", play_sound="ui_click")
        elif action == "exit_main":
            self.exit_return_screen = "MAIN_MENU"
            self.set_screen("EXIT_CONFIRM", play_sound="ui_exit")
        elif action == "exit_pause":
            self.exit_return_screen = "PAUSED"
            self.set_screen("EXIT_CONFIRM", play_sound="ui_exit")
        elif action == "exit_settings":
            self.exit_return_screen = "SETTINGS"
            self.set_screen("EXIT_CONFIRM", play_sound="ui_exit")
        elif action == "mode_ai":
            self.start_game("1P_VS_AI")
        elif action == "mode_local":
            self.set_screen("LOCAL_LEVEL_SELECT", play_sound="ui_click")
        elif action == "back_main":
            self.set_screen("MAIN_MENU", play_sound="ui_back")
        elif action == "back_mode":
            self.set_screen("MODE_SELECT", play_sound="ui_back")
        elif action == "local_level_prev":
            self.local_level_index = (self.local_level_index - 1) % len(LEVELS)
            self.play_sfx("ui_click")
        elif action == "local_level_next":
            self.local_level_index = (self.local_level_index + 1) % len(LEVELS)
            self.play_sfx("ui_click")
        elif action == "local_level_start":
            self.start_game("LOCAL_2P", self.local_level_index)
        elif action == "back_from_settings":
            self.set_screen(self.settings_return_screen, play_sound="ui_back")
        elif action in ("player_sleeve_prev", "player_sleeve_next", "cycle_player_sleeve"):
            step = -1 if action == "player_sleeve_prev" else 1
            self.player_sleeve_color_index = (self.player_sleeve_color_index + step) % len(self.SLEEVE_PALETTE)
            self.apply_sleeve_colors()
            self.play_sfx("ui_click")
        elif action in ("enemy_sleeve_prev", "enemy_sleeve_next", "cycle_enemy_sleeve"):
            step = -1 if action == "enemy_sleeve_prev" else 1
            self.enemy_sleeve_color_index = (self.enemy_sleeve_color_index + step) % len(self.SLEEVE_PALETTE)
            self.apply_sleeve_colors()
            self.play_sfx("ui_click")
        elif action == "volume_down":
            self.master_volume = self._clamp(self.master_volume - 0.10, 0.0, 1.0)
            self.update_music_volume()
            self.play_sfx("ui_click")
        elif action == "volume_up":
            self.master_volume = self._clamp(self.master_volume + 0.10, 0.0, 1.0)
            self.update_music_volume()
            self.play_sfx("ui_click")
        elif action == "resume":
            self.resume_game()
        elif action == "main_from_pause":
            self.set_screen("MAIN_MENU", play_sound="ui_back")
        elif action == "confirm_exit_no":
            self.set_screen(self.exit_return_screen, play_sound="ui_back")
        elif action == "confirm_exit_yes":
            self.play_sfx("ui_confirm")
            try:
                bge.logic.endGame()
            except Exception:
                pass

    def set_screen(self, screen, play_sound=None):
        old_screen = getattr(self, "screen", None)
        self.screen = screen
        self.menu_selected_index = 0
        if old_screen != screen and self.transition_time > 0.0:
            self.screen_transition_timer = self.transition_time
            self.screen_transition_duration = max(0.001, self.transition_time)
        if play_sound:
            self.play_sfx(play_sound)
        self.update_screen_visibility(force=True)
        self.update_mouse_visibility()
        self.update_music_volume()

    def start_game(self, mode, level_index=None):
        self.mode = mode
        if mode == "LOCAL_2P":
            self.local_level_index = max(0, min(len(LEVELS) - 1, self.local_level_index if level_index is None else level_index))
            self.load_level(self.local_level_index)
        else:
            self.load_level(0)
        self.restart_match(keep_level=True)
        self.set_screen("PLAYING", play_sound="ui_start")

    def pause_game(self):
        self.set_screen("PAUSED", play_sound="ui_click")

    def resume_game(self):
        self.set_screen("PLAYING", play_sound="ui_back")

    def update_menu_ui(self):
        # Dynamic button labels / selected marker.
        buttons = self.current_buttons()
        if buttons and self.menu_selected_index >= len(buttons):
            self.menu_selected_index = 0
        selected_action = buttons[self.menu_selected_index][0] if buttons else None
        hovered = self.menu_hover_action
        active_action = hovered or selected_action

        for screen_buttons in self.BUTTONS.values():
            for action, obj_name, txt_name, label, cx, cy, w, h in screen_buttons:
                txt = self._obj(txt_name)
                if not txt:
                    continue
                current = label
                if action == "cycle_player_sleeve":
                    current = "Color J1"
                elif action == "cycle_enemy_sleeve":
                    current = "Color J2"
                elif action == "local_level_start":
                    current = "Iniciar nivel %d" % (self.local_level_index + 1)
                current = current.upper()
                # v8: selection is shown through button glow/cursor, not by adding debug-like text prefixes.
                self.set_text(txt, current)

        vol_text = self._obj("MENU_Settings_Txt_VolumeValue")
        self.set_text(vol_text, "Volumen: %d%%" % int(round(self.master_volume * 100.0)))
        self.update_settings_volume_meter()

        local_level_text = self._obj("MENU_Local_Txt_Level")
        if local_level_text:
            level = LEVELS[self.local_level_index]
            self.set_text(local_level_text, "NIVEL %d  |  %s" % (self.local_level_index + 1, level.get("opponent", "Rival")))

        # Lightweight hover/selection feedback. This works best with materials
        # that use object color; if a material ignores object color the text marker still shows selection.
        for screen_buttons in self.BUTTONS.values():
            for action, obj_name, txt_name, label, cx, cy, w, h in screen_buttons:
                obj = self._obj(obj_name)
                if not obj:
                    continue
                if action == active_action and self.screen in self.MENU_SCREENS:
                    color = (1.0, 0.52, 0.16, 0.86) if action not in self.DANGER_ACTIONS else (1.0, 0.10, 0.06, 0.92)
                else:
                    color = (0.18, 0.12, 0.08, 0.76) if action not in self.DANGER_ACTIONS else (0.48, 0.02, 0.02, 0.82)
                self.set_runtime_color(obj, color)

        self.update_menu_cursor()

    def update_settings_volume_meter(self):
        """Update the modelled settings volume meter.

        The v8 UI creates ten mesh bars. In v8.7 they are recolored every
        frame while the settings screen is open, so the meter clearly increases
        and decreases when the player uses the arrow buttons.
        """
        active_count = int(round(self._clamp(self.master_volume, 0.0, 1.0) * 10.0))
        for i in range(1, 11):
            bar = self._obj("MENU_Settings_VolBar_%02d" % i)
            if not bar:
                continue
            if i <= active_count:
                # Warm amber, like the reference.
                self.set_runtime_color(bar, (1.00, 0.52, 0.14, 1.0))
            else:
                # Dim unfilled segment.
                self.set_runtime_color(bar, (0.055, 0.045, 0.038, 1.0))

    def update_mouse_visibility(self):
        show = self.screen in self.MENU_SCREENS
        # v8.9: use the native OS cursor by default. The previous mesh cursor was
        # parented to the camera and could feel like it was pulled radially toward
        # the center in perspective. The native cursor removes that distortion.
        try:
            bge.render.showMouse(show)
        except Exception:
            pass
        if self.menu_cursor:
            self.set_visible(self.menu_cursor, show and self.use_custom_cursor)

    def update_menu_cursor(self):
        if not self.menu_cursor or not self.use_custom_cursor:
            if self.menu_cursor:
                self.set_visible(self.menu_cursor, False)
            return
        visible = self.screen in self.MENU_SCREENS
        self.set_visible(self.menu_cursor, visible)
        if not visible:
            return
        sx, sy = self.menu_cursor_norm
        try:
            view_w = float(self.menu_cursor.get("view_w", 1.30))
            view_h = float(self.menu_cursor.get("view_h", 0.73))
            z = float(self.menu_cursor.get("cursor_z", -1.10))
        except Exception:
            view_w, view_h, z = 1.30, 0.73, -1.10
        x = -view_w * 0.5 + sx * view_w
        y = view_h * 0.5 - sy * view_h
        try:
            self.menu_cursor.localPosition = (x, y, z)
        except Exception:
            try:
                self.menu_cursor.position = (x, y, z)
            except Exception:
                pass

    def update_screen_visibility(self, force=False):
        # v8.7: refresh lists in case the UI was repaired/rebuilt after the
        # component was assigned, or if a stale .blend was saved with old lists.
        try:
            self.menu_objects = self._collect_menu_objects()
            self.hud_objects = self._collect_hud_objects()
        except Exception:
            pass
        screen = self.screen

        # HUD is only visible during gameplay. In v7, special intro/result overlays
        # are managed as gameplay HUD layers, while debug/state panels remain hidden.
        hud_visible = screen == "PLAYING"
        for obj in self.hud_objects:
            name = obj.name
            visible = hud_visible
            if name == "UI_FadeOverlay":
                visible = self.screen_transition_timer > 0.0
            elif name == "UI_ImpactFlash":
                visible = hud_visible and self.impact_flash_timer > 0.0 and self.state == "PLAYING"
            elif name.startswith("UI_Intro_"):
                visible = hud_visible and self.state == "LEVEL_INTRO"
            elif name.startswith("UI_Result_"):
                visible = hud_visible and self.state == "ROUND_END"
            elif name.startswith("UI_Panel_Force") or name == "UI_Force" or name.startswith("UI_Force"):
                # Hide the complete force-toast frame when no hit/miss message is active.
                # v8 left some border pieces visible because only the main panel name was checked.
                visible = hud_visible and self.force_message_timer > 0.0 and self.state == "PLAYING"
            elif name in ("UI_Hint", "UI_Panel_Hint"):
                visible = False
            elif name.startswith("Pip_Player_") or name.startswith("Pip_Enemy_"):
                visible = hud_visible and self.state in ("PLAYING", "LEVEL_INTRO", "ROUND_END")
            self.set_visible(obj, visible)

        # Menu object groups.
        for obj in self.menu_objects:
            name = obj.name
            visible = False
            if name.startswith("MENU_Main_Background_Image") or name.startswith("MENU_BG_Main"):
                visible = screen in ("MAIN_MENU", "MODE_SELECT", "LOCAL_LEVEL_SELECT") or (screen == "EXIT_CONFIRM" and self.exit_return_screen != "PAUSED")
            elif name.startswith("MENU_Settings_Background_Image") or name.startswith("MENU_BG_Settings"):
                visible = screen == "SETTINGS"
            elif name in ("MENU_Main_BG_Dark", "MENU_Main_BG_LeftRain", "MENU_Settings_BG_Dark", "MENU_Settings_BG_Blur", "MENU_Main_Neon", "MENU_Main_Neon_Icon"):
                visible = False
            elif name.startswith("MENU_Main_"):
                visible = screen == "MAIN_MENU"
            elif name.startswith("MENU_Mode_"):
                visible = screen == "MODE_SELECT"
            elif name.startswith("MENU_Local_"):
                visible = screen == "LOCAL_LEVEL_SELECT"
            elif name.startswith("MENU_Settings_"):
                visible = screen == "SETTINGS"
            elif name.startswith("MENU_Exit_"):
                visible = screen == "EXIT_CONFIRM"
            elif name.startswith("MENU_Pause_"):
                # v8.7: exit confirmation must be a clean full-screen layer.
                # Do not keep the pause/options menu behind it, because the text
                # becomes unreadable and overlaps with Sí/No.
                visible = screen == "PAUSED"
            elif name.startswith("MENU_Cursor"):
                visible = screen in self.MENU_SCREENS
            self.set_visible(obj, visible)
        self.update_mouse_visibility()

    def _iter_scene_objects(self):
        for item in self.scene.objects:
            try:
                # Most UPBGE builds iterate KX_GameObjects here.
                name = item.name
                obj = item
            except Exception:
                # Fallback for mapping-like iteration by key/name.
                name = str(item)
                try:
                    obj = self.scene.objects.get(name)
                except Exception:
                    obj = None
            if obj:
                yield obj

    def _collect_menu_objects(self):
        return [obj for obj in self._iter_scene_objects() if obj.name.startswith("MENU_")]

    def _collect_hud_objects(self):
        prefixes = ("UI_", "Pip_Player_", "Pip_Enemy_")
        return [obj for obj in self._iter_scene_objects() if obj.name.startswith(prefixes)]

    # ---------- Audio ----------

    def init_audio(self):
        if self.mute_audio:
            return
        try:
            import aud
            self._aud = aud
            self.audio_device = aud.Device()
        except Exception as exc:
            self.audio_device = None
            if self.debug_prints:
                print("[Fuerzitas Audio] aud module unavailable:", exc)

    def audio_base_path(self):
        """Primary audio path shown in the component UI.

        v5.3 keeps this for compatibility, but actual file lookup uses
        audio_candidate_dirs() so user assets beside the .blend take priority.
        """
        try:
            return bge.logic.expandPath(self.audio_assets_path)
        except Exception:
            return self.audio_assets_path

    def _norm_abs_path(self, path):
        if not path:
            return None
        try:
            expanded = bge.logic.expandPath(path)
        except Exception:
            expanded = path
        try:
            return os.path.abspath(expanded)
        except Exception:
            return expanded

    def _blend_root_runtime(self):
        try:
            return self._norm_abs_path("//")
        except Exception:
            return None

    def _nearby_audio_asset_dirs(self, root, max_depth=4):
        """Find nested assets/audio folders near the .blend.

        This fixes the common project layout where the .blend is beside a
        Fuerzitas_UPBGE_Starter folder instead of beside a root assets folder.
        The scan is shallow on purpose so it stays safe inside Blender.
        """
        if not root or not os.path.isdir(root):
            return []
        found = []
        root = os.path.abspath(root)
        root_depth = root.rstrip(os.sep).count(os.sep)
        try:
            for current, dirs, files in os.walk(root):
                depth = current.rstrip(os.sep).count(os.sep) - root_depth
                if depth > max_depth:
                    dirs[:] = []
                    continue
                base = os.path.basename(current).lower()
                parent = os.path.basename(os.path.dirname(current)).lower()
                if base == "audio" and parent == "assets":
                    found.append(current)
                    dirs[:] = []
        except Exception:
            pass
        return found

    def _runtime_root_dirs(self):
        """Return possible folders used by an exported standalone .exe.

        In UPBGE standalone builds, bge.logic.expandPath("//") can keep pointing
        to the embedded runtime blend context. External assets beside the .exe
        are not always found through the blend-relative path, so v9.3 explicitly
        checks the executable folder and the current working folder.
        """
        roots = []
        try:
            exe = getattr(sys, "executable", "")
            if exe:
                roots.append(os.path.dirname(os.path.abspath(exe)))
        except Exception:
            pass
        try:
            argv0 = sys.argv[0] if getattr(sys, "argv", None) else ""
            if argv0:
                roots.append(os.path.dirname(os.path.abspath(argv0)))
        except Exception:
            pass
        try:
            roots.append(os.getcwd())
        except Exception:
            pass
        try:
            blend_root = self._blend_root_runtime()
            if blend_root:
                roots.append(blend_root)
        except Exception:
            pass

        out = []
        seen = set()
        for root in roots:
            if not root:
                continue
            try:
                root = os.path.abspath(root)
            except Exception:
                pass
            key = os.path.normcase(root)
            if key not in seen:
                seen.add(key)
                out.append(root)
        return out

    def audio_candidate_dirs(self):
        """Return audio folders in priority order.

        v9.3 fixes standalone .exe audio: the exported runtime may not resolve
        //assets/audio the same way as the editor, so we search beside the .exe,
        beside the working directory, beside the blend, and inside known starter
        layouts.
        """
        candidates = []

        # 1) Component value, normally //assets/audio.
        candidates.append(self.audio_assets_path)

        # 2) Explicit blend-relative path. This works inside the editor.
        candidates.append("//assets/audio")

        # 3) Standalone runtime folders: put assets/audio next to TGAW.exe.
        for root in self._runtime_root_dirs():
            candidates.append(os.path.join(root, "assets", "audio"))
            candidates.append(os.path.join(root, "The God of Arm Wrestling", "assets", "audio"))
            candidates.append(os.path.join(root, "Fuerzitas_UPBGE_Starter", "assets", "audio"))
            candidates.extend(self._nearby_audio_asset_dirs(root, max_depth=4))

        # 4) Known nested layouts beside the .blend.
        blend_root = self._blend_root_runtime()
        if blend_root:
            candidates.append(os.path.join(blend_root, "Fuerzitas_UPBGE_Starter", "assets", "audio"))
            candidates.append(os.path.join(blend_root, "Fuerzitas_UPBGE_Starter_v5_4", "assets", "audio"))
            candidates.extend(self._nearby_audio_asset_dirs(blend_root, max_depth=4))

        # 5) Current working directory fallback.
        try:
            candidates.append(os.path.join(os.getcwd(), "assets", "audio"))
            candidates.extend(self._nearby_audio_asset_dirs(os.getcwd(), max_depth=3))
        except Exception:
            pass

        # 6) Folder next to the loaded script, useful when testing directly from
        # the starter package before saving the .blend. __file__ may not exist
        # when the component is loaded as a Blender Text block, so this is optional.
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            candidates.append(os.path.abspath(os.path.join(script_dir, "..", "assets", "audio")))
        except Exception:
            pass

        out = []
        seen = set()
        for path in candidates:
            abs_path = self._norm_abs_path(path)
            if not abs_path:
                continue
            key = os.path.normcase(abs_path)
            if key in seen:
                continue
            seen.add(key)
            out.append(abs_path)
        return out

    def _case_insensitive_existing_file(self, folder, filename):
        direct = os.path.join(folder, filename)
        if os.path.exists(direct):
            return direct
        try:
            wanted = filename.lower()
            for entry in os.listdir(folder):
                if entry.lower() == wanted:
                    path = os.path.join(folder, entry)
                    if os.path.isfile(path):
                        return path
        except Exception:
            pass
        return None

    def resolve_sound_path(self, key):
        if key in self.sound_cache:
            return self.sound_cache[key]

        filenames = self.SOUND_FILES.get(key, ())
        searched = []
        for folder in self.audio_candidate_dirs():
            if not folder or not os.path.isdir(folder):
                searched.append(folder)
                continue
            for filename in filenames:
                path = self._case_insensitive_existing_file(folder, filename)
                searched.append(os.path.join(folder, filename))
                if path:
                    self.sound_cache[key] = path
                    if self.debug_prints:
                        print("[TGAW Audio v9.3]", key, "->", path)
                    return path

        self.sound_cache[key] = None
        if self.debug_prints:
            print("[TGAW Audio v9.3] Missing sound:", key)
            print("[TGAW Audio v9.3] Search folders:", self.audio_candidate_dirs())
        return None

    def start_music(self):
        if self.mute_audio or not self.audio_device:
            return
        if self.music_handle:
            try:
                # If a handle exists but is stopped/invalid in a particular aud
                # build, just keep going to avoid duplicate tracks.
                self.update_music_volume()
                return
            except Exception:
                self.music_handle = None
        path = self.resolve_sound_path("music_main")
        if not path:
            return
        try:
            factory = self._aud.Sound(path)
            try:
                factory = factory.loop(-1)
            except Exception:
                pass
            self.music_handle = self.audio_device.play(factory)
            self.update_music_volume()
        except Exception as exc:
            if self.debug_prints:
                print("[TGAW Audio v9.3] Could not play music:", exc)

    def update_music_volume(self):
        if not self.music_handle:
            return
        pause_context = (
            self.screen == "PAUSED"
            or (self.screen == "SETTINGS" and self.settings_return_screen == "PAUSED")
            or (self.screen == "EXIT_CONFIRM" and self.exit_return_screen == "PAUSED")
        )
        pause_factor = 0.45 if pause_context else 1.0
        volume = 0.0 if self.mute_audio else self.master_volume * self.music_volume * pause_factor
        try:
            self.music_handle.volume = volume
        except Exception:
            pass

    def _cleanup_sfx_handles(self):
        if not getattr(self, "sfx_handles", None):
            return
        alive = []
        for handle in self.sfx_handles:
            keep = True
            try:
                status = getattr(handle, "status", None)
                # aud status values vary by Blender build. If status exists and
                # is falsy, consider the handle finished.
                if status is not None and not status:
                    keep = False
            except Exception:
                keep = True
            if keep:
                alive.append(handle)
        # Keep the list bounded even if a build does not expose status.
        self.sfx_handles = alive[-24:]

    def play_sfx(self, key):
        if self.mute_audio or not self.audio_device:
            return
        path = self.resolve_sound_path(key)
        if not path:
            return
        try:
            factory = self._aud.Sound(path)
            handle = self.audio_device.play(factory)
            try:
                handle.volume = self.master_volume * self.sfx_volume
            except Exception:
                pass
            self.sfx_handles.append(handle)
        except Exception as exc:
            if self.debug_prints:
                print("[TGAW Audio v9.3] Could not play", key, exc)

    def play_force_sound(self, force):
        if force == 1:
            self.play_sfx("hit_weak")
        elif force == 2:
            self.play_sfx("hit_medium")
        elif force == 3:
            self.play_sfx("hit_strong")

    def is_human_controlled_side(self, side):
        return side == "PLAYER" or (side == "ENEMY" and self.mode == "LOCAL_2P")

    # ---------- Sleeve customization ----------

    def apply_sleeve_colors(self):
        player_name, player_color = self.SLEEVE_PALETTE[self.player_sleeve_color_index]
        enemy_name, enemy_color = self.SLEEVE_PALETTE[self.enemy_sleeve_color_index]
        # Direct sleeve objects. If an old scene has the sleeve nested under the arm pivot,
        # _find_child_suffix() above recovers it.
        self.set_runtime_color(self.arm_player_sleeve, player_color)
        self.set_runtime_color(self.arm_enemy_sleeve, enemy_color)
        self.set_runtime_color(self._obj("MENU_Settings_Swatch_Player"), player_color)
        self.set_runtime_color(self._obj("MENU_Settings_Swatch_Enemy"), enemy_color)
        # v8.7 push bar colors follow sleeve colors, making the advantage meter
        # feel like two players physically pushing each other.
        self.set_runtime_color(self.pushbar_player, player_color)
        self.set_runtime_color(self.pushbar_enemy, enemy_color)

    def set_runtime_color(self, obj, color):
        if not obj:
            return
        try:
            obj.color = color
        except Exception:
            pass
        try:
            obj["runtime_color"] = color
        except Exception:
            pass
        # Try to modify the runtime material color as well; this is useful for
        # simple non-textured low-poly parts such as the sleeves and UI swatches.
        try:
            for mesh in obj.meshes:
                for mat in mesh.materials:
                    for attr in ("diffuseColor", "diffuse_color"):
                        try:
                            setattr(mat, attr, color)
                        except Exception:
                            pass
        except Exception:
            pass

    def _clamp(self, value, lo, hi):
        return max(lo, min(hi, value))

    def _smooth_alpha(self, speed, dt):
        # Stable exponential-like interpolation without importing math.exp.
        return self._clamp(float(speed) * max(0.0, float(dt)), 0.0, 1.0)

    def trigger_feedback(self, side, force, miss=False):
        """Small audiovisual polish layer for v9.

        It intentionally uses optional objects, so applying the component over an
        older scene will not break anything if the repair script has not created
        the flash plane yet.
        """
        if miss:
            self.impact_flash_color = (1.0, 0.06, 0.02, 0.22)
            self.camera_shake_power = self.camera_shake_strength * 0.65
        elif force == 1:
            self.impact_flash_color = (1.0, 0.96, 0.78, 0.12)
            self.camera_shake_power = self.camera_shake_strength * 0.25
        elif force == 2:
            self.impact_flash_color = (1.0, 0.70, 0.12, 0.16)
            self.camera_shake_power = self.camera_shake_strength * 0.45
        else:
            self.impact_flash_color = (1.0, 0.20, 0.05, 0.23)
            self.camera_shake_power = self.camera_shake_strength
        self.impact_flash_timer = self.impact_flash_time
        self.camera_shake_timer = max(self.camera_shake_timer, min(0.18, self.impact_flash_time + 0.03))

    def trigger_arm_pulse(self, side, force):
        # Short impact animation. It reinforces that this is an arm-wrestling duel,
        # but the hands stay outside the dial so they do not cover the objectives.
        self.arm_pulse_timer = self.arm_pulse_time
        self.arm_pulse_side = side
        self.arm_pulse_force = max(1, int(force))


    # ---------- UI / visuals ----------

    def show_force_message(self, side, force, reset=False, timeout=False):
        # Keep this message short because it appears inside the camera frame.
        if side == "PLAYER":
            actor = "J1"
        elif side == "ENEMY":
            actor = "J2"
        else:
            actor = "IA"

        if force <= 0:
            if timeout:
                message = "%s: NO PRESIONÓ" % actor
            else:
                message = "%s: FALLO" % actor
            if reset:
                message += " | REINICIO"
        else:
            if force == 1:
                label = "DÉBIL"
            elif force == 2:
                label = "MEDIO"
            else:
                label = "FUERTE"
            message = "%s: %s +%d" % (actor, label, force)

        self.set_text(self.ui_force, message)
        self.force_message_timer = self.force_toast_time

    def update_visuals(self):
        self.set_z_rotation(self.needle, self.needle_angle)
        self.update_phase_guide()

        if self.use_segmented_zone:
            self.update_segmented_zone()
            if self.green_zone:
                self.set_visible(self.green_zone, False)
        else:
            # Legacy single-wedge fallback.
            self.set_z_rotation(self.green_zone, self.green_start_angle)

        # v9 arm-wrestling animation. Balance is smoothed visually so the arms
        # feel physical instead of snapping, but the scoring/win condition stays
        # immediate and exact.
        dt = getattr(self, "frame_dt", 0.016)
        arm_alpha = self._smooth_alpha(self.arm_smooth, dt)
        self.visual_arm_balance += (float(self.balance) - float(self.visual_arm_balance)) * arm_alpha
        max_balance = float(max(1, self.balance_win))
        balance_ratio = self._clamp(float(self.visual_arm_balance) / max_balance, -1.0, 1.0)
        base_push = balance_ratio * self.arm_balance_angle
        pulse = 0.0
        if self.arm_pulse_timer > 0.0:
            phase = self.arm_pulse_timer / self.arm_pulse_time
            pulse_curve = 1.0 - abs(phase * 2.0 - 1.0)
            pulse = pulse_curve * self.arm_hit_pulse_angle * max(1, self.arm_pulse_force) / 3.0
            if self.arm_pulse_side not in ("PLAYER",):
                pulse *= -1.0

        player_z = base_push + pulse
        enemy_z = -base_push - pulse
        player_x = -abs(pulse) * 0.20
        enemy_x = -abs(pulse) * 0.20
        if self.arm_player:
            anim = Euler((radians(player_x), 0.0, radians(player_z)), "XYZ").to_matrix()
            self.arm_player.localOrientation = self.arm_player_base_orientation @ anim if self.arm_player_base_orientation else anim
        if self.arm_enemy:
            anim = Euler((radians(enemy_x), 0.0, radians(enemy_z)), "XYZ").to_matrix()
            self.arm_enemy.localOrientation = self.arm_enemy_base_orientation @ anim if self.arm_enemy_base_orientation else anim

        self.update_balance_bar()
        self.update_feedback_overlays()

    def update_feedback_overlays(self):
        # Fade overlay: short, non-blocking transition flash when changing screens.
        if self.ui_fade_overlay:
            if self.screen_transition_timer > 0.0 and self.transition_time > 0.0:
                t = self.screen_transition_timer / max(0.001, self.screen_transition_duration)
                alpha = 0.32 * t
                self.set_runtime_color(self.ui_fade_overlay, (0.0, 0.0, 0.0, alpha))
                self.set_visible(self.ui_fade_overlay, True)
            else:
                self.set_visible(self.ui_fade_overlay, False)

        # Impact flash: quick color feedback for hit/miss, kept subtle for performance.
        if self.ui_impact_flash:
            if self.impact_flash_timer > 0.0 and self.impact_flash_time > 0.0 and self.screen == "PLAYING":
                t = self.impact_flash_timer / max(0.001, self.impact_flash_time)
                r, g, b, a = self.impact_flash_color
                self.set_runtime_color(self.ui_impact_flash, (r, g, b, a * t))
                self.set_visible(self.ui_impact_flash, True)
            else:
                self.set_visible(self.ui_impact_flash, False)

        # Camera shake is deliberately tiny. It gives force feedback while keeping
        # the dial readable and avoiding motion sickness.
        if self.game_camera and self.camera_base_local_position is not None:
            try:
                if self.camera_shake_timer > 0.0 and self.camera_shake_power > 0.0 and self.screen == "PLAYING":
                    t = self.camera_shake_timer / max(0.001, self.impact_flash_time + 0.03)
                    strength = self.camera_shake_power * self._clamp(t, 0.0, 1.0)
                    self.game_camera.localPosition.x = self.camera_base_local_position.x + random.uniform(-strength, strength)
                    self.game_camera.localPosition.y = self.camera_base_local_position.y + random.uniform(-strength, strength) * 0.45
                    self.game_camera.localPosition.z = self.camera_base_local_position.z + random.uniform(-strength, strength) * 0.45
                else:
                    self.game_camera.localPosition = self.camera_base_local_position.copy()
            except Exception:
                pass

    def update_phase_guide(self):
        if not self.phase_ticks:
            return
        if not self.show_phase_guide:
            for objs in self.phase_ticks.values():
                for obj in objs:
                    self.set_visible(obj, False)
            return

        spawn_start, spawn_end = self.effective_arc(self.spawn_arc_start, self.spawn_arc_end)
        plan_start, plan_end = self.effective_arc(self.plan_arc_start, self.plan_arc_end)
        reveal_start, reveal_end = self.effective_arc(self.reveal_arc_start, self.reveal_arc_end)
        self.update_arc_ticks(self.phase_ticks.get("SPAWN", []), spawn_start, spawn_end)
        self.update_arc_ticks(self.phase_ticks.get("PLAN", []), plan_start, plan_end)
        self.update_arc_ticks(self.phase_ticks.get("REVEAL", []), reveal_start, reveal_end)

    def update_arc_ticks(self, objects, start, end):
        if not objects:
            return
        length = min(float(len(objects)), self.arc_length(start, end))
        count = int(round(length))
        for i, obj in enumerate(objects):
            visible = i < count
            self.set_visible(obj, visible)
            if visible:
                self.set_z_rotation(obj, start + i)

    def update_segmented_zone(self):
        """Shows the valid timing zone as three force bands:
        white = weak, yellow = medium, red = strong.
        The old green single wedge is no longer used when these objects exist.
        v4.2 keeps this target hidden until the orange reaction sector reveals it.
        """
        if not self.target_visible:
            for force in (1, 2, 3):
                for obj in self.zone_ticks.get(force, []):
                    self.set_visible(obj, False)
            return

        total_ticks = int(round(max(3.0, min(float(self.max_zone_ticks), self.green_size))))
        weak_count = total_ticks // 3
        medium_count = total_ticks // 3
        strong_count = total_ticks - weak_count - medium_count
        tick_step = self.green_size / float(total_ticks)

        start_offsets = {
            1: 0,
            2: weak_count,
            3: weak_count + medium_count,
        }
        counts = {
            1: weak_count,
            2: medium_count,
            3: strong_count,
        }

        for force in (1, 2, 3):
            objs = self.zone_ticks.get(force, [])
            count = counts[force]
            start_offset = start_offsets[force]
            for i, obj in enumerate(objs):
                visible = i < count
                self.set_visible(obj, visible)
                if visible:
                    angle = self.green_start_angle + (start_offset + i) * tick_step
                    self.set_z_rotation(obj, angle)

    def set_z_rotation(self, obj, degrees):
        if not obj:
            return
        angle = radians(degrees * self.visual_rotation_sign)
        obj.localOrientation = Euler((0.0, 0.0, angle), "XYZ").to_matrix()

    def update_balance_bar(self):
        """Update v8.7 push bar.

        Instead of drawing two bars on top of each other, this behaves like a
        push meter: J1 and the rival occupy opposite sides of the same bar, and
        the split point moves according to the current advantage.
        """
        # Keep sleeve colors in sync with the push bar.
        try:
            player_color = self.SLEEVE_PALETTE[self.player_sleeve_color_index][1]
            enemy_color = self.SLEEVE_PALETTE[self.enemy_sleeve_color_index][1]
            self.set_runtime_color(self.pushbar_player, player_color)
            self.set_runtime_color(self.pushbar_enemy, enemy_color)
        except Exception:
            pass

        if self.pushbar_player and self.pushbar_enemy and self.pushbar_base:
            # v9: smooth only the visual split. The actual victory check still
            # uses self.balance immediately, so the game remains responsive.
            alpha = self._smooth_alpha(self.pushbar_smooth, getattr(self, "frame_dt", 0.016))
            self.visual_balance += (float(self.balance) - float(self.visual_balance)) * alpha
            ratio = self._clamp(float(self.visual_balance) / float(max(1, self.balance_win)), -1.0, 1.0)
            player_frac = self._clamp(0.5 + ratio * 0.5, 0.0, 1.0)
            enemy_frac = 1.0 - player_frac
            center_x = self.pushbar_base["center_x"]
            center_y = self.pushbar_base["center_y"]
            center_z = self.pushbar_base["center_z"]
            width = self.pushbar_base["width"]
            left = center_x - width * 0.5
            split = left + width * player_frac

            # Set scale first, then position so each segment stays attached to
            # its side and they meet exactly at the split point.
            try:
                self.pushbar_player.localScale.x = max(0.001, player_frac)
                self.pushbar_player.localPosition.x = left + width * player_frac * 0.5
                self.pushbar_player.localPosition.y = center_y
                self.pushbar_player.localPosition.z = center_z + 0.009
                self.set_visible(self.pushbar_player, player_frac > 0.001)
            except Exception:
                pass
            try:
                self.pushbar_enemy.localScale.x = max(0.001, enemy_frac)
                self.pushbar_enemy.localPosition.x = split + width * enemy_frac * 0.5
                self.pushbar_enemy.localPosition.y = center_y
                self.pushbar_enemy.localPosition.z = center_z + 0.010
                self.set_visible(self.pushbar_enemy, enemy_frac > 0.001)
            except Exception:
                pass
            if self.pushbar_marker:
                try:
                    self.pushbar_marker.localPosition.x = split
                    self.pushbar_marker.localPosition.y = center_y
                    self.pushbar_marker.localPosition.z = center_z + 0.020
                    self.set_visible(self.pushbar_marker, True)
                except Exception:
                    pass
            # Explicitly hide old overlapping bars if they still exist.
            self.set_visible(self.balance_bar_player, False)
            self.set_visible(self.balance_bar_enemy, False)
            return

        # Legacy fallback for scenes that have not run the v8.7 repair.
        if not self.balance_bar_player and not self.balance_bar_enemy:
            return
        ratio = min(1.0, abs(float(self.visual_balance)) / float(max(1, self.balance_win)))
        if self.balance > 0:
            if self.balance_bar_player:
                self.balance_bar_player.localScale.x = ratio
                self.set_visible(self.balance_bar_player, True)
            if self.balance_bar_enemy:
                self.set_visible(self.balance_bar_enemy, False)
        elif self.balance < 0:
            if self.balance_bar_enemy:
                self.balance_bar_enemy.localScale.x = ratio
                self.set_visible(self.balance_bar_enemy, True)
            if self.balance_bar_player:
                self.set_visible(self.balance_bar_player, False)
        else:
            self.set_visible(self.balance_bar_player, False)
            self.set_visible(self.balance_bar_enemy, False)

    def update_ui(self):
        if self.use_pip_ui:
            if self.use_simple_pip_ui:
                self.update_simple_accumulator_pips("PLAYER", self.player_sequence)
                self.update_simple_accumulator_pips("ENEMY", self.enemy_sequence)
            else:
                self.update_accumulator_pips("PLAYER", self.player_sequence)
                self.update_accumulator_pips("ENEMY", self.enemy_sequence)
            # Text sequence objects are only fallback now. Hide their old monochrome circles if pips exist.
            self.set_text(self.ui_player, "")
            self.set_text(self.ui_enemy, "")
        else:
            self.set_text(self.ui_player, self.sequence_text(self.player_sequence))
            self.set_text(self.ui_enemy, self.sequence_text(self.enemy_sequence))

        level_label = "Nivel %d" % self.level["display_level"]
        if self.level.get("is_roguelike"):
            level_label += " | Roguelike"
        self.set_text(self.ui_level, level_label)

        if self.balance > 0:
            balance_label = "EMPUJE J1  +%d / %d" % (self.balance, self.balance_win)
        elif self.balance < 0:
            balance_label = "EMPUJE RIVAL  +%d / %d" % (abs(self.balance), self.balance_win)
        else:
            balance_label = "EMPUJE NEUTRO  0 / %d" % self.balance_win
        self.set_text(self.ui_balance, balance_label)
        self.set_text(self.ui_player_label, "JUGADOR 1  |  SPACE")
        self.set_text(self.ui_enemy_label, ("IA" if self.mode == "1P_VS_AI" else "JUGADOR 2  |  ENTER"))

        if self.state == "ROUND_END":
            winner_name = "Jugador" if self.round_winner == "PLAYER" else ("IA" if self.mode == "1P_VS_AI" else "Jugador 2")
            status = "Ganó: %s" % winner_name
            hint = ""
        else:
            if self.mode == "1P_VS_AI":
                status = self.level["opponent"]
            else:
                status = "Duelo local"
            # v6 clean HUD: do not expose internal states such as preparing/reveal/window.
            # The player reads timing from the dial itself.
            hint = "¡PRESIONA!" if (self.show_debug_hint and self.is_in_timing_window) else ""

        self.set_text(self.ui_status, status)
        self.set_text(self.ui_hint, hint)

        # v7 intro/result overlays: clear, short and non-debug.
        if self.state == "LEVEL_INTRO":
            self.set_text(self.ui_intro_title, "NIVEL %d" % self.level["display_level"])
            self.set_text(self.ui_intro_subtitle, self.level["opponent"] if self.mode == "1P_VS_AI" else "DUELO LOCAL")
            self.set_text(self.ui_intro_hint, "Gana con una ventaja de %d puntos" % self.balance_win)
        elif self.state == "ROUND_END":
            winner_name = "JUGADOR 1" if self.round_winner == "PLAYER" else ("IA" if self.mode == "1P_VS_AI" else "JUGADOR 2")
            self.set_text(self.ui_result_title, "GANÓ %s" % winner_name)
            stats = "Ventaja final: %+d   |   J1: %d pts   Rival: %d pts" % (self.balance, self.player_force_total, self.enemy_force_total)
            stats += "\nFuertes J1: %d   Rival: %d   |   Fallos J1: %d   Rival: %d" % (
                self.player_force_counts.get(3, 0),
                self.enemy_force_counts.get(3, 0),
                self.player_misses,
                self.enemy_misses,
            )
            self.set_text(self.ui_result_stats, stats)
            self.set_text(self.ui_result_hint, "Preparando siguiente duelo...")

    def update_simple_accumulator_pips(self, side, sequence):
        slots = self.simple_pips.get(side, [])
        for idx, slot_data in enumerate(slots):
            force = sequence[idx] if idx < len(sequence) else 0
            ring = slot_data.get("ring")
            fill = slot_data.get("fill")
            self.set_visible(ring, True)
            if fill:
                self.set_visible(fill, force > 0)
                self.set_runtime_color(fill, self.FORCE_COLORS.get(force, self.FORCE_COLORS[0]))

    def update_accumulator_pips(self, side, sequence):
        slots = self.pips.get(side, [])
        for idx, slot_data in enumerate(slots):
            force = sequence[idx] if idx < len(sequence) else 0
            for variant_force, obj in slot_data.items():
                self.set_visible(obj, variant_force == force)

    def sequence_text(self, sequence):
        count = max(0, min(self.target_hits, len(sequence)))
        return " ".join(["●"] * count + ["○"] * (self.target_hits - count))

    def set_text(self, obj, value):
        if not obj:
            return
        try:
            obj.text = str(value)
        except Exception:
            # Fallback for unusual text object setups.
            try:
                obj["Text"] = str(value)
            except Exception:
                pass

    def set_visible(self, obj, value):
        if not obj:
            return
        visible = bool(value)
        # In UPBGE/KX_GameObject, setVisible is the safest runtime method.
        # Some objects accept `.visible`, others behave better with setVisible().
        try:
            obj.setVisible(visible, True)
        except Exception:
            pass
        try:
            obj.visible = visible
        except Exception:
            pass
