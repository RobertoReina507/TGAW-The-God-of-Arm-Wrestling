# GDD Final - TGAW

## Ficha técnica

- Nombre: TGAW (The God of Arm Wrestling)
- Género: minijuego competitivo de precisión y reacción.
- Motor: UPBGE 0.50.
- Lenguaje: Python mediante Python Components.
- Plataforma: PC.
- Modos: jugador contra IA y dos jugadores local.

## Concepto final

TGAW es un videojuego de pulseadas donde el jugador debe presionar en el momento exacto mientras una aguja gira sobre un dial. La precisión determina la fuerza del golpe y la ventaja sobre el rival.

## Mecánica principal

El jugador observa el dial, espera la aparición del objetivo y presiona la tecla correspondiente. El sistema evalúa si el golpe fue débil, medio o fuerte.

## Core loop

1. El sistema prepara el objetivo.
2. El objetivo aparece en el dial.
3. La aguja se aproxima a la zona de acierto.
4. El jugador presiona la tecla.
5. El sistema evalúa el resultado.
6. Se actualizan discos, ventaja y barra de empuje.
7. Se repite hasta que alguien alcance ventaja de +6.

## Reglas finales

- Débil: suma 1 punto.
- Medio: suma 2 puntos.
- Fuerte: suma 3 puntos.
- La victoria se obtiene al alcanzar una ventaja de +6.
- El fallo reinicia la racha visual de aciertos.

## Modos de juego

- Campaña contra IA hasta nivel 15.
- Modo local para dos jugadores en el mismo teclado.

## Sistema de IA

La IA evalúa oportunidades de acierto según el nivel. A mayor nivel, aumenta la precisión y la probabilidad de golpes de mayor fuerza.

## Arte y audio

El juego utiliza estética de bar oscuro, tonos ámbar, mesa 3D, dial circular, brazos low-poly, HUD con discos de aciertos, barra de empuje, música principal y efectos de sonido para aciertos, fallos y navegación.

## Monetización

La versión académica de TGAW es gratuita. En una posible versión comercial, el modelo recomendado sería compra única de bajo costo o contenido cosmético opcional, como colores de mangas, escenarios adicionales y nuevos rivales. No se plantea monetización agresiva porque el juego está diseñado para partidas rápidas y accesibles.

## Análisis de mercado

TGAW se orienta a jugadores casuales de PC interesados en minijuegos competitivos, partidas rápidas, experiencias locales para dos jugadores y mecánicas basadas en reflejos. El juego se diferencia por combinar precisión, lectura visual del dial, sensación de pulseada y barra de empuje en una experiencia corta y directa.

## Estado final

El juego cuenta con menú principal, opciones, selección de modo, HUD, audio, IA, modo local, sistema de niveles, build ejecutable y repositorio organizado.
